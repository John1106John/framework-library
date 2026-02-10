# GitHub 架構庫設置指南

> 🗂️ 建立您的個人或團隊架構庫，讓架構可以在任何專案中快速存取

---

## 📖 什麼是架構庫？

架構庫是一個 GitHub repository，專門用來存放您的可重用架構規格。

**優勢：**
- ✅ 集中管理所有架構
- ✅ 版本控制和歷史記錄
- ✅ 團隊協作和分享
- ✅ 在任何專案中快速存取
- ✅ 使用 `/framework-integrator` 一鍵整合

---

## 🚀 快速設置（5 分鐘）

### 方法 1：使用模板建立（推薦）

#### 步驟 1：建立 GitHub Repository

```bash
# 1. 在 GitHub 上建立新 repository
Repository 名稱：framework-library
描述：My reusable framework specifications
公開/私人：根據需求選擇
```

#### 步驟 2：Clone 並設置結構

```bash
# Clone repository
git clone https://github.com/your-username/framework-library
cd framework-library

# 建立基本結構
mkdir -p frameworks
```

#### 步驟 3：建立架構索引檔案

創建 `FRAMEWORKS.json`：

```json
{
  "version": "1.0",
  "last_updated": "2026-02-10",
  "frameworks": []
}
```

#### 步驟 4：建立 README

創建 `README.md`：

```markdown
# Framework Library

> 我的可重用架構規格庫

## 📦 可用架構

目前有 0 個架構。

## 🔧 使用方式

### 方法 1：使用 Claude Code Skills

\```bash
cd your-project
/framework-integrator
# 選擇「從 GitHub 架構庫選擇」
\```

### 方法 2：手動下載

\```bash
# 下載架構
curl -O https://raw.githubusercontent.com/your-username/framework-library/main/frameworks/架構名稱/架構名稱_spec.yaml

# 整合到專案
/framework-integrator 架構名稱_spec.yaml
\```

## 📝 新增架構

使用 `/framework-architect` skill 建立規格後，選擇上傳到此 repository。
```

#### 步驟 5：提交並推送

```bash
git add .
git commit -m "Initial framework library setup"
git push origin main
```

**完成！🎉** 您的架構庫已經建立完成。

---

## 📁 完整目錄結構

架構庫的標準結構：

```
framework-library/
├── README.md                           # 架構庫說明
├── FRAMEWORKS.json                     # 架構索引（重要！）
│
├── frameworks/                         # 所有架構存放處
│   ├── api_config_framework/           # 架構 1
│   │   ├── api_config_framework_spec.yaml
│   │   ├── AI_INTEGRATION_PROMPT.md
│   │   ├── README.md
│   │   ├── templates/                  # 模板檔案
│   │   │   ├── config.yaml.template
│   │   │   ├── config_loader.py.template
│   │   │   └── api_manager.py.template
│   │   └── examples/                   # 範例程式碼（可選）
│   │       └── integration_example.py
│   │
│   ├── prompt_management_framework/    # 架構 2
│   │   ├── prompt_management_system_spec.yaml
│   │   ├── AI_INTEGRATION_PROMPT.md
│   │   ├── README.md
│   │   └── templates/
│   │       └── ...
│   │
│   └── data_validation_framework/      # 架構 3
│       └── ...
│
└── .github/                            # GitHub 配置（可選）
    └── workflows/
        └── validate-frameworks.yml     # 自動驗證（進階）
```

---

## 📋 FRAMEWORKS.json 格式

這是最重要的檔案，`/framework-integrator` 依賴它來列出所有架構。

### 完整範例

