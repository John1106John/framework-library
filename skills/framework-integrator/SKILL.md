# Framework Integrator - 架構自動整合工具

> 🔧 自動讀取架構規格文檔並整合到當前專案

## 功能說明

此 skill 會自動：
1. 掃描並讀取架構規格文檔（`*_spec.yaml`）
2. 分析當前專案結構
3. 根據規格執行完整整合
4. 驗證整合結果
5. 產生整合報告

**與 framework-architect 的關係：**
- `framework-architect`：設計規格（產生文檔）
- `framework-integrator`：執行整合（讀取文檔並實作）

## 使用場景

✅ **適合使用此 skill：**
- 您有一個現成的架構規格文檔（`*_spec.yaml`）
- 想要將此架構快速整合到當前專案
- 希望自動化整合過程，避免手動操作錯誤

❌ **不適合：**
- 還沒有規格文檔（請先使用 `/framework-architect` 建立）
- 需要高度客製化的整合（建議手動整合）

## 執行方式

### 使用方法 1：互動式選擇（推薦）

```bash
/framework-integrator
```

會提供三個來源選項：
1. **從 GitHub 架構庫選擇**（推薦）- 存取雲端架構庫
2. **從本地專案掃描** - 掃描當前目錄的規格
3. **指定本地檔案路徑** - 直接指定規格檔案

### 使用方法 2：直接從 GitHub

```bash
/framework-integrator --github
```

直接開啟 GitHub 架構庫選單。

### 使用方法 3：指定規格檔案

```bash
/framework-integrator path/to/spec.yaml
```

直接指定規格檔案路徑進行整合。

### 使用方法 4：指定 GitHub 架構

```bash
/framework-integrator --github framework-name
```

直接從 GitHub 下載並整合指定架構。

---

## 整合流程

當使用者呼叫此 skill 時，請按照以下步驟執行：

### 第 1 步：選擇架構來源

**展示給使用者：**
```
🏗️ Framework Integrator - 架構自動整合工具

請選擇架構來源：

1. 📦 從 GitHub 架構庫選擇（推薦）
   - 存取雲端架構庫
   - 自動下載最新版本
   - 支援搜尋和預覽

2. 📁 從本地專案掃描
   - 掃描當前目錄的規格檔案
   - 適合本地開發的架構

3. 📄 指定本地檔案路徑
   - 直接指定規格檔案位置

您的選擇（1/2/3）：
```

#### 選項 1：從 GitHub 架構庫選擇

**步驟 1.1：設定 GitHub 架構庫 URL**

```python
# 偽代碼
def get_github_library_url():
    """
    取得或設定 GitHub 架構庫 URL
    """
    # 檢查是否有設定檔
    config_file = Path.home() / ".claude" / "framework_library.yaml"

    if config_file.exists():
        config = load_yaml(config_file)
        library_url = config.get('github_url')
    else:
        library_url = None

    if not library_url:
        # 詢問使用者
        print("請設定 GitHub 架構庫 URL：")
        print("預設：https://github.com/{username}/framework-library")
        library_url = input("您的 URL（Enter 使用預設）：").strip()

        if not library_url:
            username = get_github_username()
            library_url = f"https://github.com/{username}/framework-library"

        # 儲存設定
        save_yaml(config_file, {'github_url': library_url})

    return library_url
```

**展示：**
```
⚙️ GitHub 架構庫設定

預設 URL：https://github.com/{您的username}/framework-library

選項：
1. 使用預設 URL
2. 使用自訂 URL
3. 使用公開架構庫（https://github.com/framework-library/frameworks）

您的選擇：
```

**步驟 1.2：讀取架構索引**

```python
def fetch_framework_index(library_url):
    """
    從 GitHub 讀取架構索引
    """
    # 構建 raw URL
    raw_url = convert_to_raw_url(library_url) + "/FRAMEWORKS.json"

    try:
        # 下載索引
        response = requests.get(raw_url)
        frameworks = json.loads(response.text)['frameworks']
        return frameworks
    except Exception as e:
        print(f"❌ 無法讀取架構庫：{e}")
        print("請確認：")
        print("1. URL 正確")
        print("2. Repository 存在")
        print("3. FRAMEWORKS.json 檔案存在")
        return []
```

