# Prompt Management System 規格使用指南

> 🎯 **一份給 AI 的完整系統規格，讓 AI 為你的專案快速建立 Prompt 管理系統**

## 📖 這是什麼？

`prompt_management_system_spec.yaml` 是一份詳細的系統設計規格文檔，專門用於指導 AI（Claude、GPT、Gemini 等）為你的專案建構一套完整的 **Prompt 版本管理系統**。

### 核心功能

這個規格會讓 AI 為你生成：

✅ **Prompt 管理器**：從 Python 腳本提取/更新 Prompt
✅ **Streamlit UI**：視覺化編輯介面
✅ **版本管理**：自動快照和版本切換
✅ **草稿系統**：暫存修改不影響執行
✅ **預覽功能**：即時查看變數替換後的 Prompt
✅ **共用程式碼架構** ⭐：預覽與實際執行使用相同的程式碼，確保 100% 一致性
✅ **安全啟動**：三種安全模式的啟動腳本

---

## 🎯 適用場景

**✅ 適合使用這個規格的專案：**

- 多階段 AI Workflow（如報告生成、內容分析、數據處理）
- 需要頻繁調整 Prompt 的專案
- 需要 A/B 測試不同 Prompt 效果的場景
- 團隊協作需要 Prompt 版本管理的專案

**❌ 不適合的場景：**

- 只有 1-2 個簡單 Prompt 的小專案
- Prompt 很少修改的靜態專案
- 不需要 UI 的純命令行工具

---

## 🚀 快速開始

### 方法 1：給 Claude/ChatGPT 的完整 Prompt

```markdown
我想為我的 AI Workflow 專案建立 Prompt 管理系統。

我的專案情況：
- 有 X 個階段（Stage 1-X）
- 每個階段呼叫 LLM API
- Prompt 寫在 Python 腳本中
- 需要頻繁調整 Prompt

請根據以下規格為我設計並實作完整系統：

[複製貼上整個 prompt_management_system_spec.yaml 的內容]

請為我生成：
1. utils/prompt_manager.py - PromptManager 類別
2. ui_app.py 的 Prompt 編輯器組件（含預覽功能）
3. 版本管理相關函數
4. 三種安全啟動腳本
5. .streamlit/config.toml 配置文件
6. 使用說明文檔
```

### 方法 2：分階段實作

如果專案較小，可以只參考部分章節：

```markdown
我需要一個簡單的 PromptManager 類別來管理 Prompt。

請參考以下規格的 prompt_manager_class 章節實作：

[貼上 YAML 中的 prompt_manager_class 章節]
```

---

## 📋 使用步驟

### Step 1：分析你的專案

在使用這個規格前，先整理你的專案資訊：

```
我的專案有幾個 Stage？
- Stage 1: XXX（1 個 API 呼叫）
- Stage 2: YYY（2 個 API 呼叫）
- ...

Prompt 目前寫在哪裡？
- scripts/stage1_xxx.py
- scripts/stage2_yyy.py
- ...

Prompt 的格式是？
- 單一變數：PROMPT = """..."""
- 多個變數：PROMPT_A = """...""", PROMPT_B = """..."""
- 動態生成：包含前面 stage 的輸出
```

### Step 2：準備給 AI 的 Prompt

將你的專案資訊整理成清晰的描述：

```markdown
專案：[專案名稱]
階段數：[N 個]

Stage 配置：
Stage 1: [名稱]（[N] 個 API）
  - 腳本: scripts/stage1_xxx.py
  - Prompt 變數: PROMPT
  - 輸入: [圖片/資料]
  - 輸出: temp/stage1_output.md

Stage 2: ...
```

### Step 3：呼叫 AI

將你的專案描述 + 完整的 YAML 規格一起提供給 AI。

**建議使用的 AI：**
- **Claude Sonnet 3.5/4.5**（推薦）：理解能力強，生成的代碼品質高
- **GPT-4/4o**：也很好用
- **Gemini 2.0 Flash**：速度快，適合快速迭代

### Step 4：驗證和調整

AI 生成代碼後：

1. **檢查檔案結構**
   ```
   project/
   ├── utils/
   │   └── prompt_manager.py  ← 檢查是否生成
   ├── prompts/              ← 檢查目錄
   ├── .streamlit/
   │   └── config.toml       ← 檢查配置
   ├── start_ui.bat          ← 檢查啟動腳本
   └── ui_app.py             ← 檢查 UI
   ```