```json
{
  "version": "1.0",
  "last_updated": "2026-02-10",
  "repository": {
    "name": "framework-library",
    "owner": "your-username",
    "url": "https://github.com/your-username/framework-library",
    "description": "可重用的架構規格庫"
  },
  "frameworks": [
    {
      "id": "api-config-framework",
      "name": "API 設定與金鑰管理框架",
      "version": "1.0.0",
      "description": "集中式 API 設定與自動循環金鑰輪替系統",
      "author": "your-username",
      "created_at": "2026-02-10",
      "updated_at": "2026-02-10",
      "tech_stack": ["Python 3.10+", "pyyaml", "python-dotenv"],
      "tags": ["api-management", "key-rotation", "config", "yaml"],
      "path": "frameworks/api_config_framework",
      "files": {
        "spec": "api_config_framework_spec.yaml",
        "readme": "README.md",
        "integration_prompt": "AI_INTEGRATION_PROMPT.md"
      },
      "has_templates": true,
      "has_examples": true,
      "download_url": "https://github.com/your-username/framework-library/tree/main/frameworks/api_config_framework",
      "raw_spec_url": "https://raw.githubusercontent.com/your-username/framework-library/main/frameworks/api_config_framework/api_config_framework_spec.yaml"
    },
    {
      "id": "prompt-management",
      "name": "Prompt 管理系統",
      "version": "1.0.0",
      "description": "AI Workflow 的 Prompt 版本管理系統",
      "author": "your-username",
      "created_at": "2026-02-09",
      "updated_at": "2026-02-09",
      "tech_stack": ["Python 3.10+", "Streamlit", "json"],
      "tags": ["prompt-management", "version-control", "ui", "streamlit"],
      "path": "frameworks/prompt_management_framework",
      "files": {
        "spec": "prompt_management_system_spec.yaml",
        "readme": "README.md",
        "integration_prompt": "AI_INTEGRATION_PROMPT.md"
      },
      "has_templates": true,
      "has_examples": false,
      "download_url": "https://github.com/your-username/framework-library/tree/main/frameworks/prompt_management_framework",
      "raw_spec_url": "https://raw.githubusercontent.com/your-username/framework-library/main/frameworks/prompt_management_framework/prompt_management_system_spec.yaml"
    }
  ]
}
```

### 欄位說明

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `id` | string | ✅ | 唯一識別碼（kebab-case） |
| `name` | string | ✅ | 架構名稱（顯示用） |
| `version` | string | ✅ | 版本號（語義化版本） |
| `description` | string | ✅ | 簡短描述（1-2 句話） |
| `author` | string | ✅ | 作者（GitHub username） |
| `created_at` | string | ✅ | 建立日期（YYYY-MM-DD） |
| `updated_at` | string | ✅ | 更新日期（YYYY-MM-DD） |
| `tech_stack` | array | ✅ | 技術棧列表 |
| `tags` | array | ✅ | 標籤（用於搜尋） |
| `path` | string | ✅ | 架構在 repo 中的路徑 |
| `files` | object | ✅ | 檔案路徑（相對於 path） |
| `has_templates` | boolean | ⭕ | 是否包含模板檔案 |
| `has_examples` | boolean | ⭕ | 是否包含範例程式碼 |
| `download_url` | string | ⭕ | GitHub 頁面 URL |
| `raw_spec_url` | string | ⭕ | 規格檔案的 raw URL |

---

## 🔄 新增架構到架構庫

### 方法 1：使用 framework-architect 自動上傳（推薦）

```bash
# 1. 在開發專案中設計架構
cd /path/to/your-project
/framework-architect

# 2. 回答 16 個問題...

# 3. 選擇上傳到 GitHub
# → AI 會自動：
#    - 複製架構檔案到 framework-library
#    - 更新 FRAMEWORKS.json
#    - 建立 commit 和 push
#    - 可選建立 PR
```

### 方法 2：手動新增

#### 步驟 1：準備架構檔案

```bash
cd framework-library

# 建立架構目錄
mkdir -p frameworks/my_new_framework
cd frameworks/my_new_framework

# 複製架構檔案
cp /path/to/source/my_new_framework_spec.yaml .
cp /path/to/source/AI_INTEGRATION_PROMPT.md .
cp /path/to/source/README.md .

# 如果有模板
mkdir templates
cp /path/to/source/templates/* templates/
```

#### 步驟 2：更新 FRAMEWORKS.json

```bash
cd ../..  # 回到 framework-library 根目錄
```

編輯 `FRAMEWORKS.json`，在 `frameworks` 陣列中新增：

