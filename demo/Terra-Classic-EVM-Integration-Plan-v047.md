# Kế hoạch TÍCH HỢP EVM cho Terra Classic (LUNC) — Bản cấu trúc lại gọn gàng

Tài liệu này tái cấu trúc nội dung phân tích hiện có thành một bản kế hoạch nhất quán, súc tích, dễ theo dõi cho đội kỹ thuật, validator, và cộng đồng.

## Mục lục

1. Tóm tắt điều hành
1. Lựa chọn kỹ thuật & Quyết nghị
1. Tổng quan kiến trúc
1. Khác biệt Cosmos SDK v0.47 vs v0.50+
1. Kế hoạch triển khai theo giai đoạn
1. Công việc kỹ thuật cốt lõi (chi tiết ngắn)
1. Cấu hình vận hành (JSON-RPC, phí EIP-1559, bảo mật)
1. Kiểm thử & đảm bảo chất lượng (IBC-EVM, stress test)
1. An toàn bảo mật & quy trình ứng phó sự cố
1. Quản trị & triển khai (proposal, rollout)
1. Chỉ số thành công (KPI) & giám sát vận hành
1. Phụ lục (mẫu cấu hình/nghiệp vụ)
1. Tài liệu tham khảo cốt lõi

---

## 1. Tóm tắt điều hành

- Khuyến nghị: Tích hợp trực tiếp EVM trên Cosmos SDK v0.47 của Terra Classic.
- Thời gian: 4–6 tháng phát triển + 1–2 tháng kiểm thử công khai.
- Rủi ro: Trung bình, có thể kiểm soát nhờ không thay đổi nền tảng lớn và quy trình rollout theo pha.
- Kết quả: EVM tương thích Ethereum (JSON-RPC, EIP-1559, MetaMask/Hardhat/Foundry), IBC hoạt động với tài sản EVM.

## 2. Lựa chọn kỹ thuật & Quyết nghị

- Phương án A — EVM trên v0.47 (khuyến nghị):
  - Ưu: Nhanh nhất, ít đụng chạm module Terra hiện hữu, dễ rollback.
  - Nhược: Cần backport một số thành phần (feemarket, JSON-RPC), tự làm compatibility shims.
- Phương án B — Nâng SDK v0.50+ rồi tích hợp EVM:
  - Ưu: Nhiều tính năng mới, có sẵn ABCI++/Collections.
  - Nhược: Nhiều breaking changes, migration phức tạp, timeline dài (8–12 tháng).
- Phương án C — Fork EVM tùy chỉnh:
  - Ưu: Toàn quyền tuỳ biến.
  - Nhược: Gánh nặng bảo trì, rủi ro bảo mật, tương thích tooling hạn chế.

Quyết nghị: Chọn Phương án A để đạt mục tiêu nhanh, giảm rủi ro cộng đồng và tối ưu chi phí/thời gian.

## 3. Tổng quan kiến trúc

- Execution (x/vm): Thực thi EVM, tận dụng thư viện tương thích Ethereum (Ethermint/Evmos patterns).
- ABCI/Consensus: Tích hợp qua ABCI với CometBFT (finality nhanh ~2s).
- JSON-RPC: Cung cấp các namespace eth, net, web3; tối thiểu hóa bề mặt tấn công (không mở admin/personal trên public).
- Fee Market (EIP-1559): Base fee động, tip; bảo đảm đồng nhất phí giữa lớp EVM và Cosmos.

## 4. Khác biệt Cosmos SDK v0.47 vs v0.50+

- Module interface đổi nhiều ở v0.50+ (Collections, Params hóa qua gov, ABCI++/vote extensions).
- Nâng cấp lên v0.50+ đòi hỏi migration Oracle/Market/Treasury, tăng rủi ro triển khai và thời gian.
- Trên v0.47, cần shim/adapter để tương thích các API mới (encoding, params, store patterns).

## 5. Kế hoạch triển khai theo giai đoạn

