# Framework Manager - 架構庫管理工具

> 🛠️ 管理 GitHub 架構庫：編輯、同步、驗證、刪除架構規格

## 功能說明

此 skill 提供 GitHub 架構庫的完整管理功能：
1. **列出所有架構** — 查看架構庫中的所有架構及其狀態
2. **編輯架構** — 修改現有架構的規格、文檔或整合指令
3. **同步 GitHub** — Pull/Push 操作，保持本地與遠端一致
4. **驗證格式** — 執行格式驗證，確保架構規格符合標準
5. **刪除架構** — 從架構庫中移除架構
6. **查看狀態** — 查看本地與遠端的差異
7. **設定管理** — 配置架構庫路徑與 GitHub URL

**與其他 Skills 的關係：**
```
/framework-architect  ──建立──→  架構規格
                                    ↓
/framework-manager   ──管理──→  架構庫（GitHub）
                                    ↓
/framework-integrator ──下載──→  整合到專案
```

## 使用場景

✅ **適合使用此 skill：**
- 想編輯架構庫中已有的架構規格
- 需要將本地修改推送到 GitHub
- 想從 GitHub 拉取最新版本到本地
- 需要驗證架構格式是否正確
- 想查看本地與遠端的差異
- 需要從架構庫中移除某個架構

❌ **不適合：**
- 建立全新的架構規格（請使用 `/framework-architect`）
- 將架構整合到專案中（請使用 `/framework-integrator`）

---

## 執行方式

當使用者呼叫此 skill 時，請按照以下步驟執行：

### 第 1 步：設定與初始化

**檢查設定檔：**

```python
# 偽代碼
def initialize():
    """
    初始化架構庫管理器
    """
    config_file = Path.home() / ".claude" / "framework_library.yaml"

    if config_file.exists():
        config = load_yaml(config_file)
        local_path = config.get('local_path')
        github_url = config.get('github_url')
    else:
        local_path = None
        github_url = None

    # 如果沒有本地路徑，嘗試自動偵測
    if not local_path:
        # 常見位置
        candidates = [
            Path.home() / "code" / "python" / "framework-library",
            Path.cwd() / "framework-library",
        ]
        for c in candidates:
            if (c / "FRAMEWORKS.json").exists():
                local_path = c
                break

    # 如果還是找不到，詢問使用者
    if not local_path:
        print("找不到架構庫，請設定路徑（見功能 7：設定管理）")
        return None

    # 如果沒有 GitHub URL，從 git remote 讀取
    if not github_url:
        github_url = git_remote_url(local_path)

    return {
        'local_path': local_path,
        'github_url': github_url,
        'branch': config.get('branch', 'master')
    }
```

**實際執行時：**
1. 讀取 `~/.claude/framework_library.yaml`
2. 確認本地路徑存在且含有 `FRAMEWORKS.json`
3. 確認 GitHub URL（從設定檔或 git remote）
4. 如果任何設定缺失，引導使用者到「設定管理」

**展示：**
```
🛠️ Framework Library Manager

⚙️ 初始化中...
✓ 本地路徑：C:\Users\User\code\python\framework-library
✓ GitHub：https://github.com/John1106John/framework-library
✓ 分支：master
✓ 架構數量：2 個
```

### 第 2 步：主選單

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ Framework Library Manager
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

請選擇操作：

1. 📋 列出所有架構
2. ✏️ 編輯架構
3. 🔄 同步 GitHub（Pull / Push）
4. ✅ 驗證格式
5. 🗑️ 刪除架構
6. 📊 查看狀態
7. ⚙️ 設定管理

您的選擇（1-7）：
```

---

## 功能 1：📋 列出所有架構

**讀取 FRAMEWORKS.json 並顯示：**

```
📋 架構庫內容
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 📦 API 設定與金鑰管理框架
   ID：api-config-framework
   版本：v1.0.0 | 作者：John1106John
   更新：2026-02-10
   標籤：#api-management #key-rotation #config #yaml
   說明：集中式 API 設定與自動循環金鑰輪替系統
   檔案：spec.yaml ✓ | README ✓ | AI_PROMPT ✓ | templates ✓ | examples ✓

