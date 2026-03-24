# AI 整合指令 - PeriodicScribe

> 📋 複製本文件的指令，直接提供給 AI 助手使用，快速在新專案中建立定期 LLM 文章生成系統

---

## 🤖 完整整合指令（複製使用）

```
請幫我將 PeriodicScribe 框架整合到我的專案中，建立一個定期 LLM 文章生成系統。

【專案資訊】
- 專案路徑：[填入你的專案路徑]
- 報告類型：[例如：科技週報、財經月報、產品雙週報]
- 報告頻率：[每日 / 每週 / 每月 / 每季]
- 文章段落數：[幾個主要段落，對應 Stage 數量]
- 主要資料來源：[Excel / CSV / API / 網路爬蟲]
- 輸出格式：[Markdown + DOCX / 純 Markdown]
- 需要 Streamlit UI：[是 / 否]

【PeriodicScribe 規格參考】
請閱讀 PeriodicScribe_spec.yaml 中的完整技術規格。

請執行以下步驟：

### 步驟 1：複製核心工具庫
從參考實作複製以下檔案到新專案：
- utils/api/gemini_api_utils.py（GeminiAPIManager，不需修改）
- utils/config.py（設定讀取，不需修改）
建立以下新檔案：
- config.yaml（模型名稱、重試設定）
- .env（API 金鑰）
- .env.example（金鑰範例，納入版本控制）

### 步驟 2：依照段落數量建立 Stage 腳本
為每個文章段落建立對應的 stage{N}_{section_name}.py，遵循以下標準介面：

```python
PROMPT = """
[在此定義 Prompt，包含佔位符如 {{DATE_RANGE}}, {{DATA_TABLE}}]
[最後加一個 Style Reference 範例]
"""

def check_inputs(year, period) -> list:
    """回傳 [(level, message), ...] 列表"""
    pass

def build_prompts(year, period, prompt_texts=None) -> list:
    """組裝完整 Prompt，支援 UI 預覽覆蓋"""
    prompt = (prompt_texts or {}).get('PROMPT', PROMPT)
    data = load_data(year, period)  # 在此讀取並格式化資料
    final = prompt.replace("{{DATA_TABLE}}", data)
    return [{'name': 'PROMPT', 'text': final}]

def main(year, period, api_manager=None) -> bool:
    """支援獨立執行和 Workflow 共享模式"""
    if api_manager is None:
        api_manager = GeminiAPIManager()
    prompts = build_prompts(year, period)
    result = api_manager.generate_content(prompts[0]['text'])
    output_path.write_text(result, encoding='utf-8')
    return True
```

### 步驟 3：建立 Workflow 編排腳本
建立 run_{report_type}.py，關鍵模式：
```python
api_manager = GeminiAPIManager(model)  # 一次建立，全程共享
for stage_fn in stage_functions:
    result = stage_fn(year, period, api_manager=api_manager)
```

### 步驟 4：（選擇性）建立 Streamlit UI
使用 PeriodicScribe_spec.yaml 中 ui_patterns 節的模板。
關鍵元件：
- Popen 串流 Log（run_cmd 函數）
- 三 Tab 頁面架構（輸入管理 / 執行 / 版本記錄）
- Prompt 管理 UI（含 Baseline 比較）
- 版本選擇組裝（組裝 Stage 頁面）

### 步驟 5：整合報告
完成後，請提供：
1. 建立了哪些檔案（列出路徑）
2. 需要我手動填寫的部分（Prompt 內容、資料讀取邏輯）
3. 測試方法（單一 Stage 測試指令 + 完整 Workflow 測試指令）

【參考文件】
- PeriodicScribe_spec.yaml（完整技術規格）
- README.md（概念說明和使用指南）

【注意事項】
- build_prompts() 必須有 prompt_texts=None 參數（UI 預覽用）
- 所有數值換算在 Python 端完成，Prompt 中標注「禁止自行換算」
- Stage 腳本的 main() 中要輸出清楚的進度訊息（供 Popen 串流顯示）
- Windows 系統需在腳本頂部加入 sys.stdout.reconfigure(encoding='utf-8')
```

---

## 🎯 最小化版指令（快速建立單一 Stage）

