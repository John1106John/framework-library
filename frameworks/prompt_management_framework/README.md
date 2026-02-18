# Prompt Management System 規格模板

> 🎯 **可重用的系統規格，讓 AI 為任何專案快速建立 Prompt 管理系統**

## 📦 內容

本資料夾包含一套完整的 Prompt 管理系統設計規格：

### 1. **prompt_management_system_spec.yaml**
- 📄 **類型**：系統設計規格（YAML 格式）
- 🎯 **用途**：給 AI（Claude、GPT、Gemini）的完整規格
- 📊 **大小**：~34 KB
- 🔖 **版本**：v1.5.0 (2026-02-19)

**包含內容：**
- 系統架構設計
- PromptManager 類別完整實作規格
- Baseline 基準版本管理（儲存、比較、還原）
- 草稿管理（暫存、載入、刪除）
- Streamlit UI 設計模式（含 Baseline 比較 UI）
- 版本管理機制
- Prompt 預覽功能
- Stage 間依賴統一讀取機制（stage_io）
- 輸入驗證（check_inputs pre-flight check）
- 安全啟動配置（三種模式）
- 已知問題和解決方案
- AI 實作指引
- 快速開始範例
- FAQ

### 2. **README_PROMPT_SPEC.md**
- 📖 **類型**：使用指南（Markdown 格式）
- 🎯 **用途**：給開發者的完整使用說明
- 📊 **大小**：~14 KB

**包含內容：**
- 如何使用這個規格
- 給 AI 的 Prompt 範本
- 4 步驟使用流程
- 實用範例（報告生成專案）
- 常見問題解答
- 安全注意事項
- 進階使用指南

---

## 🚀 快速使用

### 步驟 1：閱讀使用指南

```bash
# 先閱讀這個文件
cat README_PROMPT_SPEC.md
```

### 步驟 2：準備給 AI 的 Prompt

複製整個 YAML 文件內容：

```bash
# 複製規格文件
cat prompt_management_system_spec.yaml
```

### 步驟 3：呼叫 AI

將你的專案描述 + YAML 規格一起提供給 Claude/GPT/Gemini。

**範例 Prompt：**
```markdown
我想為我的 AI Workflow 專案建立 Prompt 管理系統。

我的專案有 3 個階段：
- Stage 1: XXX
- Stage 2: YYY
- Stage 3: ZZZ

請根據以下規格為我建立系統：
[貼上 YAML 內容]
```

---

## 📚 文件關係

```
prompt_management_spec/
├── README.md                              ← 你在這裡（索引）
├── README_PROMPT_SPEC.md                  ← 使用指南（給開發者）
└── prompt_management_system_spec.yaml     ← 系統規格（給 AI）
```

**閱讀順序：**
1. README.md（本文件）- 快速了解
2. README_PROMPT_SPEC.md - 詳細使用說明
3. prompt_management_system_spec.yaml - 查看規格細節

---

## 🎯 適用場景

**✅ 適合使用這個規格的專案：**
- 多階段 AI Workflow（報告生成、內容分析、數據處理）
- 需要頻繁調整 Prompt 的專案
- 需要版本管理和 A/B 測試的場景
- 團隊協作的 AI 專案

**❌ 不適合的場景：**
- 只有 1-2 個簡單 Prompt 的小專案
- Prompt 很少修改的靜態專案
- 不需要 UI 的純命令行工具

---

## 🌟 核心特色

### 📋 完整性
- 從架構設計到實作細節
- 包含代碼範例和 regex 模式
- 涵蓋已知問題和解決方案

### 🎨 實用性
- 基於真實專案驗證
- 可直接作為 AI prompt 使用
- 包含快速開始範例

### 🔐 安全第一
- 三種安全啟動模式
- 詳細的安全說明
- 遠端訪問替代方案

### 📌 Baseline 管理
- Baseline 基準版本（穩定參考點）
- 與目前腳本即時差異比較
- 一鍵還原到 Baseline 版本
- Baseline 不可刪除，僅能覆蓋更新
- 草稿記錄中置頂顯示 Baseline

### 🚀 易於使用
- 清晰的使用步驟
- 複製即用的 Prompt 範本
- 豐富的範例和 FAQ

---

## 🎁 AI 會為你生成

按照這個規格，AI 會生成：

```
project/
├── utils/
│   ├── prompt_manager.py          # PromptManager 類別
│   └── stage_io.py                # Stage 間統一讀取模組
├── prompts/
│   ├── *.json                     # JSON 快取
│   ├── baselines/                 # Baseline 基準版本（不可刪除）
│   ├── backups/                   # 自動備份
│   └── drafts/                    # 草稿（可刪除）
├── temp/
│   └── versions/                  # 版本快照
├── .streamlit/
│   └── config.toml                # 安全配置
├── start_ui.bat                   # 🟢 安全模式
├── start_ui_network.bat           # 🟡 內網模式
├── start_ui_public.bat            # 🔴 開放模式
└── ui_app.py                      # Streamlit UI
```

---

## 📖 相關資源

### 本專案（參考實作）
- **專案**：台美 ETF 淨流量分析月報
- **位置**：專案根目錄
- **說明**：完整的實作範例，可參考學習

### 外部資源
- **Streamlit 文檔**：https://docs.streamlit.io
- **Streamlit Cloud**：https://share.streamlit.io

---

## 💡 使用建議

### 給其他開發者

如果你想分享這個規格：

```bash
# 1. 複製整個資料夾
cp -r prompt_management_spec /path/to/new/project/

# 2. 閱讀 README_PROMPT_SPEC.md
# 3. 準備專案描述
# 4. 呼叫 AI 生成代碼
```

### 給自己的其他專案

```bash
# 直接參考這個資料夾
# YAML 規格可重複使用
# 只需要調整專案描述部分
```

---

## 🤝 貢獻

如果你使用後有改進建議：
- 新增功能需求
- 修正錯誤
- 改進文檔

歡迎回饋和分享你的改進版本！

---

## 📄 授權

本規格文檔可自由使用於任何專案（商業或非商業）。

---

## 🎉 開始使用

1. 閱讀 **README_PROMPT_SPEC.md**
2. 準備你的專案描述
3. 複製 **prompt_management_system_spec.yaml**
4. 呼叫 AI 生成代碼
5. 開始使用！

**祝你的 AI Workflow 專案順利！** 🚀

---

**版本：v1.5.0 (2026-02-19)**
**來源：台美 ETF 淨流量分析月報專案**
