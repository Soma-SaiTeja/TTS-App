from fastapi import FastAPI, HTTPException
from utils import fetch_articles, analyze_sentiment, comparative_analysis, generate_tts, extract_topics

app = FastAPI()

@app.get("/analyze")
def analyze_company(company_name: str):
    try:
        # Fetch articles
        articles = fetch_articles(company_name)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found for the given company.")

        # Process articles
        report = {"Company": company_name, "Articles": []}
        for article in articles:
            sentiment = analyze_sentiment(article["summary"])
            topics = extract_topics(article["summary"])
            report["Articles"].append({
                "Title": article["title"],
                "Summary": article["summary"],
                "Sentiment": sentiment,
                "Source": article["source"],
                "Link": article["link"],
                "Topics": topics
            })

        # Comparative analysis
        comparative = comparative_analysis(report)

        # Generate TTS with the comparative analysis result
        audio_file = generate_tts(report, comparative=comparative)

        # Full report
        full_report = {**report, "Comparative Analysis": comparative, "Audio": audio_file}
        return full_report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))