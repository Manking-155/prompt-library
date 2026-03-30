# Terra Classic EVM Integration - Developer Implementation Guide
*Complete Developer Handbook for Implementation*

---

## 🎯 **Developer Quick Start**

### **Current Status: Week 1 - Oracle Precompile Implementation**
- **Your Role**: Backend/Frontend/QA/DevOps Developer
- **Current Sprint**: Sprint 1 - Terra Precompiles Foundation
- **Primary Task**: Oracle precompile implementation
- **Timeline**: 6-8 weeks total implementation

---

## 📚 **Learning Path for New Developers**

### **🏁 Day 1: Project Understanding (2-4 hours)**

#### **Step 1: Project Overview (30 minutes)**
1. **Read**: [Master README](README.md) - Project status dashboard
2. **Understand**: 70% complete → 30% remaining implementation
3. **Identify**: Your role trong 8-developer team

#### **Step 2: Architecture Understanding (60 minutes)**
1. **Study**: [System Architecture](01-architecture-design/system-architecture.md)
   - Focus: Hybrid Cosmos-EVM architecture
   - Key: Dual transaction support (Cosmos + EVM)
2. **Review**: [Before-After Comparison](01-architecture-design/before-after-comparison.md)
   - Focus: What we're building và why
   - Key: 100% backward compatibility

#### **Step 3: Implementation Context (60 minutes)**
1. **Read**: [Current Sprint Status](03-development-execution/README.md)
   - Focus: Week 1 Oracle precompile tasks
   - Key: Your specific assignments
2. **Review**: [Sprint Planning](02-implementation-planning/sprint-planning-guide.md)
   - Focus: 3-sprint roadmap
   - Key: Timeline và deliverables

#### **Step 4: Code Patterns (30 minutes)**
1. **Study**: [Implementation Patterns](03-development-execution/code-references/implementation-patterns.md)
   - Focus: EVMKeeper setup, AnteHandler security
   - Key: Production-tested patterns

---

### **🔧 Day 2: Development Environment Setup (4-6 hours)**

#### **Prerequisites Installation**
```bash
# Required software
go version >= 1.19
docker && docker-compose
git, make, curl
VS Code hoặc GoLand

# Blockchain tools
cosmos-sdk v0.47.x
ethermint modules
geth (for testing)

# Testing tools
hardhat/truffle
metamask
postman/insomnia
```

#### **Repository Setup**
```bash
# Clone Terra Classic với EVM branch
git clone https://github.com/classic-terra/core.git
cd core
git checkout evm-integration-v047

# Install dependencies
go mod download

# Build với EVM support
make install-evm

# Verify installation
terrad version
```

#### **Development Environment Verification**
```bash
# Run unit tests
make test-unit

# Run integration tests (if available)
make test-integration

# Start local development node
make localnet-start

# Verify JSON-RPC endpoint
curl -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}' \
  http://localhost:8545
```

---

## 💻 **Implementation Guide by Role**

### **🔧 Backend Developers (Go/Cosmos SDK)**

#### **Your Focus Areas**
1. **Terra Precompiles Implementation**
2. **IBC-EVM Bridge Development**
3. **Security Validation**
4. **Performance Optimization**

#### **Current Week 1 Tasks**

##### **Oracle Precompile Implementation (Backend Lead)**
```go
// Location: x/evm/precompiles/oracle/oracle.go
// Reference: https://github.com/evmos/ethermint/tree/main/x/evm/precompiles

package oracle

import (
    "github.com/ethereum/go-ethereum/common"
    "github.com/ethereum/go-ethereum/core/vm"
    sdk "github.com/cosmos/cosmos-sdk/types"
    oraclekeeper "github.com/classic-terra/core/x/oracle/keeper"
)

type Precompile struct {
    oracleKeeper oraclekeeper.Keeper
}

func NewPrecompile(keeper oraclekeeper.Keeper) *Precompile {
    return &Precompile{
        oracleKeeper: keeper,
    }
}

// GetExchangeRate returns exchange rate for given denom
func (p *Precompile) GetExchangeRate(
    ctx sdk.Context,
    denom string,
) (sdk.Dec, error) {
    return p.oracleKeeper.GetExchangeRate(ctx, denom)
}

// Required interface implementation
func (p *Precompile) RequiredGas(input []byte) uint64 {
    return 10000 // Base gas cost
}

func (p *Precompile) Run(
    evm *vm.EVM,
    contract *vm.Contract,
    readonly bool,
) ([]byte, error) {
    // Implementation logic here
    return nil, nil
}
```