**展示：**
```
🔍 正在讀取 GitHub 架構庫...

已連接：https://github.com/your-username/framework-library
找到 12 個架構

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

架構列表：

1. 📦 API 設定與金鑰管理框架
   版本：v1.0.0 | 作者：your-username | 更新：2026-02-10
   標籤：api-management, key-rotation, config
   說明：集中式 API 設定與自動循環金鑰輪替

2. 📝 Prompt 管理系統
   版本：v1.0.0 | 作者：your-username | 更新：2026-02-09
   標籤：prompt-management, version-control, ui
   說明：AI Workflow 的 Prompt 版本管理系統

3. 📊 資料驗證框架
   版本：v1.2.0 | 作者：team-member | 更新：2026-02-08
   標籤：data-validation, pandas, pydantic
   說明：自動驗證 Excel/CSV 資料的格式和內容

4. 🔐 認證授權框架
   版本：v2.0.0 | 作者：security-team | 更新：2026-02-05
   標籤：authentication, authorization, jwt
   說明：JWT + OAuth 2.0 認證授權系統

... (顯示更多)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

選項：
- 輸入編號選擇架構（如：1）
- 輸入 's' 搜尋架構
- 輸入 'f' 篩選標籤
- 輸入 'q' 返回上一層

您的選擇：
```

**步驟 1.3：搜尋功能**

如果使用者輸入 's'：

```
🔎 搜尋架構

請輸入搜尋關鍵字（名稱、標籤、描述）：
```

**範例輸入：** `api`

```
搜尋結果（3 個）：

1. 📦 API 設定與金鑰管理框架
   匹配：名稱 + 標籤(api-management)

2. 🌐 API Gateway 框架
   匹配：名稱 + 說明

3. 📡 RESTful API 腳手架
   匹配：標籤(api-design)

請選擇（輸入編號）：
```

**步驟 1.4：預覽架構詳情**

選擇架構後，顯示詳細資訊：

```
📦 API 設定與金鑰管理框架

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

基本資訊：
- 版本：v1.0.0
- 作者：your-username
- 建立：2026-02-10
- 更新：2026-02-10
- 技術棧：Python 3.10+, pyyaml, python-dotenv

核心功能：
✓ 集中式 config.yaml 管理（一鍵切換模型）
✓ API 金鑰自動循環輪替
✓ 配額智慧檢測與切換
✓ 詳細日誌追蹤

標籤：
#api-management #key-rotation #config #yaml

GitHub 連結：
📄 README：https://github.com/.../frameworks/api_config_framework/README.md
📋 規格：https://github.com/.../frameworks/api_config_framework/api_config_framework_spec.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

是否要整合此架構到當前專案？(y/n/preview)
- y: 立即整合
- n: 返回架構列表
- preview: 預覽 README

您的選擇：
```

**如果選擇 preview：**

```
📖 預覽 README

[顯示 README.md 的前 50 行]

... (繼續顯示)

按 Enter 繼續閱讀，或輸入 'i' 開始整合，'b' 返回：
```

**步驟 1.5：下載架構**

確認整合後：

```python
def download_framework_from_github(framework_info, target_dir):
    """
    從 GitHub 下載架構檔案
    """
    print(f"📥 正在從 GitHub 下載架構...")

    # 構建下載 URL
    framework_path = framework_info['path']
    base_url = library_url.replace('github.com', 'raw.githubusercontent.com')
    base_url = f"{base_url}/main/{framework_path}"

    # 下載檔案
    files_to_download = [
        f"{framework_name}_spec.yaml",
        "AI_INTEGRATION_PROMPT.md",
        "README.md"
    ]

    for filename in files_to_download:
        url = f"{base_url}/{filename}"
        download_file(url, target_dir / filename)
        print(f"  ✓ {filename}")

    # 如果有 templates/ 目錄，也下載
    if framework_info.get('has_templates'):
        download_directory(f"{base_url}/templates", target_dir / "templates")
        print(f"  ✓ templates/")

    print(f"✅ 下載完成！")
    return target_dir / f"{framework_name}_spec.yaml"
```

