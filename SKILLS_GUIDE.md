# Claude Code Skills 使用指南

> 🛠️ 本專案已配置三個自訂 skills，用於架構設計、管理與整合

---

## 📦 已安裝的 Skills

### 1. framework-architect - 架構設計規格產生器

**用途：** 為您的架構/系統設計完整的 AI 導入規格

**安裝位置：** `~/.claude/skills/framework-architect.md`

**呼叫方式：**
```bash
/framework-architect
```

**功能：**
- 透過 16 個引導問題收集架構資訊
- 自動產生三個完整文檔：
  - `{架構名稱}_spec.yaml` - 給 AI 的系統規格
  - `AI_INTEGRATION_PROMPT.md` - 可直接複製的整合指令
  - `README.md` - 給人類閱讀的完整文檔

**使用場景：**
- ✅ 開發了可重用的架構，想要文檔化
- ✅ 希望讓 AI 理解並幫您整合到其他專案
- ✅ 需要標準化的架構規格文檔

**範例輸出：** 參考本專案的 `frameworks/api_config_framework/` 和 `frameworks/prompt_management_framework/`

---

### 2. framework-manager - 架構庫管理工具

**用途：** 管理 GitHub 架構庫：編輯、同步、驗證、刪除架構規格

**安裝位置：** `~/.claude/skills/framework-manager.md`

**呼叫方式：**
```bash
# 互動式主選單
/framework-manager

# 快捷用法
/framework-manager edit              # 直接進入編輯模式
/framework-manager sync              # 直接同步 GitHub
/framework-manager validate          # 直接驗證格式
/framework-manager status            # 直接查看狀態
/framework-manager edit prompt-management  # 編輯特定架構
```

**功能：**
- 📋 列出所有架構及其狀態
- ✏️ 編輯現有架構的規格、文檔或整合指令
- 🔄 同步 GitHub（Pull / Push / Clone）
- ✅ 驗證架構格式是否符合標準
- 🗑️ 刪除架構
- 📊 查看本地與遠端的差異
- ⚙️ 管理設定（路徑、URL、分支）

**使用場景：**
- ✅ 想編輯架構庫中已有的架構規格
- ✅ 需要將本地修改推送到 GitHub
- ✅ 想從 GitHub 拉取最新版本到本地
- ✅ 需要驗證架構格式

**與其他 Skills 的關係：**
```
/framework-architect  ──建立──→  架構規格
                                    ↓
/framework-manager   ──管理──→  架構庫（GitHub）
                                    ↓
/framework-integrator ──下載──→  整合到專案
```

---

### 3. framework-integrator - 架構自動整合工具

**用途：** 自動讀取架構規格並整合到當前專案

**安裝位置：** `~/.claude/skills/framework-integrator.md`

**呼叫方式：**
```bash
# 方法 1：自動掃描
/framework-integrator

# 方法 2：指定規格檔案
/framework-integrator path/to/spec.yaml

# 方法 3：乾跑模式（只預覽）
/framework-integrator --dry-run
```

**功能：**
- 自動掃描並讀取 `*_spec.yaml` 規格文檔
- 分析當前專案結構
- 執行完整整合流程：
  - 複製模板檔案
  - 修改設定檔
  - 掃描並更新程式碼
  - 建立環境檔案
  - 產生測試腳本
- 驗證整合結果
- 產生詳細報告

**使用場景：**
- ✅ 想將現成的架構快速整合到專案
- ✅ 希望自動化整合過程
- ✅ 需要完整的整合報告和驗證

---

## 🚀 完整工作流程

### 場景 1：設計新架構並上傳到 GitHub（推薦）⭐

#### 步驟 0：（可選）先查看架構庫狀態

```bash
/framework-manager status
# 了解當前架構庫有哪些架構
```

#### 步驟 1：在源專案中設計架構規格

```bash
# 在開發架構的專案中
cd /path/to/source_project

# 呼叫 framework-architect
/framework-architect
```

回答 16 個問題後，產生：
```
source_project/
└── my_awesome_framework/
    ├── my_awesome_framework_spec.yaml
    ├── AI_INTEGRATION_PROMPT.md
    └── README.md
```

#### 步驟 2：上傳到 GitHub 架構庫

在 `/framework-architect` 完成後：
```
是否要將此架構上傳到 GitHub 架構庫？
1. 上傳到 GitHub（推薦）← 選這個
2. 僅保存在本地
3. 稍後手動上傳

您的選擇：1
```

AI 會自動：
- 複製架構到 GitHub repository
- 更新 FRAMEWORKS.json 索引
- 建立 commit 和 push
- 提供 GitHub URL

#### 步驟 3：在任何專案中快速整合

```bash
cd /path/to/any_project

# 啟動整合工具
/framework-integrator

# 選擇來源
1. 📦 從 GitHub 架構庫選擇（推薦）← 選這個
2. 📁 從本地專案掃描
3. 📄 指定本地檔案路徑

您的選擇：1
```

