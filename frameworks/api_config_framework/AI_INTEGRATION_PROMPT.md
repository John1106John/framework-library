# AI 整合指令 - API 設定與金鑰管理框架

> 📋 複製本檔案的指令，直接提供給 AI 助手使用

---

## 🤖 完整整合指令（複製使用）

```
請幫我將「API 設定與金鑰管理框架」整合到我的專案中。

專案資訊：
- 專案路徑：[填入你的專案路徑]
- 使用的 API：Google Gemini / OpenAI / Anthropic（選一個）
- 現有腳本位置：[填入腳本路徑，如 scripts/]

請執行以下步驟：

### 步驟 1：複製框架檔案
從 api_config_framework/templates/ 複製 4 個模板檔案到我的專案：
- config.yaml.template → config.yaml（專案根目錄）
- config_loader.py.template → utils/config.py
- api_manager.py.template → utils/api/api_manager.py
- .env.example → .env（專案根目錄）

### 步驟 2：修改 API 設定（如果不是 Google Gemini）
如果我使用的不是 Google Gemini API，請修改 api_manager.py：
1. 修改 import 語句（如改為 import openai）
2. 修改 _load_api_keys() 中的環境變數名稱
3. 修改 _configure_current_key() 的 API 設定方式
4. 修改 generate_content() 的 API 呼叫邏輯

### 步驟 3：掃描並替換硬編碼
掃描我的專案中所有 Python 腳本，找出並替換：
1. 硬編碼的模型名稱（如 "gemini-2.5-flash", "gpt-4", "claude-3"）
   - 替換為：from utils.config import get_model_name; MODEL = get_model_name()
2. 硬編碼的 API 呼叫邏輯
   - 替換為：from utils.api.api_manager import APIManager; manager = APIManager()
3. time.sleep(2) 或其他固定延遲
   - 替換為：from utils.config import get_api_call_interval; time.sleep(get_api_call_interval())

### 步驟 4：設定環境檔案
1. 編輯 .env 檔案，加入我的 API 金鑰
2. 確認 .env 已加入 .gitignore
3. 如果 .gitignore 不存在，請建立並加入 .env

### 步驟 5：設定 config.yaml
編輯 config.yaml，設定我要使用的模型：
- model_name: 改為我的目標模型
- retry_delay: 配額重試延遲（建議 2.0）
- api_call_interval: API 呼叫間隔（建議 2）

### 步驟 6：建立測試腳本
建立 test_integration.py 測試檔案，驗證整合是否成功：
- 測試 APIManager 初始化
- 測試基本的 API 呼叫
- 測試金鑰狀態查詢
- 輸出測試結果

### 步驟 7：整合報告
完成後，請提供：
1. 修改了哪些檔案（列出檔案路徑）
2. 替換了多少處硬編碼
3. 是否需要我手動調整的部分
4. 測試腳本的執行結果

參考文件：
- api_config_framework/README.md（完整使用文檔）
- api_config_framework/QUICKSTART.md（5 分鐘快速指南）
- api_config_framework/api_config_framework_spec.yaml（系統規格 - 給 AI 看）
- api_config_framework/examples/integration_example.py（10 個整合範例）

注意事項：
- 確保 utils/ 目錄有 __init__.py
- 確保 utils/api/ 目錄有 __init__.py
- 不要提交 .env 到版本控制
- 保留原始腳本的備份
```

---

## 🎯 簡化版指令（快速整合）

```
請將 api_config_framework 整合到我的專案：

專案路徑：[你的專案路徑]
使用 API：[Google Gemini / OpenAI / Anthropic]

步驟：
1. 複製 templates/ 中的 4 個檔案到專案對應位置
2. 根據我的 API 修改 api_manager.py（如果不是 Gemini）
3. 掃描專案，替換所有硬編碼的模型名稱和 API 呼叫
4. 建立 .env 並確保在 .gitignore 中
5. 建立測試腳本驗證整合

參考：api_config_framework/QUICKSTART.md
```

---

## 📋 使用方式

### 方法 1：完整整合
1. 複製上方「完整整合指令」區塊
2. 填入你的專案資訊（路徑、API 類型、腳本位置）
3. 提供給 AI 助手（Claude、ChatGPT 等）
4. AI 會自動執行所有步驟並提供報告

### 方法 2：快速整合
1. 複製「簡化版指令」區塊
2. 填入基本資訊（專案路徑和 API 類型）
3. 提供給 AI 助手
4. 適合簡單專案的快速整合

### 方法 3：自訂整合
根據你的需求，從完整指令中選擇需要的步驟：
- 只需要集中式設定？→ 只執行步驟 1、3、5
- 只需要金鑰輪替？→ 只執行步驟 1、2、4
- 需要完整功能？→ 執行所有步驟

---

## 🔧 常見自訂需求

### 需求 1：只整合到單一腳本

