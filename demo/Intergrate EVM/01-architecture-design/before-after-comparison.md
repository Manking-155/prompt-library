# Terra Classic (LUNC) - So Sánh Trước và Sau Khi Tích Hợp EVM

## Tổng Quan
Document này cung cấp so sánh chi tiết về kiến trúc và tính năng của Terra Classic trước và sau khi tích hợp EVM module.

## 1. Kiến Trúc Hệ Thống - So Sánh Tổng Thể

### Tóm tắt kiến trúc (bảng so sánh nhanh):

| Thành phần                | Trước (Cosmos SDK)         | Sau (Cosmos SDK + EVM)         |
|--------------------------|----------------------------|---------------------------------|
| Application Layer        | Terra Station, CLI         | + MetaMask, Web3 DApps         |
| API                      | LCD API                    | + JSON-RPC Server              |
| Smart Contract           | CosmWasm                   | + EVM (Solidity)               |
| Module                   | Auth, Bank, Staking, ...   | + EVM, Fee Market, ERC20       |
| Consensus                | Tendermint                 | Tendermint (Dual AnteHandler)   |
| Storage                  | IAVL, LevelDB              | + EVM State, Precompiles        |
### So Sánh Kiến Trúc Chi Tiết

<div style="display: flex; gap: 20px; align-items: flex-start;">

<div style="flex: 1;">

#### TRƯỚC: Terra Classic Original

```mermaid
flowchart TD
    subgraph BEFORE["🔵 TRƯỚC: Terra Classic Original"]
        subgraph AppLayer["Application Layer"]
            A1[Terra Station] 
            A3[CLI Tools]
            A2[Terra Classic API]
        end
        subgraph CosmosSDK["Cosmos SDK v0.46"]
            B1[Auth Module]
            B2[Bank Module] 
            B3[Staking Module]
            B4[Gov Module]
            B5[Oracle Module]
            B6[Market Module]
            B7[Treasury Module]
            B8[Wasm Module]
        end
        subgraph Consensus["Consensus & Networking"]
            C1[Tendermint Core]
            C2[P2P Network]
            C3[ABCI Interface]
        end
        subgraph Storage["Storage"]
            D1[IAVL Tree]
            D2[LevelDB]
        end
        
        A1 --> A2
        A3 --> A2
        A2 --> B1
        B1 --> B2
        B2 --> B3
        B3 --> B4
        B4 --> B5
        B5 --> B6
        B6 --> B7
        B7 --> B8
        B8 --> C1
        C1 --> C2
        C2 --> C3
        C3 --> D1
        D1 --> D2
    end
```

</div>

<div style="flex: 1;">

#### SAU: Terra Classic với EVM

```mermaid
flowchart TD
    subgraph AFTER["🟢 SAU: Terra Classic with EVM"]
        subgraph AppLayer2["Application Layer Enhanced"]
            E1[Terra Station]
            E3[🆕 MetaMask]
            E5[🆕 Web3 DApps]
            E6[CLI Tools]
            E2[Terra Classic API]
            E4[🆕 JSON-RPC Server]
        end
        subgraph CosmosSDK2["Cosmos SDK v0.47 + EVM"]
            F1[Auth Module]
            F2[Bank Module]
            F3[Staking Module]
            F4[Gov Module]
            F5[Oracle Module]
            F6[Market Module]
            F7[Treasury Module]
            F8[Wasm Module]
            F9[🆕 EVM Module]
            F10[🆕 Fee Market]
            F11[🆕 ERC20 Module]
        end
        subgraph EVMRuntime["🆕 EVM Runtime"]
            G1[Go-Ethereum VM]
            G2[StateDB]
            G3[🆕 Precompiles]
            G4[🆕 EVM Keeper]
        end
        subgraph Consensus2["Enhanced Consensus"]
            H1[Tendermint Core]
            H2[P2P Network]
            H3[🆕 EVM AnteHandler]
            H4[ABCI Interface]
        end
        subgraph Storage2["Hybrid Storage"]
            I1[IAVL Tree]
            I2[🆕 EVM State]
            I3[LevelDB]
        end
        
        E1 --> E2
        E3 --> E4
        E5 --> E4
        E6 --> E2
        E2 --> F1
        E4 --> F9
        F1 --> F2
        F2 --> F3
        F3 --> F4
        F4 --> F5
        F5 --> F6
        F6 --> F7
        F7 --> F8
        F8 --> F9
        F9 --> F10
        F10 --> F11
        F11 --> G1
        G1 --> G2
        G2 --> G3
        G3 --> G4
        G4 --> H1
        H1 --> H2
        H2 --> H3
        H3 --> H4
        H4 --> I1
        I1 --> I2
        I2 --> I3
    end
    
    %% Styles for new components
    style F9 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style F10 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style F11 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style G1 fill:#FF9800,stroke:#F57C00,color:#fff
    style G2 fill:#FF9800,stroke:#F57C00,color:#fff
    style G3 fill:#FF9800,stroke:#F57C00,color:#fff
    style G4 fill:#FF9800,stroke:#F57C00,color:#fff
    style H3 fill:#2196F3,stroke:#1976D2,color:#fff
    style I2 fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style E3 fill:#FFC107,stroke:#FF8F00,color:#000
    style E4 fill:#FFC107,stroke:#FF8F00,color:#000
    style E5 fill:#FFC107,stroke:#FF8F00,color:#000
```

