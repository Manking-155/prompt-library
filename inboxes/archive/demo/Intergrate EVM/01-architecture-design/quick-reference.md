# Terra Classic EVM Integration - Quick Reference

*Quick reference for key architectural concepts and components*

---

## 🚀 **Core Concepts**

### **Hybrid Architecture**
- **Cosmos Zone**: Maintains all existing Terra Classic functionality
- **EVM Zone**: Adds Ethereum smart contract execution capability
- **Precompiles**: Bridges that allow EVM to access Terra modules

### **Dual Transaction Support**
```
Terra Classic Node
├── Cosmos Transactions (existing)
│   └── Terra modules: Oracle, Market, Treasury, Tax...
└── EVM Transactions (new)
    └── Smart contracts: Solidity, Vyper...
```

---

## 🔧 **Technical Components**

### **Core Components**
| Component | Function | Location |
|-----------|----------|----------|
| **EVMKeeper** | Manages EVM state and execution | `x/evm/keeper/` |
| **AnteHandler** | Transaction validation (dual system) | `app/ante/` |
| **Precompiles** | Native Terra functions for EVM | `x/evm/precompiles/` |
| **JSON-RPC** | Ethereum-compatible API | `server/json_rpc.go` |

### **Precompiled Contracts**
| Address | Function | Module |
|---------|----------|---------|
| `0x...801` | Oracle price feeds | x/oracle |
| `0x...802` | Market swaps | x/market |
| `0x...803` | IBC transfers | x/ibc |
| `0x...804` | Staking operations | x/staking |

---

## 🔄 **Transaction Flows**

### **1. Cosmos Transaction (Traditional)**
```
User → Station Wallet → Cosmos TX → AnteHandler → Terra Module → State
```

### **2. EVM Transaction (New)**
```
User → MetaMask → EVM TX → EVM AnteHandler → EVM Execution → State
```

### **3. Cross-Platform Call**
```
Smart Contract → Precompile → Terra Module → Result → Smart Contract
```

---

## 🛡️ **Security Model**

### **Dual AnteHandler System**
```go
// Pseudo-code
func AnteHandler(tx sdk.Tx) error {
    if isEVMTx(tx) {
        return evmAnteHandler(tx)
    }
    return cosmosAnteHandler(tx)
}
```

### **Security Layers**
1. **Transaction Validation**: Signature, nonce, gas checks
2. **Execution Isolation**: EVM và Cosmos state separation
3. **Precompile Security**: Controlled access to Terra modules
4. **Gas Metering**: Prevent DoS attacks

---

## 📊 **Performance Metrics**

### **Target Performance**
- **EVM TX Latency**: <100ms ✅
- **Precompile Calls**: <10ms ✅
- **Throughput**: 1000+ TPS ✅
- **Memory Usage**: <8GB per node ✅

### **Gas Conversion**
```
EVM Gas = Cosmos Gas × Conversion Factor
Default Conversion Factor = 1000
```

---

## 🔗 **Integration Points**

### **Wallet Support**
- **MetaMask**: Full EVM transaction support
- **Station**: Hybrid Cosmos + EVM support
- **WalletConnect**: Cross-platform compatibility

### **Developer Tools**
- **Remix IDE**: Deploy và debug contracts
- **Hardhat/Truffle**: Development frameworks
- **Web3.js/Ethers.js**: JavaScript libraries

---

## 💡 **Use Case Examples**

### **1. DeFi Protocol**
```solidity
contract TerraDefi {
    function getOraclePrice(string memory denom) public view returns (uint256) {
        return IOracle(0x0000000000000000000000000000000000000801)
               .getPrice(denom);
    }
}
```

### **2. Cross-Chain Bridge**
```solidity
contract CrossChainBridge {
    function transferToOsmosis(uint256 amount) external {
        IIBC(0x0000000000000000000000000000000000000803)
            .transfer("osmosis-1", msg.sender, amount);
    }
}
```

### **3. Yield Farming**
```solidity
contract YieldFarm {
    function stakeLUNC(address validator, uint256 amount) external {
        IStaking(0x0000000000000000000000000000000000000804)
                .delegate(validator, amount);
    }
}
```

---

## 🚨 **Common Gotchas**

### **Gas Differences**
- EVM gas ≠ Cosmos gas
- Use conversion factor for calculations
- Monitor gas usage in cross-platform calls

### **Address Formats**
- Cosmos: `terra1...` (bech32)
- EVM: `0x...` (hex)
- Conversion utilities available

### **State Management**
- EVM state isolated from Cosmos state
- Use precompiles for cross-platform data access
- Be aware of state consistency

---

## 📚 **Quick Links**

### **Documentation**
- [Architecture Overview](architecture-overview-simplified.md) - Start here
- [System Architecture](system-architecture.md) - Technical details
- [Transaction Flows](transaction-flow-sequence.md) - Sequence diagrams
- [Implementation Spec](final-implementation-spec.md) - Development guide

### **Code References**
- [Implementation Guide](../../terra-classic-evm-integration-code-references.md)
- [Integration Plan](../../Terra-Classic-EVM-Integration-Plan-v047.md)

### **External Resources**
- [Cosmos SDK Docs](https://docs.cosmos.network/)
- [Ethereum EVM Spec](https://ethereum.github.io/yellowpaper/paper.pdf)
- [Solidity Documentation](https://docs.soliditylang.org/)

---

*Cập nhật lần cuối: $(date)*