```
請將 API 設定框架整合到我的單一腳本：script.py

步驟：
1. 複製 config.yaml.template → config.yaml
2. 複製 config_loader.py.template → utils/config.py
3. 複製 api_manager.py.template → utils/api/api_manager.py
4. 在 script.py 中替換 API 呼叫邏輯
5. 建立 .env 並設定金鑰

參考：api_config_framework/examples/integration_example.py 範例 1
```

### 需求 2：多腳本專案批次整合

```
請批次整合到我的多個腳本：scripts/script1.py, scripts/script2.py, ...

步驟：
1. 複製框架檔案到專案
2. 掃描 scripts/ 目錄下所有 .py 檔案
3. 對每個檔案：
   - 替換硬編碼模型名稱
   - 替換 API 呼叫邏輯
   - 替換 time.sleep()
4. 建立整合測試腳本
5. 輸出修改報告

參考：api_config_framework/examples/integration_example.py 範例 8
```

### 需求 3：整合到 Streamlit/Gradio UI

```
請將 API 設定框架整合到我的 UI 應用（Streamlit/Gradio）：

步驟：
1. 複製框架檔案到專案
2. 在 UI 腳本中：
   - 加入 APIManager 初始化
   - 在 sidebar 顯示當前設定（模型、金鑰數量）
   - 加入「重置金鑰」按鈕
   - 加入錯誤處理提示
3. 測試 UI 功能

參考：README.md「進階使用 > 2. 在 UI 中顯示設定」
```

### 需求 4：從現有硬編碼遷移

```
我的專案現在是硬編碼方式，請幫我遷移到框架：

現狀：
- 模型名稱寫死在程式碼中
- API Key 寫死或用環境變數
- 沒有重試機制
- 沒有金鑰輪替

請幫我：
1. 安裝框架
2. 重構所有 API 呼叫邏輯
3. 移除所有硬編碼
4. 加入錯誤處理和重試
5. 提供 Before/After 對照

參考：api_config_framework/examples/integration_example.py 範例 9
```

---

## 📖 框架功能說明（給 AI 參考）

此框架提供以下核心功能：

### 1. 集中式設定（config.yaml）
- 一處修改，全域生效
- 統一管理：模型名稱、重試延遲、呼叫間隔等參數
- 支援自訂參數擴充

### 2. 自動循環金鑰輪替
- 多把金鑰自動輪替：key1 → key2 → key3 → key1（循環）
- 智慧配額檢測：自動識別 429、quota、rate limit 錯誤
- 循環保護：完整輪替一圈後停止，避免無限重試
- 手動重置：支援透過 reset_key_index() 重置到第一把金鑰

### 3. 詳細日誌追蹤
- 記錄所有 API 呼叫（時間、耗時、金鑰索引）
- 記錄金鑰切換事件
- 記錄錯誤和重試過程
- 日誌檔案位置：utils/api/logs/api_YYYYMMDD.log

### 4. 易於整合
- 只需 3-4 個核心檔案
- 最小化程式碼變更
- 支援多種 API：Google Gemini、OpenAI、Anthropic 等
- 提供完整模板和 10 個範例程式

### 5. 錯誤處理機制
- 自動重試機制
- 配額錯誤自動切換金鑰
- 非配額錯誤直接拋出（避免無效重試）
- 詳細錯誤訊息記錄

---

## ✅ 整合檢查清單（給 AI 使用）

整合完成後，請 AI 確認以下項目：

**檔案結構：**
- [ ] config.yaml 在專案根目錄
- [ ] utils/config.py 存在且可正常 import
- [ ] utils/api/api_manager.py 存在且可正常 import
- [ ] utils/__init__.py 存在
- [ ] utils/api/__init__.py 存在

**環境設定：**
- [ ] .env 檔案已建立
- [ ] .env 中已設定 API 金鑰（API_KEYS 或單一金鑰）
- [ ] .env 已加入 .gitignore

**程式碼整合：**
- [ ] 所有硬編碼的模型名稱已替換為 get_model_name()
- [ ] 所有硬編碼的 API 呼叫已替換為 APIManager
- [ ] 所有 time.sleep(固定值) 已替換為 get_api_call_interval()

**測試驗證：**
- [ ] 建立了測試腳本
- [ ] 測試腳本執行成功
- [ ] API 呼叫正常運作
- [ ] 金鑰輪替功能正常

**文件報告：**
- [ ] 提供了修改檔案清單
- [ ] 提供了替換統計（幾處硬編碼）
- [ ] 提供了測試結果
- [ ] 說明需要手動調整的部分（如有）

---

## 🎓 範例對話

### 範例 1：完整整合對話

**用戶：**
```
請將 api_config_framework 完整整合到我的專案

專案路徑：/home/user/my_project
使用 API：Google Gemini
現有腳本：scripts/generate.py, scripts/analyze.py
```