</div>

</div>

## 2. Luồng Giao Dịch - Trước và Sau

<div style="display: flex; gap: 20px; align-items: flex-start;">

<div style="flex: 1;">

### Luồng Giao Dịch: Trước và Sau Khi Tích Hợp EVM

#### 1. TRƯỚC: Chỉ Cosmos SDK Transactions

```mermaid
sequenceDiagram
    participant User as 👤 Người Dùng
    participant CLI as 💻 Terra CLI
    participant API as 🌐 LCD API
    participant Node as 🔗 Terra Node
    participant Modules as 📦 Terra Modules
    participant DB as 💾 Database

    User->>CLI: terrad tx bank send
    CLI->>API: POST /cosmos/tx/v1beta1/txs
    API->>Node: ProcessTransaction

    Node->>Node: ValidateBasic
    Node->>Node: AnteHandler Check
    Node->>Node: DeductFee (LUNC)

    Node->>Modules: RouteMessage
    alt Bank Transfer
        Modules->>Modules: SendCoins
    else Oracle Vote
        Modules->>Modules: AggregateExchangeRateVote
    else Market Swap
        Modules->>Modules: MsgSwap
    end

    Modules->>DB: UpdateState
    DB-->>User: Transaction Hash

    Note over User,DB: Chỉ hỗ trợ Terra native operations\nKhông có smart contracts\nKhông tương thích Ethereum
```

---

#### 2. SAU: Hybrid Cosmos + EVM Transactions

##### a. EVM Transaction Flow (MỚI)

```mermaid
sequenceDiagram
    participant MetaMask as 🦊 MetaMask
    participant RPC as 🌐 JSON-RPC
    participant Node as 🔗 Terra Node
    participant EVMKeeper as ⚡ EVM Keeper
    participant EVMState as 💾 EVM State

    MetaMask->>RPC: eth_sendTransaction
    RPC->>Node: MsgEthereumTx
    Node->>Node: EVM AnteHandler
    Node->>EVMKeeper: ProcessEthereumTx
    EVMKeeper->>EVMKeeper: Execute Smart Contract
    EVMKeeper->>EVMState: Update EVM State
    EVMState-->>MetaMask: Transaction Hash

    Note over MetaMask,EVMState: Giao dịch EVM, hỗ trợ smart contract, tương thích Ethereum
```

##### b. Cosmos Transaction Flow (CŨ + CẢI TIẾN)

