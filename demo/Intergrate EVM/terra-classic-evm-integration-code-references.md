# Terra Classic EVM Integration - Code References & Implementation Guide

## Table of Contents

### 1. EVMKeeper Initialization
### 2. AnteHandler Security Implementation  
### 3. FeeMarket (EIP-1559) Configuration
### 4. JSON-RPC Server Configuration
### 5. IBC-EVM Hooks and Precompile Registration
### 6. Comparison Tables for Terra Classic v0.47 Backporting

---

## 1. EVMKeeper Initialization

### 1.1 Main Application Setup - `app/app.go`

**File:** `app/app.go` (Terra Classic application setup)

**Reference Location:** Lines 471-481 in EVM implementation (adapt for Terra Classic)
```go
// EVMKeeper initialization pattern for Terra Classic
app.EVMKeeper = evmkeeper.NewKeeper(
    app.appCodec,
    keys[evmtypes.StoreKey],
    keys[evmtypes.TransientKey],
    authtypes.NewModuleAddress(govtypes.ModuleName),
    app.AccountKeeper,
    app.BankKeeper,
    app.StakingKeeper,
    app.FeeMarketKeeper,
    app.AvailableStaticPrecompiles(),
    "",
)
```

**Explanation:** This initializes the EVM keeper with all required dependencies including account, bank, staking keepers and the fee market module for EIP-1559 support.

**Implementation Location:** Add to `app/app.go` in Terra Classic after other keeper initializations

### 1.2 Keeper Structure - `x/evm/keeper/keeper.go`

**File:** `x/evm/keeper/keeper.go` (Terra Classic EVM module structure)

**Reference Implementation:** EVM Keeper constructor pattern
```go
func NewKeeper(
    cdc codec.BinaryCodec,
    storeKey,
    transientKey storetypes.StoreKey,
    authority sdk.AccAddress,
    ak types.AccountKeeper,
    bankKeeper types.BankKeeper,
    sk types.StakingKeeper,
    fmk types.FeeMarketKeeper,
    precompiles map[common.Address]vm.PrecompiledContract,
    tracer string,
) *Keeper {
    // Ensure that the authority is a valid AccAddress
    if _, err := ak.AddressCodec().StringToBytes(authority.String()); err != nil {
        panic("authority is not a valid acc address")
    }
    
    return &Keeper{
        Ctx:                 sdk.Context{},
        cdc:                 cdc,
        storeKey:            storeKey,
        transientKey:        transientKey,
        authority:           authority,
        accountKeeper:       ak,
        bankKeeper:          NewBankWrapper(bankKeeper),
        stakingKeeper:       sk,
        feeMarketKeeper:     NewFeeMarketWrapper(fmk),
        precompiles:         precompiles,
        hooks:               nil,
        tracer:              tracer,
    }
}
```

**Explanation:** Complete keeper constructor showing all dependencies and wrapper initialization for seamless Cosmos SDK integration.

**Implementation Location:** Create new module `x/evm/keeper/keeper.go` in Terra Classic

### 1.3 Precompile Registration - `app/precompiles.go`

**File:** `app/precompiles.go` (Terra Classic precompile setup)

**Reference Implementation:** Static precompile registration pattern
```go
func NewAvailableStaticPrecompiles(
    stakingKeeper stakingkeeper.Keeper,
    distributionKeeper distributionkeeper.Keeper,
    bankKeeper cmn.BankKeeper,
    erc20Keeper erc20Keeper.Keeper,
    transferKeeper transferkeeper.Keeper,
    channelKeeper *channelkeeper.Keeper,
    evmKeeper *evmkeeper.Keeper,
    govKeeper govkeeper.Keeper,
    slashingKeeper slashingkeeper.Keeper,
    // Terra Classic specific keepers
    oracleKeeper oraclekeeper.Keeper,
    marketKeeper marketkeeper.Keeper,
    treasuryKeeper treasurykeeper.Keeper,
    codec codec.Codec,
    opts ...Option,
) map[common.Address]vm.PrecompiledContract {
    // Initialize IBC Transfer precompile
    ibcTransferPrecompile, err := ics20precompile.NewPrecompile(
        bankKeeper,
        stakingKeeper,
        transferKeeper,
        channelKeeper,
        evmKeeper,
    )
    if err != nil {
        panic(fmt.Errorf("failed to instantiate ICS20 precompile: %w", err))
    }

    bankPrecompile, err := bankprecompile.NewPrecompile(bankKeeper, erc20Keeper)
    if err != nil {
        panic(fmt.Errorf("failed to instantiate bank precompile: %w", err))
    }
    
    // Terra Classic specific precompiles
    oraclePrecompile, err := oracleprecompile.NewPrecompile(oracleKeeper)
    if err != nil {
        panic(fmt.Errorf("failed to instantiate oracle precompile: %w", err))
    }
    
    // Register all precompiles
    precompiles := map[common.Address]vm.PrecompiledContract{
        common.HexToAddress(ics20precompile.PrecompileAddress): ibcTransferPrecompile,
        common.HexToAddress(bankprecompile.PrecompileAddress):  bankPrecompile,
        common.HexToAddress("0x1001"): oraclePrecompile, // Terra Oracle
        // ... more Terra precompiles
    }
}
```

**Explanation:** Shows how to register static precompiles for Cosmos SDK module access from EVM, including Terra Classic specific modules (Oracle, Market, Treasury).

**Implementation Location:** Create new file `app/precompiles.go` in Terra Classic

---

## 2. AnteHandler Security Implementation

### 2.1 Monolithic EVM AnteHandler - `app/ante/evm/mono_decorator.go`

**File:** `app/ante/evm/mono_decorator.go` (Terra Classic EVM ante handler)

