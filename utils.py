import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os
from collections import Counter
import nltk
# Download NLTK data (only needed once)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading punkt_tab...")
    nltk.download('punkt_tab', download_dir=r"C:\Users\somas\Documents\TTS App\.venv\nltk_data")

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading stopwords...")
    nltk.download('stopwords', download_dir=r"C:\Users\somas\Documents\TTS App\.venv\nltk_data")

print(nltk.data.path)
def fetch_articles(company_name, num_articles=10):
    articles = []
    search_url = f"https://www.bbc.co.uk/search?q={company_name}&filter=news"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract links to news articles
        news_links = []
        for item in soup.find_all("a", href=True):
            link = item["href"]
            if "/news/" in link and link.startswith("https://www.bbc.co.uk/news/"):
                news_links.append(link)
        
        # Fetch article summaries
        for link in news_links[:num_articles]:
            article_response = requests.get(link, headers=headers, timeout=10)
            article_soup = BeautifulSoup(article_response.text, "html.parser")
            title = article_soup.find("h1")
            summary_tag = article_soup.find("meta", {"name": "description"})
            
            articles.append({
                "title": title.get_text(strip=True) if title else "No title",
                "summary": summary_tag["content"] if summary_tag else "Summary not available.",
                "source": "BBC News",
                "link": link
            })

        if not articles:
            raise Exception("No articles found from BBC News.")

    except requests.RequestException as e:
        print(f"BBC scraping failed: {e}")
        return []

    return articles

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def extract_topics(text, num_topics=3):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    return [word for word, _ in Counter(filtered_words).most_common(num_topics)]

def comparative_analysis(report):
    sentiments = [article["Sentiment"] for article in report["Articles"]]
    topics = [article["Topics"] for article in report["Articles"]]
    
    # Sentiment distribution
    sentiment_distribution = {
        "Positive": sentiments.count("Positive"),
        "Negative": sentiments.count("Negative"),
        "Neutral": sentiments.count("Neutral")
    }
    
    # Topic overlap
    common_topics = set(topics[0]).intersection(*topics[1:])
    unique_topics = [set(article_topics) - common_topics for article_topics in topics]
    
    # Coverage differences
    coverage_diff = []
    for i in range(len(report["Articles"]) - 1):
        article1 = report["Articles"][i]
        article2 = report["Articles"][i + 1]
        comparison = f"Article {i+1} focuses on {', '.join(article1['Topics'][:2])}, while Article {i+2} focuses on {', '.join(article2['Topics'][:2])}."
        coverage_diff.append({"Comparison": comparison, "Impact": "Varies based on topic focus."})
    
    return {
        "Sentiment Distribution": sentiment_distribution,
        "Topic Overlap": {
            "Common Topics": list(common_topics),
            "Unique Topics": [list(topics) for topics in unique_topics]
        },
        "Coverage Differences": coverage_diff
    }

def generate_tts(report, comparative=None, filename="output.mp3"):
    try:
        # Use the provided comparative analysis, or compute it if not provided
        if comparative is None:
            comparative = comparative_analysis(report)
        
        distribution = comparative["Sentiment Distribution"]
        positive = distribution["Positive"]
        negative = distribution["Negative"]
        neutral = distribution["Neutral"]
        total = positive + negative + neutral

        # Determine the dominant sentiment
        if total == 0:
            summary = f"{report['Company']} के बारे में कोई खबर नहीं मिली।"
        else:
            sentiments = {"Positive": positive, "Negative": negative, "Neutral": neutral}
            dominant_sentiment = max(sentiments, key=sentiments.get)
            dominant_count = sentiments[dominant_sentiment]

            if dominant_sentiment == "Positive":
                summary = (f"{report['Company']} की खबरें ज्यादातर सकारात्मक हैं। "
                           f"कुल {total} खबरों में से {positive} सकारात्मक, {negative} नकारात्मक, और {neutral} तटस्थ हैं।")
            elif dominant_sentiment == "Negative":
                summary = (f"{report['Company']} की खबरें ज्यादातर नकारात्मक हैं। "
                           f"कुल {total} खबरों में से {positive} सकारात्मक, {negative} नकारात्मक, और {neutral} तटस्थ हैं।")
            else:
                summary = (f"{report['Company']} की खबरें ज्यादातर तटस्थ हैं। "
                           f"कुल {total} खबरों में से {positive} सकारात्मक, {negative} नकारात्मक, और {neutral} तटस्थ हैं।")

        # Generate Hindi TTS
        tts = gTTS(text=summary, lang="hi", slow=False)
        tts.save(filename)
        
        if os.path.exists(filename):
            print(f"TTS file created successfully: {filename}")
            print(f"Absolute path: {os.path.abspath(filename)}")
        else:
            print(f"TTS file not found: {filename}")
            return None
        
        return os.path.abspath(filename)
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None