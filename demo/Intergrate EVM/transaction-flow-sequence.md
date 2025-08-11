# Terra Classic EVM Integration - Transaction Flow Sequence Diagrams

## Overview
This document provides detailed sequence diagrams showing how different types of transactions flow through the Terra Classic EVM integration system.

## Sequence Diagrams

### 1. EVM Transaction Flow (Smart Contract Call)

```mermaid
sequenceDiagram
    participant User as 👤 User (MetaMask)
    participant RPC as 🌐 JSON-RPC Server
    participant Ante as 🛡️ AnteHandler
    participant EVM as ⚡ EVMKeeper
    participant VM as 🔧 Go-Ethereum VM
    participant State as 💾 StateDB
    participant Terra as 🌍 Terra Modules
    participant Consensus as ⚖️ Consensus

    User->>RPC: eth_sendTransaction
    Note over User,RPC: EIP-1559 tra◊nsaction with<br/>gas price and priority fee
    
    RPC->>Ante: ProcessTransaction
    Note over RPC,Ante: Convert JSON-RPC to<br/>Cosmos SDK transaction
    
    Ante->>Ante: CheckEVMExtension
    Note over Ante: Detect EVM transaction<br/>by ExtensionOptionsEthereumTx
    
    Ante->>Ante: ValidateBasic
    Ante->>Ante: CheckGasPrice (EIP-1559)
    Ante->>Ante: VerifySignature
    Ante->>Ante: DeductFee
    
    Ante->>EVM: ProcessEthereumTx
    
    EVM->>State: NewStateDB
    Note over EVM,State: Create isolated state<br/>for transaction execution
    
    EVM->>VM: NewEVM
    EVM->>VM: Call(to, data, gas, value)
    
    alt Smart Contract Call
        VM->>VM: ExecuteContract
        VM->>State: GetCode
        VM->>State: GetState
        VM->>State: SetState
        
        alt Precompile Call
            VM->>Terra: CallPrecompile
            Note over VM,Terra: Access Oracle, Market,<br/>Treasury, Staking, Gov
            Terra-->>VM: Result
        end
        
        VM-->>EVM: ExecutionResult
    else Contract Creation
        VM->>VM: Create
        VM->>State: SetCode
        VM-->>EVM: ContractAddress
    end
    
    EVM->>State: Commit
    Note over EVM,State: Apply state changes<br/>to main state tree
    
    EVM-->>Ante: TransactionResponse
    Ante-->>RPC: Success/Error
    RPC-->>User: Transaction Hash
    
    Note over Consensus: Transaction included<br/>in next block
    
    Consensus->>State: FinalizeBlock
    State->>Terra: UpdateModuleState
```

### 2. Cross-Chain IBC-EVM Transaction Flow

```mermaid
sequenceDiagram
    participant SourceChain as 🔗 Source Chain
    participant SourceEVM as ⚡ Source EVM
    participant IBCCore as 🌉 IBC Core
    participant TerraIBC as 🌍 Terra IBC
    participant TerraEVM as ⚡ Terra EVM
    participant ERC20 as 💰 ERC20 Bridge
    participant Callback as 📞 IBC Callback
    
    SourceChain->>SourceEVM: Transfer ERC20 via IBC
    Note over SourceChain,SourceEVM: User calls ICS20 precompile<br/>to initiate cross-chain transfer
    
    SourceEVM->>IBCCore: SendPacket
    Note over SourceEVM,IBCCore: IBC packet with<br/>ERC20 token data
    
    IBCCore->>TerraIBC: RelayPacket
    
    TerraIBC->>ERC20: OnRecvPacket
    Note over TerraIBC,ERC20: ERC20 middleware processes<br/>incoming token transfer
    
    ERC20->>ERC20: ConvertCoin
    Note over ERC20: Convert IBC token to<br/>ERC20 representation
    
    ERC20->>TerraEVM: MintERC20
    TerraEVM->>TerraEVM: CreateContract
    
    ERC20->>Callback: TriggerCallback
    Note over ERC20,Callback: Optional smart contract<br/>callback execution
    
    alt Callback Enabled
        Callback->>TerraEVM: ExecuteContract
        TerraEVM->>TerraEVM: ProcessCallback
        Note over TerraEVM: Execute receiving contract<br/>with transferred tokens
        TerraEVM-->>Callback: CallbackResult
    end
    
    Callback-->>TerraIBC: PacketAck
    TerraIBC-->>IBCCore: AckPacket
    IBCCore-->>SourceChain: RelayAck
    
    Note over SourceChain,TerraEVM: Cross-chain ERC20 transfer<br/>with optional callback complete
```