2. 📝 Prompt 管理系統
   ID：prompt-management
   版本：v1.0.0 | 作者：John1106John
   更新：2026-02-10
   標籤：#prompt-management #version-control #ui #streamlit #workflow
   說明：AI Workflow 的 Prompt 版本管理系統
   檔案：spec.yaml ✓ | README ✓ | AI_PROMPT ✓ | templates ✗ | examples ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
共 2 個架構

選項：
- 輸入編號查看詳情
- 輸入 'b' 返回主選單
```

**查看詳情時：**

```python
def show_framework_detail(framework_id, local_path):
    """
    顯示架構詳細資訊
    """
    # 1. 從 FRAMEWORKS.json 讀取基本資訊
    framework = get_framework_by_id(framework_id)

    # 2. 檢查本地檔案
    fw_path = local_path / "frameworks" / framework['path']
    files = list_files(fw_path)

    # 3. 讀取 spec.yaml 的 metadata
    spec = load_yaml(fw_path / framework['files']['spec'])
    metadata = spec.get('metadata', {})

    # 4. 計算檔案大小
    total_size = sum(f.stat().st_size for f in files)

    # 5. 顯示完整資訊
    display_detail(framework, metadata, files, total_size)
```

**詳情展示：**
```
📦 API 設定與金鑰管理框架
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

基本資訊：
- ID：api-config-framework
- 版本：v1.0.0
- 作者：John1106John
- 建立：2026-02-10
- 更新：2026-02-10
- 授權：MIT

技術棧：Python 3.10+, pyyaml, python-dotenv

檔案清單：
  1. api_config_framework_spec.yaml (449 行)
  2. README.md (545 行)
  3. AI_INTEGRATION_PROMPT.md
  4. QUICKSTART.md
  5. templates/.env.example
  6. templates/config.yaml.template
  7. templates/config_loader.py.template
  8. templates/api_manager.py.template
  9. examples/integration_example.py

GitHub 連結：
🔗 https://github.com/John1106John/framework-library/tree/main/frameworks/api_config_framework

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選項：
- 'e' 編輯此架構
- 'v' 驗證此架構
- 'd' 刪除此架構
- 'b' 返回列表
```

---

## 功能 2：✏️ 編輯架構

這是最核心的功能，提供完整的架構編輯工作流程。

### 2.1 選擇要編輯的架構

```
✏️ 編輯架構
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選擇要編輯的架構：

1. 📦 API 設定與金鑰管理框架 (api-config-framework)
2. 📝 Prompt 管理系統 (prompt-management)

您的選擇：
```

### 2.2 選擇要編輯的檔案

```
✏️ 編輯：Prompt 管理系統
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選擇要編輯的檔案：

1. 📄 prompt_management_system_spec.yaml（系統規格）
   1,122 行 | 核心規格文檔
2. 📖 README.md（使用文檔）
   給開發者閱讀的完整使用指南
3. 🤖 AI_INTEGRATION_PROMPT.md（AI 整合指令）
   可直接複製給 AI 使用的整合 prompt
4. 📋 README_PROMPT_SPEC.md（規格說明）
   完整規格說明文檔
5. 📝 其他（手動指定檔案名稱）

您的選擇：
```

### 2.3 AI 讀取並展示當前內容

```python
def edit_framework_file(framework_path, filename):
    """
    編輯架構檔案的工作流程
    """
    file_path = framework_path / filename

    # 1. 讀取檔案
    content = file_path.read_text(encoding='utf-8')

    # 2. 顯示檔案摘要
    print(f"📄 {filename}")
    print(f"   行數：{len(content.splitlines())}")
    print(f"   大小：{len(content)} 字元")
    print()

    # 3. 顯示結構摘要（對 YAML 顯示頂層 key，對 MD 顯示標題結構）
    if filename.endswith('.yaml'):
        show_yaml_structure(content)
    elif filename.endswith('.md'):
        show_markdown_headings(content)

    # 4. 詢問使用者要做什麼修改
    print()
    print("請描述您要做的修改：")
    print("（可以描述要修改的章節、要新增的內容、要刪除的部分等）")
    print()
    print("範例：")
    print("- '更新 metadata 的 version 為 1.1.0'")
    print("- '在 architecture 章節新增一個 component'")
    print("- '重寫 integration_guide 的 quick_start 章節'")
    print("- '新增 known_pitfalls 的一個項目'")

    return content
