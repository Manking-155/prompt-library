# Terra Classic EVM Integration - System Architecture Diagram

## Overview
This document provides visual representations of the Terra Classic EVM integration architecture, showing the flow of transactions, module interactions, and security implementations.

## Architecture Diagrams

### 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "User Layer"
        A[Web3 Wallet<br/>MetaMask/WalletConnect]
        B[Terra Station]
        C[CLI/SDK]
    end

    subgraph "API Layer"
        D[JSON-RPC Server<br/>:8545/:8546]
        E[Cosmos REST API<br/>:1317]
        F[Tendermint RPC<br/>:26657]
    end

    subgraph "Application Layer"
        G[Terra Classic Node<br/>terrad]
        H[AnteHandler Router]
        I[Transaction Pool]
    end

    subgraph "Execution Layer"
        J[EVM Execution Engine]
        K[Cosmos SDK Modules]
        L[Go-Ethereum VM]
        M[StateDB]
    end

    subgraph "Storage Layer"
        N[IAVL+ State Store]
        O[Block Storage]
        P[Transaction Index]
    end

    subgraph "Security Layer"
        Q[Validator Set]
        R[Consensus Engine]
        S[Cryptographic Verification]
    end

    %% User to API connections
    A --> D
    B --> E
    C --> F

    %% API to Application
    D --> G
    E --> G
    F --> G

    %% Application layer flow
    G --> H
    H --> I
    I --> J
    I --> K

    %% Execution layer
    J --> L
    J --> M
    K --> M

    %% Storage connections
    M --> N
    G --> O
    G --> P

    %% Security layer
    G --> Q
    Q --> R
    R --> S

    %% Styling
    classDef userLayer fill:#e1f5fe
    classDef apiLayer fill:#f3e5f5
    classDef appLayer fill:#fff3e0
    classDef execLayer fill:#e8f5e8
    classDef storageLayer fill:#fce4ec
    classDef securityLayer fill:#fff8e1

    class A,B,C userLayer
    class D,E,F apiLayer
    class G,H,I appLayer
    class J,K,L,M execLayer
    class N,O,P storageLayer
    class Q,R,S securityLayer
```

### 2. Transaction Flow Architecture

```mermaid
graph TD
    A[User Transaction] --> B{Transaction Type Detection}
    
    B -->|Has EVM Extension| C[EVM Transaction Path]
    B -->|Standard Cosmos| D[Cosmos Transaction Path]
    
    subgraph "EVM Path"
        C --> E[EVM AnteHandler]
        E --> F[Gas Price Validation<br/>EIP-1559]
        F --> G[Account Verification]
        G --> H[Signature Validation]
        H --> I[EVMKeeper.ApplyMessage]
        I --> J[Go-Ethereum VM]
        J --> K[Smart Contract Execution]
        K --> L[Precompile Access]
        L --> M[Terra Module Calls]
        M --> N[State Transition]
    end
    
    subgraph "Cosmos Path"
        D --> O[Cosmos AnteHandler]
        O --> P[Fee Deduction]
        P --> Q[Signature Verification]
        Q --> R[Message Router]
        R --> S[Module Execution]
        S --> T[Native Module Logic]
        T --> U[State Update]
    end
    
    subgraph "Terra Classic Modules"
        M --> V[Oracle Module<br/>Price Feeds]
        M --> W[Market Module<br/>Asset Swaps]
        M --> X[Treasury Module<br/>Burn/Mint]
        M --> Y[Staking Module<br/>Delegation]
        M --> Z[Gov Module<br/>Proposals]
    end
    
    subgraph "Cross-Chain Integration"
        K --> AA[IBC-EVM Hooks]
        AA --> BB[ERC20 Middleware]
        BB --> CC[IBC Transfer]
        CC --> DD[Cross-Chain Assets]
    end
    
    N --> EE[State Commitment]
    U --> EE
    EE --> FF[Block Production]
    FF --> GG[Consensus]
    
    %% Styling
    classDef evmPath fill:#fff3e0
    classDef cosmosPath fill:#f3e5f5
    classDef terraModules fill:#e8f5e8
    classDef ibcPath fill:#e1f5fe
    
    class C,E,F,G,H,I,J,K,L,M,N evmPath
    class D,O,P,Q,R,S,T,U cosmosPath
    class V,W,X,Y,Z terraModules
    class AA,BB,CC,DD ibcPath