**展示：**
```
📥 正在從 GitHub 下載架構...

下載中：
  ✓ api_config_framework_spec.yaml
  ✓ AI_INTEGRATION_PROMPT.md
  ✓ README.md
  ✓ templates/config.yaml.template
  ✓ templates/config_loader.py.template
  ✓ templates/api_manager.py.template
  ✓ templates/.env.example

✅ 下載完成！

已儲存到：.framework_cache/api_config_framework/

繼續整合流程...
```

#### 選項 2：從本地專案掃描

```python
# 原本的掃描邏輯
def scan_local_frameworks():
    """
    掃描本地專案的規格檔案
    """
    patterns = [
        "**/*_framework/*_spec.yaml",
        "**/*_spec.yaml"
    ]

    found_specs = []
    for pattern in patterns:
        found_specs.extend(glob.glob(pattern, recursive=True))

    return found_specs
```

**展示：**
```
🔍 掃描本地專案...

找到以下規格：
1. api_config_framework/api_config_framework_spec.yaml
   - 名稱：API 設定與金鑰管理框架
   - 版本：v1.0

2. prompt_management_spec/prompt_management_system_spec.yaml
   - 名稱：Prompt Management System
   - 版本：v1.0

請選擇要整合的規格（輸入編號）：
```

#### 選項 3：指定本地檔案路徑

```
📄 請輸入規格檔案的完整路徑：

範例：
- /path/to/framework/spec.yaml
- C:\Users\User\frameworks\my_framework\spec.yaml
- ./local_framework/spec.yaml

您的路徑：
```

### 第 2 步：分析當前專案

```python
# 分析項目
1. 檢查專案根目錄
2. 掃描現有檔案結構
3. 識別程式語言和框架
4. 檢查是否有衝突的檔案

展示資訊：
- 專案路徑：{當前目錄}
- 檢測到的語言：Python 3.x
- 現有目錄：utils/, scripts/, data/
- 潛在衝突：[列出可能被覆蓋的檔案]
```

**詢問使用者：**
```
📊 專案分析完成

當前專案資訊：
- 路徑：C:\Users\User\code\python\my_project
- 語言：Python 3.10
- 現有結構：
  ├── scripts/
  ├── utils/
  └── data/

即將整合：{架構名稱}

⚠️ 注意：以下檔案可能會被修改或新增：
- utils/config.py（新增）
- config.yaml（新增）
- utils/api/api_manager.py（新增）

是否繼續？(y/n)
```

### 第 3 步：執行整合

根據規格中的 `integration_guide.integration_steps` 執行每個步驟：

#### 3.1 複製模板檔案

```python
# 讀取規格中的 directory_structure 和檔案清單
# 從規格對應的 framework 目錄中複製模板檔案

範例：
從：api_config_framework/templates/config.yaml.template
到：{專案}/config.yaml
```

**展示進度：**
```
【步驟 1/5】複製框架檔案

✓ 已複製 config.yaml 到專案根目錄
✓ 已複製 utils/config.py
✓ 已複製 utils/api/api_manager.py
✓ 已複製 .env.example
```

#### 3.2 修改設定檔

```python
# 根據規格中的 configuration 章節
# 更新設定檔中的參數

範例：
- 讀取 config.yaml.template
- 根據使用者輸入或預設值填入參數
- 儲存為 config.yaml
```

**互動詢問：**
```
【步驟 2/5】設定參數

規格要求設定以下參數：

1. model_name（必填）
   - 說明：AI 模型名稱
   - 預設值：gemini-2.5-flash
   - 您的輸入：[直接 Enter 使用預設，或輸入新值]

2. retry_delay（選填）
   - 說明：配額重試延遲秒數
   - 預設值：2.0
   - 您的輸入：

[依次詢問所有必填參數]
```

#### 3.3 掃描並更新程式碼

```python
# 根據規格中的說明，掃描專案中需要修改的程式碼

範例（API 管理框架）：
1. 掃描所有 .py 檔案
2. 找出硬編碼的模型名稱（如 "gemini-2.5-flash"）
3. 替換為：from utils.config import get_model_name; MODEL = get_model_name()
4. 找出 time.sleep(固定值)
5. 替換為：from utils.config import get_api_call_interval; time.sleep(get_api_call_interval())
```

