# Stage-1C v2 pre-calibration workbench

状态：`SIGNED_320_CALIBRATION_INPUT_AWAITING_INDEPENDENT_CODERS`

Owner token `AUTHORIZE_STAGE1C_V2_CALIBRATION_PREPARATION` 只授权有界方法整合、schema/codebook、
只读 reproduction-candidate closure 和 calibration。两个 Stage-1B overlays 已由后续独立签名释放，
320 现仅作为 calibration input；它仍不是 320-paper full-mapping 或研究执行授权。

## 当前产物

- `stage1c-v2-precalibration-contract-zh.md`：唯一自洽的当前 pre-calibration 方法合同；
- `release-merge-manifest-v1.json`：226/282/14/24/320 分层 signed calibration input；
- `stage1b-overlay-release-receipts-v1.json`：两个签名与各自 reviewed RC1 字节的独立绑定；
- `problem-intervention-crosswalk-v1.json`：六个未排序 problem nodes × D0-D4 intervention axes；
- `pending-problem-routing-v1.json`：15 个 pending 标签的逐条路由，未升级新 problem；
- `claim-registry-v1.json`：13 个 canonical synthesis claims 及全部 38 个 overlay records 的 links；
- `candidate-protocol-templates-v1.json`：旧八个 family 全部降格为可 merge/split/unrouted template；
- `translation-contract-queue-v1.json`：远域 analogue 的显式 translation queue；
- `schema-bundle-v1.json`：paper/run/observation/comparison/dataset/claim/family/review schemas；
- `calibration-manifest-v1.json`：38 overlay + 18 inherited sentinels，精确 N=56；
- `calibration-blind-packet-v1.json`：不含既有 role/primary direction/family 标签的空白 coder packet；
- `agreement-contract-v1.json`：字段级 agreement、一次 codebook consolidation、全包重编码与裁决规则；
- `reproduction-readiness-v1.json`：五个 speech/omni candidates 的只读 closure checklist；
- `discovery-provenance-v1.json`：诚实记录本轮搜索只能重放 26 exact IDs，不能声称系统综述 closure；
- `review-package-manifest.json`：pre-calibration RC1 的字节与 SHA-256。

## 已闭合的输入门

1. `SIGN_STAGE1B_CAPABILITY_DELTA_RELEASE`：已按 RC1 精确字节登记；
2. `SIGN_STAGE1B_TARGETED_ANCHOR_SCAN_RELEASE`：已按 RC1 精确字节登记。

## 仍然关闭的门

1. 两名独立 coder 的 calibration：未执行；
2. calibration agreement 与 adjudication：未产生；
3. `SIGN_STAGE1C_V2_EXPERIMENT_MAPPING`：缺失且不能提前生效；
4. 320-paper full mapping、模型/API/metric、reproduction、prototype、方向选择与 novelty verdict：未授权。