```

### 3. Security Model & Attack Prevention

```mermaid
graph TB
    subgraph "Security Layers"
        A[Network Layer Security]
        B[Application Layer Security]
        C[Execution Layer Security]
        D[State Layer Security]
    end

    subgraph "Network Security"
        A --> E[Rate Limiting<br/>100 req/min/IP]
        A --> F[CORS Protection<br/>Localhost Only]
        A --> G[TLS Encryption<br/>HTTPS/WSS]
    end

    subgraph "Application Security"
        B --> H[AnteHandler Validation]
        B --> I[Gas Limit Enforcement]
        B --> J[Fee Market Protection]
        H --> K[AuthZ Bypass Prevention]
        H --> L[Extension Validation]
        H --> M[Signature Verification]
    end

    subgraph "Execution Security"
        C --> N[VM Isolation]
        C --> O[Precompile Access Control]
        C --> P[Gas Metering]
        N --> Q[State Snapshots]
        N --> R[Revert on Error]
        O --> S[Module Permission Checks]
    end

    subgraph "State Security"
        D --> T[IAVL+ Merkle Proofs]
        D --> U[Atomic Transactions]
        D --> V[Consensus Validation]
        T --> W[State Root Verification]
        U --> X[All-or-Nothing Updates]
    end

    subgraph "Threat Mitigation"
        Y[DoS Attack Prevention]
        Z[Smart Contract Exploits]
        AA[Cross-Chain Attacks]
        BB[Economic Attacks]
    end

    E --> Y
    I --> Y
    P --> Y
    
    N --> Z
    S --> Z
    
    L --> AA
    CC --> AA
    
    J --> BB
    DD --> BB

    %% Styling
    classDef security fill:#ffebee
    classDef mitigation fill:#e8f5e8
    
    class A,B,C,D security
    class Y,Z,AA,BB mitigation
```

### 4. Module Integration Map

```mermaid
graph LR
    subgraph "Core EVM Components"
        A[EVMKeeper]
        B[FeeMarket]
        C[ERC20 Bridge]
        D[StateDB]
    end

    subgraph "Terra Classic Modules"
        E[Oracle Module]
        F[Market Module]
        G[Treasury Module]
        H[Staking Module]
        I[Gov Module]
        J[Bank Module]
        K[Auth Module]
    end

    subgraph "IBC Components"
        L[IBC Core]
        M[Transfer Module]
        N[Callbacks]
    end

    subgraph "Precompile Interfaces"
        O[Oracle Precompile<br/>0x1001]
        P[Market Precompile<br/>0x1002]
        Q[Treasury Precompile<br/>0x1003]
        R[Staking Precompile<br/>0x1004]
        S[Gov Precompile<br/>0x1005]
    end

    %% EVM to Terra connections
    A --> O
    A --> P
    A --> Q
    A --> R
    A --> S

    %% Precompile to Module connections
    O --> E
    P --> F
    Q --> G
    R --> H
    S --> I

    %% Core module dependencies
    A --> J
    A --> K
    B --> J
    C --> J
    C --> M

    %% IBC connections
    C --> L
    C --> N
    N --> M

    %% Styling
    classDef evmCore fill:#fff3e0
    classDef terraModules fill:#e8f5e8
    classDef ibcComponents fill:#e1f5fe
    classDef precompiles fill:#f3e5f5

    class A,B,C,D evmCore
    class E,F,G,H,I,J,K terraModules
    class L,M,N ibcComponents
    class O,P,Q,R,S precompiles
```

## Component Details

### EVMKeeper Configuration
- **Go-Ethereum Version**: v1.13.5+
- **EVM Version**: London (EIP-1559 support)
- **Gas Limit**: 50M per block
- **Precompile Range**: 0x1001-0x1FFF (Terra specific)

### Fee Market Parameters
- **Base Fee**: 25 gwei initial
- **Elasticity Multiplier**: 2x
- **Adjustment Rate**: 12.5% per block
- **Min Gas Price**: 12.5 gwei floor

### Security Configurations
- **Rate Limiting**: 100 requests/minute/IP
- **Gas Cap**: 50M gas per call
- **Timeout**: 5s EVM execution
- **Batch Limit**: 100 requests per batch

### IBC Integration
- **Callback Gas**: 1M gas limit
- **ERC20 Conversion**: Automatic
- **Channel Binding**: ICS-20 compatible
- **Cross-chain Assets**: Full support

## Implementation Status

| Component | Status | Dependencies | Security Review |
|-----------|--------|--------------|-----------------|
| EVMKeeper | ✅ Ready | cosmos-sdk v0.47 | ✅ Complete |
| AnteHandler | ✅ Ready | EVMKeeper | ✅ Complete |
| FeeMarket | ✅ Ready | Bank Module | ✅ Complete |
| JSON-RPC | ✅ Ready | EVMKeeper | ✅ Complete |
| Precompiles | 🟡 In Progress | Terra Modules | 🟡 Pending |
| IBC-EVM | 🟡 In Progress | IBC Core | 🟡 Pending |

## Next Steps

1. **Precompile Development**: Complete Terra-specific precompile implementations
2. **Integration Testing**: Full end-to-end testing with Terra Classic testnet
3. **Security Audit**: Third-party security review of all components
4. **Governance Proposal**: Community vote for mainnet activation
5. **Phased Rollout**: Gradual activation with monitoring

---

*This document is part of the Terra Classic EVM Integration project. Last updated: 2025-08-11*