```mermaid
sequenceDiagram
    participant CLI as 💻 Terra CLI
    participant API as 🌐 LCD API
    participant Node as 🔗 Terra Node
    participant CosmosModules as 📦 Terra Modules
    participant CosmosState as 💾 Cosmos State

    CLI->>API: POST /cosmos/tx/v1beta1/txs
    API->>Node: Standard Cosmos Tx
    Node->>Node: Cosmos AnteHandler
    Node->>CosmosModules: RouteMessage
    CosmosModules->>CosmosState: Update Cosmos State
    CosmosState-->>CLI: Transaction Hash

    Note over CLI,CosmosState: Giao dịch Cosmos truyền thống, vẫn được hỗ trợ đầy đủ
```

##### c. Cross-Chain Interaction (MỚI)

```mermaid
sequenceDiagram
    participant MetaMask as 🦊 MetaMask
    participant RPC as 🌐 JSON-RPC
    participant EVMKeeper as ⚡ EVM Keeper
    participant CosmosModules as 📦 Terra Modules
    participant CosmosState as 💾 Cosmos State

    MetaMask->>RPC: Call Precompile (0x1001)
    RPC->>EVMKeeper: InvokePrecompile
    EVMKeeper->>CosmosModules: Access Terra Modules
    CosmosModules->>CosmosState: Read/Write State
    CosmosState-->>MetaMask: Result via EVM

    Note over MetaMask,CosmosState: Tương tác cross-chain, truy cập module Terra từ EVM
```


## 3. So Sánh Tính Năng Chi Tiết
<div style="display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">

<div style="flex: 1; min-width: 320px;">

#### 3.1 Khả Năng Giao Dịch

```mermaid
graph LR
    subgraph "TRƯỚC"
        A1[✅ LUNC Transfers] --> A2[✅ Staking LUNC]
        A2 --> A3[✅ Governance Voting]
        A3 --> A4[✅ Oracle Price Feeds]
        A4 --> A5[✅ Market Swaps]
        A5 --> A6[✅ IBC Transfers]
        A6 --> A7[✅ CosmWasm Contracts]
    end
```

</div>

<div style="flex: 1; min-width: 320px;">

#### 3.1 Khả Năng Giao Dịch (SAU)

```mermaid
graph LR
    subgraph "SAU"
        B1[✅ LUNC Transfers] --> B2[✅ Staking LUNC]
        B2 --> B3[✅ Governance Voting]
        B3 --> B4[✅ Oracle Price Feeds]
        B4 --> B5[✅ Market Swaps]
        B5 --> B6[✅ IBC Transfers]
        B6 --> B7[✅ CosmWasm Contracts]
        B7 --> B8[🆕 EVM Smart Contracts]
        B8 --> B9[🆕 ERC20 Tokens]
        B9 --> B10[🆕 Ethereum DApps]
        B10 --> B11[🆕 MetaMask Support]
        B11 --> B12[🆕 Cross-EVM Bridge]
        B12 --> B13[🆕 Terra Precompiles]
    end

    style B8 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style B9 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style B10 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style B11 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style B12 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style B13 fill:#4CAF50,stroke:#2E7D32,color:#fff
```

</div>
</div>

<div style="height: 32px"></div>

<div style="display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">

<div style="flex: 1; min-width: 320px;">
<div style="display: flex; gap: 32px; align-items: flex-start; flex-wrap: wrap;">

<div style="flex: 1; min-width: 320px;">

#### 3.2 Wallet Support (TRƯỚC)

```mermaid
graph TD
    subgraph "TRƯỚC - Wallet Support"
        C1[Terra Station] --> C2[Keplr]
        C2 --> C3[CLI Wallet]
        C3 --> C4[Ledger Hardware]
    end
```

</div>

<div style="flex: 1; min-width: 320px;">

#### 3.2 Wallet Support (SAU)

```mermaid
graph TD
    subgraph "SAU - Enhanced Wallet Support"
        D1[Terra Station] --> D2[Keplr]
        D2 --> D3[CLI Wallet]
        D3 --> D4[Ledger Hardware]
        D4 --> D5[🆕 MetaMask]
        D5 --> D6[🆕 WalletConnect]
        D6 --> D7[🆕 Trust Wallet]
        D7 --> D8[🆕 Coinbase Wallet]
        D8 --> D9[🆕 All Ethereum Wallets]
    end

    style D5 fill:#FF9800,stroke:#F57C00,color:#fff
    style D6 fill:#FF9800,stroke:#F57C00,color:#fff
    style D7 fill:#FF9800,stroke:#F57C00,color:#fff
    style D8 fill:#FF9800,stroke:#F57C00,color:#fff
    style D9 fill:#FF9800,stroke:#F57C00,color:#fff
```

