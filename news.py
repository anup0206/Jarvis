import requests
import os

# Fetch news using NewsAPI
def get_news_headlines(country="np", limit=3):  # 'np' is the correct ISO code for Nepal
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return ["News API key is missing. Please set NEWS_API_KEY in environment."]

    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return [f"Failed to fetch news. Status code: {response.status_code}"]

        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return ["I couldn't find any news articles at the moment."]
        
        headlines = []
        for i, article in enumerate(articles[:limit], start=1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            headlines.append(f"Headline {i}: {title} — from {source}")
        return headlines

    except Exception as e:
        return [f"[News Error]: {str(e)}"]
