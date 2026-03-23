import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import quote

def get_latest_news(query="今日台股熱門焦點", max_results=5):
    """
    使用免費且穩定的 Google News RSS 抓取最新新聞
    不需要任何 API Key 且不會被阻擋
    """
    print(f"🔍 正在透過 Google新聞 搜尋 '{query}' 的最新報導...")
    results = []
    
    # 將關鍵字加上時間限制 (when:1d 代表一天內的新聞) 並轉碼
    encoded_query = quote(f"{query} when:1d")
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    
    try:
        # 發送 HTTP GET 請求 (偽裝成一般瀏覽器)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        # 解析 XML (RSS 格式)
        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')
        
        for item in items[:max_results]:
            title = item.find('title')
            link = item.find('link')
            pubDate = item.find('pubDate')
            source = item.find('source')
            
            title_text = title.text if title is not None else "無標題"
            link_text = link.text if link is not None else ""
            date_text = pubDate.text if pubDate is not None else ""
            source_text = source.text if source is not None else "未知來源"
            
            results.append({
                "title": title_text,
                "snippet": title_text, # Google新聞摘要通常是 HTML，這裡直接使用乾淨的標題作為重點
                "source": source_text,
                "url": link_text,
                "date": date_text
            })
            
        print(f"✅ 成功獲取 {len(results)} 則新聞。")
        return results
        
    except Exception as e:
        print(f"❌ 搜尋過程發生錯誤: {e}")
        return []

if __name__ == "__main__":
    # 本機測試方法
    news = get_latest_news()
    for n in news:
        print(f"- {n['title']} ({n['source']})")
