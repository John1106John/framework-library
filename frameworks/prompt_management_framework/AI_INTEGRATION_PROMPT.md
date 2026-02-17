# AI 整合指令 - Prompt 管理系統

> 📋 複製本檔案的指令，直接提供給 AI 助手使用

---

## 🤖 完整整合指令（複製使用）

```
請幫我將「Prompt 管理系統」整合到我的專案中。

專案資訊：
- 專案路徑：[填入你的專案路徑]
- Workflow 類型：[多階段 AI 報告生成 / 內容分析 / 數據處理]
- Stage 腳本位置：[填入腳本目錄，如 scripts/stages/]
- 是否已有 Streamlit UI：[是 / 否]

請執行以下步驟：

### 步驟 1：建立目錄結構
在專案根目錄建立以下目錄：
- prompts/（JSON 快取）
- prompts/baselines/（Baseline 基準版本，不可刪除）
- prompts/backups/（自動備份）
- prompts/drafts/（UI 草稿暫存，可刪除）
- temp/versions/{YYYYMM}/（輸出版本快照）
- utils/（工具模組，如不存在）

### 步驟 2：創建核心模組
建立 utils/prompt_manager.py，實作以下功能：
1. PromptManager 類別：
   - extract_prompts_from_script(script_path) - 從 .py 提取 PROMPT 常數
   - get_prompts(report_type) - 取得 prompt（永遠從腳本提取）
   - save_prompts(report_type, prompts) - 儲存到 JSON 快取
   - update_script_prompts(report_type, prompts) - 寫回 .py 腳本
   - list_backups(stage_num) - 列出所有備份
   - restore_from_backup(backup_path) - 還原備份
   - get_baseline(report_type) - 讀取 baseline 基準版本
   - save_baseline(report_type) - 將目前腳本設為 baseline
   - compare_with_baseline(report_type) - 比較目前腳本與 baseline 差異
   - restore_from_baseline(report_type) - 從 baseline 還原腳本

2. 設計原則：
   - Prompt 以 Python 常數形式寫在腳本中（PROMPT_1 = """..."""）
   - get_prompts() 永遠從 .py 腳本提取（不依賴 JSON 快取）
   - JSON 快取僅用於草稿暫存，不作為讀取來源
   - 修改前自動備份 .py 和 .json 檔案
   - Baseline 為穩定參考版本，不可刪除僅能覆蓋

### 步驟 3：掃描 Stage 腳本
掃描我的 Stage 腳本（scripts/stages/stage*.py），找出所有 Prompt：
1. 提取所有 PROMPT_* 常數
2. 為每個 Stage 建立 prompts/stage{N}_prompts.json
3. 記錄每個 Prompt 的：
   - 變數名稱（如 PROMPT_1）
   - 內容
   - 起始行號（用於寫回）
   - 字數、行數統計

### 步驟 4：建立共用資料格式化模組（重要！）
建立 utils/data_formatter.py，實作資料格式化函數：
1. 從每個 Stage 腳本中提取資料載入和格式化邏輯
2. 將這些邏輯抽取為獨立函數（如 load_us_etf_data、format_market_trends）
3. Stage 腳本和 UI 預覽都使用這些共用函數
4. 確保預覽與實際執行完全一致

範例結構：
```python
# utils/data_formatter.py
def load_excel_data(file_path, year, month):
    """從 Excel 載入並格式化數據（Stage 腳本和 UI 預覽共用）"""
    # 資料載入和格式化邏輯
    return formatted_data