**展示進度：**
```
【步驟 3/5】掃描並更新程式碼

正在掃描專案中的 Python 檔案...

找到需要修改的檔案：
1. scripts/stage1.py
   - 第 15 行：MODEL_NAME = "gemini-2.5-flash" → 使用 get_model_name()
   - 第 42 行：time.sleep(2) → 使用 get_api_call_interval()

2. scripts/stage2.py
   - 第 10 行：MODEL_NAME = "gemini-2.5-flash" → 使用 get_model_name()

共發現 5 個檔案需要修改，8 處需要替換。

是否執行替換？(y/n/preview)
- y: 立即執行
- n: 跳過
- preview: 先預覽變更
```

**如果選擇 preview：**
```
【變更預覽】scripts/stage1.py

第 15 行：
- MODEL_NAME = "gemini-2.5-flash"
+ from utils.config import get_model_name
+ MODEL_NAME = get_model_name()

第 42 行：
- time.sleep(2)
+ from utils.config import get_api_call_interval
+ time.sleep(get_api_call_interval())

確認執行此變更？(y/n)
```

#### 3.4 建立環境檔案

```python
# 根據規格中的 configuration.environment_variables
# 建立 .env 檔案

範例：
1. 複製 .env.example → .env
2. 確認 .env 在 .gitignore 中
3. 提示使用者填入實際的金鑰/密碼
```

**展示：**
```
【步驟 4/5】建立環境檔案

✓ 已建立 .env 檔案（從 .env.example 複製）
✓ 已確認 .env 在 .gitignore 中

⚠️ 請手動編輯 .env 檔案，填入以下資訊：
- API_KEYS: 您的 API 金鑰（多個用逗號分隔）
- GOOGLE_API_KEY: （或使用單一金鑰）

.env 檔案位置：{專案}/.env
```

#### 3.5 建立測試腳本

```python
# 根據規格中的 verification 章節
# 建立測試腳本

範例：
創建 test_integration.py，包含：
- 測試核心類別初始化
- 測試基本功能
- 測試設定檔讀取
```

**展示：**
```
【步驟 5/5】建立測試腳本

✓ 已建立 test_integration.py

測試內容：
- 測試 1：APIManager 初始化
- 測試 2：設定檔讀取
- 測試 3：基本 API 呼叫（需要有效金鑰）

執行測試：
python test_integration.py
```

### 第 4 步：驗證整合

根據規格中的 `integration_guide.verification` 執行驗證：

```python
# 自動檢查
1. 檢查所有必要檔案是否存在
2. 檢查 Python import 是否正常
3. 執行測試腳本（如果使用者同意）

展示檢查清單
```

**展示：**
```
【整合驗證】

檔案結構檢查：
✓ config.yaml 存在
✓ utils/config.py 存在且可 import
✓ utils/api/api_manager.py 存在且可 import
✓ .env 檔案已建立
✓ .env 在 .gitignore 中

程式碼檢查：
✓ 找到 5 個檔案已更新
✓ 8 處硬編碼已替換
✓ 所有 import 語句正常

是否執行測試腳本驗證功能？(y/n)
```

**如果使用者選擇執行測試：**
```
執行測試中...

python test_integration.py

測試結果：
✓ 測試 1：APIManager 初始化 - PASSED
✓ 測試 2：設定檔讀取 - PASSED
✗ 測試 3：API 呼叫 - FAILED (需要填入有效的 API 金鑰)

2/3 測試通過。請在 .env 中填入有效金鑰後重新測試。
```

### 第 5 步：產生整合報告

