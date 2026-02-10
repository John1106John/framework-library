# API 設定與金鑰管理框架

> 🚀 可重用的 AI API 集中式設定與自動循環金鑰輪替框架
>
> **Version:** 1.0.0 | **License:** MIT | **Last Updated:** 2026-02-10

---

## 📖 目錄

- [概述](#概述)
- [核心功能](#核心功能)
- [快速開始](#快速開始)
- [完整整合指南](#完整整合指南)
- [設定參考](#設定參考)
- [進階使用](#進階使用)
- [常見問題](#常見問題)
- [實際案例](#實際案例)

---

## 概述

### 為什麼需要這個框架？

在開發 AI 應用時，你是否遇到過：
- ❌ 要換模型需要修改多個檔案的硬編碼字串
- ❌ API 配額用完就停止，沒有自動重試機制
- ❌ 單一金鑰不穩定，想用多把金鑰但不知道怎麼實作
- ❌ 每個專案都要重寫 API 管理邏輯

### 這個框架解決了什麼？

- ✅ **集中式設定** - 改一處 `config.yaml` 就能切換所有腳本使用的模型
- ✅ **自動循環輪替** - 多把金鑰自動循環重試，最大化可用性
- ✅ **配額智慧檢測** - 自動識別 429/quota 錯誤並切換金鑰
- ✅ **詳細日誌追蹤** - 記錄每次 API 呼叫與金鑰切換
- ✅ **快速整合** - 3 個檔案即可整合到任何 Python 專案

---

## 核心功能

### 1. 集中式設定檔（config.yaml）

```yaml
# 一鍵切換模型
model_name: "gemini-2.5-flash"

# 統一管理參數
retry_delay: 2.0
api_call_interval: 2
```

**好處：** 改一處，全域生效！

### 2. 自動循環金鑰輪替

```
key1 → key2 → key3 → key1 → key2 → ...
（完整循環一圈後才停止）
```

**舊行為：** key1 → key2 → key3 → 停止（用完即死）
**新行為：** key1 → key2 → key3 → key1（循環重試）

### 3. 配額智慧檢測

自動識別以下錯誤並切換金鑰：
- `quota exceeded`
- `rate limit`
- `resource exhausted`
- HTTP `429`

### 4. 詳細日誌追蹤

```
[2026-02-10 10:00:00] 初始化 APIManager (模型: gemini-2.5-flash)
[2026-02-10 10:00:00] 配置 API 金鑰 #1/3: AIzaSyAB...XYZ1
[2026-02-10 10:00:05] API 呼叫成功 (耗時: 2.5秒, 金鑰: #1)
[2026-02-10 10:00:10] 配額限制錯誤，循環切換到金鑰 #2
```

---

## 快速開始

### 前置需求

- Python >= 3.8
- 已安裝 `pyyaml`, `python-dotenv`

```bash
pip install pyyaml python-dotenv
```

### 5 分鐘快速整合

#### 1. 複製核心檔案

```bash
# 從框架目錄複製到你的專案
cp api_config_framework/templates/config.yaml.template your_project/config.yaml
cp api_config_framework/templates/config_loader.py.template your_project/utils/config.py
cp api_config_framework/templates/api_manager.py.template your_project/utils/api/api_manager.py
```

#### 2. 設定環境變數

建立 `.env` 檔案：

```env
# 方法一：使用單一金鑰
GOOGLE_API_KEY=your_api_key_here

# 方法二：使用多個金鑰（推薦）
API_KEYS=key1,key2,key3,key4,key5
```

**重要：** 確認 `.env` 在 `.gitignore` 中！

#### 3. 修改 config.yaml

```yaml
model_name: "gemini-2.5-flash"  # 改成你要用的模型
retry_delay: 2.0
api_call_interval: 2
```

#### 4. 在程式碼中使用

```python
from utils.api.api_manager import APIManager

# 初始化（自動從 config.yaml 讀取模型）
manager = APIManager()

# 呼叫 API
result = manager.generate_content("你的 prompt")
print(result)
```

**就這麼簡單！🎉**

---

## 完整整合指南

### 步驟 1：專案準備

#### 1.1 建立目錄結構

```bash
your_project/
├── config.yaml          # 新增
├── .env                 # 新增
├── .env.example         # 新增（模板）
├── utils/
│   ├── __init__.py
│   ├── config.py        # 新增
│   └── api/
│       ├── __init__.py
│       └── api_manager.py  # 新增
└── scripts/
    └── your_script.py
```

#### 1.2 複製模板檔案

從 `api_config_framework/templates/` 複製以下檔案：
- `config.yaml.template` → `config.yaml`
- `config_loader.py.template` → `utils/config.py`
- `api_manager.py.template` → `utils/api/api_manager.py`

### 步驟 2：修改模板（根據你使用的 API）

#### 2.1 修改 `api_manager.py`

**如果使用 Google Gemini：** 不需要修改，直接使用！

**如果使用其他 API（如 OpenAI）：**

```python
# 1. 修改 import
# from:
import google.generativeai as genai

# to:
import openai

# 2. 修改 _load_api_keys()
single_key = os.getenv("OPENAI_API_KEY", "")  # 改環境變數名稱

# 3. 修改 _configure_current_key()
openai.api_key = current_key  # 改設定方式

# 4. 修改 generate_content()
response = openai.ChatCompletion.create(
    model=self.model_name,
    messages=[{"role": "user", "content": prompt}]
)
return response.choices[0].message.content.strip()
```

#### 2.2 修改 `.env`

```env
# Google Gemini
GOOGLE_API_KEY=your_key
API_KEYS=key1,key2,key3

# OpenAI
OPENAI_API_KEY=your_key
API_KEYS=key1,key2,key3

# Anthropic Claude
ANTHROPIC_API_KEY=your_key
API_KEYS=key1,key2,key3
```

### 步驟 3：整合到現有程式碼

#### 3.1 替換硬編碼的模型名稱

**Before:**
```python
MODEL_NAME = "gemini-2.5-flash"
```

**After:**
```python
from utils.config import get_model_name

MODEL_NAME = get_model_name()
```

#### 3.2 替換 API 呼叫邏輯

**Before:**
```python
import google.generativeai as genai

genai.configure(api_key="your_key")
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)
result = response.text
```

**After:**
```python
from utils.api.api_manager import APIManager

manager = APIManager()
result = manager.generate_content(prompt)
```

#### 3.3 替換 time.sleep

**Before:**
```python
import time
time.sleep(2)
```

**After:**
```python
from utils.config import get_api_call_interval
import time

time.sleep(get_api_call_interval())
```

### 步驟 4：測試整合

```python
# test_integration.py
from utils.api.api_manager import APIManager

def test_api_manager():
    manager = APIManager()

    # 測試 1：基本呼叫
    result = manager.generate_content("Hello, world!")
    print(f"✓ 基本呼叫成功：{result[:50]}...")

    # 測試 2：取得金鑰狀態
    info = manager.get_current_key_info()
    print(f"✓ 金鑰狀態：{info}")

    # 測試 3：重置金鑰
    manager.reset_key_index()
    print("✓ 金鑰重置成功")

if __name__ == "__main__":
    test_api_manager()
```

---

## 設定參考

### config.yaml 完整說明

```yaml
# ===== 必要參數 =====

# AI 模型名稱（必填）
model_name: "gemini-2.5-flash"
# 可選值：
#   - Google Gemini: "gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"
#   - OpenAI: "gpt-4-turbo", "gpt-3.5-turbo"
#   - Anthropic: "claude-3-opus", "claude-3-sonnet"

# 配額重試延遲秒數（選填，預設 2.0）
retry_delay: 2.0
# 說明：當金鑰配額用盡時，等待此秒數再重試

# API 呼叫間隔秒數（選填，預設 2）
api_call_interval: 2
# 說明：同腳本內連續 API 呼叫之間的等待時間，避免觸發 rate limit

# ===== 專案特定參數（可選） =====

# 範例：
max_tokens: 1000
temperature: 0.7
top_p: 0.9
```

### 環境變數說明

| 變數名稱 | 說明 | 優先順序 | 格式 |
|---------|------|---------|------|
| `API_KEYS` | 多個金鑰（推薦） | 1（最高） | `key1,key2,key3` |
| `GOOGLE_API_KEY` | 單一金鑰 | 2 | `your_key` |

**注意：** 如果同時設定，會優先使用 `API_KEYS`

---

## 進階使用

### 1. 自訂參數

在 `config.yaml` 新增參數：

```yaml
max_tokens: 1000
temperature: 0.7
```

在 `utils/config.py` 新增 getter：

```python
def get_max_tokens() -> int:
    return int(_load_config().get("max_tokens", 1000))

def get_temperature() -> float:
    return float(_load_config().get("temperature", 0.7))
```

使用：

```python
from utils.config import get_max_tokens, get_temperature

max_tokens = get_max_tokens()
temperature = get_temperature()
```

### 2. 在 UI 中顯示設定

```python
import streamlit as st
from utils.config import get_model_name, get_retry_delay

st.sidebar.caption(f"模型：`{get_model_name()}`")
st.sidebar.caption(f"重試延遲：`{get_retry_delay()}s`")
```

### 3. 動態重新載入設定

```python
from utils.config import reload_config, get_model_name

# 原本的模型
print(get_model_name())  # gemini-2.5-flash

# 修改 config.yaml 後重新載入
reload_config()
print(get_model_name())  # gemini-2.0-flash-exp
```

### 4. 手動重置金鑰索引

```python
manager = APIManager()

# 使用了一陣子後，想從頭開始
manager.reset_key_index()

# 下次 API 呼叫會使用第一把金鑰
```

---

## 常見問題

### Q1: FileNotFoundError: config.yaml

**原因：** config.yaml 不在專案根目錄

**解決：**
1. 確認 config.yaml 在專案根目錄
2. 檢查 `utils/config.py` 中的 `_CONFIG_PATH` 是否正確

### Q2: 未找到任何 API 金鑰

**原因：** .env 檔案不存在或格式錯誤

**解決：**
1. 確認 .env 檔案存在
2. 確認格式正確（`API_KEYS=key1,key2` 或 `GOOGLE_API_KEY=key`）
3. 確認沒有多餘的空格或引號

### Q3: ModuleNotFoundError: utils.config

**原因：** utils/ 目錄缺少 `__init__.py`

**解決：**
```bash
touch utils/__init__.py
touch utils/api/__init__.py
```

### Q4: 所有 API 金鑰都已嘗試過一輪

**原因：** 所有金鑰配額都用完了

**解決方案：**
1. 等待配額重置（通常是每分鐘或每天）
2. 新增更多金鑰到 `.env`
3. 升級 API 方案以獲得更高配額

### Q5: 如何切換到其他 API（如 OpenAI）？

**步驟：**
1. 修改 `api_manager.py` 的 import 和 API 呼叫邏輯
2. 修改 `.env` 的環境變數名稱
3. 修改 `config.yaml` 的 `model_name`

詳見「完整整合指南 > 步驟 2」

---

## 實際案例

### 案例 1：ETF 分析報告生成系統

**專案：** 台美 ETF 淨流量分析月報

**整合前：**
- 7 個 Stage 腳本各自硬編碼模型名稱
- 單一金鑰，配額用完就停止
- 沒有日誌追蹤

**整合後：**
- 改一處 `config.yaml` 就能切換所有 Stage 的模型
- 5 把金鑰自動循環輪替，穩定性提升 5 倍
- 詳細日誌追蹤所有 API 呼叫

**結果：** 從每月手動調整變成完全自動化！

### 案例 2：多語言翻譯服務

**整合方式：**
```python
# scripts/translate.py
from utils.api.api_manager import APIManager
from utils.config import get_api_call_interval
import time

manager = APIManager()

for text in texts:
    result = manager.generate_content(f"翻譯：{text}")
    translations.append(result)
    time.sleep(get_api_call_interval())
```

**效果：** 大量翻譯任務中，自動輪替金鑰避免配額限制！

---

## 與 AI 協作整合

### 給 AI 的整合指令範例

```
請幫我將「API 設定與金鑰管理框架」整合到我的專案中。

專案資訊：
- 專案路徑：/path/to/my/project
- 使用的 API：Google Gemini / OpenAI / Anthropic
- 現有腳本：scripts/script1.py, scripts/script2.py

請執行：
1. 複製 api_config_framework/templates/ 中的 3 個檔案到我的專案
2. 根據我使用的 API 修改 api_manager.py
3. 掃描我的專案，找出所有硬編碼的模型名稱並替換
4. 找出所有 time.sleep(2) 並替換為 get_api_call_interval()
5. 建立 .env.example 模板

參考文件：api_config_framework/README.md
系統規格：api_config_framework/api_config_framework_spec.yaml
```

---

## 延伸閱讀

- [api_config_framework_spec.yaml](api_config_framework_spec.yaml) - 完整系統規格
- [Prompt 管理系統](../prompt_management_spec/README_PROMPT_SPEC.md) - 可搭配使用

---

## 授權

MIT License - 自由使用、修改、分發

---

## 變更日誌

### v1.0.0 (2026-02-10)
- ✨ 初始版本發布
- ✅ 支援 Google Gemini API
- ✅ 自動循環金鑰輪替
- ✅ 集中式 config.yaml 設定
- ✅ 詳細日誌追蹤

---

**🎯 快速開始：只需 3 個檔案，5 分鐘整合！**
