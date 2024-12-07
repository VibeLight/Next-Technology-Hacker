import feedparser

def fetch_rss(rss_url):
    try:
        feed = feedparser.parse(rss_url)
        return [{"title": entry.title, "link": entry.link} for entry in feed.entries]
    except Exception as e:
        return [{"error": str(e)}]
