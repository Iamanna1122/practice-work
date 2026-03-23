import os
import requests

def send_telegram_message(message):
    """傳送訊息到 Telegram Bot"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id or bot_token == "your_telegram_bot_token_here":
        print("⏭️ 未設定 Telegram 資訊，略過 Telegram 發送功能。")
        return False
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        # 使用 MarkdownV2 回傳容易有格式錯誤，使用純文字或是 HTML 較保險，這裡使用預設
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Telegram 訊息成功推播發送！")
        return True
    except Exception as e:
        print(f"❌ Telegram 發送失敗: {e}\n回傳內容: {response.text}")
        return False

def send_line_message(message):
    """傳送訊息到 LINE Bot (Messaging API)"""
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")
    
    if not channel_access_token or not user_id or channel_access_token == "your_line_channel_access_token_here":
        print("⏭️ 未設定 LINE 資訊，略過 LINE 發送功能。")
        return False

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}"
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ LINE 訊息成功推播發送！")
        return True
    except Exception as e:
        print(f"❌ LINE 發送失敗: {e}\n回傳內容: {response.text}")
        return False

def push_notification(message):
    """同時嘗試推播到所有已設定的平台"""
    print("📤 準備發送每日報表...")
    tg_sent = send_telegram_message(message)
    line_sent = send_line_message(message)
    
    if not tg_sent and not line_sent:
        print("⚠️ 警告：沒有任何通訊軟體發送成功，請檢查您的 .env 設定。")
    return tg_sent or line_sent