```json
{
  "id": "my-new-framework",
  "name": "My New Framework",
  "version": "1.0.0",
  "description": "簡短描述",
  "author": "your-username",
  "created_at": "2026-02-10",
  "updated_at": "2026-02-10",
  "tech_stack": ["Python 3.10+"],
  "tags": ["tag1", "tag2"],
  "path": "frameworks/my_new_framework",
  "files": {
    "spec": "my_new_framework_spec.yaml",
    "readme": "README.md",
    "integration_prompt": "AI_INTEGRATION_PROMPT.md"
  },
  "has_templates": true,
  "has_examples": false,
  "download_url": "https://github.com/your-username/framework-library/tree/main/frameworks/my_new_framework",
  "raw_spec_url": "https://raw.githubusercontent.com/your-username/framework-library/main/frameworks/my_new_framework/my_new_framework_spec.yaml"
}
```

#### 步驟 3：提交到 GitHub

```bash
git add .
git commit -m "Add my new framework v1.0.0"
git push origin main
```

---

## 🔍 使用架構庫

### 從任何專案中存取

```bash
cd /path/to/any-project

# 啟動 framework-integrator
/framework-integrator

# 選擇「從 GitHub 架構庫選擇」
# → 會自動讀取您的架構庫
# → 列出所有可用架構
# → 選擇後自動下載並整合
```

### 設定架構庫 URL

第一次使用時，會詢問架構庫 URL：

```
⚙️ GitHub 架構庫設定

請輸入您的 GitHub 架構庫 URL：
預設：https://github.com/{username}/framework-library

您的 URL：
```

URL 會儲存在 `~/.claude/framework_library.yaml`：

```yaml
github_url: https://github.com/your-username/framework-library
last_accessed: 2026-02-10
cache_enabled: true
```

### 使用公開架構庫

也可以使用他人的公開架構庫：

```bash
/framework-integrator --github-url https://github.com/someone/their-framework-library
```

---

## 🎯 最佳實踐

### 1. 命名規範

**架構 ID（kebab-case）：**
- ✅ `api-config-framework`
- ✅ `prompt-management-system`
- ❌ `API_Config_Framework`
- ❌ `promptManagementSystem`

**目錄名稱：**
- ✅ `api_config_framework`
- ✅ `prompt_management_framework`
- ❌ `API-Config`
- ❌ `framework1`

### 2. 版本管理

