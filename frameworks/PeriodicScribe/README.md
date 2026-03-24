# PeriodicScribe

> 🖊️ 用 LLM 定期自動生成結構化文章的框架——多金鑰輪替、Prompt 版控、版本管理，一次建立，持續複用。

---

## 📖 目錄

- [概述](#概述)
- [核心功能](#核心功能)
- [快速開始](#快速開始)
- [目錄結構](#目錄結構)
- [擴展到新週期類型](#擴展到新週期類型)
- [設定參考](#設定參考)
- [常見問題](#常見問題)
- [實際案例](#實際案例)
- [與 AI 協作整合](#與-ai-協作整合)

---

## 概述

### 為什麼需要這個框架？

在開發「定期 LLM 文章生成」系統時，你可能遇到過：

- ❌ **API 金鑰配額管理困難**：多個金鑰手動切換，出錯才知道配額耗盡
- ❌ **Prompt 修改後無法比較差異**：改了之前的版本找不回來
- ❌ **文章輸出品質不穩定**：不知道哪個版本是最好的，也無法回退
- ❌ **段落腳本互相耦合**：想單獨重跑某一段落，但它依賴其他段落的全域狀態
- ❌ **LLM 自行換算數字**：給了「-1,234,567,890」讓 LLM 換算成億元，結果出錯

PeriodicScribe 解決了以上所有問題：

- ✅ **多金鑰自動輪替**：配額耗盡自動切換，Workflow 內共享狀態
- ✅ **Prompt 版本控制**：Baseline 機制，隨時比較差異、還原
- ✅ **輸出版本快照**：每次執行後自動存版，UI 可選版本組裝
- ✅ **Stage 分段架構**：每個段落獨立可單獨執行，也支援完整 Workflow 串接
- ✅ **Python 端預算數據**：所有換算在注入 Prompt 前完成，LLM 只接收最終數字

---

## 核心功能

### 1. 多金鑰 API 輪替

```python
# .env 設定
API_KEYS=key1,key2,key3,key4,key5

# 程式碼無需任何改動，自動輪替
api_manager = GeminiAPIManager()
result = api_manager.generate_content(prompt)
# key1 配額耗盡 → 自動切換 key2 → key3 → ...
```

**配額錯誤自動偵測**：當 API 返回 `429` 或包含 `quota`/`exhausted` 的錯誤訊息時，自動切換到下一個金鑰。

**Workflow 共享模式**：同一個 `GeminiAPIManager` 實例貫穿所有 Stage——Stage 1 耗盡 key1 後，Stage 2 直接從 key2 開始，不重複嘗試已知失效的金鑰。

```python
# Workflow 共享模式（推薦）
api_manager = GeminiAPIManager()
stage1_main(2026, "202603", api_manager=api_manager)  # 可能耗盡 key1
stage2_main(2026, "202603", api_manager=api_manager)  # 從 key2 開始
stage3_main(2026, "202603", api_manager=api_manager)  # 繼續共享狀態
```

---

### 2. Stage 分段架構

每個文章段落對應一個獨立的 Stage 腳本，遵循統一介面：

```python
# 每個 Stage 腳本的標準介面
PROMPT = """[在此定義 Prompt]"""

def check_inputs(year, period) -> list:
    """回傳 [(level, message)] 列表"""
    pass

def build_prompts(year, period, prompt_texts=None) -> list:
    """組裝完整 Prompt，支援 UI 預覽覆蓋"""
    pass

def main(year, period, api_manager=None) -> bool:
    """支援獨立執行和 Workflow 共享兩種模式"""
    pass
```

**獨立執行**：
```bash
python -m scripts.stages.stage1_us_summary --year 2026 --period 202603
```

**Workflow 串接**：
```bash
python run_complete_workflow.py 2026 202603
```

---

### 3. Python 端預算數據

所有單位換算、數學運算在 Python 端完成，Prompt 中只接收最終數字。

```python
# Python 端換算（utils/data_formatter.py）
us_flow_yi = raw_value / 100        # $mm → 億美元
tw_flow_yi = raw_value / 1e8        # NTD → 億台幣
group_totals = compute_group_totals(df)  # 17 分類 → 4 大群組加總

# Prompt 中的佔位符（直接替換，禁止 LLM 再計算）
prompt = PROMPT.replace("{{equity_flow_curr}}", f"{group_totals['equity']:.1f}")
```

**Prompt 中標注**：`# Input Data（精確數據變數，禁止自行換算）`

---

### 4. Prompt 版本控制

```python
pm = WeeklyPromptManager()

# 設定 Baseline（基準版本）
pm.save_baseline(3)                  # 將 Stage 3 目前的 Prompt 存為 Baseline

# 比較差異
result = pm.compare_with_baseline(3)
# result = {
#     'has_baseline': True,
#     'is_identical': False,
#     'diffs': {'PROMPT_OVERVIEW': {'baseline': '...', 'current': '...', 'changed': True}}
# }

# 還原到 Baseline
pm.restore_from_baseline(3)         # 回退到上一個穩定版本

# 直接修改 Prompt（會自動備份原檔）
pm.update_script_prompts(3, {'PROMPT_OVERVIEW': '修改後的 Prompt 內容'})
```

---

### 5. 輸出版本管理

```python
# 執行後自動快照
vid = snapshot(stage_num=3, period="2026-W12")
# 存至：temp/versions/2026-W12/stage3/v20260324_143022.md

# 標記為主要版本（UI 組裝時使用）
set_active_vid(stage_num=3, period="2026-W12", vid=vid)

# 套用指定版本（在組裝前）
apply_version(stage_num=3, period="2026-W12", vid="v20260320_091500")
# 從版本庫複製到 temp/，組裝腳本讀取 temp/ 的檔案

# 查詢所有版本
versions = get_versions(stage_num=3, period="2026-W12")
# ["v20260324_143022", "v20260323_160000", "v20260320_091500"]
```

---

### 6. Streamlit UI（可選）

Streamlit UI 提供以下功能，讓非技術使用者也能操作：

- **Popen 串流 Log**：即時看到 LLM 生成進度
- **Prompt 編輯器**：直接在 UI 修改 Prompt，預覽替換後的完整內容
- **版本歷史**：查看所有歷史版本，一鍵設為主要版本或刪除
- **組裝配置**：Stage 4/8（組裝段落）可為每個前置段落選擇要組裝的版本
- **三 Tab 頁面**：每個 Stage 分為「輸入管理／執行／版本記錄」三個頁籤

---

## 快速開始

### 前置需求

```bash
Python >= 3.10
pip install google-generativeai python-dotenv pyyaml pandas openpyxl streamlit python-docx
```

### 5 分鐘快速整合

#### 步驟 1：複製核心工具庫

從 PeriodicScribe 參考實作複製以下檔案（**不需修改**）：

```
utils/
├── api/
│   └── gemini_api_utils.py    # GeminiAPIManager（多金鑰輪替）
└── config.py                   # 設定讀取
```

#### 步驟 2：建立設定檔

**`config.yaml`**：
```yaml
model_name: "gemini-2.5-flash"
retry_delay: 5
api_call_interval: 3
```

**`.env`**（不納入版控）：
```
API_KEYS=your_key1,your_key2,your_key3
```

**`.env.example`**（納入版控）：
```
API_KEYS=your_gemini_api_key_here
```

#### 步驟 3：建立 Stage 腳本

為每個文章段落建立 `stage{N}_{section_name}.py`：

```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from utils.api.gemini_api_utils import GeminiAPIManager
from utils.config import get_model_name

PROMPT = """
# Role
你是一位[描述角色]。

# Input Data（精確數據變數，禁止自行換算）
- 報告期間：{{DATE_RANGE}}
- 核心數據：{{KEY_DATA}}

# Requirements
[列出輸出要求]

# Style Reference
[期望輸出格式的範例]
"""

def check_inputs(year, period) -> list:
    issues = []
    # 檢查資料檔是否存在
    return issues

def build_prompts(year, period, prompt_texts=None) -> list:
    prompt = (prompt_texts or {}).get('PROMPT', PROMPT)
    # 載入資料並換算
    data = load_and_format_data(year, period)
    final = prompt.replace("{{KEY_DATA}}", data)
    return [{'name': 'PROMPT', 'text': final}]

def main(year, period, api_manager=None) -> bool:
    if api_manager is None:
        api_manager = GeminiAPIManager(get_model_name())
    prompts = build_prompts(year, period)
    result = api_manager.generate_content(prompts[0]['text'])
    output_path = Path(f"temp/section1_{period}.md")
    output_path.write_text(result, encoding='utf-8')
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, default=2026)
    parser.add_argument('--period', type=str, default="202603")
    args = parser.parse_args()
    main(args.year, args.period)
```

#### 步驟 4：建立 Workflow 腳本

**`run_my_report.py`**：

```python
import sys
from utils.api.gemini_api_utils import GeminiAPIManager
from utils.config import get_model_name
from scripts.stages.stage1_section1 import main as stage1_main
from scripts.stages.stage2_section2 import main as stage2_main

def run_workflow(year: int, period: str):
    print(f"開始生成 {period} 報告...")
    api_manager = GeminiAPIManager(get_model_name())  # 一次建立，全程共享

    results = {}
    results['stage1'] = stage1_main(year, period, api_manager=api_manager)
    results['stage2'] = stage2_main(year, period, api_manager=api_manager)

    success = all(results.values())
    print(f"\n{'✅ 完成' if success else '❌ 有 Stage 失敗'}")
    return success

if __name__ == "__main__":
    run_workflow(2026, sys.argv[1] if len(sys.argv) > 1 else "202603")
```

#### 步驟 5：測試執行

```bash
# 單一 Stage 測試
python -m scripts.stages.stage1_section1 --year 2026 --period 202603

# 完整 Workflow
python run_my_report.py 202603
```

**完成！** 輸出檔案會在 `temp/section1_202603.md`。

---

## 目錄結構

### 建議的標準結構

```
{your_project}/
├── run_{report_type}.py           # Workflow 入口腳本
│
├── scripts/
│   └── stages/
│       ├── stage0_data_prep.py    # 資料準備（0 API 呼叫）
│       ├── stage1_{section}.py    # 段落 1（1+ API 呼叫）
│       ├── stage2_{section}.py    # 段落 2
│       └── stageN_assembly.py    # 最終組裝（0 API 呼叫）
│
├── utils/
│   ├── api/
│   │   └── gemini_api_utils.py   # 核心工具（不修改）
│   ├── config.py                  # 設定讀取（不修改）
│   └── data_formatter.py         # 自訂資料格式化
│
├── {report_type}/                 # 報告類型子目錄（若有多個類型）
│   ├── utils/
│   │   └── {report_type}_prompt_manager.py
│   ├── prompts/
│   │   ├── baselines/             # Baseline JSON
│   │   └── backups/               # 腳本備份
│   └── temp/
│       └── versions/              # 輸出版本快照
│
├── config.yaml                    # 模型設定
├── .env                           # API 金鑰（不納入版控）
└── .env.example                   # 金鑰範例（納入版控）
```

### 參考實作的實際結構（etfflow_article）

```
etfflow_article/
├── run_complete_workflow.py        # 月報 Workflow
├── ui_app.py                       # 月報 Streamlit UI
│
├── scripts/stages/
│   ├── stage0_*/                   # 資料準備（7 個子腳本）
│   ├── stage1_us_summary.py        # 美國市場摘要
│   ├── stage2_us_flow.py           # 美國淨流量
│   ├── stage3_tw_flow.py           # 台灣淨流量（2 API）
│   ├── stage4_tw_summary.py        # 台灣市場摘要
│   ├── stage5_etf_flow.py          # ETF 淨流量表現
│   ├── stage6_etf_return.py        # ETF 報酬率表現
│   ├── stage7_conclusion.py        # 摘要結論（4 API）
│   └── stage8_assembly.py          # 組裝 DOCX
│
├── weekly_report/                  # 週報子系統
│   ├── run_weekly.py
│   ├── weekly_ui.py
│   └── stages/
│       ├── stage1_us_summary.py
│       ├── stage2_us_flow.py
│       ├── stage3_tw_flow.py
│       └── stage4_assembly.py
│
└── utils/
    ├── api/gemini_api_utils.py     # 共用工具
    ├── config.py
    ├── data_formatter.py
    ├── stage_io.py
    └── prompt_manager.py
```

---

## 擴展到新週期類型

以下示範如何新增一個「雙週報」系統。

### 1. 建立報告子目錄

```bash
mkdir biweekly_report
mkdir biweekly_report/stages
mkdir biweekly_report/utils
mkdir biweekly_report/temp
```

### 2. 定義週期格式

選擇一個清楚的格式，例如 `YYYY-B{NN}`（第 N 個雙週）。

在 `biweekly_report/utils/biweekly_data_formatter.py` 中建立週期工具：

```python
def biweek_label(year: int, biweek: int) -> str:
    return f"{year}-B{biweek:02d}"

def biweek_date_range(year: int, biweek: int) -> str:
    # 計算雙週的開始/結束日期
    start_day = (biweek - 1) * 14 + 1
    # ... 計算邏輯
    return f"{start_date} ~ {end_date}"
```

### 3. 複製並修改 Stage 腳本

以週報的 Stage 為基礎修改：

```python
# biweekly_report/stages/stage1_summary.py
biweekly_root = Path(__file__).parent.parent  # biweekly_report/
project_root = biweekly_root.parent

# 更改 output 前綴
output_file = output_dir / f"biweekly_summary_{biweek_label(year, biweek)}.md"
```

### 4. 建立 PromptManager

```python
# biweekly_report/utils/biweekly_prompt_manager.py
biweekly_root = Path(__file__).parent.parent

SCRIPT_MAP = {
    1: biweekly_root / "stages" / "stage1_summary.py",
    2: biweekly_root / "stages" / "stage2_analysis.py",
}

class BiweeklyPromptManager:
    baseline_dir = biweekly_root / "prompts" / "baselines"
    backup_dir   = biweekly_root / "prompts" / "backups"
    # ... 完整複製 WeeklyPromptManager 邏輯
```

### 5. 建立 Workflow 腳本

```python
# run_biweekly.py
from biweekly_report.stages.stage1_summary import main as stage1_main
from biweekly_report.stages.stage2_analysis import main as stage2_main

def run_biweekly(year: int, biweek: int):
    api_manager = GeminiAPIManager(get_model_name())
    stage1_main(year, biweek, api_manager=api_manager)
    stage2_main(year, biweek, api_manager=api_manager)
```

### 關鍵點

- **週期函數**：`check_inputs(year, biweek)`、`build_prompts(year, biweek)`、`main(year, biweek)` — 第二個參數換成你的週期單位
- **輸出前綴**：保持一致，例如 `biweekly_{section}_{label}.md`
- **版本路徑**：`temp/versions/{label}/stage{N}/v{timestamp}.md`
- **不修改** `utils/api/gemini_api_utils.py` 和 `utils/config.py`

---

## 設定參考

### `config.yaml` 完整說明

```yaml
# ===== 模型設定 =====
model_name: "gemini-2.5-flash"
# 可選值：gemini-2.5-flash / gemini-2.5-pro / gemini-1.5-flash
# 建議使用 gemini-2.5-flash（成本低、速度快，品質足夠）

# ===== 重試設定 =====
retry_delay: 5
# 說明：API 呼叫失敗後，等待幾秒再重試
# 單位：秒
# 預設值：5
# 建議範圍：3~10

# ===== API 呼叫間隔 =====
api_call_interval: 3
# 說明：同一個 Stage 內，兩次 API 呼叫之間的等待時間（避免速率限制）
# 單位：秒
# 預設值：3
# Stage 3（2 次 API）和 Stage 7（4 次 API）會用到
```

### 環境變數說明

| 變數名稱 | 必要 | 說明 | 範例 |
|---------|------|------|------|
| `API_KEYS` | 優先 | 多個 Gemini API 金鑰，逗號分隔 | `key1,key2,key3` |
| `GOOGLE_API_KEY` | 備用 | 單一 API 金鑰（`API_KEYS` 未設定時使用） | `AIzaSy...` |

**注意**：`API_KEYS` 的值不可包含空格（`key1, key2` 會導致解析錯誤）。

---

## 常見問題

### Q1：API 金鑰配額耗盡後系統如何反應？

`GeminiAPIManager` 會偵測包含 `quota`、`exhausted`、`429` 的錯誤訊息，自動切換到下一個金鑰並重試。若所有金鑰都耗盡，才會拋出例外。

---

### Q2：為什麼要 Workflow 共享 `api_manager`？

若每個 Stage 各自建立 `GeminiAPIManager`，Stage 1 耗盡 key1 後，Stage 2 又從 key1 開始嘗試，重複失敗。共享同一個實例，key 的耗盡狀態可以跨 Stage 保留。

---

### Q3：`build_prompts()` 的 `prompt_texts=None` 參數是做什麼的？

這是為 Streamlit UI 的「Prompt 預覽」功能預留的覆蓋接口。UI 編輯器在使用者修改 Prompt 後、尚未儲存前，可以呼叫 `build_prompts(year, period, prompt_texts={'PROMPT': 修改後內容})` 來預覽替換結果，而不影響腳本檔案本身。

---

### Q4：Prompt 中有 `{{variable}}` 但替換後 Prompt 還是顯示 `{{variable}}`？

檢查以下幾點：
1. Python 的 f-string 中 `{}` 有特殊含義，若 Prompt 字串是 f-string，需要改成普通字串或用 `{{` / `}}` 跳脫
2. 確認 `.replace("{{variable}}", value)` 的變數名稱大小寫與 Prompt 中完全一致
3. 確認 `build_prompts()` 中呼叫了 `.replace()` 且有賦值給新變數（`final = prompt.replace(...)`）

---

### Q5：Windows 環境下執行出現亂碼？

在每個 Stage 腳本頂部加入：
```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
```

---

### Q6：Streamlit Popen 串流 Log 沒有即時更新？

確認以下幾點：
1. Stage 腳本有加 `sys.stdout.reconfigure(encoding='utf-8')` 確保輸出可被讀取
2. `Popen` 命令包含 `-u` 參數：`python -u -m your.stage`（unbuffered output）
3. `st.empty()` 物件在迴圈內更新：`placeholder.code("\n".join(lines))`

---

### Q7：版本快照目錄在哪裡？如何手動清理？

版本快照在 `temp/versions/{period}/stage{N}/` 目錄下，每次執行會新增一個 `v{timestamp}.md` 檔案。可以安全刪除舊的版本檔案，但刪除前確認 `active_versions_{period}.json` 中記錄的 active 版本沒有被刪除。

---

### Q8：想要在不同報告類型之間切換使用同一個 `GeminiAPIManager`？

不建議跨報告類型共享，因為不同報告可能有不同的 `model_name`。每個報告類型的 Workflow 各自建立一個 `GeminiAPIManager` 即可。

---

### Q9：`check_inputs()` 回傳的 level 有哪些值？

標準值：
- `"ERROR"`：嚴重問題，`main()` 應中止執行
- `"WARN"`：警告，執行但提示使用者（例如：找不到上週資料，將以 0 代替）
- `"INFO"`：一般資訊（例如：找到 5 個資料檔案）

---

### Q10：Stage 腳本可以有多個 Prompt 嗎？

可以。Stage 3（台灣淨流量）就有 `PROMPT_OVERVIEW` 和 `PROMPT_DETAIL` 兩個 Prompt。`build_prompts()` 回傳一個 list，每個元素是 `{'name': 'PROMPT_XXX', 'text': final_prompt}`。`WeeklyPromptManager.get_prompts()` 會用 regex 提取所有 `PROMPT_XXX = """..."""` 格式的變數。

---

### Q11：Baseline 和普通備份有什麼差別？

- **Baseline（基準）**：儲存在 `prompts/baselines/stage{N}_baseline.json`，代表「已確認品質良好」的版本，供比較和還原用。主動呼叫 `save_baseline()` 才會更新。
- **Backup（備份）**：每次 `update_script_prompts()` 呼叫前自動備份整個腳本檔案到 `prompts/backups/stage{N}_{timestamp}.py`，是安全網而非版本控制。

---

### Q12：DOCX 組裝需要什麼格式的 Markdown？

Assembly Stage 解析 Markdown 時依賴特定的標題格式。確保前置 Stage 輸出的 Markdown 使用 `###` 而非 `##` 或 `#`，且標題文字需精確匹配（例如：`### 股票型 ETF`）。如需修改標題格式，需同步更新 Assembly Stage 的解析邏輯。

---

## 實際案例

### 案例 1：台灣+美國 ETF 月報

**專案**：每月生成台灣+美國 ETF 資金流量分析報告

**規格**：
- 8 個 Stage（Stage 0~8），共 13 次 API 呼叫
- 資料來源：Excel（台灣 SITCA 爬蟲）+ Excel（美國手動更新）
- 輸出：Markdown + DOCX（含圖表）

**整合後成果**：
- 月報生成時間：30~45 分鐘（API 速率限制為主因）
- Prompt 調整效率：Baseline 比較 + 一鍵還原，30 秒完成
- 金鑰管理：5 個金鑰輪替，不再因為配額問題手動介入

---

### 案例 2：台灣+美國 ETF 週報

**專案**：每週生成資金流量週報

**規格**：
- 4 個 Stage（Stage 0~4），共 4 次 API 呼叫
- 資料來源：每日 CSV 聚合（自動彙總，無需手動準備）
- 輸出：Markdown + DOCX
- 週期格式：`YYYY-WXX`（ISO 週次）

**與月報的差異**：
- 台灣資料不需下載 Excel，由每日 CSV 自動聚合
- Stage 數量更少，執行更快（10~15 分鐘）
- 獨立的 `WeeklyPromptManager`，不依賴月報的 `PromptManager`

---

## 與 AI 協作整合

### 快速整合新報告類型

複製 `PeriodicScribe_framework/AI_INTEGRATION_PROMPT.md` 中的指令，填入你的專案資訊，提供給 Claude 或 ChatGPT：

```
請幫我將 PeriodicScribe 框架整合到我的專案中，建立一個定期 LLM 文章生成系統。

【專案資訊】
- 專案路徑：/path/to/my_project
- 報告類型：科技雙週報
- 報告頻率：每兩週
- 文章段落數：4（市場摘要、產品動態、趨勢分析、結論）
- 主要資料來源：CSV 檔案
- 輸出格式：Markdown + DOCX
- 需要 Streamlit UI：否

【參考文件】
PeriodicScribe_spec.yaml（完整技術規格）
```

AI 會根據 `PeriodicScribe_spec.yaml` 的規格，為你的專案產生：
- 4 個 Stage 腳本骨架
- Workflow 入口腳本
- PromptManager 類別
- `config.yaml` 和 `.env.example`

你只需要填入業務邏輯（資料讀取函數、Prompt 內容）。

---

## 授權

MIT License — 自由使用、修改、分發。

---

## 變更日誌

### v1.0（2026-03-24）

- ✨ 初始版本，基於月報（Stage 0~8）和週報（Stage 0~4）的實際專案提煉
- ✅ 多金鑰 API 輪替（`GeminiAPIManager`）
- ✅ Workflow 共享 API Manager 模式
- ✅ Stage 標準介面（`check_inputs` / `build_prompts` / `main`）
- ✅ Prompt 版本控制（Baseline / Backup / Draft）
- ✅ 輸出版本快照與 Active 版本追蹤
- ✅ Streamlit UI（三 Tab 頁面 + Popen 串流 Log）
- ✅ Python 端預算數據模式

---

**🎯 快速開始：複製 `utils/api/gemini_api_utils.py`，建立你的第一個 Stage 腳本，5 分鐘內讓 LLM 開始生成你的第一篇定期文章！**