```

**展示：**
```
📄 prompt_management_system_spec.yaml
   行數：1,122
   大小：38,456 字元

YAML 結構摘要：
├── metadata (name, version, description, author, ...)
├── system_overview (name, purpose, tech_stack)
├── architecture (design_principle, components)
├── directory_structure (description, layout, file_naming)
├── shared_formatters (design_principle, architecture, implementation, ...)
├── prompt_manager_class (description, constructor, methods)
├── script_prompt_conventions (supported_formats, unsupported)
├── ui_integration (stage_config, prompt_editor_ui, session_state_keys, ...)
├── version_management (description, storage, operations, ...)
├── known_pitfalls (5 items)
├── ai_implementation_guide (5 steps)
├── quick_start_example (description, prompt_to_ai, expected_file_structure)
├── faq (5 questions)
├── streamlit_security (description, security_levels, ...)
├── integration_guide (prerequisites, quick_start, integration_methods, ...)
└── license (description, attribution)

請描述您要做的修改：
```

### 2.4 AI 執行修改

```python
def apply_edits(file_path, content, user_description):
    """
    根據使用者描述修改檔案
    """
    # 1. AI 根據使用者描述理解修改意圖
    # 2. 讀取完整檔案內容
    # 3. 使用 Edit 工具進行精確修改
    # 4. 產生變更摘要

    # 修改完成後顯示 diff 預覽
    print("【變更預覽】")
    print()
    show_diff(original_content, new_content)
    print()
    print("確認此變更？(y/n/edit)")
    print("- y: 確認修改")
    print("- n: 放棄修改")
    print("- edit: 繼續編輯")
```

**展示：**
```
【變更預覽】

--- prompt_management_system_spec.yaml（修改前）
+++ prompt_management_system_spec.yaml（修改後）

@@ metadata @@
- version: "1.0.0"
+ version: "1.1.0"
- updated_at: "2026-02-10"
+ updated_at: "2026-02-11"

@@ architecture.components @@
+ - name: DataFormatter
+   role: 共用資料格式化模組
+   responsibilities:
+     - 提供統一的資料讀取和格式化函數
+     - 確保 Stage 腳本和 UI 預覽使用相同邏輯

確認此變更？(y/n/edit)
```

### 2.5 儲存與後續操作

使用者確認後：

```
✅ 已儲存修改！

📄 已修改：prompt_management_system_spec.yaml
   變更：2 處修改

後續操作：
1. ✅ 驗證格式（自動執行）
2. 🔄 推送到 GitHub

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【自動驗證結果】
✅ prompt_management_framework：通過驗證

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

是否推送到 GitHub？(y/n)
- y: 建立 commit 並推送
- n: 僅保存在本地（稍後手動推送）

您的選擇：
```

**如果選擇推送：**

```python
def push_changes(local_path, files_changed, description):
    """
    推送變更到 GitHub
    """
    # 1. git add 修改的檔案
    git_add(local_path, files_changed)

    # 2. 產生 commit message
    commit_msg = f"Update {framework_name}: {description}"

    # 3. git commit
    git_commit(local_path, commit_msg)

    # 4. git push
    git_push(local_path, branch)

    print(f"✅ 已推送到 GitHub！")
    print(f"   commit: {commit_msg}")
    print(f"   分支：{branch}")
```

**展示：**
```
🔄 推送到 GitHub...

git add frameworks/prompt_management_framework/prompt_management_system_spec.yaml
git commit -m "Update prompt-management: 更新版本號和新增 DataFormatter 組件"
git push origin master

✅ 推送成功！
   commit：Update prompt-management: 更新版本號和新增 DataFormatter 組件
   分支：master
   遠端：https://github.com/John1106John/framework-library

返回主選單...
```

---

## 功能 3：🔄 同步 GitHub

### 3.1 同步選單

```
🔄 同步 GitHub
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

當前狀態：
- 本地：C:\Users\User\code\python\framework-library
- 遠端：https://github.com/John1106John/framework-library
- 分支：master

選擇操作：

1. ⬇️ Pull（從 GitHub 拉取最新）
   - 將遠端的變更同步到本地
   - 適合：其他地方推送了更新

2. ⬆️ Push（推送到 GitHub）
   - 將本地的變更推送到遠端
   - 適合：本地做了修改

