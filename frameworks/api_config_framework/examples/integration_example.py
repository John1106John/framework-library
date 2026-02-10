"""
API 設定與金鑰管理框架 - 整合範例

此範例展示如何在實際專案中使用本框架
"""

# ===== 範例 1：最簡單的使用方式 =====

def example_1_basic():
    """最基本的使用範例"""
    from utils.api.api_manager import APIManager

    # 初始化（自動從 config.yaml 讀取模型）
    manager = APIManager()

    # 呼叫 API
    prompt = "請用一句話介紹 Python 程式語言。"
    result = manager.generate_content(prompt)

    print(f"結果：{result}")


# ===== 範例 2：批次處理 + 呼叫間隔 =====

def example_2_batch_processing():
    """批次處理多個 prompt，並使用呼叫間隔"""
    from utils.api.api_manager import APIManager
    from utils.config import get_api_call_interval
    import time

    manager = APIManager()
    interval = get_api_call_interval()

    prompts = [
        "介紹 Python",
        "介紹 JavaScript",
        "介紹 Rust",
    ]

    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] 處理中...")
        result = manager.generate_content(f"請用一句話介紹 {prompt}")
        results.append(result)

        # 等待間隔（避免 rate limit）
        if i < len(prompts):
            time.sleep(interval)

    print("\n所有結果：")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")


# ===== 範例 3：帶圖片的多模態呼叫 =====

def example_3_multimodal():
    """帶圖片的 API 呼叫範例"""
    from utils.api.api_manager import APIManager
    from PIL import Image

    manager = APIManager()

    # 載入圖片
    image_path = "your_image.png"
    image = Image.open(image_path)

    # 呼叫 API（prompt + 圖片）
    prompt = "請描述這張圖片的內容。"
    result = manager.generate_content(prompt, images=[image])

    print(f"圖片描述：{result}")


# ===== 範例 4：錯誤處理與重試 =====

def example_4_error_handling():
    """完整的錯誤處理範例"""
    from utils.api.api_manager import APIManager

    manager = APIManager()

    try:
        result = manager.generate_content("你的 prompt")
        print(f"成功：{result}")

    except ValueError as e:
        # 金鑰設定錯誤
        print(f"設定錯誤：{e}")
        print("請檢查 .env 檔案是否正確設定 API 金鑰")

    except Exception as e:
        error_msg = str(e)

        if "所有 API 金鑰的配額都已用完" in error_msg:
            # 所有金鑰配額用完
            print("配額耗盡：請等待配額重置或新增更多金鑰")
        else:
            # 其他錯誤
            print(f"未知錯誤：{e}")


# ===== 範例 5：手動管理金鑰索引 =====

def example_5_manual_key_management():
    """手動管理金鑰索引"""
    from utils.api.api_manager import APIManager

    manager = APIManager()

    # 查看當前金鑰狀態
    info = manager.get_current_key_info()
    print(f"當前金鑰：#{info['index'] + 1}/{info['total_keys']}")
    print(f"剩餘金鑰：{info['remaining_keys']} 把")

    # 使用 API
    result = manager.generate_content("測試 prompt")

    # 手動重置金鑰索引（回到第一把）
    manager.reset_key_index()
    print("金鑰索引已重置到第一把")


# ===== 範例 6：自訂參數 =====

def example_6_custom_params():
    """使用自訂參數的範例"""
    from utils.config import get_config

    # 取得完整設定
    config = get_config()

    # 讀取自訂參數
    max_tokens = config.get("max_tokens", 1000)
    temperature = config.get("temperature", 0.7)

    print(f"Max Tokens: {max_tokens}")
    print(f"Temperature: {temperature}")

    # TODO: 將參數傳給 API 呼叫


# ===== 範例 7：動態切換模型 =====

def example_7_dynamic_model_switching():
    """動態切換模型的範例"""
    from utils.api.api_manager import APIManager

    # 使用預設模型（從 config.yaml 讀取）
    manager1 = APIManager()
    result1 = manager1.generate_content("測試預設模型")

    # 手動指定模型（覆蓋 config.yaml）
    manager2 = APIManager(model_name="gemini-2.0-flash-exp")
    result2 = manager2.generate_content("測試指定模型")

    print(f"預設模型結果：{result1}")
    print(f"指定模型結果：{result2}")