```
請幫我建立一個 PeriodicScribe Stage 腳本，用於[描述此段落的內容]。

配置：
- 輸入資料：[Excel 檔案 / CSV / API]
- 資料內容：[描述資料格式]
- 輸出段落：[描述要生成的文字內容]
- 週期格式：[YYYYMM / YYYY-WXX / 其他]

請遵循以下介面（從 PeriodicScribe_spec.yaml）：
- PROMPT = """..."""（含佔位符）
- check_inputs(year, period) -> list
- build_prompts(year, period, prompt_texts=None) -> list
- main(year, period, api_manager=None) -> bool

Prompt 要求：
- 包含 Role 定義、Input Data、Requirements 三個區塊
- 最後加一個 Style Reference（期望輸出的格式範例）
- 數值佔位符要在 build_prompts() 中替換完畢
```

---

## 🔧 常見客製化需求

### 需求 1：為現有系統加入版本管理

```
我有一個已存在的定期報告生成腳本，想加入 PeriodicScribe 的版本管理系統。

現有腳本路徑：[路徑]
週期格式：[YYYYMM / YYYY-WXX]

請在執行成功後加入快照邏輯（參考 PeriodicScribe_spec.yaml 的 version_management 節）：
def snapshot(stage_num, period, tag=None):
    src = TEMP_DIR / f"{output_prefix}_{period}.md"
    d = VERSIONS_BASE / period / f"stage{stage_num}"
    d.mkdir(parents=True, exist_ok=True)
    vid = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(src, d / f"{vid}.md")
    return vid

並在 main() 成功後呼叫：
vid = snapshot(stage_num, period)
set_active_vid(stage_num, period, vid)
```

### 需求 2：加入 Prompt 管理系統到現有 Stage

```
我有 [N] 個 Stage 腳本，每個腳本中有 PROMPT = """..."""。
請幫我加入 PeriodicScribe 的 Prompt 管理系統：

1. 建立 {report_type}/utils/{report_type}_prompt_manager.py
   - 複製 WeeklyPromptManager 的結構（PeriodicScribe_spec.yaml prompt_management 節）
   - 修改 SCRIPT_MAP 指向我的 Stage 腳本
   - 修改 baseline_dir 和 backup_dir 路徑

2. 為每個 Stage 的 build_prompts() 加入 prompt_texts=None 參數：
   prompt = (prompt_texts or {}).get('PROMPT', PROMPT)

3. 建立初始 Baseline：
   pm = {ReportType}PromptManager()
   for sn in range(1, N+1):
       pm.save_baseline(sn)
```

### 需求 3：建立最小化 Streamlit UI（只有執行 + Log）

```
請幫我建立一個最小化的 PeriodicScribe Streamlit UI，只需要：
1. Sidebar：週期選擇 + Stage 導覽
2. 每個 Stage 頁面：執行按鈕 + Popen 串流 Log + 輸出預覽
3. 不需要版本管理、Prompt 編輯等進階功能

報告類型：[名稱]
Stage 數量：[N]
週期格式：[YYYYMM / YYYY-WXX]
Module 路徑：[如 myproject.stages.stage1_xxx]

參考 PeriodicScribe_spec.yaml 的 ui_patterns.popen_streaming 節。
```

### 需求 4：加入 DOCX 組裝 Stage

```
請幫我建立 stage{N}_assembly.py，將前面 Stage 的 Markdown 輸出組裝成 DOCX 檔案。

Stage 輸出檔案：
- Stage 1：[路徑/格式]
- Stage 2：[路徑/格式]
- Stage 3：[路徑/格式]

DOCX 結構：
- 標題：[格式]
- 各段落 H2 標題：[名稱列表]
- 字型：[微軟正黑體 / 其他]
- 是否有免責聲明：[是/否]

參考 weekly_report/stages/stage4_assembly.py 的 generate_docx() 函數。
```

### 需求 5：整合多個 API 金鑰

```
我有多個 Gemini API 金鑰，請幫我設定 PeriodicScribe 的多金鑰輪替。

金鑰數量：[N 個]

請：
1. 在 .env 中設定 API_KEYS=key1,key2,...（不含空格）
2. 確認 GeminiAPIManager 初始化時讀取所有金鑰
3. 說明金鑰輪替觸發條件（配額錯誤關鍵詞）
4. 說明如何在 Workflow 中共享單一 Manager 實例
```

---

## 📋 使用方式