3. 🔃 完整同步（Pull → 檢查 → Push）
   - 先拉取最新，再推送本地變更
   - 適合：確保完全同步

4. 📥 Clone（首次設定）
   - 從 GitHub 複製整個架構庫到本地
   - 適合：新電腦或重新設定

您的選擇（1-4）：
```

### 3.2 Pull 操作

```python
def pull_from_github(local_path, branch):
    """
    從 GitHub 拉取最新版本
    """
    # 1. 檢查本地是否有未提交的變更
    if has_uncommitted_changes(local_path):
        print("⚠️ 本地有未提交的變更：")
        show_git_status(local_path)
        print()
        print("選項：")
        print("1. 先 stash（暫存）再 pull")
        print("2. 先 commit 再 pull")
        print("3. 取消 pull")
        choice = input()
        if choice == '1':
            git_stash(local_path)
        elif choice == '2':
            git_add_commit(local_path, "WIP: save before pull")
        else:
            return

    # 2. 執行 pull
    result = git_pull(local_path, branch)

    # 3. 顯示結果
    if result.success:
        print("✅ Pull 成功！")
        show_pull_summary(result)
    else:
        print("❌ Pull 失敗")
        print(result.error)
        suggest_resolution(result)
```

**展示：**
```
⬇️ 正在從 GitHub 拉取...

git pull origin master

✅ Pull 成功！

變更摘要：
- 更新：2 個檔案
  - frameworks/api_config_framework/README.md
  - FRAMEWORKS.json
- 新增：0 個檔案
- 刪除：0 個檔案

本地架構庫已是最新版本。
```

### 3.3 Push 操作

```python
def push_to_github(local_path, branch):
    """
    推送本地變更到 GitHub
    """
    # 1. 檢查是否有變更
    status = git_status(local_path)
    if not status.has_changes:
        print("✅ 沒有需要推送的變更")
        return

    # 2. 顯示變更清單
    print("📋 待推送的變更：")
    for f in status.modified:
        print(f"  修改：{f}")
    for f in status.added:
        print(f"  新增：{f}")
    for f in status.deleted:
        print(f"  刪除：{f}")

    # 3. 詢問 commit 訊息
    print()
    print("請輸入 commit 訊息：")
    print("（或按 Enter 使用自動生成的訊息）")
    auto_msg = generate_commit_message(status)
    print(f"自動訊息：{auto_msg}")

    # 4. 執行 git add + commit + push
    git_add_all(local_path)
    git_commit(local_path, commit_msg)
    git_push(local_path, branch)
```

**展示：**
```
⬆️ 推送到 GitHub
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 待推送的變更：
  修改：frameworks/prompt_management_framework/prompt_management_system_spec.yaml
  修改：FRAMEWORKS.json

請輸入 commit 訊息（Enter 使用自動訊息）：
自動訊息：Update prompt-management framework spec

> [使用者輸入或直接 Enter]

🔄 推送中...

git add .
git commit -m "Update prompt-management framework spec"
git push origin master

✅ 推送成功！
   commit hash：a1b2c3d
   分支：master → origin/master
```

### 3.4 Clone 操作

```
📥 Clone 架構庫
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GitHub URL：https://github.com/John1106John/framework-library

本地存放路徑：
預設：C:\Users\User\code\python\framework-library
您的選擇（Enter 使用預設）：

🔄 正在 Clone...

git clone https://github.com/John1106John/framework-library.git "C:\Users\User\code\python\framework-library"

✅ Clone 成功！

架構庫已下載到：C:\Users\User\code\python\framework-library
包含 2 個架構

已更新設定檔：~/.claude/framework_library.yaml
```

---

## 功能 4：✅ 驗證格式

### 4.1 驗證選單

```
✅ 驗證格式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選擇驗證範圍：

1. 🔍 驗證全部架構
2. 📦 驗證特定架構
   a. API 設定與金鑰管理框架
   b. Prompt 管理系統

您的選擇：
```

### 4.2 執行驗證

```python
def validate_frameworks(local_path, framework_id=None):
    """
    執行架構格式驗證
    """
    validate_script = local_path / "validate_framework.py"

    if not validate_script.exists():
        print("❌ 找不到 validate_framework.py")
        return

    # 執行驗證腳本
    if framework_id:
        # 驗證特定架構
        fw_path = get_framework_path(local_path, framework_id)
        result = run_command(f"python {validate_script} {fw_path}")
    else:
        # 驗證全部
        result = run_command(f"python {validate_script}")

    display_validation_result(result)