使用[語義化版本](https://semver.org/lang/zh-TW/)：

- **Major (1.0.0)**: 不向後相容的變更
- **Minor (1.1.0)**: 新增功能，向後相容
- **Patch (1.1.1)**: Bug 修復，向後相容

**範例：**
```json
{
  "version": "1.2.3",
  "changelog": {
    "1.2.3": "修復設定檔讀取錯誤",
    "1.2.0": "新增自動重試機制",
    "1.0.0": "初始版本"
  }
}
```

### 3. 標籤系統

使用清楚、一致的標籤：

**類別標籤：**
- `api-management` - API 管理
- `data-processing` - 資料處理
- `ui-framework` - UI 框架
- `authentication` - 認證授權

**技術標籤：**
- `python` - Python 專用
- `javascript` - JavaScript 專用
- `cross-platform` - 跨平台

**功能標籤：**
- `config` - 設定管理
- `logging` - 日誌系統
- `version-control` - 版本控制

### 4. 文檔品質

每個架構必須包含：
- ✅ `README.md` - 完整使用文檔
- ✅ `*_spec.yaml` - 給 AI 的系統規格
- ✅ `AI_INTEGRATION_PROMPT.md` - 整合指令
- ✅ `templates/` - 模板檔案（如果需要）
- ⭕ `examples/` - 範例程式碼（建議有）

### 5. 定期維護

**每個月：**
- 檢查過時的架構
- 更新相依套件版本
- 回應使用者回饋

**每個季度：**
- 審查所有架構
- 移除不再維護的架構
- 整理標籤系統

---

## 🔐 私人架構庫

### 使用私人 Repository

```bash
# 1. 建立私人 repository
# 2. 設定 GitHub Personal Access Token (PAT)
# 3. 在 ~/.claude/framework_library.yaml 中設定

github_url: https://github.com/your-username/private-framework-library
access_token: ghp_xxxxxxxxxxxx  # 您的 PAT
```

### 團隊協作

**Organization Repository：**
```
https://github.com/your-org/framework-library
```

**分支策略：**
- `main` - 穩定版本
- `dev` - 開發版本
- `feature/架構名稱` - 新架構開發

**PR 審核流程：**
1. 建立新架構在 feature branch
2. 建立 PR 到 dev
3. 團隊審核
4. Merge 到 main

---

## 📊 範例架構庫

### 公開範例

本專案提供兩個架構作為起點：

**1. API 設定與金鑰管理框架**
```
frameworks/api_config_framework/
├── api_config_framework_spec.yaml
├── AI_INTEGRATION_PROMPT.md
├── README.md
└── templates/
    ├── config.yaml.template
    ├── config_loader.py.template
    ├── api_manager.py.template
    └── .env.example
```

**2. Prompt 管理系統**
```
frameworks/prompt_management_framework/
├── prompt_management_system_spec.yaml
├── AI_INTEGRATION_PROMPT.md
└── README.md
```

### 建立您的架構庫

```bash
# 1. Fork 或複製本專案的架構
git clone https://github.com/your-username/etfflow_article
cd etfflow_article

# 2. 建立您的架構庫 repository
cd ..
mkdir framework-library
cd framework-library
git init

# 3. 複製架構
cp -r ../etfflow_article/api_config_framework frameworks/
cp -r ../etfflow_article/prompt_management_spec frameworks/prompt_management_framework

# 4. 建立索引
# （使用上面的 FRAMEWORKS.json 範例）

# 5. 推送到 GitHub
git add .
git commit -m "Initial commit with 2 frameworks"
git remote add origin https://github.com/your-username/framework-library
git push -u origin main
```

---

## ❓ 常見問題

### Q1: 架構庫必須是公開的嗎？

**A:** 不一定。

- **公開 repo**: 任何人都能存取（適合開源專案）
- **私人 repo**: 需要 GitHub token（適合企業內部）

### Q2: 可以使用他人的架構庫嗎？

**A:** 可以！

```bash
/framework-integrator --github-url https://github.com/someone/framework-library
```

### Q3: 如何更新架構？

**A:** 兩種方式：

**方式 1（自動）:**
```bash
cd framework-library
# 修改架構檔案
# 更新 FRAMEWORKS.json 中的 version 和 updated_at
git add .
git commit -m "Update framework to v1.1.0"
git push
```

**方式 2（使用 framework-architect）:**
```bash
# 重新執行 /framework-architect
# 選擇覆蓋現有架構
# 選擇上傳到 GitHub
```

### Q4: FRAMEWORKS.json 必須手動維護嗎？

**A:** 不一定。

- 使用 `/framework-architect` 會自動更新
- 手動新增時需要手動編輯
- 可以寫腳本自動產生（進階）

### Q5: 可以有多個架構庫嗎？

**A:** 可以！

```yaml
# ~/.claude/framework_library.yaml
libraries:
  - name: personal
    url: https://github.com/user/framework-library
  - name: work
    url: https://github.com/company/framework-library
  - name: public
    url: https://github.com/community/framework-library

default: personal
```

---

## 🎉 開始建立您的架構庫

### 檢查清單

- [ ] 在 GitHub 建立 repository
- [ ] 建立基本目錄結構
- [ ] 建立 FRAMEWORKS.json
- [ ] 建立 README.md
- [ ] 複製第一個架構
- [ ] 更新 FRAMEWORKS.json
- [ ] 提交並推送
- [ ] 使用 `/framework-integrator` 測試

### 下一步

1. **新增更多架構**: 使用 `/framework-architect`
2. **分享架構**: 邀請團隊成員協作
3. **持續改進**: 收集回饋並更新

---

**版本:** 1.0
**最後更新:** 2026-02-10
**相關文件:**
- [SKILLS_GUIDE.md](SKILLS_GUIDE.md) - Skills 使用指南
- [framework-architect.md](~/.claude/skills/framework-architect.md) - 架構設計 skill
- [framework-integrator.md](~/.claude/skills/framework-integrator.md) - 架構整合 skill
