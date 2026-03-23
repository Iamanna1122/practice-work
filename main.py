import os
import sys
from dotenv import load_dotenv

# 載入我們的自訂模組
from search_module import get_latest_news
from llm_module import analyze_news
from notify_module import push_notification

def main():
    print("==========================================")
    print("🚀 啟動程式：每日新聞情緒分析與推播機器人")
    print("==========================================")
    
    # 首先檢查是否存在 .env 檔案
    if not os.path.exists(".env"):
        print("❌ 找不到 .env 檔案！")
        print("請將 .env.example 複製一份命名為 .env，並填寫您的 API 金鑰。")
        sys.exit(1)

    # 載入環境變數
    load_dotenv()
    
    # =========== 步驟 1: 利用搜尋引擎蒐集資訊 ===========
    # 您可以自行修改此字串來隨時變更追蹤的主題
    keyword = "今日台股熱門焦點"
    news_data = get_latest_news(query=keyword, max_results=6)
    
    if not news_data:
        print("❌ 找不到新聞，程式提前結束。")
        sys.exit()
        
    # =========== 步驟 2: 呼叫 Gemini 進行報告生成 ===========
    report_text = analyze_news(news_data, keyword)
    
    print("\n------------------------------")
    print("📝 最終生成的 AI 簡報如下：")
    print("------------------------------")
    print(report_text)
    print("------------------------------\n")
    
    # =========== 步驟 3: 通知 (LINE/Telegram) ===========
    push_notification(report_text)
    
    # =========== 步驟 4: 將報告儲存成本地檔案 (供 GitHub 備份) ===========
    import datetime
    os.makedirs("reports", exist_ok=True)
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    file_path = f"reports/news_report_{today_str}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"💾 報告已自動存檔至：{file_path}，準備進行備份！")
        
    print("🏁 全部流程執行完畢。")

if __name__ == "__main__":
    main()