- Phase 1 (Tháng 1–2): Backport EVM module, dựng JSON-RPC, route tx (AnteHandler), unit test cốt lõi.
- Phase 2 (Tháng 2–3): Tích hợp Oracle/Market/Treasury, đồng bộ mô hình gas, thử IBC với EVM, chuẩn bị migration plan.
- Phase 3 (Tháng 3–4): Precompiles đặc thù Terra, EIP-1559 (feemarket), tương thích MetaMask/Hardhat/Foundry, tối ưu hiệu năng.
- Phase 4 (Tháng 4–6): Devnet → Public testnet (incentivized) → Audit → Chuẩn bị mainnet rollout.

## 6. Công việc kỹ thuật cốt lõi (chi tiết ngắn)

- Wiring module (app.go): thêm EVMKeeper, FeeMarketKeeper, khởi tạo thứ tự module, hooks cần thiết.
- AnteHandler (dual routing): Phân luồng EVM tx vs Cosmos tx; chặn trộn lẫn EVM msg trong Cosmos tx để ngừa bypass.
- Encoding/registry: Đăng ký types EVM, tạo tx/codec config tương thích v0.47.
- Fee market: Tính baseFee theo EIP-1559 thích nghi thông số Cosmos; đảm bảo min_gas_price nhất quán.

Ví dụ cấu hình tham chiếu (rút gọn):

```go
// Khởi tạo keeper (ý tưởng)
type App struct {
  // Terra keepers
  OracleKeeper oracle.Keeper
  MarketKeeper market.Keeper
  TreasuryKeeper treasury.Keeper
  // EVM
  EvmKeeper evmkeeper.Keeper
  FeeMarketKeeper feemarketkeeper.Keeper
}
```

```go
// AnteHandler (ý tưởng)
func NewAnteHandler(opt Options) sdk.AnteHandler {
  return func(ctx sdk.Context, tx sdk.Tx, sim bool) (sdk.Context, error) {
    if isEVMTx(tx) { return evmAnte(ctx, tx, sim) }
    if containsEVMMessages(tx) { return ctx, ErrInvalidTxType }
    return cosmosAnte(ctx, tx, sim)
  }
}
```

## 7. Cấu hình vận hành (JSON-RPC, phí EIP-1559, bảo mật)

- JSON-RPC (app.toml – gợi ý):

```toml
[json-rpc]
enable = true
address = "127.0.0.1:8545"
ws-address = "127.0.0.1:8546"
api = ["eth", "net", "web3"]
gas-cap = 50000000
http-timeout = "30s"
```

- Nginx trước RPC (gợi ý):

```nginx
upstream terra_rpc { server 127.0.0.1:8545; }
server {
  listen 443 ssl http2;
  server_name rpc.terraclassic.org;
  limit_req_zone $binary_remote_addr zone=rpc:10m rate=10r/s;
  limit_req zone=rpc burst=20 nodelay;
  location / { proxy_pass http://terra_rpc; add_header Access-Control-Allow-Origin "https://app.terraclassic.community"; }
}
```

- EIP-1559 thông số khuyến nghị:

```yaml
feemarket:
  no_base_fee: false
  base_fee: "25000000000"          # 25 gwei
  base_fee_change_denominator: 8
  elasticity_multiplier: 2
  min_gas_price: "12500000000"
  min_gas_multiplier: "0.5"
  enable_height: 1
```

Bảo mật: ràng buộc RPC vào localhost, rate-limit, không mở personal/admin; CORS chỉ định miền tin cậy; theo dõi logs/metrics.

## 8. Kiểm thử & đảm bảo chất lượng (IBC-EVM, stress test)

- Kịch bản ưu tiên: IBC transfer LUNC ↔ Osmosis/Kujira; ERC20 wrapped asset qua cầu; multi-hop với Axelar; IBC hooks kích hoạt từ sự kiện EVM.
- Stress: 100–1000 giao dịch/giây trong 10 phút, success >99%, latency p95 <2s; kiểm tra khôi phục khi reset channel; 100% xử lý packet timeout.
- Devnet/Testnet: Bộ test tự động (CosmJS/Go), đối soát số dư 2 chuỗi, cảnh báo bất nhất.