</div>
</div>

## 4. Developer Experience Comparison

### 4.1 Trước: Terra Classic Development

```mermaid
graph TD
    subgraph "Terra Classic Development (TRƯỚC)"
        E1[Go Language] --> E2[Cosmos SDK]
        E2 --> E3[Terra Modules]
        E3 --> E4[CLI Testing]
        E4 --> E5[Testnet Deploy]
        
        F1[CosmWasm] --> F2[Rust Language]
        F2 --> F3[Wasm Contracts]
        F3 --> F4[terra.js Testing]
        F4 --> F5[Upload to Chain]
    end
```

### 4.2 Sau: Enhanced Development

```mermaid
graph TD
    subgraph "Enhanced Development (SAU)"
        G1[Go Language] --> G2[Cosmos SDK v0.47]
        G2 --> G3[Terra Modules]
        G3 --> G4[CLI Testing]
        G4 --> G5[Testnet Deploy]
        
        H1[CosmWasm] --> H2[Rust Language]
        H2 --> H3[Wasm Contracts]
        H3 --> H4[terra.js Testing]
        H4 --> H5[Upload to Chain]
        
        I1[🆕 Solidity] --> I2[🆕 Ethereum Tools]
        I2 --> I3[🆕 Hardhat/Truffle]
        I3 --> I4[🆕 Web3.js/Ethers.js]
        I4 --> I5[🆕 Remix IDE]
        I5 --> I6[🆕 MetaMask Testing]
        I6 --> I7[🆕 EVM Deploy]
        
        J1[🆕 Cross-Platform] --> J2[🆕 Terra Precompiles]
        J2 --> J3[🆕 Solidity ↔ Cosmos]
        J3 --> J4[🆕 Unified DApps]
    end
    
    style I1 fill:#2196F3,stroke:#1976D2,color:#fff
    style I2 fill:#2196F3,stroke:#1976D2,color:#fff
    style I3 fill:#2196F3,stroke:#1976D2,color:#fff
    style I4 fill:#2196F3,stroke:#1976D2,color:#fff
    style I5 fill:#2196F3,stroke:#1976D2,color:#fff
    style I6 fill:#2196F3,stroke:#1976D2,color:#fff
    style I7 fill:#2196F3,stroke:#1976D2,color:#fff
    style J1 fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style J2 fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style J3 fill:#9C27B0,stroke:#7B1FA2,color:#fff
    style J4 fill:#9C27B0,stroke:#7B1FA2,color:#fff
```

## 5. So Sánh Hiệu Suất và Chi Phí

### 5.1 Gas Fees Comparison

```mermaid
graph TB
    subgraph "TRƯỚC - Fixed Gas Prices"
        K1[Bank Transfer: 100,000 gas] --> K2[Cost: ~0.15 LUNC]
        K3[Staking: 200,000 gas] --> K4[Cost: ~0.30 LUNC]
        K5[Governance: 150,000 gas] --> K6[Cost: ~0.23 LUNC]
        K7[Market Swap: 300,000 gas] --> K8[Cost: ~0.45 LUNC]
    end
    
    subgraph "SAU - Dynamic EIP-1559 + Fixed Cosmos"
        L1[Bank Transfer: 100,000 gas] --> L2[Cost: ~0.15 LUNC]
        L3[Staking: 200,000 gas] --> L4[Cost: ~0.30 LUNC]
        L5[Governance: 150,000 gas] --> L6[Cost: ~0.23 LUNC]
        L7[Market Swap: 300,000 gas] --> L8[Cost: ~0.45 LUNC]
        
        M1[🆕 ERC20 Transfer: 21,000 gas] --> M2[🆕 Cost: Dynamic]
        M3[🆕 Smart Contract Call: 50,000 gas] --> M4[🆕 Cost: Base + Priority]
        M5[🆕 Contract Deploy: 500,000 gas] --> M6[🆕 Cost: Auto-adjusted]
        M7[🆕 DeFi Interaction: 200,000 gas] --> M8[🆕 Cost: Market-based]
    end
    
    style M1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M4 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M5 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M6 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M7 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M8 fill:#4CAF50,stroke:#2E7D32,color:#fff
```

