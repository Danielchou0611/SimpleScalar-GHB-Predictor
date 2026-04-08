# SimpleScalar 3.0 - GHB Prefetcher Experiment

這是一個基於 SimpleScalar 3.0 模擬器的開發環境，主要的目標是在 `sim-outorder` 模擬器中實作 **GHB (Global History Buffer) Prefetcher**。

## 目錄結構整理

經過整理後的目錄配置如下：

*   **根目錄 (`/`)**: 包含模擬器的原始程式碼 (`.c`, `.h`) 及 `Makefile`。
    *   `sim-outorder.c`: 亂序執行模擬器的核心，包含 GHB Prefetch器的主要邏輯。
    *   `cache.c`: 修改了Cache存取邏輯以配合預取器。
*   **`scripts/`**: 實驗自動化與數據處理腳本。
    *   執行實驗的 Shell 腳本 (`run_*.sh`)。
    *   處理數據的 Python 腳本 (`make_*_tsv.py`)。
    *   繪圖用的 Gnuplot (`.gp`) 腳本。
*   **`stats_data/`**: 存放目前實驗產出的數據。
    *   `ghb_*.stats` / `pf_*.stats`: 開啟預取功能後的實驗數據。
    *   `*.log`: 模擬器執行的日誌。
*   **`baselines/`**: 存放基準測試 (Baseline) 的原始數據與執行檔。
    *   `sim-outorder` / `sim-cache`: 原始版本模擬器。
    *   `base_*.txt`: 關閉預取功能下的效能指標數據。
*   **`figures/`**: 存放由腳本產生的效能分析圖表（如 L2 miss rate, IPC...）。
*   **`benchmarks/`**: 模擬器執行的測試程式 (Benchmarks)。

## 目前開發重點：GHB Prefetcher

在 `sim-outorder.c` 中新增並實作了以下功能：
1.  **GHB (Global History Buffer)**: 儲存過去的記憶體存取歷史。
2.  **IT (Index Table)**: 根據 PC index至 GHB 中的歷史並將相同的鏈結起來。
3.  **Stride Detection**: 自動偵測存取模式中的步長 (Stride) 並發出Prefetch請求。
4.  **統計指標**: 追蹤 `ghb_lookups`, `ghb_stride_found`, `ghb_trains` 等指標以評估效能。

## 常用指令

### 編譯模擬器
```bash
make clean
make sim-outorder
```

### 執行實驗
腳本目前已移動至 `scripts/` 資料夾：
```bash
# Ex : 執行 Phase Sweep 實驗
./scripts/run_phase_sweep.sh
```

### 產生圖表
```bash
# Ex : 使用 Python 處理數據
python3 ./scripts/make_ipc_norm_tsv.py
# 使用 Gnuplot 繪圖
gnuplot ./scripts/plot_ul2_norm.gp
```

---

