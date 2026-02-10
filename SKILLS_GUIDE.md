# Claude Code Skills 使用指南

> 🛠️ 本專案已配置兩個自訂 skills，用於架構設計與整合

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

**範例輸出：** 參考本專案的 `api_config_framework/` 和 `prompt_management_spec/`

---

### 2. framework-integrator - 架構自動整合工具

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

### 場景 2：使用本專案的架構框架

本專案已經包含兩個完整的架構規格：

#### 2.1 API 設定與金鑰管理框架

**位置：** `api_config_framework/`

**快速整合到新專案：**

```bash
# 方法 1：使用 framework-integrator（推薦）
cd /path/to/new_project
cp -r /path/to/etfflow_article/api_config_framework .
/framework-integrator api_config_framework/api_config_framework_spec.yaml

# 方法 2：手動複製整合指令給 AI
# 打開 api_config_framework/AI_INTEGRATION_PROMPT.md
# 複製「完整整合指令」
# 填入新專案資訊
# 提供給 Claude/ChatGPT
```

**核心功能：**
- ✅ 集中式 config.yaml 管理（一鍵切換模型）
- ✅ API 金鑰自動循環輪替
- ✅ 配額智慧檢測與切換
- ✅ 詳細日誌追蹤

#### 2.2 Prompt 管理系統

**位置：** `prompt_management_spec/`

**快速整合到新專案：**

```bash
cd /path/to/new_project
cp -r /path/to/etfflow_article/prompt_management_spec .
/framework-integrator prompt_management_spec/prompt_management_system_spec.yaml
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
cp -r ../template_project/my_template_framework .
/framework-integrator
```

---

## 📚 學習資源

### 範例 1：本專案的 API 框架

查看完整實作範例：
- **規格文檔：** `api_config_framework/api_config_framework_spec.yaml`
- **整合指令：** `api_config_framework/AI_INTEGRATION_PROMPT.md`
- **使用文檔：** `api_config_framework/README.md`
- **程式碼範例：** `api_config_framework/examples/integration_example.py`

### 範例 2：Prompt 管理系統

查看完整實作範例：
- **規格文檔：** `prompt_management_spec/prompt_management_system_spec.yaml`
- **使用指南：** `prompt_management_spec/README_PROMPT_SPEC.md`

### 實際應用

本專案就是使用這些架構構建的：
- **API 管理：** 使用 API 配置框架（`utils/api/gemini_api_utils.py` + `config.yaml`）
- **Prompt 管理：** 使用 Prompt 管理系統（`utils/prompt_manager.py` + UI）

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
  - `framework-integrator`：如何整合架構

- **規格文檔（在專案中）**：內容，描述「什麼」架構
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
2. 使用 /framework-architect 建立規格
   ↓
3. 將規格目錄提交到 Git
   ↓
4. 其他專案可以複製規格並使用 /framework-integrator 整合
```

### 2. 版本管理

規格文檔應該包含版本號：
```yaml
# 在 spec.yaml 中
version: "1.0.0"
last_updated: "2026-02-10"
```

### 3. 文檔結構

建議的專案結構：
```
project/
├── src/                        # 專案程式碼
├── my_framework/               # 可重用的架構規格
│   ├── my_framework_spec.yaml
│   ├── AI_INTEGRATION_PROMPT.md
│   ├── README.md
│   ├── templates/              # 模板檔案
│   └── examples/               # 範例程式碼
└── SKILLS_GUIDE.md            # 本檔案（說明如何使用 skills）
```

---

## 📞 取得協助

### 查看 Skill 文檔

```bash
# 方法 1：直接閱讀
cat ~/.claude/skills/framework-architect.md

# 方法 2：在對話中詢問
"請說明 framework-architect skill 的使用方式"
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
- [ ] 查看範例規格：`api_config_framework/` 和 `prompt_management_spec/`
- [ ] 嘗試呼叫：`/framework-architect`
- [ ] 閱讀完整文檔：`framework-architect.md` 和 `framework-integrator.md`

### 第一次使用

建議從整合現成的架構開始：

```bash
# 1. 進入任何測試專案
cd /path/to/test_project

# 2. 複製 API 框架規格
cp -r /path/to/etfflow_article/api_config_framework .

# 3. 執行整合
/framework-integrator

# 4. 查看結果
```

這樣可以快速了解整個流程！

---

**版本：** 1.0
**最後更新：** 2026-02-10
**相關文件：**
- [API 設定框架](api_config_framework/README.md)
- [Prompt 管理系統](prompt_management_spec/README_PROMPT_SPEC.md)
