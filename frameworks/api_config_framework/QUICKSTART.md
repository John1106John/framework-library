# 快速開始 - API 設定與金鑰管理框架

> 🚀 5 分鐘快速整合指南

---

## 📁 框架結構

```
api_config_framework/
├── README.md                          # 完整使用文檔
├── QUICKSTART.md                      # 本檔案（快速開始）
├── api_config_framework_spec.yaml     # 系統規格（給 AI 看）
│
├── templates/                         # 模板檔案（複製到你的專案）
│   ├── config.yaml.template          # → config.yaml
│   ├── config_loader.py.template     # → utils/config.py
│   ├── api_manager.py.template       # → utils/api/api_manager.py
│   └── .env.example                  # → .env
│
└── examples/                          # 範例程式碼
    └── integration_example.py        # 10 個整合範例
```

---

## ⚡ 5 步驟快速整合

### 步驟 1：複製檔案

```bash
# 在你的專案目錄執行
cp api_config_framework/templates/config.yaml.template config.yaml
cp api_config_framework/templates/config_loader.py.template utils/config.py
cp api_config_framework/templates/api_manager.py.template utils/api/api_manager.py
cp api_config_framework/templates/.env.example .env
```

### 步驟 2：設定 API 金鑰

編輯 `.env`：

```env
# 使用多個金鑰（推薦）
API_KEYS=key1,key2,key3,key4,key5

# 或使用單一金鑰
GOOGLE_API_KEY=your_api_key_here
```

**重要：** 確認 `.env` 在 `.gitignore` 中！

```bash
echo ".env" >> .gitignore
```

### 步驟 3：修改 config.yaml

```yaml
model_name: "gemini-2.5-flash"  # 改成你要用的模型
retry_delay: 2.0
api_call_interval: 2
```

### 步驟 4：在程式碼中使用

```python
from utils.api.api_manager import APIManager

# 初始化（自動從 config.yaml 讀取模型）
manager = APIManager()

# 呼叫 API
result = manager.generate_content("你的 prompt")
print(result)
```

### 步驟 5：測試

```bash
python -c "from utils.api.api_manager import APIManager; m = APIManager(); print(m.generate_content('Hello'))"
```

**完成！🎉**

---

## 🤖 給 AI 的整合指令

複製以下指令，請 AI 幫你整合：

```
請幫我將「API 設定與金鑰管理框架」整合到我的專案中。

專案路徑：[填入你的專案路徑]
使用的 API：Google Gemini / OpenAI / Anthropic（選一個）

請執行以下步驟：

1. 複製框架檔案
   - 從 api_config_framework/templates/ 複製 3 個模板檔案到我的專案
   - config.yaml.template → config.yaml（專案根目錄）
   - config_loader.py.template → utils/config.py
   - api_manager.py.template → utils/api/api_manager.py

2. 修改 API 設定（如果不是 Google Gemini）
   - 在 api_manager.py 中修改 import 和 API 呼叫邏輯
   - 根據我使用的 API 調整程式碼

3. 掃描並替換硬編碼
   - 找出所有硬編碼的模型名稱（如 "gemini-2.5-flash"）
   - 替換為 get_model_name()
   - 找出所有 time.sleep(2) 並替換為 time.sleep(get_api_call_interval())

4. 建立環境檔案
   - 複製 .env.example 為 .env
   - 確認 .env 在 .gitignore 中

5. 測試整合
   - 建立 test_integration.py 測試 API Manager

參考文件：
- api_config_framework/README.md（詳細文檔）
- api_config_framework/api_config_framework_spec.yaml（系統規格）
- api_config_framework/examples/integration_example.py（範例）
```

---

## 📚 進階功能

### 自訂參數

在 `config.yaml` 新增：

```yaml
max_tokens: 1000
temperature: 0.7
```

在 `utils/config.py` 新增 getter：

```python
def get_max_tokens() -> int:
    return int(_load_config().get("max_tokens", 1000))
```

### 金鑰管理

```python
# 查看金鑰狀態
info = manager.get_current_key_info()
print(info)  # {'index': 0, 'total_keys': 5, 'remaining_keys': 5}

# 手動重置金鑰
manager.reset_key_index()
```

### 錯誤處理

```python
try:
    result = manager.generate_content(prompt)
except ValueError as e:
    print("設定錯誤，請檢查 .env")
except Exception as e:
    if "配額都已用完" in str(e):
        print("等待配額重置或新增更多金鑰")
```

---

## 🔍 常見問題

| 問題 | 解決方案 |
|------|---------|
| FileNotFoundError: config.yaml | 確認 config.yaml 在專案根目錄 |
| 未找到任何 API 金鑰 | 檢查 .env 檔案格式 |
| ModuleNotFoundError: utils.config | 確認 utils/ 有 `__init__.py` |
| 所有金鑰都已嘗試過一輪 | 等待配額重置或新增更多金鑰 |

---

## 📖 完整文檔

- [README.md](README.md) - 完整使用指南
- [api_config_framework_spec.yaml](api_config_framework_spec.yaml) - 系統規格（給 AI）
- [examples/integration_example.py](examples/integration_example.py) - 10 個範例

---

## ✅ 檢查清單

整合完成後，確認：

- [ ] `config.yaml` 在專案根目錄
- [ ] `utils/config.py` 存在
- [ ] `utils/api/api_manager.py` 存在
- [ ] `.env` 檔案已設定金鑰
- [ ] `.env` 在 `.gitignore` 中
- [ ] 測試 API Manager 可正常運作
- [ ] 硬編碼的模型名稱已替換
- [ ] `time.sleep(2)` 已替換為 `get_api_call_interval()`

---

**🎯 目標：3 個檔案，5 分鐘整合，零程式碼變更！**