2. **測試核心功能**
   - Prompt 提取：能否從腳本提取 Prompt？
   - UI 編輯：能否在 UI 中編輯？
   - 寫回腳本：修改後能否寫回 .py？
   - 版本管理：執行後有版本快照嗎？

3. **根據需要調整**
   - 如果 Prompt 提取失敗，檢查 regex 是否匹配你的格式
   - 如果需要更多變數支援，擴展 `render_prompt_with_variables()`
   - 如果需要密碼保護，參考 `.streamlit/secrets.toml`

---

## 💡 實用範例

### 範例 1：報告生成專案

**專案描述：**
```
3 階段的市場報告生成系統
- Stage 1: 數據摘要（1 API）
- Stage 2: 詳細分析（2 API）
- Stage 3: 總結（1 API，動態 Prompt）
```

**給 AI 的 Prompt：**
```markdown
我有一個 3 階段的報告生成專案：

Stage 1: 數據摘要（1 個 API 呼叫）
  腳本: scripts/stage1_summary.py
  Prompt 變數: PROMPT
  Prompt 內容: 包含 {{YEAR}}, {{MONTH}} 變數

Stage 2: 詳細分析（2 個 API 呼叫）
  腳本: scripts/stage2_analysis.py
  Prompt 變數: PROMPT_SECTION_A, PROMPT_SECTION_B
  Prompt 內容: 包含 {{data}} 動態變數

Stage 3: 總結（1 個 API 呼叫）
  腳本: scripts/stage3_conclusion.py
  Prompt 變數: PROMPT（動態，包含 Stage 1-2 的輸出）

請根據以下規格建立 Prompt 管理系統：
[貼上 YAML 內容]
```

### 範例 2：只需要 PromptManager

**給 AI 的 Prompt：**
```markdown
我只需要一個 Python 類別來管理 Prompt：
- 從 .py 腳本提取 PROMPT 變數
- 儲存到 JSON 快取
- 能夠寫回腳本

請參考以下規格實作 PromptManager 類別：
[貼上 YAML 中的 prompt_manager_class 章節]
```

---

## 📚 YAML 規格結構說明

```yaml
# ============================================================================
# 核心架構（必讀）
# ============================================================================
system_overview          # 系統概述，了解整體設計
architecture             # 核心架構和資料流
directory_structure      # 檔案組織結構
shared_formatters        # ⭐ 共用程式碼架構（預覽與實際執行一致性）

# ============================================================================
# 實作細節（給 AI 看的）
# ============================================================================
prompt_manager_class     # PromptManager 類別完整設計
script_prompt_conventions # Prompt 寫法規範（很重要！）
ui_integration           # Streamlit UI 設計
version_management       # 版本管理機制
streamlit_security       # 安全啟動配置

# ============================================================================
# 輔助資訊
# ============================================================================
known_pitfalls          # 已知問題和解決方案
ai_implementation_guide # 給 AI 的實作步驟
quick_start_example     # 快速開始範例
faq                     # 常見問題
```

---

## 🔍 常見問題

### Q1：AI 生成的代碼不能正確提取我的 Prompt？

**A：** 檢查你的 Prompt 格式是否符合規範：

**✅ 支援的格式：**
```python
# 格式 1：單一變數
PROMPT = """
你的 prompt 內容...
"""

# 格式 2：多個變數
PROMPT_SECTION_A = """..."""
PROMPT_SECTION_B = """..."""

# 格式 3：字典格式
PROMPTS = {
    "section_1": """...""",
    "section_2": """..."""
}
```

**❌ 不支援的格式：**
```python
# 動態 f-string（無法靜態提取）
prompt = f"""
根據 {previous_output} 分析...
"""

# 不是 module-level 常數
def my_function():
    prompt = """..."""  # 無法提取
```

### Q2：需要修改 AI 生成的代碼嗎？

**A：** 通常需要微調：

1. **Prompt 變數名稱**：確保 regex 能匹配你的命名規則
2. **變數替換**：擴展 `render_prompt_with_variables()` 支援更多變數
3. **STAGE_META 配置**：根據你的實際 stage 調整
4. **安全模式**：選擇適合的預設啟動模式

### Q3：可以用於非 Python 的專案嗎？

**A：** 規格是針對 Python + Streamlit 設計的，但核心概念可以遷移：

- **核心思想**：Prompt 即程式碼，版本管理，UI 編輯
- **其他語言**：可以參考架構，用對應語言實作
- **其他框架**：PromptManager 不依賴 Streamlit，可用於 Flask/FastAPI