## 9. An toàn bảo mật & quy trình ứng phó sự cố

- Trọng tâm audit: EVM core, AnteHandler (dual routing), FeeMarket, JSON-RPC.
- Đa hãng audit (khuyến nghị): BlockSec/CertiK/ToB tùy phạm vi; audit trước testnet công khai và sau giai đoạn testnet.
- Playbook sự cố (rút gọn):
  - Tắt EVM khi tỉ lệ lỗi > ngưỡng; rollback handler; reset tham số phí; chuyển RPC sang node dự phòng; thông báo validator; điều tra và phát hành bản vá.

## 10. Quản trị & triển khai (proposal, rollout)

- Proposal nâng cấp phần mềm bật EVM, chỉ rõ chiều cao khối, tham số EIP-1559, endpoint JSON-RPC, liên kết phát hành binary.
- Lộ trình: Devnet → Public testnet (incentive) → Canary/mainnet; onboarding validator + RPC; đề cao khả năng rollback.

Mẫu đề xuất (rút gọn):

```yaml
title: "Enable EVM Module on Terra Classic"
description: |
  Kích hoạt EVM, hỗ trợ EIP-1559, JSON-RPC, tương thích Ethereum tooling.
plan:
  name: "v3.6.0-evm"
  height: 15500000
info: "https://github.com/classic-terra/core/releases/tag/v3.6.0"
deposit: "50000000000uluna"
```

## 11. Chỉ số thành công (KPI) & giám sát vận hành

- Kỹ thuật: JSON-RPC p95 <200ms; ước lượng gas chính xác >95%; EVM tx success >99.5%; IBC success >99%; uptime >99.9%.
- Hệ sinh thái: 10–30 DApp sau 1 quý; 5k–10k EVM tx/ngày; 80% validator hỗ trợ RPC.
- Monitoring: Prometheus + Grafana, cảnh báo failure rate/latency/IBC errors; đo size state EVM, gas per block, contract deployments.

## 12. Phụ lục (mẫu cấu hình/nghiệp vụ)

- Prometheus metrics (gợi ý):
  - terra_evm_transactions_total{status}
  - terra_evm_gas_used_per_block
  - terra_ibc_evm_transfers_total{source_chain,destination_chain}
  - terra_json_rpc_latency_histogram{method,status}

- Checklist tiền mainnet:
  - [ ] Hoàn tất audit (0 critical, <5 medium còn lại đã chấp nhận/giảm thiểu)
  - [ ] Testnet >30 ngày, >80% validator tham gia
  - [ ] JSON-RPC tương thích MetaMask/Remix/Hardhat
  - [ ] Quy trình rollback kiểm chứng

## 13. Tài liệu tham khảo cốt lõi

- Cosmos EVM (Ethermint/Evmos) — kiến trúc, tích hợp:
  - <https://evm.cosmos.network>
  - <https://docs.ethermint.zone>
  - <https://github.com/evmos/ethermint>
- Cosmos SDK — build/migration/upgrade:
  - <https://docs.cosmos.network/v0.47>
  - <https://docs.cosmos.network/main/build/migrations/upgrading>
- Terra Classic Core:
  - <https://github.com/classic-terra/core>
- Cronos/HAQQ — fee market/JSON-RPC tham chiếu:
  - <https://docs.cronos.org/cronos-chain-protocol/module_overview/module_feemarket>
  - <https://docs.haqq.network/develop/api/ethereum-json-rpc/>

---

Kết luận: Tích hợp EVM trên Cosmos SDK v0.47 là con đường tối ưu cho Terra Classic về thời gian, rủi ro và chi phí, đồng thời duy trì tương thích hệ sinh thái hiện hữu và mở rộng nhanh năng lực thu hút nhà phát triển Ethereum.