### 3. Terra Native Module Access via Precompiles

```mermaid
sequenceDiagram
    participant Contract as 📄 Smart Contract
    participant EVM as ⚡ EVMKeeper
    participant Precompile as 🔧 Precompile
    participant Oracle as 🔮 Oracle Module
    participant Market as 📈 Market Module
    participant Treasury as 🏛️ Treasury Module
    participant Bank as 🏦 Bank Module
    
    Contract->>EVM: Call Oracle Precompile (0x1001)
    Note over Contract,EVM: Get LUNC/USD price feed
    
    EVM->>Precompile: InvokePrecompile
    Precompile->>Oracle: GetExchangeRate("uusd")
    Oracle-->>Precompile: Price Data
    Precompile-->>EVM: Encoded Result
    EVM-->>Contract: Price (uint256)
    
    Contract->>EVM: Call Market Precompile (0x1002)
    Note over Contract,EVM: Swap LUNC for Terra assets
    
    EVM->>Precompile: InvokePrecompile
    Precompile->>Market: Swap(offer_coin, ask_denom)
    Market->>Bank: SendCoins
    Bank-->>Market: Transfer Result
    Market-->>Precompile: Swap Result
    Precompile-->>EVM: Success/Failure
    EVM-->>Contract: Transaction Result
    
    Contract->>EVM: Call Treasury Precompile (0x1003)
    Note over Contract,EVM: Burn/Mint operations
    
    EVM->>Precompile: InvokePrecompile
    Precompile->>Treasury: BurnCoins(amount)
    Treasury->>Bank: BurnCoins
    Note over Treasury,Bank: Reduce total supply
    Bank-->>Treasury: Burn Confirmation
    Treasury-->>Precompile: Operation Result
    Precompile-->>EVM: Success/Failure
    EVM-->>Contract: Burn Confirmed
    
    Note over Contract,Bank: Smart contract successfully<br/>accessed Terra Classic modules
```

### 4. Fee Market (EIP-1559) Processing

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant RPC as 🌐 JSON-RPC
    participant FeeMarket as 💰 Fee Market
    participant Ante as 🛡️ AnteHandler
    participant Bank as 🏦 Bank Module
    participant Block as 📦 Block Processing
    
    User->>RPC: eth_sendTransaction
    Note over User,RPC: maxFeePerGas: 50 gwei<br/>maxPriorityFeePerGas: 5 gwei
    
    RPC->>FeeMarket: GetBaseFee
    FeeMarket-->>RPC: baseFee: 25 gwei
    
    RPC->>RPC: CalculateEffectiveGas
    Note over RPC: effectiveGasPrice = min(<br/>maxFeePerGas,<br/>baseFee + maxPriorityFeePerGas)
    
    RPC->>Ante: ProcessTransaction
    Note over RPC,Ante: effectiveGasPrice = 30 gwei<br/>(25 + 5)
    
    Ante->>FeeMarket: ValidateGasPrice
    FeeMarket->>FeeMarket: CheckMinGasPrice
    Note over FeeMarket: Ensure >= 12.5 gwei minimum
    
    FeeMarket-->>Ante: GasPrice Valid
    
    Ante->>Bank: DeductFees
    Note over Ante,Bank: Deduct: gasLimit × effectiveGasPrice
    Bank-->>Ante: Fee Deducted
    
    Note over Block: Transaction executed<br/>Gas used: 21,000
    
    Block->>Bank: RefundGas
    Note over Block,Bank: Refund: (gasLimit - gasUsed)<br/>× effectiveGasPrice
    
    Block->>FeeMarket: UpdateBaseFee
    Note over Block,FeeMarket: Based on block gas usage<br/>vs target (15M gas)
    
    alt Block > Target
        FeeMarket->>FeeMarket: IncreaseBaseFee
        Note over FeeMarket: baseFee × 1.125<br/>(12.5% increase)
    else Block < Target
        FeeMarket->>FeeMarket: DecreaseBaseFee
        Note over FeeMarket: baseFee × 0.875<br/>(12.5% decrease)
    end
    
    FeeMarket->>Block: NewBaseFee
    Note over FeeMarket,Block: New base fee for<br/>next block: 28.125 gwei