AI 會：
1. 連接 GitHub 架構庫
2. 顯示所有可用架構（包含您剛上傳的）
3. 讓您選擇要整合的架構
4. 自動下載並整合
5. 產生報告

**優勢：**
- ✅ 在任何專案中都能存取
- ✅ 自動下載最新版本
- ✅ 支援搜尋和標籤篩選
- ✅ 團隊成員可以共用

---

### 場景 1.5：編輯已有的架構

```bash
# 使用 framework-manager 編輯架構
/framework-manager edit

# 或直接指定架構
/framework-manager edit prompt-management

# 流程：
# 1. 選擇架構 → 選擇檔案
# 2. AI 讀取並顯示結構摘要
# 3. 描述修改 → AI 執行修改
# 4. 確認 → 自動驗證 → 推送到 GitHub
```

---

### 場景 2：本地開發和測試（不上傳 GitHub）

#### 步驟 1：設計架構規格

```bash
cd /path/to/source_project
/framework-architect
```

#### 步驟 2：選擇僅保存在本地

```
是否要將此架構上傳到 GitHub 架構庫？
1. 上傳到 GitHub（推薦）
2. 僅保存在本地 ← 選這個
3. 稍後手動上傳

您的選擇：2
```

#### 步驟 3：複製到目標專案並整合

```bash
# 方法 1：複製後自動掃描
cp -r source_project/my_awesome_framework target_project/
cd target_project
/framework-integrator
# 選擇「從本地專案掃描」

# 方法 2：直接指定路徑
cd target_project
/framework-integrator ../source_project/my_awesome_framework/my_awesome_framework_spec.yaml
```

---

### 場景 3：使用本架構庫中的框架

本架構庫包含兩個完整的架構規格：

#### 3.1 API 設定與金鑰管理框架

**位置：** `frameworks/api_config_framework/`

**快速整合到新專案：**

```bash
# 推薦：使用 framework-integrator 從 GitHub 直接下載
cd /path/to/new_project
/framework-integrator --github api-config-framework
```

**核心功能：**
- ✅ 集中式 config.yaml 管理（一鍵切換模型）
- ✅ API 金鑰自動循環輪替
- ✅ 配額智慧檢測與切換
- ✅ 詳細日誌追蹤

#### 3.2 Prompt 管理系統

**位置：** `frameworks/prompt_management_framework/`

**快速整合到新專案：**

```bash
cd /path/to/new_project
/framework-integrator --github prompt-management
```

**核心功能：**
- ✅ 從 Python 腳本提取/更新 Prompt
- ✅ Streamlit UI 視覺化編輯
- ✅ 版本管理與快照
- ✅ 草稿系統（暫存修改）
- ✅ 預覽功能（變數替換）
- ✅ 共用程式碼架構（預覽與執行一致）

---

## 💡 實用技巧

### 技巧 1：快速查看 Skill 說明

```bash
# 查看 skill 的完整文檔
cat ~/.claude/skills/framework-architect.md
cat ~/.claude/skills/framework-manager.md
cat ~/.claude/skills/framework-integrator.md
```

### 技巧 2：列出所有可用的 Skills

```bash
ls -la ~/.claude/skills/
```

### 技巧 3：在任何專案中使用

因為 skills 安裝在 `~/.claude/skills/`，所以在**任何專案**中都可以直接呼叫：

```bash
cd /path/to/any_project
/framework-architect    # ✅ 可用
/framework-manager      # ✅ 可用
/framework-integrator   # ✅ 可用
```

### 技巧 4：建立專案模板

```bash
# 1. 設計架構
cd template_project
/framework-architect

# 2. 產生規格
# → template_project/my_template_framework/

# 3. 在新專案中使用
cd new_project
/framework-integrator --github my-template
```

---

## 📚 學習資源

### 範例 1：API 設定框架

查看完整實作範例：
- **規格文檔：** `frameworks/api_config_framework/api_config_framework_spec.yaml`
- **整合指令：** `frameworks/api_config_framework/AI_INTEGRATION_PROMPT.md`
- **使用文檔：** `frameworks/api_config_framework/README.md`
- **程式碼範例：** `frameworks/api_config_framework/examples/integration_example.py`

### 範例 2：Prompt 管理系統

查看完整實作範例：
- **規格文檔：** `frameworks/prompt_management_framework/prompt_management_system_spec.yaml`
- **整合指令：** `frameworks/prompt_management_framework/AI_INTEGRATION_PROMPT.md`
- **使用指南：** `frameworks/prompt_management_framework/README.md`

---

## 🔧 自訂與擴展

### 修改 Skills

Skills 位於：`~/.claude/skills/`

可以直接編輯：
```bash
# Windows
notepad ~/.claude/skills/framework-architect.md

# Linux/Mac
vim ~/.claude/skills/framework-architect.md
```