### Q4：如何處理大量 Prompt（10+ 個 Stage）？

**A：** 建議策略：

1. **分類管理**：將相關 stage 分組
2. **統一命名**：使用一致的變數命名規則（`PROMPT_STAGE1_XXX`）
3. **批量操作**：添加「批量更新」功能
4. **搜尋功能**：在 UI 添加 Prompt 搜尋

### Q5：版本管理會佔用很多空間嗎？

**A：** 不會，Markdown 文件很小：

- 單個 Prompt：< 10 KB
- 100 個版本：< 1 MB
- 建議：定期清理舊版本（保留最近 20 個）

---

## 🛡️ 安全注意事項

使用 Streamlit UI 時，請注意：

### 🟢 安全模式（推薦）

```bash
start_ui.bat  # 僅本機訪問
```

**特點：**
- 只有你的電腦能訪問
- 無外網暴露風險
- 資料不會外洩

### 🟡 內網模式

```bash
start_ui_network.bat  # 區域網路訪問
```

**特點：**
- 同網路的設備可訪問
- 適合團隊協作
- 確保在可信網路

### 🔴 開放模式（高風險）

```bash
start_ui_public.bat  # 全世界可訪問
```

**⚠️ 警告：**
- 全世界任何人都可訪問
- 可執行腳本、查看資料
- 僅短期測試使用（< 10 分鐘）

**安全建議：**
- 預設使用安全模式
- 遠端訪問改用 Streamlit Cloud + 密碼保護
- 定期檢查 `.env` 是否在 `.gitignore` 中

---

## 📦 生成的檔案結構

AI 按照規格生成後，你會得到：

```
project/
├── utils/
│   └── prompt_manager.py          # PromptManager 類別
│       ├── extract_prompts_from_script()
│       ├── get_prompts()
│       ├── save_prompts()
│       ├── update_script_prompts()
│       └── list_backups() / restore_from_backup()
│
├── prompts/
│   ├── stage1_prompts.json        # JSON 快取
│   ├── stage2_prompts.json
│   ├── backups/                   # 自動備份
│   │   ├── stage1_prompts_20260209_143022.json
│   │   └── stage1_xxx_20260209_143022.py
│   └── drafts/                    # UI 草稿
│       └── stage1_20260209_150000.json
│
├── temp/
│   ├── versions/                  # 版本快照
│   │   └── 202512/
│   │       └── stage1/
│   │           ├── v20260209_143022.md
│   │           └── v20260209_150000.md
│   └── active_versions_202512.json  # 主要版本追蹤
│
├── .streamlit/
│   ├── config.toml                # Streamlit 配置
│   └── secrets.toml               # 密碼保護（可選）
│
├── start_ui.bat                   # 🟢 安全模式啟動
├── start_ui_network.bat           # 🟡 內網模式啟動
├── start_ui_public.bat            # 🔴 開放模式啟動
│
└── ui_app.py                      # Streamlit UI
    ├── ui_prompts()               # Prompt 編輯器
    ├── render_prompt_with_variables()  # 預覽功能
    ├── snapshot() / get_versions()     # 版本管理
    └── save_draft() / load_active()    # 草稿和活動版本
```

---

## 🎓 進階使用

### 添加自定義功能

**1. 支援更多變數類型**

在 `render_prompt_with_variables()` 中添加：

```python
# 支援日期範圍
rendered = rendered.replace("{{START_DATE}}", start_date)
rendered = rendered.replace("{{END_DATE}}", end_date)

# 支援配置變數
rendered = rendered.replace("{{MODEL_NAME}}", config.model)
```

**2. 添加 Prompt 模板**

創建常用 Prompt 模板庫：

```python
PROMPT_TEMPLATES = {
    "market_analysis": """分析 {{YEAR}}年{{MONTH}}月 的市場...""",
    "trend_summary": """總結趨勢...""",
}
```

**3. 批量操作**

添加批量更新所有 Stage 的功能：

```python
def batch_update_prompts(year, month):
    for stage in range(1, 8):
        # 批量替換變數
        # 批量寫回腳本
```

### 整合到 CI/CD

**1. 自動化測試**

```python
# tests/test_prompt_manager.py
def test_extract_prompts():
    pm = PromptManager()
    prompts = pm.extract_prompts_from_script("scripts/stage1.py")
    assert "PROMPT" in prompts
```

**2. Git Hooks**