```

**展示：**
```
🔍 正在驗證所有架構...

python validate_framework.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 api_config_framework
  ✅ metadata：通過
  ✅ system_overview：通過
  ✅ architecture：通過
  ✅ directory_structure：通過
  ✅ integration_guide：通過
  ✅ 必要檔案：通過（spec.yaml ✓, README.md ✓, AI_INTEGRATION_PROMPT.md ✓）
  結果：✅ 通過

📝 prompt_management_framework
  ✅ metadata：通過
  ✅ system_overview：通過
  ✅ architecture：通過
  ✅ directory_structure：通過
  ✅ integration_guide：通過
  ✅ 必要檔案：通過（spec.yaml ✓, README.md ✓, AI_INTEGRATION_PROMPT.md ✓）
  結果：✅ 通過

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FRAMEWORKS.json 一致性：✅ 通過

總結：2/2 架構通過驗證 ✅
```

---

## 功能 5：🗑️ 刪除架構

### 5.1 選擇要刪除的架構

```
🗑️ 刪除架構
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 注意：此操作將永久刪除架構及其所有檔案！

選擇要刪除的架構：

1. 📦 API 設定與金鑰管理框架 (api-config-framework)
   9 個檔案 | templates ✓ | examples ✓

2. 📝 Prompt 管理系統 (prompt-management)
   4 個檔案

您的選擇：
```

### 5.2 確認刪除

```
⚠️ 確認刪除

您即將刪除：
📦 API 設定與金鑰管理框架 (api-config-framework)

將移除以下檔案：
- frameworks/api_config_framework/api_config_framework_spec.yaml
- frameworks/api_config_framework/README.md
- frameworks/api_config_framework/AI_INTEGRATION_PROMPT.md
- frameworks/api_config_framework/QUICKSTART.md
- frameworks/api_config_framework/templates/ (4 個檔案)
- frameworks/api_config_framework/examples/ (1 個檔案)

同時更新：
- FRAMEWORKS.json（移除此架構的條目）

此操作不可撤銷！確認刪除？
請輸入架構 ID 'api-config-framework' 確認：
```

### 5.3 執行刪除

```python
def delete_framework(local_path, framework_id):
    """
    刪除架構
    """
    # 1. 確認操作（要求輸入完整 ID）
    confirmation = input(f"請輸入 '{framework_id}' 確認刪除：")
    if confirmation != framework_id:
        print("❌ 取消刪除")
        return

    # 2. 刪除目錄
    fw_path = get_framework_path(local_path, framework_id)
    shutil.rmtree(fw_path)

    # 3. 更新 FRAMEWORKS.json
    update_frameworks_json(local_path, remove_id=framework_id)

    # 4. 詢問是否推送
    print("✅ 本地已刪除")
    print()
    print("是否推送到 GitHub？(y/n)")
```

**展示：**
```
🗑️ 正在刪除...

✓ 已刪除：frameworks/api_config_framework/ (9 個檔案)
✓ 已更新：FRAMEWORKS.json

✅ 架構已從本地刪除！

是否推送到 GitHub？(y/n)
```

---

## 功能 6：📊 查看狀態

### 6.1 狀態總覽

```python
def show_status(local_path, github_url, branch):
    """
    顯示架構庫狀態
    """
    # 1. Git 狀態
    git_status = run_git_status(local_path)

    # 2. 本地 vs 遠端比較
    ahead, behind = git_ahead_behind(local_path, branch)

    # 3. 修改的檔案
    modified_files = git_diff_files(local_path)

    # 4. 架構統計
    frameworks = load_frameworks_json(local_path)

    display_status(git_status, ahead, behind, modified_files, frameworks)
```

**展示：**
```
📊 架構庫狀態
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Git 狀態：
  分支：master
  遠端：origin/master
  同步：✅ 已同步（或 ⚠️ 領先 2 個 commit / 落後 1 個 commit）

工作區變更：
  修改：0 個檔案
  新增：0 個檔案
  刪除：0 個檔案
  （或列出具體變更的檔案）