## 6. Ecosystem Integration

### 6.1 Trước: Limited Ecosystem

```mermaid
graph LR
    subgraph "Terra Classic Ecosystem (TRƯỚC)"
        N1[Terra Station] --> N2[TerraSwap]
        N2 --> N3[Anchor Protocol]
        N3 --> N4[Mirror Protocol]
        N4 --> N5[Limited DeFi]
        N5 --> N6[IBC Chains]
    end
```

### 6.2 Sau: Expanded Ecosystem

```mermaid
graph LR
    subgraph "Enhanced Ecosystem (SAU)"
        O1[Terra Station] --> O2[TerraSwap]
        O2 --> O3[Anchor Protocol]
        O3 --> O4[Mirror Protocol]
        O4 --> O5[Enhanced DeFi]
        O5 --> O6[IBC Chains]
        
        P1[🆕 Ethereum DApps] --> P2[🆕 Uniswap V3]
        P2 --> P3[🆕 Aave]
        P3 --> P4[🆕 Compound]
        P4 --> P5[🆕 OpenSea NFTs]
        P5 --> P6[🆕 DeFi Protocols]
        P6 --> P7[🆕 Cross-Chain Bridges]
        
        Q1[🆕 Developer Tools] --> Q2[🆕 Hardhat]
        Q2 --> Q3[🆕 Remix]
        Q3 --> Q4[🆕 OpenZeppelin]
        Q4 --> Q5[🆕 Web3 Libraries]
    end
    
    style P1 fill:#FF5722,stroke:#D84315,color:#fff
    style P2 fill:#FF5722,stroke:#D84315,color:#fff
    style P3 fill:#FF5722,stroke:#D84315,color:#fff
    style P4 fill:#FF5722,stroke:#D84315,color:#fff
    style P5 fill:#FF5722,stroke:#D84315,color:#fff
    style P6 fill:#FF5722,stroke:#D84315,color:#fff
    style P7 fill:#FF5722,stroke:#D84315,color:#fff
    style Q1 fill:#607D8B,stroke:#455A64,color:#fff
    style Q2 fill:#607D8B,stroke:#455A64,color:#fff
    style Q3 fill:#607D8B,stroke:#455A64,color:#fff
    style Q4 fill:#607D8B,stroke:#455A64,color:#fff
    style Q5 fill:#607D8B,stroke:#455A64,color:#fff
```

## 7. Security Comparison

<div style="display: flex; flex-direction: row; gap: 24px; align-items: flex-start; flex-wrap: wrap;">

<div style="flex: 1; min-width: 320px;">

#### 7.1 Security Model (TRƯỚC)

```mermaid
graph TD
    R1[Tendermint Consensus] --> R2[Cosmos AnteHandler]
    R2 --> R3[Module Authorization]
    R3 --> R4[Signature Verification]
    R4 --> R5[Gas Limit Protection]
```

</div>

<div style="flex: 1; min-width: 320px;">

#### 7.1 Security Model (SAU)