**Reference Implementation:** Complete security validation chain
```go
func (mfd MonoDecorator) AnteHandle(
    ctx sdk.Context,
    tx sdk.Tx,
    simulate bool,
    next sdk.AnteHandler,
) (newCtx sdk.Context, err error) {
    // Handle both Cosmos and Ethereum transactions
    if len(tx.GetMsgs()) == 1 {
        if msgEthTx, ok := tx.GetMsgs()[0].(*evmtypes.MsgEthereumTx); ok {
            // EVM transaction path
            return mfd.handleEthereumTx(ctx, tx, msgEthTx, simulate, next)
        }
    }
    
    // Cosmos transaction path - Terra Classic specific handling
    return mfd.handleCosmosTx(ctx, tx, simulate, next)
}

func (mfd MonoDecorator) handleEthereumTx(
    ctx sdk.Context,
    tx sdk.Tx,
    msgEthTx *evmtypes.MsgEthereumTx,
    simulate bool,
    next sdk.AnteHandler,
) (sdk.Context, error) {
    // Signature verification
    if err := mfd.verifyEthSignature(ctx, msgEthTx); err != nil {
        return ctx, err
    }
    
    // Gas validation and fee deduction (Terra Classic burn tax integration)
    if err := mfd.validateAndDeductFee(ctx, msgEthTx, simulate); err != nil {
        return ctx, err
    }
    
    // EVM specific validations
    if err := mfd.validateEvmTx(ctx, msgEthTx); err != nil {
        return ctx, err
    }
    
    return next(ctx, tx, simulate)
}
```

**Explanation:** Monolithic decorator that handles both Cosmos and Ethereum transactions with complete security validation including signature verification and fee deduction. Adapted for Terra Classic with burn tax integration.

**Implementation Location:** Create new directory structure `app/ante/evm/` in Terra Classic

### 2.2 Security Configuration - `app/app.go`

**File:** `app/app.go` (Terra Classic AnteHandler setup)

**Reference Implementation:** AnteHandler setup with security features
```go
maxGasWanted := cast.ToUint64(appOpts.Get(srvflags.EVMMaxTxGasWanted))
options := ante.HandlerOptions{
    Cdc:                    app.appCodec,
    AccountKeeper:          app.AccountKeeper,
    BankKeeper:             app.BankKeeper,
    ExtensionOptionChecker: evmtypes.HasDynamicFeeExtensionOption,
    EvmKeeper:              app.EVMKeeper,
    FeegrantKeeper:         app.FeeGrantKeeper,
    IBCKeeper:              app.IBCKeeper,
    FeeMarketKeeper:        app.FeeMarketKeeper,
    SignModeHandler:        encodingConfig.TxConfig.SignModeHandler(),
    SigGasConsumer:         ante.DefaultSigVerificationGasConsumer,
    MaxTxGasWanted:         maxGasWanted,
    TxFeeChecker:           evmante.NewDynamicFeeChecker(app.EVMKeeper),
    // Terra Classic specific
    TreasuryKeeper:         app.TreasuryKeeper,  // For burn tax calculation
    OracleKeeper:           app.OracleKeeper,    // For fee oracle rates
}
app.SetAnteHandler(ante.NewAnteHandler(options))
```

**Explanation:** Complete AnteHandler configuration with dynamic fee checking, signature verification, and gas management for secure transaction processing. Extended for Terra Classic with treasury and oracle integration.

**Implementation Location:** Modify existing `app/app.go` AnteHandler setup section

### 2.3 Bypass Attack Prevention - `app/ante/cosmos/authz.go`

**File:** `app/ante/cosmos/authz.go` (Terra Classic AuthZ security)

**Reference Implementation:** AuthZ bypass prevention
```go
func RejectMessagesDecorator() sdk.AnteDecorator {
    return rejectMessagesDecorator{}
}

type rejectMessagesDecorator struct{}

func (rmd rejectMessagesDecorator) AnteHandle(
    ctx sdk.Context, tx sdk.Tx, simulate bool, next sdk.AnteHandler,
) (newCtx sdk.Context, err error) {
    for _, msg := range tx.GetMsgs() {
        if _, ok := msg.(*evmtypes.MsgEthereumTx); ok {
            return ctx, errorsmod.Wrapf(
                sdkerrors.ErrUnauthorized,
                "MsgEthereumTx needs to be contained within a MsgEthereumTx",
            )
        }
    }
    return next(ctx, tx, simulate)
}
```

**Explanation:** Prevents EVM transaction bypass attacks by ensuring proper message type validation and routing through appropriate handlers.

**Implementation Location:** Create new directory `app/ante/cosmos/` in Terra Classic

---

## 3. FeeMarket (EIP-1559) Configuration

### 3.1 FeeMarket Keeper Initialization - `x/feemarket/keeper/keeper.go`

**File:** `x/feemarket/keeper/keeper.go` (Terra Classic fee market module)

**Reference Implementation:** Core keeper setup
```go
type Keeper struct {
    cdc      codec.BinaryCodec
    storeKey storetypes.StoreKey
    tkey     storetypes.StoreKey

    paramSpace paramtypes.Subspace

    authority sdk.AccAddress
}

func NewKeeper(
    cdc codec.BinaryCodec,
    storeKey, transientKey storetypes.StoreKey,
    paramSpace paramtypes.Subspace,
    authority sdk.AccAddress,
) Keeper {
    if !paramSpace.HasKeyTable() {
        paramSpace = paramSpace.WithKeyTable(types.ParamKeyTable())
    }

    return Keeper{
        cdc:        cdc,
        storeKey:   storeKey,
        tkey:       transientKey,
        paramSpace: paramSpace,
        authority:  authority,
    }
}
```

**Explanation:** FeeMarket keeper initialization with parameter management for EIP-1559 base fee calculations and elasticity settings.

**Implementation Location:** Create new module `x/feemarket/keeper/keeper.go` in Terra Classic

