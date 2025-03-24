import os
import streamlit as st
import requests

st.title("News Summarization & Sentiment Analysis")

company_name = st.text_input("Enter Company Name", "Tesla")
popular_companies = ["Tesla", "Apple", "Google", "Amazon", "Microsoft"]
selected_company = st.selectbox("Or select a popular company:", popular_companies)

if st.button("Analyze"):
    if not company_name:
        company_name = selected_company

    try:
        response = requests.get(f"http://localhost:8000/analyze?company_name={company_name}")
        if response.status_code == 200:
            result = response.json()

            st.subheader("Sentiment Report")
            st.json(result)

            sentiment_distribution = result["Comparative Analysis"]["Sentiment Distribution"]
            st.bar_chart(sentiment_distribution)

            st.subheader("Extracted Articles")
            for article in result["Articles"]:
                st.markdown(f"**[{article['Title']}]({article['Link']})** - {article['Source']}")
                st.write(f"Sentiment: {article['Sentiment']}")
                st.write(f"Topics: {', '.join(article['Topics'])}")
                st.write(f"Summary: {article['Summary']}")
                st.write("---")

            if result["Audio"]:
                st.subheader("Hindi Text-to-Speech Summary")
                audio_path = result["Audio"]
                if os.path.exists(audio_path):
                    with open(audio_path, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.error(f"Audio file not found at: {audio_path}")
            else:
                st.warning("Audio generation failed.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")