```

### 5. AnteHandler Security Flow

```mermaid
sequenceDiagram
    participant Tx as 📄 Transaction
    participant Router as 🔀 Ante Router
    participant EVMAnte as 🛡️ EVM AnteHandler
    participant CosmosAnte as 🛡️ Cosmos AnteHandler
    participant Security as 🔒 Security Checks
    participant Execution as ⚡ Execution
    
    Tx->>Router: IncomingTransaction
    
    Router->>Router: DetectTransactionType
    
    alt EVM Transaction
        Router->>Security: CheckEVMExtension
        Security->>Security: ValidateExtensionOptions
        
        alt Missing Extension
            Security-->>Router: Reject: MsgEthereumTx without extension
            Router-->>Tx: Error: Security violation
        end
        
        Security->>EVMAnte: ProcessEVMTx
        
        EVMAnte->>EVMAnte: ValidateBasic
        EVMAnte->>EVMAnte: CheckNonce
        EVMAnte->>EVMAnte: VerifySignature
        EVMAnte->>EVMAnte: ValidateGasPrice
        EVMAnte->>EVMAnte: CheckGasLimit
        EVMAnte->>EVMAnte: DeductFee
        
        EVMAnte-->>Execution: ProcessTransaction
        
    else Cosmos Transaction
        Router->>Security: CheckAuthZBypass
        Note over Router,Security: Prevent AuthZ bypass attacks
        
        Security->>CosmosAnte: ProcessCosmosTx
        
        CosmosAnte->>CosmosAnte: SetUpContextDecorator
        CosmosAnte->>CosmosAnte: RejectExtensionOptionsDecorator
        CosmosAnte->>CosmosAnte: MempoolFeeDecorator
        CosmosAnte->>CosmosAnte: ValidateBasicDecorator
        CosmosAnte->>CosmosAnte: TxTimeoutHeightDecorator
        CosmosAnte->>CosmosAnte: ValidateMemoDecorator
        CosmosAnte->>CosmosAnte: ConsumeGasForTxSizeDecorator
        CosmosAnte->>CosmosAnte: DeductFeeDecorator
        CosmosAnte->>CosmosAnte: SetPubKeyDecorator
        CosmosAnte->>CosmosAnte: ValidateSigCountDecorator
        CosmosAnte->>CosmosAnte: SigGasConsumeDecorator
        CosmosAnte->>CosmosAnte: SigVerificationDecorator
        CosmosAnte->>CosmosAnte: IncrementSequenceDecorator
        
        CosmosAnte-->>Execution: ProcessTransaction
    end
    
    Execution->>Execution: ExecuteTransaction
    Execution-->>Router: TransactionResult
    Router-->>Tx: Success/Error
    
    Note over Tx,Execution: Dual security validation<br/>for hybrid EVM/Cosmos chain
```

## Transaction Types Summary

### EVM Transactions
- **Type**: `MsgEthereumTx` with `ExtensionOptionsEthereumTx`
- **Gas**: EIP-1559 pricing (base fee + priority fee)
- **Signature**: ECDSA secp256k1 (Ethereum format)
- **Data**: Contract calls, deployments, transfers
- **Routing**: EVM AnteHandler → EVMKeeper → Go-Ethereum VM

### Cosmos Transactions
- **Type**: Standard Cosmos SDK messages
- **Gas**: Fixed gas prices in LUNC
- **Signature**: ECDSA secp256k1 (Cosmos format)
- **Data**: Bank transfers, staking, governance, IBC
- **Routing**: Cosmos AnteHandler → Message Router → Module

### Cross-Chain Transactions
- **Type**: IBC packets with EVM callbacks
- **Processing**: IBC Core → ERC20 Middleware → Callback execution
- **Assets**: Automatic ERC20 representation of IBC tokens
- **Security**: Gas-limited callback execution (1M gas max)

## Security Checkpoints

1. **Transaction Type Detection**: Prevent mixing EVM/Cosmos transaction types
2. **Extension Validation**: Ensure EVM transactions have proper extensions
3. **AuthZ Bypass Prevention**: Block unauthorized privilege escalation
4. **Gas Limit Enforcement**: Prevent DoS attacks through resource exhaustion
5. **Signature Verification**: Validate cryptographic signatures for both formats
6. **Fee Market Protection**: Ensure adequate fees to prevent spam
7. **State Isolation**: Isolate EVM execution from Cosmos state until commit
8. **Precompile Access Control**: Validate permissions for Terra module access

---

*This document is part of the Terra Classic EVM Integration project. Last updated: 2025-08-11*
