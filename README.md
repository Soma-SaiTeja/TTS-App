# TTS-App
 a web-based application that extracts key details from multiple news articles related  to a given company, performs sentiment analysis, conducts a comparative analysis, and  generates a text-to-speech (TTS) output in Hindi. The tool should allow users to input a  company name and receive a structured sentiment report along with an audio output.

TTS App - News Summarization, Sentiment Analysis, and Hindi TTS
This project is a Text-to-Speech (TTS) App that fetches news articles about a company, performs sentiment analysis, and generates a Hindi TTS summary of the results. It uses a FastAPI backend for processing and a Streamlit frontend for the user interface.

Features
Fetches news articles from BBC News for a given company.
Performs sentiment analysis on article summaries using VADER.
Generates a comparative analysis of sentiment distribution.
Creates a Hindi TTS summary using gTTS.
Displays results in a user-friendly Streamlit interface with a bar chart and audio playback.
Prerequisites
Before you begin, ensure you have the following installed on your system:

Visual Studio Code (VSCode)
Python 3.11
Git (optional, for cloning the repository)
Setup Instructions
1. Install Python 3.11
Download Python 3.11 from the official Python website.
Run the installer:
On Windows, check the box to "Add Python 3.11 to PATH" during installation.
On macOS/Linux, Python is often pre-installed, but you may need to install Python 3.11 using a package manager (e.g., brew on macOS or apt on Ubuntu).
Verify the installation by opening a terminal and running:
python3 --version
You should see Python 3.11.x. If not, ensure Python 3.11 is added to your PATH.

2. Clone the Repository (Optional)
If you have Git installed, clone the repository:
git clone <repository-url>
cd tts-app
Alternatively, download the project files as a ZIP and extract them to a folder named tts-app.

3. Open the Project in VSCode
Launch VSCode.
Open the project folder:
Go to File > Open Folder and select the tts-app folder.
Open a new terminal in VSCode:
Go to Terminal > New Terminal. This will open a terminal at the bottom of VSCode, already set to the project directory.

4. Set Up a Virtual Environment
Create a virtual environment named .venv:
code in terminal -- python3 -m venv .venv

Activate the virtual environment:
On Windows:
code in terminal -- .venv\Scripts\activate
On macOS/Linux:
source .venv/bin/activate

After activation, you should see (.venv) in your terminal prompt.
Verify that the correct Python version is being used:
python --version
It should show Python 3.11.x.

5. Install Dependencies
Ensure you have a requirements.txt file in your project directory. If not, create one with the following content:
fastapi==0.115.0
uvicorn==0.30.6
streamlit==1.38.0
requests==2.32.3
beautifulsoup4==4.12.3
vaderSentiment==3.3.2
gtts==2.5.3
nltk==3.9.1
Install the dependencies:
pip install -r requirements.txt
Verify the installations:
pip list
You should see all the packages listed above.

6. Set Up NLTK Resources
This app uses NLTK for tokenization and stopwords (required by vaderSentiment). NLTK resources need to be downloaded before running the app.

The app automatically downloads the required resources (punkt_tab and stopwords) to ~/nltk_data (e.g., C:\Users\<username>\nltk_data on Windows) at startup. However, you can manually download them to ensure there are no issues:

Run the following command in your virtual environment:
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('stopwords')"
The resources will be downloaded to a default NLTK data directory (e.g., ~/nltk_data).
If you encounter network issues, the app will log an error. Ensure you have an active internet connection the first time you run the app.

7. Write or Verify the Code
Ensure the following files are in your project directory:

utils.py: Contains utility functions for fetching articles, sentiment analysis, comparative analysis, and TTS generation.
app.py: The Streamlit frontend for the user interface.
main.py (or similar): The FastAPI backend for processing requests.

8. Run the Application
Start the FastAPI Backend: In one terminal (in VSCode), ensure your virtual environment is activated, then run:
code in terminal--- uvicorn main:app --host 0.0.0.0 --port 8000 --reload
main:app refers to the FastAPI app instance in main.py.
--reload enables auto-reload for development. You should see output indicating the server is running at http://localhost:8000.

Start the Streamlit Frontend: Open a second terminal in VSCode (Terminal > New Terminal), activate the virtual environment, and run:
code in terminal -- streamlit run app.py
Use the App:
Enter a company name (e.g., "Tesla") or select a popular company from the dropdown.
Click the "Analyze" button.
View the sentiment report, article summaries, and listen to the Hindi TTS summary.

Key Edge Cases Handled
Empty or Invalid Input: The app now checks if the company name is empty or invalid.

Network Issues: Handles network errors during web scraping.

No Articles Found: Returns a 404 error if no articles are found.

TTS Generation Failure: Returns a 500 error if TTS generation fails.

API Errors: Handles API errors gracefully in the frontend.

Project Structure
tts-app/
│
├── .venv/              # Virtual environment
├── utils.py            # Utility functions (fetching articles, sentiment analysis, TTS)
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend
├── requirements.txt    # Dependencies
└── README.md           # This file

Contact
For questions or feedback, please contact:

Name: Soma || somasaiteja0@gmail.com

GitHub: Soma-SaiTeja