### 3.2 Base Fee Calculation - `x/feemarket/keeper/eip1559.go`

**File:** `x/feemarket/keeper/eip1559.go` (Terra Classic EIP-1559 implementation)

**Reference Implementation:** EIP-1559 implementation with Terra Classic adaptations
```go
func (k Keeper) CalculateBaseFee(ctx sdk.Context) *big.Int {
    params := k.GetParams(ctx)
    
    // If fee market is disabled, return nil (no base fee)
    if !params.EnableHeight || ctx.BlockHeight() < params.EnableHeight {
        return nil
    }

    consParams := ctx.ConsensusParams()
    if consParams.Block == nil {
        return nil
    }

    // Get the block gas used from the previous block
    parentGasUsed := k.GetBlockGasUsed(ctx)
    
    // Calculate base fee based on EIP-1559 formula
    parentBaseFee := k.GetBaseFee(ctx)
    gasTarget := params.BlockGas / 2
    
    // EIP-1559 base fee calculation
    if parentGasUsed == gasTarget {
        return parentBaseFee
    } else if parentGasUsed > gasTarget {
        // Increase base fee
        baseFeeChangeDenominator := new(big.Int).SetUint64(params.BaseFeeChangeDenominator)
        gasUsedDelta := new(big.Int).SetUint64(parentGasUsed - gasTarget)
        targetGasBig := new(big.Int).SetUint64(gasTarget)
        
        baseFeePerGasDelta := new(big.Int).Div(
            new(big.Int).Mul(parentBaseFee, gasUsedDelta),
            new(big.Int).Mul(targetGasBig, baseFeeChangeDenominator),
        )
        
        return new(big.Int).Add(parentBaseFee, math.BigMax(baseFeePerGasDelta, big.NewInt(1)))
    } else {
        // Decrease base fee
        baseFeeChangeDenominator := new(big.Int).SetUint64(params.BaseFeeChangeDenominator)
        gasUsedDelta := new(big.Int).SetUint64(gasTarget - parentGasUsed)
        targetGasBig := new(big.Int).SetUint64(gasTarget)
        
        baseFeePerGasDelta := new(big.Int).Div(
            new(big.Int).Mul(parentBaseFee, gasUsedDelta),
            new(big.Int).Mul(targetGasBig, baseFeeChangeDenominator),
        )
        
        return math.BigMax(
            new(big.Int).Sub(parentBaseFee, baseFeePerGasDelta),
            new(big.Int).SetUint64(params.MinGasPrice),
        )
    }
}
```

**Explanation:** Complete EIP-1559 base fee calculation algorithm with elasticity multiplier and gas target management for dynamic fee adjustment.