```
【整合完成報告】

================================================================================
架構：API 設定與金鑰管理框架
版本：v1.0
整合時間：2026-02-10 12:00:00
================================================================================

✅ 整合成功！

【新增檔案】(4 個)
- config.yaml
- utils/config.py
- utils/api/api_manager.py
- .env

【修改檔案】(5 個)
- scripts/stage1.py (2 處變更)
- scripts/stage2.py (1 處變更)
- scripts/stage3.py (1 處變更)
- scripts/stage4.py (1 處變更)
- scripts/stage5.py (3 處變更)

【總計變更】
- 新增：4 個檔案
- 修改：5 個檔案
- 替換：8 處硬編碼
- 新增程式碼：約 300 行

【下一步操作】
1. 編輯 .env 檔案，填入您的 API 金鑰：
   API_KEYS=key1,key2,key3

2. 執行測試驗證：
   python test_integration.py

3. 開始使用：
   - 修改 config.yaml 可一鍵切換模型
   - 系統會自動輪替 API 金鑰
   - 查看日誌：utils/api/logs/

【相關文檔】
- 架構文檔：api_config_framework/README.md
- 系統規格：api_config_framework/api_config_framework_spec.yaml

【需要手動調整的部分】
⚠️ 無（所有整合已自動完成）

================================================================================
🎉 整合成功！您現在可以使用 {架構名稱} 的所有功能了！
================================================================================

是否將此報告儲存為檔案？(y/n)
```

**如果選擇儲存：**
```
✓ 已儲存整合報告：integration_report_20260210_120000.md
```

---

## 進階功能

### 功能 1：乾跑模式（Dry Run）

```bash
/framework-integrator --dry-run
```

只分析和預覽，不實際修改任何檔案：
- 顯示會建立哪些檔案
- 顯示會修改哪些程式碼
- 提供完整的變更預覽

### 功能 2：部分整合

```bash
/framework-integrator --steps 1,2,4
```

只執行特定步驟：
- 1: 複製檔案
- 2: 設定參數
- 3: 更新程式碼
- 4: 環境檔案
- 5: 測試腳本

### 功能 3：回滾整合

```bash
/framework-integrator --rollback
```

撤銷最近一次的整合：
- 刪除新增的檔案
- 還原修改的檔案（從備份）
- 清理相關設定

---

## 實作邏輯

### 核心演算法

```python
def integrate_framework(spec_path: str, project_path: str):
    """
    主要整合流程
    """
    # 1. 讀取規格
    spec = load_yaml(spec_path)
    framework_dir = get_framework_dir(spec_path)

    # 2. 分析專案
    project_info = analyze_project(project_path)

    # 3. 檢查衝突
    conflicts = check_conflicts(spec, project_info)
    if conflicts and not user_confirms(conflicts):
        return

    # 4. 執行整合步驟
    for step in spec['integration_guide']['integration_steps']:
        execute_step(step, spec, framework_dir, project_path)

    # 5. 驗證
    verification_results = verify_integration(spec, project_path)

    # 6. 產生報告
    report = generate_report(spec, project_info, verification_results)

    return report


def execute_step(step, spec, framework_dir, project_path):
    """
    執行單一整合步驟
    """
    step_type = step['title']

    if '複製' in step_type or 'copy' in step_type.lower():
        copy_template_files(framework_dir, project_path, spec)

    elif '設定' in step_type or 'config' in step_type.lower():
        configure_parameters(project_path, spec)

    elif '掃描' in step_type or 'scan' in step_type.lower():
        scan_and_update_code(project_path, spec)

    elif '環境' in step_type or 'env' in step_type.lower():
        setup_environment(project_path, spec)

    elif '測試' in step_type or 'test' in step_type.lower():
        create_test_script(project_path, spec)


def scan_and_update_code(project_path, spec):
    """
    掃描並更新程式碼

    這是最複雜的部分，需要：
    1. 識別需要修改的模式（從規格中讀取）
    2. 掃描所有相關檔案
    3. 執行替換（支援 regex）
    4. 新增必要的 import
    5. 保持程式碼格式
    """
    # 從規格中讀取替換規則
    replacement_rules = extract_replacement_rules(spec)

    # 掃描專案
    files = glob_python_files(project_path)

    changes = []
    for file in files:
        file_changes = apply_rules(file, replacement_rules)
        if file_changes:
            changes.append((file, file_changes))

    # 顯示預覽
    show_preview(changes)

    # 詢問確認
    if user_confirms():
        apply_changes(changes)
```

### 規格解析