# ===== 範例 8：在多腳本專案中使用 =====

def example_8_multi_script_project():
    """多腳本專案的使用範例"""

    # script1.py
    # ------------------
    # from utils.config import get_model_name
    # from utils.api.api_manager import APIManager
    #
    # MODEL = get_model_name()  # 從 config.yaml 讀取
    # manager = APIManager(MODEL)
    #
    # result = manager.generate_content("Script 1 的 prompt")

    # script2.py
    # ------------------
    # from utils.config import get_model_name, get_api_call_interval
    # from utils.api.api_manager import APIManager
    # import time
    #
    # MODEL = get_model_name()  # 同樣的模型
    # interval = get_api_call_interval()
    #
    # manager = APIManager(MODEL)
    # result1 = manager.generate_content("Prompt 1")
    # time.sleep(interval)
    # result2 = manager.generate_content("Prompt 2")

    print("參考上方註解的程式碼範例")


# ===== 範例 9：整合到現有腳本（Before & After） =====

def example_9_migration():
    """從硬編碼遷移到框架的範例"""

    # Before: 硬編碼方式
    # ------------------
    # import google.generativeai as genai
    #
    # MODEL_NAME = "gemini-2.5-flash"  # 硬編碼
    # API_KEY = "AIzaSy..."  # 不安全
    #
    # genai.configure(api_key=API_KEY)
    # model = genai.GenerativeModel(MODEL_NAME)
    # response = model.generate_content("prompt")
    # result = response.text

    # After: 使用框架
    # ------------------
    from utils.api.api_manager import APIManager

    manager = APIManager()  # 自動從 config.yaml 讀取
    result = manager.generate_content("prompt")

    # 好處：
    # ✅ 模型名稱集中管理
    # ✅ API Key 安全儲存在 .env
    # ✅ 多金鑰自動輪替
    # ✅ 配額檢測與重試
    # ✅ 詳細日誌追蹤

    print(f"結果：{result}")


# ===== 範例 10：完整的生產環境使用 =====

def example_10_production_usage():
    """生產環境的完整使用範例"""
    from utils.api.api_manager import APIManager
    from utils.config import get_api_call_interval, get_model_name
    import time
    import logging

    # 設定日誌
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # 初始化
        manager = APIManager()
        logger.info(f"使用模型：{get_model_name()}")

        # 批次處理
        tasks = ["task1", "task2", "task3"]
        results = []

        for i, task in enumerate(tasks, 1):
            logger.info(f"處理任務 {i}/{len(tasks)}: {task}")

            try:
                result = manager.generate_content(f"處理：{task}")
                results.append({"task": task, "result": result, "status": "success"})

            except Exception as e:
                logger.error(f"任務 {task} 失敗：{e}")
                results.append({"task": task, "result": None, "status": "failed"})

            # 等待間隔
            if i < len(tasks):
                time.sleep(get_api_call_interval())

        # 輸出結果
        success_count = sum(1 for r in results if r["status"] == "success")
        logger.info(f"完成：{success_count}/{len(tasks)} 個任務成功")

        return results

    except Exception as e:
        logger.error(f"執行失敗：{e}")
        raise


# ===== 主程式 =====

if __name__ == "__main__":
    print("===== API 設定與金鑰管理框架 - 整合範例 =====\n")

    # 選擇要執行的範例
    examples = {
        1: ("基本使用", example_1_basic),
        2: ("批次處理", example_2_batch_processing),
        4: ("錯誤處理", example_4_error_handling),
        5: ("金鑰管理", example_5_manual_key_management),
        6: ("自訂參數", example_6_custom_params),
        7: ("動態切換模型", example_7_dynamic_model_switching),
        9: ("遷移範例", example_9_migration),
        10: ("生產環境", example_10_production_usage),
    }

    print("可用範例：")
    for num, (name, _) in examples.items():
        print(f"{num}. {name}")

    try:
        choice = int(input("\n請選擇範例編號（直接 Enter 執行範例 1）: ") or "1")
        if choice in examples:
            name, func = examples[choice]
            print(f"\n執行範例 {choice}：{name}\n")
            print("=" * 50)
            func()
            print("=" * 50)
        else:
            print("無效的選擇")
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n錯誤：{e}")