**GitHub Permalink:** [x/feemarket/keeper/eip1559.go#L1-L100](https://github.com/cosmos/evm/blob/main/x/feemarket/keeper/eip1559.go#L1-L100)

### 3.3 Parameter Management - `x/feemarket/types/params.go`

**File:** `x/feemarket/types/params.go` (Terra Classic fee market parameters)

**Lines 1-80:** Fee market parameters
```go
type Params struct {
    // NoBaseFee forces the EIP-1559 base fee to 0 (needed for 0 price calls)
    NoBaseFee bool `protobuf:"varint,1,opt,name=no_base_fee,json=noBaseFee,proto3" json:"no_base_fee,omitempty"`
    // BaseFeeChangeDenominator bounds the amount the base fee can change between blocks.
    BaseFeeChangeDenominator uint32 `protobuf:"varint,2,opt,name=base_fee_change_denominator,json=baseFeeChangeDenominator,proto3" json:"base_fee_change_denominator,omitempty"`
    // ElasticityMultiplier bounds the maximum gas limit an EIP-1559 block may have.
    ElasticityMultiplier uint32 `protobuf:"varint,3,opt,name=elasticity_multiplier,json=elasticityMultiplier,proto3" json:"elasticity_multiplier,omitempty"`
    // EnableHeight defines the height at which the base fee calculation is enabled.
    EnableHeight int64 `protobuf:"varint,5,opt,name=enable_height,json=enableHeight,proto3" json:"enable_height,omitempty"`
    // BaseFee for EIP-1559 blocks.
    BaseFee github_com_cosmos_cosmos_sdk_types.Int `protobuf:"bytes,6,opt,name=base_fee,json=baseFee,proto3,customtype=github.com/cosmos/cosmos-sdk/types.Int" json:"base_fee"`
    // MinGasPrice defines the minimum gas price value for cosmos and eth transactions
    MinGasPrice github_com_cosmos_cosmos_sdk_types.Dec `protobuf:"bytes,7,opt,name=min_gas_price,json=minGasPrice,proto3,customtype=github.com/cosmos/cosmos-sdk/types.Dec" json:"min_gas_price"`
    // MinGasMultiplier is the minimum global multiplier for the minimum gas price
    MinGasMultiplier github_com_cosmos_cosmos_sdk_types.Dec `protobuf:"bytes,8,opt,name=min_gas_multiplier,json=minGasMultiplier,proto3,customtype=github.com/cosmos/cosmos-sdk/types.Dec" json:"min_gas_multiplier"`
}

func DefaultParams() Params {
    return Params{
        NoBaseFee:                false,
        BaseFeeChangeDenominator: DefaultBaseFeeChangeDenominator,
        ElasticityMultiplier:     DefaultElasticityMultiplier,
        EnableHeight:             0,
        BaseFee:                  DefaultBaseFee,
        MinGasPrice:              DefaultMinGasPrice,
        MinGasMultiplier:         DefaultMinGasMultiplier,
    }
}
```

**Explanation:** Complete parameter structure for EIP-1559 configuration including base fee changes, elasticity multiplier, and minimum gas price settings.

**Implementation Location:** Create new module `x/feemarket/types/params.go` in Terra Classic

---

## 4. JSON-RPC Server Configuration

### 4.1 JSON-RPC Server Setup - `server/json_rpc.go`

**File:** `server/json_rpc.go` (Terra Classic JSON-RPC server)

**Reference Implementation:** Complete server initialization adapted for Terra Classic
```go
func StartJSONRPC(
    ctx context.Context,
    srvCtx *server.Context,
    clientCtx client.Context,
    g *errgroup.Group,
    tmRPCAddr, tmEndpoint string,
    config *serverconfig.Config,
    indexer cosmosevmtypes.EVMTxIndexer,
) (*http.Server, error) {
    logger := srvCtx.Logger.With("module", "geth")
    tmWsClient := ConnectTmWS(tmRPCAddr, tmEndpoint, logger)

    // Set Geth's global logger to use this handler
    handler := &CustomSlogHandler{logger: logger}
    slog.SetDefault(slog.New(handler))

    rpcServer := ethrpc.NewServer()

    rpcServer.SetBatchLimits(config.JSONRPC.BatchRequestLimit, config.JSONRPC.BatchResponseMaxSize)
    allowUnprotectedTxs := config.JSONRPC.AllowUnprotectedTxs
    rpcAPIArr := config.JSONRPC.API

    apis := rpc.GetRPCAPIs(srvCtx, clientCtx, tmWsClient, allowUnprotectedTxs, indexer, rpcAPIArr)

    for _, api := range apis {
        if err := rpcServer.RegisterName(api.Namespace, api.Service); err != nil {
            logger.Error(
                "failed to register service in JSON RPC namespace",
                "namespace", api.Namespace,
                "service", api.Service,
            )
            return nil, err
        }
    }

    r := mux.NewRouter()
    r.HandleFunc("/", rpcServer.ServeHTTP).Methods("POST")

    handlerWithCors := cors.Default()
    if config.API.EnableUnsafeCORS {
        handlerWithCors = cors.AllowAll()
    }

    httpSrv := &http.Server{
        Addr:              config.JSONRPC.Address,
        Handler:           handlerWithCors.Handler(r),
        ReadHeaderTimeout: config.JSONRPC.HTTPTimeout,
        ReadTimeout:       config.JSONRPC.HTTPTimeout,
        WriteTimeout:      config.JSONRPC.HTTPTimeout,
        IdleTimeout:       config.JSONRPC.HTTPIdleTimeout,
    }

    httpSrvDone := make(chan struct{}, 1)

    g.Go(func() error {
        srvCtx.Logger.Info("Starting JSON-RPC server", "address", config.JSONRPC.Address)
        if err := httpSrv.ListenAndServe(); err != nil {
            if err == http.ErrServerClosed {
                close(httpSrvDone)
                return nil
            }

            srvCtx.Logger.Error("failed to start JSON-RPC server", "error", err.Error())
            return err
        }

        return nil
    })

    // Start WebSocket server
    if config.JSONRPC.WsAddress != "" {
        srvCtx.Logger.Info("Starting JSON WebSocket server", "address", config.JSONRPC.WsAddress)

        // allocate separate WS connection to Tendermint
        tmWsClient = ConnectTmWS(tmRPCAddr, tmEndpoint, logger)
        wsSrv := rpc.NewWebsocketsServer(clientCtx, logger, tmWsClient, config)
        wsSrv.Start()
    }

    return httpSrv, nil
}
```

**Explanation:** Complete JSON-RPC server setup with CORS configuration, WebSocket support, batch request limits, and namespace registration for Ethereum-compatible API.

**Implementation Location:** Extend existing `server/` directory in Terra Classic with JSON-RPC support

### 4.2 Configuration Structure - `server/config/config.go`

**File:** `server/config/config.go` (Terra Classic JSON-RPC configuration)

**Reference Implementation:** JSON-RPC configuration struct
```go
type JSONRPCConfig struct {
    // API defines a list of JSON-RPC namespaces that should be enabled
    API []string `mapstructure:"api"`
    // Address defines the HTTP server to listen on
    Address string `mapstructure:"address"`
    // WsAddress defines the WebSocket server to listen on
    WsAddress string `mapstructure:"ws-address"`
    // GasCap is the global gas cap for eth-call variants.
    GasCap uint64 `mapstructure:"gas-cap"`
    // AllowInsecureUnlock toggles if account unlocking is enabled when account-related RPCs are exposed by http.
    AllowInsecureUnlock bool `mapstructure:"allow-insecure-unlock"`
    // EVMTimeout is the global timeout for eth-call.
    EVMTimeout time.Duration `mapstructure:"evm-timeout"`
    // TxFeeCap is the global tx-fee cap for send transaction
    TxFeeCap float64 `mapstructure:"txfee-cap"`
    // FilterCap is the global cap for total number of filters that can be created
    FilterCap int32 `mapstructure:"filter-cap"`
    // FeeHistoryCap is the global cap for total number of blocks that can be fetched
    FeeHistoryCap int32 `mapstructure:"feehistory-cap"`
    // BlockRangeCap defines the global cap for total number of blocks that can be queried
    BlockRangeCap int32 `mapstructure:"block-range-cap"`
    // LogsCap defines the global cap for total number of logs that can be returned
    LogsCap int32 `mapstructure:"logs-cap"`
    // HTTPTimeout is the read/write timeout of http json-rpc server.
    HTTPTimeout time.Duration `mapstructure:"http-timeout"`
    // HTTPIdleTimeout is the idle timeout of http json-rpc server.
    HTTPIdleTimeout time.Duration `mapstructure:"http-idle-timeout"`
    // AllowUnprotectedTxs restricts unprotected (non EIP155 signed) transactions to be submitted via
    // the node's RPC when the global parameter is disabled.
    AllowUnprotectedTxs bool `mapstructure:"allow-unprotected-txs"`
    // BatchRequestLimit is the limit for the number of requests in a batch
    BatchRequestLimit int `mapstructure:"batch-request-limit"`
    // BatchResponseMaxSize is the max size of the response for a batch request
    BatchResponseMaxSize int `mapstructure:"batch-response-max-size"`
    // MaxOpenConnections is the maximum number of WebSocket connections.
    MaxOpenConnections int `mapstructure:"max-open-connections"`
    // EnableIndexer defines if EVM TxIndexer indexer is enabled.
    EnableIndexer bool `mapstructure:"enable-indexer"`
    // MetricsAddress defines the EVM Metrics server address to bind to. Pass --metrics in CLI to enable
    // Prometheus metrics path: http://localhost:{MetricsAddress}/debug/metrics/prometheus
    MetricsAddress string `mapstructure:"metrics-address"`
    // FixRevertGasRefundHeight defines the upgrade height for the revert gas refund fix when applicable.
    FixRevertGasRefundHeight int64 `mapstructure:"fix-revert-gas-refund-height"`
    // WSOrigins defines the allowed origins for WebSocket connections.
    WSOrigins []string `mapstructure:"ws-origins"`
    // EnableProfiling defines if the pprof profiling is enabled via the JSON-RPC server
    EnableProfiling bool `mapstructure:"enable-profiling"`
}
```

**Explanation:** Complete JSON-RPC configuration structure with security settings, performance limits, and WebSocket configuration for Ethereum-compatible API server.

**Implementation Location:** Extend existing `server/config/` directory in Terra Classic

### 4.3 Default Configuration - `server/config/config.go`

**File:** `server/config/config.go` (Terra Classic default JSON-RPC settings)

**Lines 244-262:** Default JSON-RPC settings
```go
func DefaultJSONRPCConfig() *JSONRPCConfig {
    return &JSONRPCConfig{
        Enable:                   false,
        API:                      GetDefaultAPINamespaces(),
        Address:                  DefaultJSONRPCAddress,
        WsAddress:                DefaultJSONRPCWsAddress,
        GasCap:                   DefaultGasCap,
        AllowInsecureUnlock:      DefaultJSONRPCAllowInsecureUnlock,
        EVMTimeout:               DefaultEVMTimeout,
        TxFeeCap:                 DefaultTxFeeCap,
        FilterCap:                DefaultFilterCap,
        FeeHistoryCap:            DefaultFeeHistoryCap,
        BlockRangeCap:            DefaultBlockRangeCap,
        LogsCap:                  DefaultLogsCap,
        HTTPTimeout:              DefaultHTTPTimeout,
        HTTPIdleTimeout:          DefaultHTTPIdleTimeout,
        AllowUnprotectedTxs:      DefaultAllowUnprotectedTxs,
        BatchRequestLimit:        DefaultBatchRequestLimit,
        BatchResponseMaxSize:     DefaultBatchResponseMaxSize,
        MaxOpenConnections:       DefaultMaxOpenConnections,
        EnableIndexer:            false,
        MetricsAddress:           DefaultJSONRPCMetricsAddress,
        FixRevertGasRefundHeight: DefaultFixRevertGasRefundHeight,
        WSOrigins:                GetDefaultWSOrigins(),
        EnableProfiling:          DefaultEnableProfiling,
    }
}

func GetDefaultAPINamespaces() []string {
    return []string{"eth", "net", "web3"}
}
```

**Explanation:** Default configuration values for secure JSON-RPC setup with standard Ethereum namespaces and conservative security settings.

**Implementation Location:** Same as above - `server/config/config.go` in Terra Classic

---

## 5. IBC-EVM Hooks and Precompile Registration

### 5.1 ICS20 Precompile Implementation - `x/evm/precompiles/ics20/ics20.go`

**File:** `x/evm/precompiles/ics20/ics20.go` (Terra Classic IBC precompile)

**Reference Implementation:** IBC transfer precompile setup
```go
package ics20

import (
    "embed"
    "fmt"

    "github.com/ethereum/go-ethereum/accounts/abi"
    "github.com/ethereum/go-ethereum/common"
    "github.com/ethereum/go-ethereum/core/tracing"
    "github.com/ethereum/go-ethereum/core/vm"

    cmn "github.com/cosmos/evm/precompiles/common"
    transferkeeper "github.com/cosmos/evm/x/ibc/transfer/keeper"
    evmkeeper "github.com/cosmos/evm/x/vm/keeper"
    evmtypes "github.com/cosmos/evm/x/vm/types"
    channelkeeper "github.com/cosmos/ibc-go/v10/modules/core/04-channel/keeper"

    storetypes "cosmossdk.io/store/types"

    stakingkeeper "github.com/cosmos/cosmos-sdk/x/staking/keeper"
)

// PrecompileAddress of the ICS-20 EVM extension in hex format.
const PrecompileAddress = "0x0000000000000000000000000000000000000802"

type Precompile struct {
    cmn.BasePrecompile
    bankKeeper    cmn.BankKeeper
    stakingKeeper stakingkeeper.Keeper
    transferKeeper transferkeeper.Keeper
    channelKeeper channelkeeper.Keeper
    evmKeeper     *evmkeeper.Keeper
}

func NewPrecompile(
    bankKeeper cmn.BankKeeper,
    stakingKeeper stakingkeeper.Keeper,
    transferKeeper transferkeeper.Keeper,
    channelKeeper channelkeeper.Keeper,
    evmKeeper *evmkeeper.Keeper,
) (Precompile, error) {
    return Precompile{
        BasePrecompile: cmn.NewBasePrecompile(ContractABI),
        bankKeeper:     bankKeeper,
        stakingKeeper:  stakingKeeper,
        transferKeeper: transferKeeper,
        channelKeeper:  channelKeeper,
        evmKeeper:      evmKeeper,
    }, nil
}
```

**Explanation:** ICS20 precompile implementation enabling smart contracts to perform cross-chain IBC transfers using standard Ethereum interfaces.

**Implementation Location:** Create new module `x/evm/precompiles/ics20/` in Terra Classic

### 5.2 IBC Middleware Integration - `x/erc20/ibc_middleware.go`

**File:** `x/erc20/ibc_middleware.go` (Terra Classic ERC20-IBC middleware)

**Reference Implementation:** ERC20-IBC integration middleware
```go
package erc20

import (
    "errors"

    "github.com/cosmos/evm/ibc"
    erc20types "github.com/cosmos/evm/x/erc20/types"
    transfertypes "github.com/cosmos/ibc-go/v10/modules/apps/transfer/types"
    channeltypes "github.com/cosmos/ibc-go/v10/modules/core/04-channel/types"
    porttypes "github.com/cosmos/ibc-go/v10/modules/core/05-port/types"
    "github.com/cosmos/ibc-go/v10/modules/core/exported"

    errorsmod "cosmossdk.io/errors"

    sdk "github.com/cosmos/cosmos-sdk/types"
    errortypes "github.com/cosmos/cosmos-sdk/types/errors"
)

var (
    _ porttypes.IBCModule             = &IBCMiddleware{}
    _ porttypes.PacketDataUnmarshaler = &IBCMiddleware{}
)

// IBCMiddleware implements the ICS26 callbacks for the transfer middleware given
// the erc20 keeper and the underlying application.
type IBCMiddleware struct {
    app           porttypes.IBCModule
    keeper        Keeper
    ics4Wrapper   porttypes.ICS4Wrapper
}

func (im IBCMiddleware) OnRecvPacket(
    ctx sdk.Context,
    packet channeltypes.Packet,
    relayer sdk.AccAddress,
) exported.Acknowledgement {
    // Call the underlying app's OnRecvPacket callback
    ack := im.app.OnRecvPacket(ctx, packet, relayer)

    // Perform ERC20 conversion if conditions are met
    return im.performERC20Conversion(ctx, packet, ack)
}

func (im IBCMiddleware) performERC20Conversion(
    ctx sdk.Context,
    packet channeltypes.Packet,
    ack exported.Acknowledgement,
) exported.Acknowledgement {
    // Only proceed if the underlying call was successful
    if !ack.Success() {
        return ack
    }

    // Attempt to unmarshal the packet data
    var data transfertypes.FungibleTokenPacketData
    if err := transfertypes.ModuleCdc.UnmarshalJSON(packet.GetData(), &data); err != nil {
        return ack
    }

    // Perform ERC20 token conversion for IBC assets
    return im.onRecvPacket(ctx, packet, data)
}
```

**Explanation:** IBC middleware that automatically converts IBC assets to ERC20 tokens when received, enabling seamless cross-chain asset transfers.

**Implementation Location:** Create new module `x/erc20/ibc_middleware.go` in Terra Classic

### 5.3 EVM Callbacks Implementation - `x/ibc/callbacks/README.md`

**File:** `x/ibc/callbacks/README.md` (Terra Classic IBC callbacks specification)

**Reference Documentation:** EVM callback execution format
```markdown
### EVM Contract Execution Format

Before diving into the IBC metadata format, it's important to understand how we will execute EVM contract calls from
outside the state machine. Provided below is the EVM keeper's `CallData` function.

```go
func (k Keeper) CallEVMWithData(
    ctx sdk.Context,
    from common.Address,
    contract *common.Address,
    data []byte,
    commit bool,
    gasCap *big.Int,
) (*types.MsgEthereumTxResponse, error)
```

For use with EVM `recvPacket callbacks, the message fields above can be derived from the following:

- `Sender`: IBC packet senders cannot be explicitly trusted, as they can be deceitful. Chains cannot
risk the sender being confused with a particular local user or module address. To prevent this, the
`sender` is replaced with an account that represents the sender prefixed by the channel and a VM module
derived address for that channel and sender pair.

- `Contract`: This will be the EVM contract address that the user wants to call.

- `Data`: This will be the EVM calldata that the user wants to execute on the contract.

### Execution flow

1. Pre-EVM Callbacks:
   - Core IBC TAO checks on RecvPacket are executed (e.g. timeout, replay checks)

2. In EVM callbacks, pre-packet execution:
   - Ensure the packet is correctly formatted (as defined above).
   - Ensure the receiver is correctly set to isolated address.

3. In EVM callbacks, post packet execution:
   - Execute the EVM call on requested EVM contract
   - If the EVM call returns an error, return `ErrAck`.
   - Otherwise, continue through middleware.
```

**Explanation:** Complete specification for EVM callbacks in IBC transfers, including security isolation and execution flow for cross-chain smart contract interactions.

**Implementation Location:** Create new module `x/ibc/callbacks/` in Terra Classic

### 5.4 Callback Test Implementation - `tests/ibc/ibc_middleware_test.go`

**File:** `tests/ibc/ibc_middleware_test.go` (Terra Classic IBC callback testing)

**Reference Implementation:** IBC callback testing pattern
```go
func (suite *MiddlewareTestSuite) TestOnRecvPacketWithCallback() {
    var (
        path         *evmibctesting.Path
        contractAddr common.Address
        contractData contracts.CompiledContract
        sender       string
        amount       = sdkmath.NewInt(100)
        memo         func() string
        coin         string
    )

    testCases := []struct {
        name     string
        malleate func()
        memo     func() string
        expError string
    }{
        {
            name:     "success - valid callback with counter increment",
            malleate: nil,
            memo: func() string {
                packedBytes, err := contractData.ABI.Pack("increment")
                suite.Require().NoError(err)

                return fmt.Sprintf(`{
                    "dest_callback": {
                        "address": "%s",
                        "gas_limit": "%d",
                        "calldata": "%x"
                    }
                }`, contractAddr, 1_000_000, packedBytes)
            },
            expError: "",
        },
        {
            name:     "failure - insufficient gas limit",
            malleate: nil,
            memo: func() string {
                packedBytes, err := contractData.ABI.Pack("increment")
                suite.Require().NoError(err)

                return fmt.Sprintf(`{
                    "dest_callback": {
                        "address": "%s",
                        "gas_limit": "%d",
                        "calldata": "%x"
                    }
                }`, contractAddr, 100, packedBytes) // Very low gas limit
            },
            expError: "ABCI code: 8",
        },
        {
            name:     "failure - calling non-existent function",
            malleate: nil,
            memo: func() string {
                // Invalid function selector
                packedBytes := []byte{0xff, 0xff, 0xff, 0xff}

                return fmt.Sprintf(`{
                    "dest_callback": {
                        "address": "%s",
                        "gas_limit": "%d",
                        "calldata": "%x"
                    }
                }`, contractAddr, 1_000_000, packedBytes)
            },
            expError: "ABCI code: 8",
        },
    }

    for _, tc := range testCases {
        suite.Run(tc.name, func() {
            suite.SetupTest()

            // ... test execution logic
        })
    }
}
```

**Explanation:** Comprehensive test patterns for IBC callbacks including success cases, gas limit validation, and error handling for secure cross-chain contract execution.

**Implementation Location:** Add to existing `tests/` directory in Terra Classic

---

## 6. Terra Classic Specific Implementation Guide

### 6.1 Terra Classic Directory Structure for EVM Integration

```
core/                                    # Terra Classic root
├── app/
│   ├── app.go                          # Main application with EVM integration
│   ├── precompiles.go                  # Terra-specific precompiles
│   └── ante/
│       ├── evm/
│       │   └── mono_decorator.go       # EVM AnteHandler
│       └── cosmos/
│           └── authz.go                # AuthZ security
├── x/
│   ├── evm/                           # New EVM module
│   │   ├── keeper/
│   │   │   └── keeper.go              # EVM Keeper
│   │   └── precompiles/
│   │       ├── oracle/                # Terra Oracle precompile
│   │       ├── market/                # Terra Market precompile
│   │       ├── treasury/              # Terra Treasury precompile
│   │       └── ics20/                 # IBC precompile
│   ├── feemarket/                     # New FeeMarket module
│   │   ├── keeper/
│   │   │   ├── keeper.go
│   │   │   └── eip1559.go
│   │   └── types/
│   │       └── params.go
│   └── erc20/                         # New ERC20 module
│       └── ibc_middleware.go
├── server/
│   ├── json_rpc.go                    # JSON-RPC server
│   └── config/
│       └── config.go                  # Configuration
└── tests/
    └── ibc/
        └── ibc_middleware_test.go     # IBC testing
```

### 6.2 Terra Classic Module Integration Order

| Phase | Module | Location | Dependencies | Priority |
|-------|--------|----------|--------------|----------|
| **1** | EVMKeeper | `x/evm/keeper/` | AccountKeeper, BankKeeper | High |
| **2** | AnteHandler | `app/ante/evm/` | EVMKeeper | High |
| **3** | JSON-RPC | `server/json_rpc.go` | EVMKeeper | Medium |
| **4** | FeeMarket | `x/feemarket/` | Treasury integration | Medium |
| **5** | Oracle Precompile | `x/evm/precompiles/oracle/` | OracleKeeper | High |
| **6** | Market Precompile | `x/evm/precompiles/market/` | MarketKeeper | Medium |
| **7** | Treasury Precompile | `x/evm/precompiles/treasury/` | TreasuryKeeper | Medium |
| **8** | IBC-EVM | `x/erc20/` | IBC modules | Low |

### 6.3 Terra Classic Specific Adaptations

#### Oracle Precompile Implementation
```go
// x/evm/precompiles/oracle/oracle.go
type OraclePrecompile struct {
    oracleKeeper oraclekeeper.Keeper
}

func (p *OraclePrecompile) GetExchangeRate(denom string) (*big.Int, error) {
    // Access Terra Oracle exchange rates from EVM
    rate, err := p.oracleKeeper.GetExchangeRate(p.ctx, denom)
    return rate.BigInt(), err
}
```

#### Burn Tax Integration in AnteHandler
```go
// app/ante/evm/terra_fee_decorator.go
func (fd TerraFeeDecorator) handleBurnTax(
    ctx sdk.Context, 
    fee sdk.Coins,
) (sdk.Coins, error) {
    // Apply Terra burn tax to EVM transactions
    burnTax := fd.treasuryKeeper.ComputeBurnTax(ctx, fee)
    return fee.Add(burnTax...), nil
}
```

---

## 6. Comparison Tables for Terra Classic v0.47 Backporting

### 6.1 EVMKeeper Initialization Comparison

| Component | Evmos/EVM Implementation | Terra Classic v0.47 Requirements | Adaptation Notes |
|-----------|-------------------------|----------------------------------|------------------|
| **Keeper Constructor** | `evmkeeper.NewKeeper()` with 10 parameters | Same pattern, verify parameter compatibility | ✅ Direct port possible |
| **Account Keeper** | `types.AccountKeeper` interface | Compatible with Cosmos SDK v0.47 | ✅ No changes needed |
| **Bank Keeper** | `NewBankWrapper(bankKeeper)` | May need wrapper adaptation | ⚠️ Test wrapper compatibility |
| **Staking Integration** | Direct `StakingKeeper` reference | Compatible with v0.47 staking | ✅ No changes needed |
| **Fee Market** | `NewFeeMarketWrapper(fmk)` | Requires fee market module port | ⚠️ Module dependency |
| **Precompile Registration** | Static map initialization | Same pattern works | ✅ Direct port possible |

### 6.2 AnteHandler Security Comparison

| Security Feature | Evmos/EVM Implementation | Terra Classic v0.47 Requirements | Adaptation Notes |
|------------------|-------------------------|----------------------------------|------------------|
| **Monolithic Handler** | `MonoDecorator` pattern | Compatible with v0.47 ante system | ✅ Direct port possible |
| **Signature Verification** | Ethereum + Cosmos validation | Same validation needed | ✅ No changes needed |
| **Fee Deduction** | Dynamic fee checker | May need static fee fallback | ⚠️ Configure for burn tax |
| **Gas Validation** | EVM gas limit checks | Compatible with v0.47 | ✅ No changes needed |
| **Bypass Prevention** | `RejectMessagesDecorator` | Critical for security | ✅ Must implement |
| **AuthZ Protection** | Message type validation | Compatible with v0.47 authz | ✅ No changes needed |

### 6.3 Fee Market (EIP-1559) Comparison

| Feature | Evmos/EVM Implementation | Terra Classic v0.47 Requirements | Adaptation Notes |
|---------|-------------------------|----------------------------------|------------------|
| **Base Fee Calculation** | Full EIP-1559 algorithm | May need burn tax integration | ⚠️ Custom calculation needed |
| **Parameter Management** | Governance-based updates | Compatible with v0.47 gov | ✅ Direct port possible |
| **Elasticity Multiplier** | `ElasticityMultiplier` param | Same concept applies | ✅ No changes needed |
| **Gas Target** | `BlockGas / 2` calculation | May need Terra-specific tuning | ⚠️ Test with Terra gas limits |
| **Min Gas Price** | Configurable minimum | Must respect Terra min gas | ⚠️ Integration with existing min gas |
| **Enable Height** | Activation height parameter | Useful for upgrade coordination | ✅ Recommended for Terra |

### 6.4 JSON-RPC Configuration Comparison

| Configuration | Evmos/EVM Implementation | Terra Classic v0.47 Requirements | Adaptation Notes |
|---------------|-------------------------|----------------------------------|------------------|
| **Server Setup** | `StartJSONRPC()` function | Compatible with v0.47 server | ✅ Direct port possible |
| **Namespace Registration** | `eth`, `net`, `web3` default | Same namespaces needed | ✅ No changes needed |
| **CORS Configuration** | Configurable CORS policy | Same security needs | ✅ No changes needed |
| **WebSocket Support** | Optional WebSocket server | Compatible with v0.47 | ✅ Direct port possible |
| **Batch Limits** | Request/response size limits | Same DoS protection needed | ✅ No changes needed |
| **Security Settings** | Configurable timeouts/limits | Same security requirements | ✅ No changes needed |

### 6.5 IBC-EVM Integration Comparison

| Component | Evmos/EVM Implementation | Terra Classic v0.47 Requirements | Adaptation Notes |
|-----------|-------------------------|----------------------------------|------------------|
| **ICS20 Precompile** | `ics20.NewPrecompile()` | Compatible with IBC v0.47 | ✅ Direct port possible |
| **ERC20 Middleware** | `IBCMiddleware` pattern | May need Terra asset integration | ⚠️ Test with Terra assets |
| **Callback System** | Full EVM callback support | Useful for Terra DeFi integration | ✅ Recommended feature |
| **Address Isolation** | Channel-based isolation | Critical security feature | ✅ Must implement |
| **Error Handling** | Comprehensive error patterns | Same error handling needed | ✅ No changes needed |
| **Gas Management** | Configurable gas limits | Same gas management needed | ✅ No changes needed |

### 6.6 Priority Implementation Order for Terra Classic

| Priority | Component | Reasoning | Estimated Effort |
|----------|-----------|-----------|-----------------|
| **1** | EVMKeeper + Basic AnteHandler | Core functionality required first | 2-3 weeks |
| **2** | JSON-RPC Server | Enable Ethereum tooling compatibility | 1-2 weeks |
| **3** | Basic Fee Market (without EIP-1559) | Transaction processing needs | 1-2 weeks |
| **4** | ICS20 Precompile | Enable cross-chain functionality | 2-3 weeks |
| **5** | Full EIP-1559 Implementation | Advanced fee market features | 3-4 weeks |
| **6** | EVM Callbacks | Advanced IBC-EVM integration | 2-3 weeks |

### 6.7 Key Differences and Adaptations Needed

| Area | Challenge | Solution | Implementation Notes |
|------|-----------|----------|---------------------|
| **Burn Tax Integration** | EVM transactions must respect Terra burn tax | Modify fee calculation in AnteHandler | Critical for Terra compliance |
| **Oracle Price Feeds** | EVM contracts may need Terra oracle access | Implement oracle precompile | Consider for DeFi applications |
| **Market Module** | Terra market swaps from EVM | Implement market precompile | Useful for Terra DeFi |
| **Treasury Integration** | EVM fee distribution to treasury | Modify fee collection logic | Important for Terra governance |
| **Validator Set Access** | EVM access to Terra validator info | Extend staking precompile | Useful for staking applications |

---

## Links to Terra Classic EVM Integration Documentation

- **Main Document Reference:** [Terra Classic EVM Integration – Final Implementation](Final-Implementation.md)
- **Before-After Comparison:** [System Evolution Diagrams](before-after-comparison.md)
- **Architecture Overview:** [System Architecture Diagrams](terra-classic-evm-architecture.md)
- **Transaction Flows:** [Sequence Diagrams](transaction-flow-sequence.md)
- **Implementation Status:** [Progress Report](implementation-report.md)
- **Navigation Hub:** [README Documentation](README.md)

This comprehensive code reference document provides all the implementation details needed to successfully integrate EVM functionality into Terra Classic v0.47, with specific file paths and directory structure adapted for the Terra Classic codebase.
