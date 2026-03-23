import os
from google import genai

def analyze_news(news_list, keyword="今日台股熱門焦點"):
    """
    使用最新版 Gemini Flash 模型分析新聞情緒與重點
    """
    if not news_list:
        return "⚠️ 今日無相關新聞可供分析，請稍後再試。"

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        return "❌ 尚未設定 GEMINI_API_KEY。請在 .env 檔案中填寫。"

    print("🧠 正在使用滿血版 Gemini 2.0 Flash 進行新聞情緒分析...")
    
    # 組合新聞內容交給 LLM
    news_text = ""
    for idx, news in enumerate(news_list, 1):
        news_text += f"[{idx}] 標題：{news['title']}\n"
        news_text += f"來源：{news['source']}\n"
        news_text += f"摘要：{news['snippet']}\n"
        news_text += f"連結：{news['url']}\n\n"

    # 設定給 Gemini 的指示框架 (Prompt)
    prompt = f"""
請你扮演一位資深的財經分析師。
請根據以下我今天蒐集到關於「{keyword}」的最新新聞，產生一份適合在手機通訊軟體 (LINE/Telegram) 閱讀的簡明繁體中文重點包。

🗞️ 新聞內容如下：
{news_text}

請嚴格依照以下格式與要求輸出報告，並多使用適當的 emoji 增加可讀性：

🌟 【今日 {keyword} 重點總整理】 🌟

1. 📊 整體市場情緒：
(明確標示為 🟢正面 / 🔴負面 / 🟡中立，並用 1-2 句話簡述原因)

2. 💡 重點新聞摘要：
(請條列式列出 3-5 個最重要的新聞核心重點，每點不超過 30 字，需濃縮資訊)

3. 🔎 消息面與來源評估：
(簡單分析這批新聞來源的多元性及可靠性，例如是否多為官方數據或特定媒體風向)

4. 📖 推薦閱讀連結：
(請從上面的新聞中選出 1 到 2 篇最具代表性的新聞，附上標題與連結)
"""

    try:
        # 初始化 Gemini Client
        client = genai.Client(api_key=api_key)
        
        # 呼叫最新的 Gemini 2.5 Flash 模型
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        print("✅ LLM 分析生成完成。")
        return response.text
        
    except Exception as e:
        err_msg = f"❌ Gemini 分析過程發生錯誤: {e}"
        print(err_msg)
        return err_msg

if __name__ == "__main__":
    # 本地端測試方法
    print("請先從 main.py 執行測試。")