```

### 步驟 5：整合 Streamlit UI
如果專案已有 Streamlit UI（如 ui_app.py）：
1. 在現有 UI 中新增「Prompt 編輯」頁面
2. 實作功能：
   - 選擇 Stage（下拉選單）
   - 顯示該 Stage 的所有 Prompt（text_area 編輯器）
   - 顯示字數、行數統計
   - 顯示修改狀態（Modified / Saved）
   - 按鈕：儲存草稿、載入草稿、更新腳本、重新載入
   - 草稿記錄：Baseline 置頂（可載入，不可刪除），草稿可載入和刪除（🗑 按鈕）
   - Baseline 比較：顯示目前腳本與 Baseline 的差異（左右並排），可設為新 Baseline 或從 Baseline 還原
   - 預覽功能：使用 utils/data_formatter.py 生成實際變數替換後的 Prompt

如果專案沒有 Streamlit UI：
1. 建立新的 prompt_editor_ui.py
2. 實作基本的 Prompt 編輯介面

### 步驟 6：整合版本管理（可選但推薦）
建立 utils/version_manager.py，實作輸出版本管理：
1. VersionManager 類別：
   - snapshot_output(stage_num, output_md, version_id) - 快照輸出
   - set_active_version(stage_num, version_id) - 設定主要版本
   - get_active_version(stage_num) - 取得主要版本
   - list_versions(stage_num) - 列出所有版本
   - delete_version(stage_num, version_id) - 刪除版本

2. 在每個 Stage 腳本執行成功後，自動呼叫 snapshot_output()

### 步驟 7：更新 Stage 腳本
重構 Stage 腳本：
1. 將資料格式化邏輯移到 utils/data_formatter.py
2. 在腳本開頭 import 共用函數
3. 在腳本結尾加入版本快照（如果使用版本管理）

範例：
```python
# scripts/stages/stage1_xxx.py

from utils.data_formatter import load_us_etf_data, format_market_trends
from utils.version_manager import VersionManager

PROMPT_1 = """
您是一位金融分析師...
"""

def main(year, month):
    # 使用共用函數載入資料
    data = load_us_etf_data(excel_file, year, month)

    # 使用 Prompt 呼叫 API
    result = api_manager.generate_content(PROMPT_1.format(data=data), ...)

    # 儲存結果並快照
    save_output(result)
    VersionManager().snapshot_output(stage_num=1, output_md=result, version_id=f"v{timestamp}")
```

### 步驟 8：建立測試腳本
建立 test_prompt_manager.py：
1. 測試 Prompt 提取（從 .py 腳本）
2. 測試 JSON 快取讀寫
3. 測試寫回腳本功能
4. 測試備份和還原
5. 測試共用資料格式化模組
6. 輸出測試結果

### 步驟 9：整合報告
完成後，請提供：
1. 建立了哪些新檔案（列出路徑）
2. 修改了哪些現有檔案
3. 從 Stage 腳本中提取了多少個 Prompt
4. 共用資料格式化模組包含哪些函數
5. UI 預覽功能是否正常運作
6. 測試腳本的執行結果

參考文件：
- prompt_management_system_spec.yaml（完整系統規格 - 給 AI 看）
- README_PROMPT_SPEC.md（詳細使用文檔 - 給人類看）

注意事項：
- Prompt 必須保留在 .py 腳本中作為 single source of truth
- JSON 快取僅用於加速載入，不是主要存儲
- 修改腳本前必須自動備份
- 確保 utils/ 和所有子目錄都有 __init__.py
- UI 預覽與實際執行必須使用相同的資料格式化函數
```

---

## 🎯 簡化版指令（快速整合）

```
請將 Prompt 管理系統整合到我的專案：

專案路徑：[你的專案路徑]
Stage 腳本目錄：[如 scripts/stages/]

步驟：
1. 建立目錄結構（prompts/, prompts/backups/, utils/）
2. 建立 utils/prompt_manager.py（Prompt 提取、JSON 快取、寫回腳本）
3. 建立 utils/data_formatter.py（共用資料格式化模組）
4. 掃描 Stage 腳本，提取所有 PROMPT 常數
5. 整合到現有 Streamlit UI 或建立新 UI
6. 建立測試腳本驗證功能

參考：prompt_management_system_spec.yaml
```

---

## 📋 使用方式

### 方法 1：完整整合（推薦）
1. 複製上方「完整整合指令」區塊
2. 填入你的專案資訊（路徑、Workflow 類型、腳本位置）
3. 提供給 AI 助手（Claude、ChatGPT 等）
4. AI 會自動執行所有步驟並提供報告