```mermaid
graph TD
    S1[Tendermint Consensus] --> S2[Dual AnteHandler]
    S2 --> S3[🆕 EVM Extension Check]
    S3 --> S4[🆕 Transaction Type Routing]
    S4 --> S5[Module Authorization]
    S5 --> S6[🆕 EVM State Isolation]
    S6 --> S7[🆕 Precompile Access Control]
    S7 --> S8[Signature Verification]
    S8 --> S9[🆕 Gas Market Protection]
    S9 --> S10[🆕 Cross-Chain Validation]

    style S2 fill:#F44336,stroke:#C62828,color:#fff
    style S3 fill:#F44336,stroke:#C62828,color:#fff
    style S4 fill:#F44336,stroke:#C62828,color:#fff
    style S6 fill:#F44336,stroke:#C62828,color:#fff
    style S7 fill:#F44336,stroke:#C62828,color:#fff
    style S9 fill:#F44336,stroke:#C62828,color:#fff
    style S10 fill:#F44336,stroke:#C62828,color:#fff
```

</div>
</div>

## 8. Migration Benefits Summary

| Khía Cạnh | Trước | Sau | Lợi Ích |
|-----------|-------|-----|---------|
| **Smart Contracts** | ❌ Chỉ CosmWasm | ✅ CosmWasm + Solidity | Tương thích Ethereum ecosystem |
| **Wallet Support** | 🔵 Terra Station, Keplr | 🔵 Terra Station, Keplr + 🆕 MetaMask | Tiếp cận người dùng Ethereum |
| **DApps** | 🔵 Limited Terra DApps | 🔵 Terra DApps + 🆕 Ethereum DApps | Hàng nghìn DApps có sẵn |
| **Developer Tools** | 🔵 Go, Rust | 🔵 Go, Rust + 🆕 Solidity, JS | Cộng đồng developer lớn hơn |
| **Liquidity** | 🔵 Terra native assets | 🔵 Terra assets + 🆕 ERC20 tokens | Tăng thanh khoản đáng kể |
| **Gas System** | 🔵 Fixed pricing | 🔵 Fixed + 🆕 EIP-1559 dynamic | Tối ưu chi phí giao dịch |
| **Interoperability** | 🔵 IBC only | 🔵 IBC + 🆕 Ethereum bridges | Kết nối đa hệ sinh thái |

## 9. Implementation Timeline

```mermaid
gantt
    title Terra Classic EVM Integration Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1 - Foundation
    Core EVM Module         :done, foundation, 2024-01-01, 2024-03-31
    AnteHandler Security    :done, security, 2024-02-01, 2024-04-30
    section Phase 2 - Integration
    Fee Market EIP-1559     :active, feemarket, 2024-04-01, 2024-06-30
    JSON-RPC Server         :active, jsonrpc, 2024-05-01, 2024-07-31
    section Phase 3 - Enhancement
    Terra Precompiles       :precompiles, 2024-06-01, 2024-08-31
    IBC-EVM Bridge          :bridge, 2024-07-01, 2024-09-30
    section Phase 4 - Production
    Testnet Deployment      :testnet, 2024-08-01, 2024-10-31
    Mainnet Launch          :mainnet, 2024-10-01, 2024-12-31
```

## Kết Luận

Việc tích hợp EVM vào Terra Classic mang lại:

### ✅ **Lợi Ích Chính**
- **Tương thích ngược 100%**: Tất cả tính năng Terra Classic hiện tại được bảo toàn
- **Mở rộng hệ sinh thái**: Tiếp cận hàng nghìn DApps Ethereum
- **Tăng thanh khoản**: ERC20 tokens và DEX protocols
- **Trải nghiệm người dùng**: MetaMask và các wallet phổ biến
- **Cộng đồng developer**: Solidity và Ethereum tooling

### 🔄 **Hybrid Architecture**
- **Dual Transaction Support**: Cosmos SDK + EVM transactions
- **Unified Security**: Single consensus với dual validation
- **Cross-Platform Access**: Terra modules accessible from Solidity
- **Optimized Performance**: EIP-1559 gas market + Terra efficiency

### 🚀 **Strategic Impact**
- **Market Position**: Trở thành bridge giữa Cosmos và Ethereum
- **Developer Adoption**: Thu hút developers từ cả hai ecosystems
- **User Growth**: Mở rộng user base từ cộng đồng Ethereum
- **Innovation Platform**: Foundation cho DeFi và NFT innovations

---

*Document này là phần của dự án Terra Classic EVM Integration. Cập nhật cuối: 2025-08-11*