##### **Testing Framework Setup (Backend Dev #3)**
```go
// Location: x/evm/precompiles/oracle/oracle_test.go

package oracle_test

import (
    "testing"
    "github.com/stretchr/testify/suite"
    sdk "github.com/cosmos/cosmos-sdk/types"
    "github.com/classic-terra/core/app"
    "github.com/classic-terra/core/x/evm/precompiles/oracle"
)

type OraclePrecompileTestSuite struct {
    suite.Suite
    app        *app.TerraApp
    ctx        sdk.Context
    precompile *oracle.Precompile
}

func (s *OraclePrecompileTestSuite) SetupTest() {
    s.app = app.NewTerraApp(/* test setup */)
    s.ctx = s.app.BaseApp.NewContext(false, tmproto.Header{})
    s.precompile = oracle.NewPrecompile(s.app.OracleKeeper)
}

func (s *OraclePrecompileTestSuite) TestGetExchangeRate() {
    // Test implementation
    testCases := []struct {
        name     string
        denom    string
        expected sdk.Dec
        wantErr  bool
    }{
        {"Valid LUNC rate", "uluna", sdk.NewDec(100), false},
        {"Invalid denom", "invalid", sdk.ZeroDec(), true},
    }
    
    for _, tc := range testCases {
        s.Run(tc.name, func() {
            rate, err := s.precompile.GetExchangeRate(s.ctx, tc.denom)
            if tc.wantErr {
                s.Require().Error(err)
            } else {
                s.Require().NoError(err)
                s.Require().Equal(tc.expected, rate)
            }
        })
    }
}

func TestOraclePrecompileTestSuite(t *testing.T) {
    suite.Run(t, new(OraclePrecompileTestSuite))
}
```

#### **Development Workflow**
```bash
# Daily development cycle
git checkout -b feature/oracle-precompile
# Implement changes
make test-unit
make lint
git commit -m "feat: implement Oracle precompile basic functionality"
git push origin feature/oracle-precompile
# Create PR for review
```

---

### **🌐 Frontend Developers (JavaScript/Web3)**

#### **Your Focus Areas**
1. **JavaScript SDK Development**
2. **MetaMask Integration**
3. **DApp Examples**
4. **Documentation & Tutorials**

#### **Current Week 1 Tasks**

##### **JavaScript SDK Foundation (Frontend Lead)**
```javascript
// Location: sdk/javascript/terra-evm-sdk/
// Terra Classic EVM SDK

class TerraEVMSDK {
    constructor(rpcUrl = 'http://localhost:8545') {
        this.provider = new ethers.providers.JsonRpcProvider(rpcUrl);
        this.precompiles = {
            oracle: '0x1001',
            market: '0x1002',
            treasury: '0x1003'
        };
    }

    // Oracle precompile integration
    async getExchangeRate(denom) {
        const oracleContract = new ethers.Contract(
            this.precompiles.oracle,
            ORACLE_ABI,
            this.provider
        );
        
        return await oracleContract.getExchangeRate(denom);
    }

    // MetaMask connection
    async connectWallet() {
        if (typeof window.ethereum !== 'undefined') {
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            this.signer = new ethers.providers.Web3Provider(window.ethereum).getSigner();
            return this.signer;
        }
        throw new Error('MetaMask not installed');
    }
}

// Usage example
const sdk = new TerraEVMSDK();
await sdk.connectWallet();
const luncPrice = await sdk.getExchangeRate('uluna');
console.log('LUNC Price:', luncPrice.toString());
```

##### **Example DApp (Frontend Dev)**
```javascript
// Location: examples/oracle-price-feed/
// React component for Oracle price display

import React, { useState, useEffect } from 'react';
import { TerraEVMSDK } from 'terra-evm-sdk';

function OraclePriceDisplay() {
    const [price, setPrice] = useState(null);
    const [loading, setLoading] = useState(false);
    const [sdk, setSdk] = useState(null);

    useEffect(() => {
        const initSDK = async () => {
            const terraSDK = new TerraEVMSDK();
            await terraSDK.connectWallet();
            setSdk(terraSDK);
        };
        initSDK();
    }, []);

    const fetchPrice = async () => {
        if (!sdk) return;
        
        setLoading(true);
        try {
            const luncPrice = await sdk.getExchangeRate('uluna');
            setPrice(luncPrice.toString());
        } catch (error) {
            console.error('Error fetching price:', error);
        }
        setLoading(false);
    };

    return (
        <div>
            <h2>Terra Classic Oracle Price Feed</h2>
            <button onClick={fetchPrice} disabled={loading}>
                {loading ? 'Loading...' : 'Get LUNC Price'}
            </button>
            {price && <p>LUNC Price: ${price}</p>}
        </div>
    );
}

export default OraclePriceDisplay;
```