### 新增自己的 Skills

1. 在 `~/.claude/skills/` 目錄建立新的 `.md` 檔案
2. 使用 Markdown 格式撰寫 skill 說明
3. 定義 skill 的行為和互動流程
4. 儲存後即可使用 `/your-skill-name` 呼叫

**參考：** 查看現有 skills 的格式

---

## ❓ 常見問題

### Q1：Skills 是全域的還是專案特定的？

**A：** 全域的。

Skills 安裝在 `~/.claude/skills/`，所以在**任何專案**中都可以使用。這樣設計的好處：
- ✅ 一次安裝，到處使用
- ✅ 不需要每個專案都複製一份
- ✅ 更新 skill 會自動套用到所有專案

### Q2：如何更新 Skills？

**A：** 直接修改 `~/.claude/skills/` 中的檔案：

```bash
# 編輯 skill
vim ~/.claude/skills/framework-architect.md

# 或重新產生
# （如果有新版本的 skill 定義）
```

### Q3：可以分享 Skills 給其他人嗎？

**A：** 可以！

```bash
# 匯出 skill
cp ~/.claude/skills/framework-architect.md /path/to/share/

# 其他人安裝
cp framework-architect.md ~/.claude/skills/
```

### Q4：Skills 與專案中的規格文檔有什麼關係？

**A：** 分工不同：

- **Skills（在 ~/.claude/skills/）**：工具，定義「如何」操作
  - `framework-architect`：如何設計規格
  - `framework-manager`：如何管理架構庫
  - `framework-integrator`：如何整合架構

- **規格文檔（在架構庫中）**：內容，描述「什麼」架構
  - `api_config_framework_spec.yaml`：API 框架的內容
  - `prompt_management_system_spec.yaml`：Prompt 系統的內容

**比喻：**
- Skills = 工具（錘子、螺絲起子）
- 規格文檔 = 材料（木頭、螺絲）

### Q5：如何在沒有這些 Skills 的環境中使用規格文檔？

**A：** 規格文檔是獨立的！

即使沒有安裝 skills，仍然可以：
1. **直接給 AI：** 將 `*_spec.yaml` 內容複製給 Claude/ChatGPT
2. **使用整合指令：** 複製 `AI_INTEGRATION_PROMPT.md` 中的指令
3. **手動整合：** 閱讀 `README.md` 按步驟操作

Skills 只是讓流程更自動化、更方便。

---

## 🎯 最佳實踐

### 1. 架構開發流程

```
1. 在專案中開發架構
   ↓
2. 使用 /framework-architect 建立規格並上傳 GitHub
   ↓
3. 使用 /framework-manager 管理和編輯架構庫
   ↓
4. 其他專案使用 /framework-integrator 從 GitHub 下載並整合
```

### 2. 版本管理

規格文檔應該包含版本號：
```yaml
# 在 spec.yaml 中
version: "1.0.0"
last_updated: "2026-02-10"
```

### 3. 文檔結構

建議的架構庫結構：
```
framework-library/
├── FRAMEWORKS.json            # 架構索引
├── README.md                  # 架構庫說明
├── SKILLS_GUIDE.md            # Skills 使用指南（本檔案）
├── validate_framework.py      # 格式驗證工具
└── frameworks/
    └── my_framework/          # 每個架構一個資料夾
        ├── my_framework_spec.yaml
        ├── AI_INTEGRATION_PROMPT.md
        ├── README.md
        ├── templates/         # 模板檔案（可選）
        └── examples/          # 範例程式碼（可選）
```

---

## 📞 取得協助

### 查看 Skill 文檔

```bash
# 方法 1：直接閱讀
cat ~/.claude/skills/framework-manager.md

# 方法 2：在對話中詢問
"請說明 framework-manager skill 的使用方式"
```

### 問題回報

如果遇到問題：
1. 檢查 skill 檔案是否存在：`ls ~/.claude/skills/`
2. 檢查檔案權限
3. 查看 Claude Code 的日誌輸出

---

## 🎉 開始使用

### 快速開始檢查清單

- [ ] 確認 skills 已安裝：`ls ~/.claude/skills/`
- [ ] 查看架構庫狀態：`/framework-manager status`
- [ ] 瀏覽範例規格：`frameworks/` 目錄
- [ ] 閱讀完整文檔：三個 skill 的 `.md` 檔案

### 第一次使用

建議從查看架構庫狀態開始：

```bash
# 1. 查看架構庫有哪些架構
/framework-manager status

# 2. 在任何專案中整合架構
cd /path/to/your_project
/framework-integrator
# 選擇「從 GitHub 架構庫選擇」
```

這樣可以快速了解整個流程！

---

**版本：** 1.1
**最後更新：** 2026-02-11
**相關文件：**
- [API 設定框架](frameworks/api_config_framework/README.md)
- [Prompt 管理系統](frameworks/prompt_management_framework/README.md)