```python
def extract_replacement_rules(spec):
    """
    從規格中提取程式碼替換規則

    規格中應該包含類似的章節：

    code_replacement_rules:
      - pattern: 'MODEL_NAME = "gemini-2.5-flash"'
        replacement: |
          from utils.config import get_model_name
          MODEL_NAME = get_model_name()
        description: "將硬編碼的模型名稱改為從設定檔讀取"

      - pattern: 'time.sleep\((\d+)\)'
        replacement: |
          from utils.config import get_api_call_interval
          time.sleep(get_api_call_interval())
        description: "將固定延遲改為可設定的間隔"
    """
    rules = spec.get('code_replacement_rules', [])
    return [Rule(r['pattern'], r['replacement'], r['description']) for r in rules]
```

---

## 錯誤處理

### 常見錯誤

1. **找不到規格檔案**
```
❌ 錯誤：未找到架構規格檔案

請確認：
1. 當前目錄或子目錄中有 *_spec.yaml 檔案
2. 或使用：/framework-integrator path/to/spec.yaml 指定路徑

提示：使用 /framework-architect 可以建立新的規格文檔
```

2. **檔案衝突**
```
⚠️ 警告：檔案衝突

以下檔案已存在，整合會覆蓋它們：
- config.yaml (已存在)
- utils/config.py (已存在)

選項：
1. 備份現有檔案後覆蓋（推薦）
2. 跳過這些檔案
3. 取消整合

您的選擇：
```

3. **Python 語法錯誤**
```
❌ 錯誤：程式碼替換後出現語法錯誤

檔案：scripts/stage1.py
錯誤：IndentationError: unexpected indent

已自動回滾此檔案的變更。

建議：
- 檢查原始檔案的縮排格式
- 或選擇手動整合此檔案
```

---

## 使用範例

### 範例 1：整合 API 管理框架

```
使用者：/framework-integrator

我：
🔍 掃描架構規格文檔...

找到：api_config_framework/api_config_framework_spec.yaml
架構：API 設定與金鑰管理框架

開始整合...

[執行完整流程]

✅ 整合完成！
已新增 4 個檔案，修改 7 個檔案。
```

### 範例 2：乾跑模式

```
使用者：/framework-integrator --dry-run

我：
🔍 【乾跑模式】預覽整合變更

將會建立的檔案：
- config.yaml
- utils/config.py
- utils/api/api_manager.py

將會修改的檔案：
- scripts/stage1.py (2 處)
- scripts/stage2.py (1 處)

將會替換的程式碼：
[顯示所有 diff 預覽]

⚠️ 這只是預覽，沒有實際修改任何檔案。
要執行整合，請使用：/framework-integrator
```

---

## 與其他工具的整合

### 與 Git 整合

```python
# 整合前自動建立 Git commit
def pre_integration_backup():
    """
    在整合前自動備份
    """
    if is_git_repo():
        # 檢查是否有未提交的變更
        if has_uncommitted_changes():
            show_warning("您有未提交的變更，建議先提交")
            if user_confirms("是否自動建立備份 commit？"):
                git_commit("Backup before framework integration")

        # 建立 branch（可選）
        if user_confirms("是否建立新分支進行整合？"):
            branch_name = f"integration/{framework_name}"
            git_checkout_branch(branch_name)
```

### 與測試框架整合

```python
# 整合後自動執行測試
def post_integration_test():
    """
    整合後自動測試
    """
    if exists("pytest.ini") or exists("tests/"):
        if user_confirms("是否執行專案測試？"):
            run_command("pytest tests/")
```

---

## 總結

此 skill 的核心價值：
1. **自動化整合**：一鍵完成所有整合步驟
2. **智慧分析**：自動掃描和識別需要修改的程式碼
3. **安全可靠**：乾跑模式、預覽變更、自動備份
4. **完整報告**：詳細記錄所有變更
5. **錯誤處理**：自動檢測並處理常見問題

與 `framework-architect` 搭配使用：
- **設計階段**：`/framework-architect` → 產生規格
- **整合階段**：`/framework-integrator` → 自動整合

讓架構的複用變得**快速**、**安全**、**可靠**！