---

### **🧪 QA Engineers (Testing)**

#### **Your Focus Areas**
1. **Test Framework Development**
2. **Automated Testing**
3. **Integration Testing**
4. **Performance Testing**

#### **Current Week 1 Tasks**

##### **Test Case Development (QA Lead)**
```go
// Location: tests/integration/oracle_precompile_test.go

package integration

import (
    "testing"
    "github.com/stretchr/testify/require"
    "github.com/classic-terra/core/app"
)

func TestOraclePrecompileIntegration(t *testing.T) {
    // Setup test environment
    app := setupTestApp()
    ctx := app.NewContext(false, tmproto.Header{})
    
    // Test scenarios
    testCases := []struct {
        name        string
        setup       func()
        denom       string
        expectError bool
        expectPrice bool
    }{
        {
            name: "Valid LUNC price query",
            setup: func() {
                // Setup Oracle state với LUNC price
                app.OracleKeeper.SetExchangeRate(ctx, "uluna", sdk.NewDec(100))
            },
            denom:       "uluna",
            expectError: false,
            expectPrice: true,
        },
        {
            name:        "Invalid denom query",
            setup:       func() {},
            denom:       "invalid",
            expectError: true,
            expectPrice: false,
        },
    }
    
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            tc.setup()
            
            // Execute precompile call
            result, err := callOraclePrecompile(app, tc.denom)
            
            if tc.expectError {
                require.Error(t, err)
            } else {
                require.NoError(t, err)
                if tc.expectPrice {
                    require.NotNil(t, result)
                    require.Greater(t, result.Int64(), int64(0))
                }
            }
        })
    }
}
```

##### **Automated Testing Setup**
```bash
# Location: scripts/test-automation.sh

#!/bin/bash
# Automated testing script

echo "Running Terra Classic EVM Integration Tests..."

# Unit tests
echo "1. Running unit tests..."
make test-unit || exit 1

# Integration tests
echo "2. Running integration tests..."
make test-integration || exit 1

# Performance tests
echo "3. Running performance tests..."
make test-performance || exit 1

# Security tests
echo "4. Running security tests..."
make test-security || exit 1

echo "All tests passed! ✅"
```

---

### **🚀 DevOps Engineers (Infrastructure)**

#### **Your Focus Areas**
1. **CI/CD Pipeline Setup**
2. **Development Environment**
3. **Testing Automation**
4. **Deployment Preparation**

#### **Current Week 1 Tasks**

##### **CI/CD Pipeline Setup (DevOps Lead)**
```yaml
# Location: .github/workflows/evm-integration.yml

name: Terra Classic EVM Integration CI

on:
  push:
    branches: [ main, evm-integration-v047 ]
  pull_request:
    branches: [ main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Go
        uses: actions/setup-go@v3
        with:
          go-version: 1.19
          
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/go/pkg/mod
          key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
          
      - name: Install dependencies
        run: go mod download
        
      - name: Run unit tests
        run: make test-unit
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Go
        uses: actions/setup-go@v3
        with:
          go-version: 1.19
          
      - name: Run integration tests
        run: make test-integration

  security-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scan
        run: make security-scan-all
        
      - name: Upload security results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: security-results.sarif
```

##### **Development Environment Docker Setup**
```dockerfile
# Location: docker/dev.Dockerfile

FROM golang:1.19-alpine AS builder

# Install dependencies
RUN apk add --no-cache git make gcc musl-dev

# Set working directory
WORKDIR /terra

# Copy source code
COPY . .

# Build Terra Classic với EVM support
RUN make install-evm

# Runtime image
FROM alpine:latest

RUN apk add --no-cache ca-certificates

COPY --from=builder /go/bin/terrad /usr/local/bin/

# Expose ports
EXPOSE 26656 26657 1317 8545 8546

# Start command
CMD ["terrad", "start", "--evm.enable"]
```

---

## 🔄 **Daily Development Workflow**

### **Morning Routine (9:00 AM)**
1. **Daily Standup** (15 minutes)
   - What did you complete yesterday?
   - What will you work on today?
   - Any blockers or dependencies?

2. **Check Current Status**
   - Review [Development Execution](03-development-execution/README.md)
   - Update your progress trong documentation
   - Check for any blockers từ other team members

### **Development Cycle**
```bash
# 1. Start new feature
git checkout -b feature/your-task-name

# 2. Implement changes
# Write code, tests, documentation

# 3. Test locally
make test-unit
make test-integration
make lint

# 4. Commit changes
git add .
git commit -m "feat: implement [your feature]"

# 5. Push và create PR
git push origin feature/your-task-name
# Create Pull Request on GitHub

# 6. Code review process
# Address review comments
# Merge after approval
```