### 方法 1：完整新系統建立
1. 複製上方「完整整合指令」
2. 填入你的專案資訊
3. 附上 `PeriodicScribe_spec.yaml`
4. 提供給 Claude / ChatGPT
5. AI 會產生完整的框架骨架，你只需填入業務邏輯（資料讀取、Prompt 內容）

### 方法 2：升級現有腳本
1. 選擇對應的「常見客製化需求」指令
2. 填入現有系統資訊
3. 附上 `PeriodicScribe_spec.yaml`
4. AI 會在不破壞現有邏輯的前提下加入框架功能

### 方法 3：單一功能整合
1. 使用「最小化版指令」只建立你需要的部分
2. 例如：只要多金鑰輪替，不要 UI

---

## ✅ 整合檢查清單

**核心工具庫：**
- [ ] `utils/api/gemini_api_utils.py` 存在且可正常 import
- [ ] `utils/config.py` 存在且可正常 import
- [ ] `config.yaml` 存在（包含 model_name 設定）
- [ ] `.env` 存在（包含 API_KEYS 或 GOOGLE_API_KEY）

**Stage 腳本：**
- [ ] 每個 Stage 包含 `PROMPT = """..."""` 常數
- [ ] `build_prompts()` 有 `prompt_texts=None` 參數
- [ ] `main()` 有 `api_manager=None` 參數
- [ ] 腳本頂部有 Windows 編碼修復（sys.stdout.reconfigure）

**Workflow：**
- [ ] 建立共享 `GeminiAPIManager` 實例
- [ ] 傳入 `api_manager` 給所有 Stage
- [ ] 執行結果有摘要輸出

**版本管理（可選）：**
- [ ] `temp/versions/` 目錄結構正確
- [ ] `active_versions_{period}.json` 格式正確
- [ ] 執行後自動快照邏輯存在

**Streamlit UI（可選）：**
- [ ] `STAGE_META` 字典配置正確
- [ ] `_TEMP_FILE_MAP` 對應正確
- [ ] Popen 串流 Log 正常運作
- [ ] Prompt 管理 UI 可載入 Prompt

**測試驗證：**
- [ ] `python -m stage{N} --year 2026 --period 12` 單一 Stage 正常執行
- [ ] `python run_{report_type}.py 2026 12` 完整 Workflow 正常執行
- [ ] 輸出檔案存在於 `output_{period}/`

---

## 📊 系統功能說明（供 AI 參考）

### 1. 多金鑰 API 輪替
```python
# 環境變數設定多金鑰
API_KEYS=key1,key2,key3,key4,key5

# 自動輪替（無需任何程式碼改動）
api_manager = GeminiAPIManager()
result = api_manager.generate_content(prompt)
# 若 key1 配額耗盡，自動切換到 key2，依此類推
```

### 2. Workflow 共享模式
```python
# 一次建立，全程共享——避免 Stage 間重複嘗試已耗盡的金鑰
api_manager = GeminiAPIManager()
result1 = stage1_main(2026, 12, api_manager=api_manager)
result2 = stage2_main(2026, 12, api_manager=api_manager)
result3 = stage3_main(2026, 12, api_manager=api_manager)
```

### 3. Prompt 版本控制
```python
pm = WeeklyPromptManager()
pm.save_baseline(3)           # 設為 Baseline
pm.compare_with_baseline(3)   # 比較差異
pm.restore_from_baseline(3)   # 還原到 Baseline
```

### 4. 輸出版本管理
```python
# 執行後自動快照
vid = snapshot(stage_num, period)       # 儲存版本
set_active_vid(stage_num, period, vid)  # 標記為主要版本

# 組裝時選擇版本
apply_version(stage_num, period, "v20260224_150000")  # 套用指定版本
```

### 5. 串流 Log UI
```python
# Popen 串流——使用者可即時看到執行進度
proc = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT, ...)
for line in proc.stdout:
    lines.append(line.rstrip())
    placeholder.code("\n".join(lines[-50:]))  # 即時更新顯示
```

---

## 📚 相關文件

- **系統規格（給 AI）**：`PeriodicScribe_spec.yaml`
- **完整使用文件**：`README.md`
- **參考實作**：`etfflow_article/` 專案（月報 + 週報）

---

**🎯 這個檔案的目的：讓您可以快速複製指令，請 AI 幫您將 PeriodicScribe 框架整合到任何新的定期文章生成專案中！**
