import pyttsx3
import speech_recognition as sr
import eel
import time
import os
import pickle
import base64
import re
import string
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening..')
        eel.DisplayMessage('listening..')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    try:
        print('recognizing')
        eel.DisplayMessage('recognizing..')
        query = r.recognize_google(audio, language='en-in')
        print("user said: " + query)
        eel.DisplayMessage(query) 
        time.sleep(2)
    except Exception:
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        if "open" in query:
            from engine.features import opencommand
            opencommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "spam" in query:  
            spam_detector()  # Call Spam Detector
        else:
            print("not run")
    except:
        print("error")
    eel.showhood()

# ---------------- SPAM DETECTOR FUNCTION ---------------- #
def gmail_authenticate():
    creds = None
    token_path = "token.pickle"

    # Remove the previous login credentials
    if os.path.exists(token_path):
        os.remove(token_path)

    flow = InstalledAppFlow.from_client_secrets_file(
        'C:\\Users\\abhin\\OneDrive\\Desktop\\fluxy\\engine\\client_secret_847628883490-119tgn331uonmcb1p57b632q1gjrdbo2.apps.googleusercontent.com.json', SCOPES
    )
    creds = flow.run_local_server(port=0)

    # Save new credentials
    with open(token_path, "wb") as token:
        pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def fetch_emails(service, num_emails=5):
    results = service.users().messages().list(userId="me", maxResults=num_emails).execute()
    messages = results.get("messages", [])
    email_texts = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        email_snippet = msg_data.get("snippet", "")
        email_texts.append(email_snippet)
    return email_texts

def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_spam_detector():
    df = pd.read_csv("C:\\Users\\abhin\\OneDrive\\Desktop\\fluxy\\engine\\spam.csv", encoding="latin-1")[['v1', 'v2']]
    df.columns = ['label', 'text']
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    df['text'] = df['text'].apply(clean_text)
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    model = MultinomialNB()
    model.fit(X, y)
    return model, vectorizer

def detect_spam(emails, model, vectorizer):
    emails_cleaned = [clean_text(email) for email in emails]
    email_vectors = vectorizer.transform(emails_cleaned)
    predictions = model.predict(email_vectors)
    return ["Spam" if p == 1 else "Not Spam" for p in predictions]

@eel.expose
def spam_detector():
    speak("Logging in to Gmail...")
    service = gmail_authenticate()
    speak("Fetching emails...")
    emails = fetch_emails(service, num_emails=5)
    speak("Training spam detection model...")
    model, vectorizer = train_spam_detector()
    speak("Detecting spam emails...")
    results = detect_spam(emails, model, vectorizer)
    for i, email in enumerate(emails):
        result_text = f"Email {i+1}: {email} | Prediction: {results[i]}"
        print(result_text)
        speak(result_text)