### **Testing Requirements**
- **Unit Tests**: >90% coverage required
- **Integration Tests**: All new features tested
- **Documentation**: All APIs documented
- **Code Review**: Minimum 2 reviewers

---

## 📊 **Progress Tracking**

### **Individual Progress Tracking**
Update your progress daily trong relevant documentation:

```markdown
## My Progress (Your Name)
- **Role**: Backend Developer
- **Current Task**: Oracle precompile implementation
- **Progress**: 40% complete
- **Blockers**: None
- **Next Steps**: Complete unit tests
- **ETA**: End of week
```

### **Team Progress Metrics**
| Developer | Role | Current Task | Progress | Status |
|-----------|------|--------------|----------|--------|
| Dev 1 | Backend Lead | Oracle precompile | 40% | On Track |
| Dev 2 | Backend | Market research | 20% | On Track |
| Dev 3 | Backend | Testing framework | 30% | On Track |
| Dev 4 | Frontend | JS SDK | 25% | On Track |

---

## 🚨 **Common Issues & Solutions**

### **Build Issues**
```bash
# Issue: Go module errors
go mod tidy
go mod download

# Issue: Missing dependencies
make install-deps

# Issue: Test failures
make clean
make test-unit-verbose
```

### **Development Issues**
```bash
# Issue: Local node not starting
make localnet-clean
make localnet-start

# Issue: JSON-RPC not responding
curl -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'
```

### **Git Workflow Issues**
```bash
# Issue: Merge conflicts
git fetch origin
git rebase origin/main
# Resolve conflicts
git add .
git rebase --continue

# Issue: Commit message format
# Use: feat/fix/docs/test/refactor: description
git commit --amend -m "feat: implement Oracle precompile basic functionality"
```

---

## 📚 **Learning Resources**

### **Essential Reading**
1. **Cosmos SDK v0.47**: [docs.cosmos.network](https://docs.cosmos.network/v0.47)
2. **Ethermint Documentation**: [docs.evmos.org](https://docs.evmos.org)
3. **Go-Ethereum**: [geth.ethereum.org](https://geth.ethereum.org/docs)
4. **Terra Classic Modules**: [docs.terra.money](https://docs.terra.money)

### **Code References**
1. **Ethermint Precompiles**: [github.com/evmos/ethermint/x/evm/precompiles](https://github.com/evmos/ethermint/tree/main/x/evm/precompiles)
2. **Cosmos SDK Testing**: [github.com/cosmos/cosmos-sdk/testutil](https://github.com/cosmos/cosmos-sdk/tree/main/testutil)
3. **Terra Classic Keepers**: [github.com/classic-terra/core/x](https://github.com/classic-terra/core/tree/main/x)

### **Development Tools**
1. **VS Code Extensions**: Go, Solidity, GitLens
2. **Testing Tools**: Postman, Hardhat, Truffle
3. **Debugging**: Delve debugger, VS Code debugging
4. **Documentation**: Markdown, Mermaid diagrams

---

## 🎯 **Success Criteria**

### **Week 1 Success (Current)**
- [ ] Oracle precompile basic functionality implemented
- [ ] Testing framework foundation established
- [ ] JavaScript SDK structure created
- [ ] CI/CD pipeline configured

### **Sprint 1 Success (End Week 2)**
- [ ] Oracle precompile fully functional
- [ ] Market precompile foundation ready
- [ ] 80%+ test coverage achieved
- [ ] Documentation updated

### **Phase 3 Success (End Week 6)**
- [ ] All precompiles implemented
- [ ] IBC-EVM bridge functional
- [ ] 95%+ test coverage achieved
- [ ] Production deployment ready

---

## 📞 **Getting Help**

### **Technical Questions**
- **Architecture**: Ask system architect
- **Implementation**: Ask backend lead
- **Testing**: Ask QA lead
- **Infrastructure**: Ask DevOps lead

### **Communication Channels**
- **Daily Standups**: 9:00 AM daily
- **Slack/Discord**: Real-time questions
- **GitHub Issues**: Bug reports và feature requests
- **Documentation**: Update progress trong README files

### **Escalation Process**
1. **Level 1**: Ask team members
2. **Level 2**: Ask team lead
3. **Level 3**: Ask project manager
4. **Level 4**: Escalate to stakeholders

---

*This developer guide provides everything you need để successfully contribute to Terra Classic EVM Integration implementation.*

**🎯 Current Focus: Oracle Precompile Implementation (Week 1)**  
**📅 Next Milestone: Sprint 1 Review (End Week 2)**  
**🚀 Final Goal: Production-ready EVM integration (Week 6-8)**