### 方法 2：快速整合
1. 複製「簡化版指令」區塊
2. 填入基本資訊（專案路徑和 Stage 腳本目錄）
3. 提供給 AI 助手
4. 適合簡單專案的快速整合

### 方法 3：分階段整合
根據你的需求，從完整指令中選擇需要的步驟：
- 只需要 Prompt 編輯？→ 執行步驟 1-3、5
- 需要版本管理？→ 執行所有步驟
- 需要 UI 預覽？→ 執行步驟 1-5（包含共用資料格式化模組）

---

## 🔧 常見自訂需求

### 需求 1：整合到現有 Streamlit UI

```
我已經有 Streamlit UI（ui_app.py），請將 Prompt 編輯功能整合進去：

步驟：
1. 建立 utils/prompt_manager.py
2. 在 ui_app.py 中新增「Prompt 編輯」頁面（使用 st.sidebar 或 tab）
3. 實作 Prompt 編輯介面（選擇 Stage、編輯、儲存、預覽）
4. 建立 utils/data_formatter.py 確保預覽一致性
5. 在現有頁面中使用 data_formatter 函數

參考：prompt_management_system_spec.yaml 的 shared_formatters 章節
```

### 需求 2：僅提取和管理 Prompt（不需要 UI）

```
我只需要 Prompt 的提取和管理功能，不需要 UI：

步驟：
1. 建立 utils/prompt_manager.py
2. 掃描 Stage 腳本，提取 PROMPT 常數
3. 建立 JSON 快取
4. 提供 CLI 工具（可選）用於編輯和寫回

參考：prompt_management_system_spec.yaml 的 PromptManager 類別
```

### 需求 3：加入版本管理和輸出快照

```
請加入輸出版本管理功能：

步驟：
1. 建立 utils/version_manager.py
2. 在每個 Stage 腳本執行後自動快照輸出
3. 建立 temp/versions/{YYYYMM}/stage{N}/ 目錄結構
4. 實作版本切換和刪除功能
5. 在 UI 中顯示版本列表（可選）

參考：prompt_management_system_spec.yaml 的 Version Manager 章節
```

### 需求 4：確保 UI 預覽與實際執行一致

```
我的 UI 預覽結果與實際執行不一致，請幫我修正：

問題分析：
- 原因：UI 和 Stage 腳本各自實作了資料格式化邏輯
- 解決：建立共用資料格式化模組

步驟：
1. 建立 utils/data_formatter.py
2. 從 Stage 腳本中提取所有資料載入和格式化函數
3. 將這些函數移到 data_formatter.py
4. Stage 腳本和 UI 預覽都 import 並使用相同函數
5. 測試預覽與實際執行是否一致

參考：prompt_management_system_spec.yaml 的 shared_formatters 章節
```

---

## 🌟 關鍵設計原則

### 1. Prompt 即程式碼
- Prompt 直接寫在 .py 腳本中作為 module-level 常數
- JSON 快取僅用於加速載入，不是主要存儲
- Single Source of Truth：.py 腳本

### 2. 預覽一致性（Preview Consistency）
- UI 預覽與實際執行使用相同的資料格式化函數
- 建立 utils/data_formatter.py 共用模組
- 避免重複實作導致不一致

### 3. 安全的修改流程
- 修改 .py 腳本前自動備份（.py 和 .json）
- 草稿系統：可以暫存修改而不影響執行
- 支援還原備份

### 4. 版本管理
- 每次執行後自動快照輸出
- 可切換主要版本（active version）
- 支援版本比較和刪除

---

## 📖 延伸閱讀

- **完整規格**：prompt_management_system_spec.yaml
- **使用文檔**：README_PROMPT_SPEC.md
- **目錄結構**：見 spec.yaml 的 directory_structure 章節
- **共用格式化架構**：見 spec.yaml 的 shared_formatters 章節

---

**版本：** 1.3.0
**最後更新：** 2026-02-17
**適用專案：** 多階段 AI Workflow（報告生成、內容分析、數據處理等）
