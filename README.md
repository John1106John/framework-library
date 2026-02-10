# Framework Library

> 🗂️ 可重用的架構規格庫，讓架構在任何專案中快速存取和整合

## 📦 可用架構

目前有 **2** 個架構：

### 1. 📦 API 設定與金鑰管理框架

**版本：** v1.0.0
**技術棧：** Python 3.10+, pyyaml, python-dotenv
**標籤：** `api-management` `key-rotation` `config` `yaml`

**核心功能：**
- ✅ 集中式 config.yaml 管理（一鍵切換模型）
- ✅ API 金鑰自動循環輪替
- ✅ 配額智慧檢測與切換
- ✅ 詳細日誌追蹤

**連結：**
- [📋 規格文檔](frameworks/api_config_framework/api_config_framework_spec.yaml)
- [📖 使用說明](frameworks/api_config_framework/README.md)
- [🔧 整合指令](frameworks/api_config_framework/AI_INTEGRATION_PROMPT.md)

---

### 2. 📝 Prompt 管理系統

**版本：** v1.0.0
**技術棧：** Python 3.10+, Streamlit, json
**標籤：** `prompt-management` `version-control` `ui` `streamlit`

**核心功能：**
- ✅ 從 Python 腳本提取/更新 Prompt
- ✅ Streamlit UI 視覺化編輯
- ✅ 版本管理與快照
- ✅ 草稿系統（暫存修改）
- ✅ 預覽功能（變數替換）

**連結：**
- [📋 規格文檔](frameworks/prompt_management_framework/prompt_management_system_spec.yaml)
- [📖 使用說明](frameworks/prompt_management_framework/README_PROMPT_SPEC.md)

---

## 🔧 使用方式

### 方法 1：使用 Claude Code Skills（推薦）⭐

```bash
cd your-project

# 啟動架構整合工具
/framework-integrator

# 選擇「從 GitHub 架構庫選擇」
# → 自動列出所有可用架構
# → 選擇要整合的架構
# → 自動下載並整合
```

### 方法 2：手動下載

```bash
# 下載整個架構目錄
git clone https://github.com/John1106John/framework-library
cd framework-library/frameworks

# 複製到您的專案
cp -r api_config_framework /path/to/your-project/

# 使用整合工具
cd /path/to/your-project
/framework-integrator api_config_framework/api_config_framework_spec.yaml
```

### 方法 3：直接使用規格文檔

```bash
# 下載規格檔案
curl -O https://raw.githubusercontent.com/John1106John/framework-library/main/frameworks/api_config_framework/api_config_framework_spec.yaml

# 將規格提供給 AI（Claude、ChatGPT 等）
# AI 會根據規格自動產生整合代碼
```

---

## 📝 新增架構

### 使用 framework-architect skill（推薦）

```bash
cd your-project

# 設計架構規格
/framework-architect

# 回答 16 個引導問題...

# 完成後選擇：上傳到 GitHub
# → 自動推送到此 repository
# → 自動更新 FRAMEWORKS.json
```

### 手動新增

1. **準備架構檔案**
   ```bash
   cd framework-library/frameworks
   mkdir my_new_framework
   cd my_new_framework

   # 複製您的規格檔案
   cp /path/to/spec.yaml .
   cp /path/to/README.md .
   cp /path/to/AI_INTEGRATION_PROMPT.md .
   ```

2. **更新 FRAMEWORKS.json**
   - 在 `frameworks` 陣列中新增架構資訊
   - 參考現有架構的格式

3. **提交並推送**
   ```bash
   git add .
   git commit -m "Add new framework"
   git push
   ```

---

## 🔍 搜尋架構

### 按標籤搜尋

- **API 相關：** `api-management`, `key-rotation`, `api-gateway`
- **UI 相關：** `ui`, `streamlit`, `web-interface`
- **資料處理：** `data-processing`, `data-validation`, `etl`
- **設定管理：** `config`, `configuration`, `settings`
- **版本控制：** `version-control`, `versioning`, `git`

### 按技術棧搜尋

- **Python：** Python 3.10+
- **Web 框架：** Streamlit, Flask, FastAPI
- **資料處理：** pandas, numpy, pydantic
- **API：** requests, aiohttp

---

## 📚 相關資源

### 📖 完整文檔

- **[Skills 使用指南](SKILLS_GUIDE.md)** - framework-architect 和 framework-integrator 的完整使用教學
  - 🚀 完整工作流程（GitHub + 本地）
  - 💡 實用技巧和最佳實踐
  - 📋 範例和常見問題

- **[架構庫設置指南](FRAMEWORK_LIBRARY_SETUP.md)** - 如何建立和管理 GitHub 架構庫
  - 🏗️ 目錄結構規範
  - 📝 FRAMEWORKS.json 格式
  - ✅ 標準化檢查清單

- **[格式驗證工具](validate_framework.py)** - 自動驗證架構格式
  ```bash
  python validate_framework.py  # 驗證所有架構
  ```

- [Claude Code Skills 官方文檔](https://github.com/anthropics/claude-code)

### Skills

- **framework-architect** - 設計架構規格
- **framework-integrator** - 自動整合架構

安裝位置：`~/.claude/skills/`

---

## 🤝 貢獻

歡迎貢獻新的架構！

1. Fork 此 repository
2. 建立新架構
3. 更新 FRAMEWORKS.json
4. 提交 Pull Request

---

## 📄 授權

MIT License - 自由使用、修改、分發

---

## 📊 統計

- **架構總數：** 2
- **技術棧：** Python, Streamlit, pyyaml, python-dotenv
- **最後更新：** 2026-02-10

---

**🎯 開始使用：只需 `/framework-integrator` 即可快速整合任何架構！**