```bash
# .git/hooks/pre-commit
# 自動備份 Prompt 變更
python -c "from utils.prompt_manager import PromptManager; pm = PromptManager(); pm.create_backup()"
```

---

## 🤝 貢獻和回饋

如果你使用這個規格並有改進建議：

1. **功能建議**：缺少哪些功能？
2. **Bug 報告**：哪裡不夠清楚？
3. **最佳實踐**：你的使用經驗？

**聯絡方式：**
- 在你的專案中創建 Issue
- 或直接修改 YAML 並分享改進版本

---

## 📄 授權

本規格文檔可自由使用於任何專案（商業或非商業）。

**建議：**
- 根據你的需求調整細節
- 保留核心設計原則
- 如有改進歡迎回饋

---

## 🎉 開始使用

1. **複製 `prompt_management_system_spec.yaml`**
2. **閱讀你的專案需求**
3. **準備給 AI 的 Prompt**
4. **呼叫 AI 生成代碼**
5. **測試和調整**
6. **開始使用！**

**祝你的 AI Workflow 專案順利！** 🚀

---

## ⭐ 共用程式碼架構（Preview Consistency Pattern）

### 核心理念

**問題**：在多階段 AI Workflow 中，常見的架構問題是：
- 實際執行：Stage 腳本有自己的資料格式化邏輯
- UI 預覽：UI 中重新實作相同的邏輯
- 結果：兩份代碼，容易不一致 ❌

**解決方案**：共用程式碼架構
```
實際執行 Stage 腳本 ──┐
                     ├──> 共用資料格式化模組 (utils/data_formatter.py)
UI 預覽功能 ────────┘
```

### 為什麼重要？

✅ **保證一致性**：預覽與實際執行使用完全相同的代碼
✅ **避免重複**：單一來源原則（Single Source of Truth）
✅ **易於維護**：修改邏輯只需要改一處
✅ **降低錯誤**：減少因複製貼上導致的不一致
✅ **易於測試**：只需測試共用函數一次

### 實作步驟

本規格已包含完整的 `shared_formatters` 章節，AI 會根據此章節：

**Step 1**：創建共用函數模組
```python
# utils/data_formatter.py

def load_data(excel_file, year, month):
    """
    從 Excel 讀取數據並格式化

    Used by:
        - scripts/stages/stage1_xxx.py
        - ui_app.py (generate_dynamic_variables)
    """
    # 格式化邏輯...
    return formatted_data
```

**Step 2**：Stage 腳本使用共用函數
```python
# scripts/stages/stage1_xxx.py
from utils.data_formatter import load_data  # ✅ 使用共用函數

def main(year, month):
    data = load_data(file, year, month)
```

**Step 3**：UI 預覽使用相同函數
```python
# ui_app.py
from utils.data_formatter import load_data  # ✅ 使用相同的共用函數

def generate_dynamic_variables(stage_num, year, month):
    if stage_num == 1:
        data = load_data(file, year, month)
        dynamic_vars["{{data}}"] = data
```

### 如何讓 AI 實作？

在給 AI 的 Prompt 中加入：

```markdown
我的專案需要確保 UI 預覽與實際執行完全一致。

請根據 YAML 規格中的 shared_formatters 章節：
1. 創建 utils/data_formatter.py 模組
2. 重構 Stage 腳本使用共用函數
3. 更新 UI 預覽邏輯使用相同函數

我的專案有以下資料格式化需求：
- Stage 1: 讀取 sales_data.csv 並格式化為表格
- Stage 3: 讀取 customer_info.xlsx 並轉為 JSON
- Stage 5: 從資料庫計算統計數據

請為每種需求創建對應的共用函數。
```

### 驗證一致性

AI 也會根據規格生成驗證方法：
- 直接比對輸出
- 單元測試
- 檢查 import 語句

詳見 YAML 規格中的 `shared_formatters.verification` 章節。

### 更多資訊

- 完整文檔：`README_SHARED_FORMATTERS.md`（本專案提供範例）
- YAML 規格：`shared_formatters` 章節

---

## 📚 相關資源

- **本專案範例**：台美 ETF 淨流量分析月報（參考實作）
- **Streamlit 文檔**：https://docs.streamlit.io
- **Streamlit Cloud**：https://share.streamlit.io
- **安全指南**：docs/SECURITY.md

---

**版本：v1.0 (2026-02-09)**
**基於：台美 ETF 淨流量分析月報專案的實踐經驗**