架構統計：
  總數：2 個架構
  已驗證：2/2 通過

  📦 api-config-framework  v1.0.0  2026-02-10  ✅ 已同步
  📝 prompt-management     v1.0.0  2026-02-10  ✅ 已同步

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選項：
- 's' 同步 GitHub
- 'd' 查看詳細 diff
- 'b' 返回主選單
```

### 6.2 詳細 Diff

如果有本地修改，可以查看詳細 diff：

```
📊 詳細變更（git diff）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

frameworks/prompt_management_framework/prompt_management_system_spec.yaml：

@@ -22,7 +22,7 @@ metadata:
-  version: "1.0.0"
+  version: "1.1.0"
-  updated_at: "2026-02-10"
+  updated_at: "2026-02-11"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選項：
- 'p' 推送變更到 GitHub
- 'r' 放棄變更（git checkout）
- 'b' 返回
```

---

## 功能 7：⚙️ 設定管理

### 7.1 設定選單

```
⚙️ 設定管理
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

當前設定（~/.claude/framework_library.yaml）：

  github_url：https://github.com/John1106John/framework-library
  local_path：C:\Users\User\code\python\framework-library
  branch：master

選擇操作：

1. 🔗 修改 GitHub URL
2. 📁 修改本地路徑
3. 🌿 修改分支名稱
4. 📋 查看完整設定檔
5. 🔄 重設為預設值

您的選擇：
```

### 7.2 設定檔格式

**檔案位置：** `~/.claude/framework_library.yaml`

```yaml
# Framework Library Configuration
# 由 /framework-manager 和 /framework-integrator 共用

github_url: "https://github.com/John1106John/framework-library"
local_path: "C:\\Users\\User\\code\\python\\framework-library"
branch: "master"
```

**設定檔與其他 Skills 的共用：**
- `framework-integrator` 使用 `github_url` 連接 GitHub
- `framework-manager` 使用全部三個欄位
- 任一 skill 修改設定後，另一個 skill 也會讀到最新設定

---

## 錯誤處理

### 常見錯誤與解決方案

#### 1. 找不到本地架構庫

```
❌ 錯誤：找不到架構庫

原因：local_path 路徑不存在或不包含 FRAMEWORKS.json

解決方案：
1. 使用功能 7（設定管理）設定正確路徑
2. 使用功能 3.4（Clone）從 GitHub 下載
3. 手動確認路徑：C:\Users\User\code\python\framework-library
```

#### 2. Git push 被拒絕

```
❌ 錯誤：Push 被拒絕（rejected）

原因：遠端有本地沒有的 commit

解決方案：
1. 先執行 Pull（功能 3.1）
2. 解決衝突（如果有）
3. 再次 Push
```

#### 3. FRAMEWORKS.json 與本地目錄不一致

```
⚠️ 警告：FRAMEWORKS.json 與本地目錄不一致

發現的問題：
- FRAMEWORKS.json 列出 'data-validation' 但本地目錄不存在
- 本地目錄 'logging-framework' 存在但未在 FRAMEWORKS.json 中

解決方案：
1. 執行驗證（功能 4）查看詳細報告
2. 手動修正 FRAMEWORKS.json
3. 或使用刪除/新增來修正
```

#### 4. 驗證失敗

```
❌ 驗證失敗

框架：prompt-management
問題：
- metadata 缺少 'license' 欄位
- integration_guide 缺少 'quick_start' 章節

建議：
- 使用功能 2（編輯架構）修正缺少的欄位
- 參考 validate_framework.py 的必要欄位清單
```

#### 5. 設定檔不存在

```
⚠️ 找不到設定檔：~/.claude/framework_library.yaml

自動建立設定檔...

請提供以下資訊：

1. GitHub URL（架構庫 Repository）
   預設：https://github.com/John1106John/framework-library
   您的輸入：[Enter 使用預設]

2. 本地路徑
   預設：C:\Users\User\code\python\framework-library
   您的輸入：[Enter 使用預設]

3. 分支名稱
   預設：master
   您的輸入：[Enter 使用預設]