**AI 預期回應：**
```
我會幫您完整整合 API 設定框架到您的專案中。

【步驟 1：複製框架檔案】
✓ 已複製 config.yaml 到專案根目錄
✓ 已複製 utils/config.py
✓ 已複製 utils/api/api_manager.py
✓ 已複製 .env（請填入您的 API 金鑰）

【步驟 2：掃描專案】
發現 2 個腳本需要修改：
- scripts/generate.py：發現 2 處硬編碼
  * 第 15 行：MODEL_NAME = "gemini-2.5-flash"
  * 第 42 行：time.sleep(2)
- scripts/analyze.py：發現 3 處硬編碼
  * 第 10 行：MODEL_NAME = "gemini-2.5-flash"
  * 第 28 行：API 呼叫邏輯
  * 第 35 行：time.sleep(2)

【步驟 3：執行替換】
✓ scripts/generate.py - 已替換 2 處
✓ scripts/analyze.py - 已替換 3 處

【步驟 4：建立測試腳本】
✓ 已建立 test_integration.py

【步驟 5：更新 .gitignore】
✓ 已確認 .env 在 .gitignore 中

【整合完成報告】
✅ 已複製 4 個框架檔案
✅ 已掃描 2 個腳本
✅ 已替換 5 處硬編碼
✅ 已建立測試腳本
✅ 已更新 .gitignore

【下一步操作】
1. 編輯 .env 檔案，填入您的 API 金鑰：
   API_KEYS=key1,key2,key3

2. 執行測試驗證：
   python test_integration.py

3. （可選）修改 config.yaml 切換模型

【需要注意】
- 請確保您有有效的 Google Gemini API 金鑰
- 建議使用 3-5 把金鑰以提高穩定性
- 第一次執行時會在 utils/api/ 建立 logs/ 目錄
```

### 範例 2：單腳本快速整合

**用戶：**
```
我只想在 script.py 中使用這個框架
```

**AI 預期回應：**
```
我會幫您快速整合到單一腳本。

【執行整合】
✓ 已複製必要檔案（config.yaml, utils/config.py, utils/api/api_manager.py）
✓ 已修改 script.py（替換 1 處硬編碼）
✓ 已建立 .env 模板

【script.py 的變更】
Before:
  MODEL_NAME = "gemini-2.5-flash"
  genai.configure(api_key="your_key")
  model = genai.GenerativeModel(MODEL_NAME)
  response = model.generate_content(prompt)

After:
  from utils.api.api_manager import APIManager
  manager = APIManager()
  response = manager.generate_content(prompt)

【下一步】
在 .env 中設定：API_KEYS=key1,key2,key3

【完成】
現在 script.py 已整合框架，享受自動金鑰輪替功能！
```

---

## 💡 使用提示

### 給用戶的提示：
1. **選擇合適的指令版本**
   - 完整專案 → 使用「完整整合指令」
   - 簡單需求 → 使用「簡化版指令」
   - 特殊需求 → 參考「常見自訂需求」

2. **填寫專案資訊時要具體**
   - 專案路徑要填寫完整絕對路徑
   - 明確指定使用的 API 類型
   - 列出需要修改的腳本檔案

3. **整合後的檢查**
   - 執行測試腳本確認功能正常
   - 檢查日誌檔案確認 API 呼叫記錄
   - 嘗試修改 config.yaml 測試集中式設定

### 給 AI 的提示：
1. **完整性**
   - 確保所有檔案都正確複製
   - 確保所有硬編碼都被替換
   - 確保 __init__.py 檔案存在

2. **安全性**
   - 提醒用戶不要提交 .env
   - 確認 .gitignore 設定正確
   - 保留原始檔案備份（建議）

3. **報告清晰**
   - 列出所有修改的檔案
   - 提供統計數據（替換了幾處）
   - 說明下一步操作
   - 標註需要手動調整的部分

---

## 📚 相關文件

- **完整使用文檔**：[README.md](README.md)
- **快速開始指南**：[QUICKSTART.md](QUICKSTART.md)
- **系統規格（給 AI）**：[api_config_framework_spec.yaml](api_config_framework_spec.yaml)
- **整合範例程式**：[examples/integration_example.py](examples/integration_example.py)

---

## 🔄 版本資訊

- **版本**：1.0.0
- **最後更新**：2026-02-10
- **授權**：MIT License

---

## 📝 使用範例

### 快速複製指令（最常用）

直接複製以下內容給 AI：

```
請將 api_config_framework 整合到我的專案：
- 專案路徑：[你的路徑]
- 使用 API：Google Gemini
- 腳本位置：scripts/

參考：api_config_framework/AI_INTEGRATION_PROMPT.md 的完整整合指令
```

AI 會自動讀取本檔案並執行完整整合流程。

---

**🎯 這個檔案的目的：讓您可以快速複製指令，請 AI 幫您整合框架到任何專案！**