✅ 設定檔已建立！
```

---

## 與其他 Skills 的關係

```
┌─────────────────────────────────────────────────────────┐
│                  架構生命週期管理                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  /framework-architect    /framework-manager              │
│  ┌───────────────┐      ┌───────────────┐               │
│  │ 🏗️ 設計架構    │──→   │ 🛠️ 管理架構    │               │
│  │               │      │               │               │
│  │ - 引導式問答   │      │ - 編輯規格     │               │
│  │ - 產生 3 個檔案│      │ - 同步 GitHub  │               │
│  │ - 上傳 GitHub │      │ - 驗證格式     │               │
│  └───────────────┘      │ - 查看狀態     │               │
│                         └───────┬───────┘               │
│                                 │                       │
│                                 ↓                       │
│                    GitHub 架構庫                          │
│                    (framework-library)                   │
│                                 │                       │
│                                 ↓                       │
│                  /framework-integrator                   │
│                  ┌───────────────┐                       │
│                  │ 🔧 整合架構    │                       │
│                  │               │                       │
│                  │ - 下載架構     │                       │
│                  │ - 分析專案     │                       │
│                  │ - 自動整合     │                       │
│                  └───────────────┘                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**共用設定：** `~/.claude/framework_library.yaml`
- `github_url`：三個 skill 共用
- `local_path`：manager 主要使用
- `branch`：manager 和 architect 使用

---

## 使用範例

### 範例 1：編輯架構規格

```
使用者：/framework-manager

AI：
🛠️ Framework Library Manager

⚙️ 初始化中...
✓ 本地路徑：C:\Users\User\code\python\framework-library
✓ GitHub：https://github.com/John1106John/framework-library
✓ 架構數量：2 個

請選擇操作：
[顯示主選單]

使用者：2（編輯架構）

AI：
[顯示架構列表]

使用者：2（Prompt 管理系統）

AI：
[顯示檔案列表]

使用者：1（spec.yaml）

AI：
[讀取並顯示結構摘要]
請描述您要做的修改：

使用者：更新 version 為 1.1.0，在 architecture.components 新增 DataFormatter 組件

AI：
[執行修改、顯示 diff、確認、驗證、推送]
```

### 範例 2：同步 GitHub

```
使用者：/framework-manager

AI：[初始化 + 主選單]

使用者：3（同步 GitHub）

AI：[顯示同步選單]

使用者：1（Pull）

AI：
⬇️ 正在從 GitHub 拉取...
✅ Pull 成功！已更新 2 個檔案。
```

### 範例 3：快速查看狀態

```
使用者：/framework-manager

AI：[初始化 + 主選單]

使用者：6（查看狀態）

AI：
[顯示完整狀態報告：Git 狀態、同步狀態、架構統計]
```

---

## 快捷用法

除了互動式選單，也支援直接指定操作：

```bash
# 直接進入編輯模式
/framework-manager edit

# 直接同步
/framework-manager sync

# 直接驗證
/framework-manager validate

# 直接查看狀態
/framework-manager status

# 直接編輯特定架構
/framework-manager edit prompt-management
```

---

## 實作注意事項

### 對話流程

1. **初始化要快**：設定檢查應在 1-2 步內完成
2. **主選單清晰**：7 個功能一目了然
3. **操作可返回**：任何時候都能返回主選單
4. **自動化串接**：編輯後自動驗證 → 自動詢問是否推送

### Git 操作安全

1. **不使用 force push**：避免覆蓋遠端變更
2. **Push 前先 Pull**：確保不會衝突
3. **顯示 diff 確認**：推送前讓使用者確認變更
4. **刪除需要確認**：輸入完整 ID 才能刪除

### Windows 相容性

1. **路徑使用 Path 物件**：自動處理 / 和 \
2. **編碼使用 UTF-8**：所有檔案讀寫指定 encoding='utf-8'
3. **Git 命令**：使用 git bash 或確保 git 在 PATH 中

---

## 總結

此 skill 的核心價值：

1. **統一管理入口** — 所有架構庫操作在一個地方完成
2. **GitHub 整合** — Pull/Push/Clone 一鍵操作
3. **安全編輯** — 讀取→修改→確認→驗證→推送的完整流程
4. **與生態系統整合** — 和 architect、integrator 共用設定
5. **格式保障** — 編輯後自動驗證格式

**三個 Skills 的完整生態系統：**
- `/framework-architect` → **建立**新架構
- `/framework-manager` → **管理**架構庫
- `/framework-integrator` → **使用**架構
