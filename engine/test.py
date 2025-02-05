import os.path
import pickle
import re
import string
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def clean_text(text):
    if not isinstance(text, str):
        return ""
    print(f"Original text: {text}")
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f"Cleaned text: {text}")
    return text

def authenticate_gmail():
    print("Starting Gmail authentication...")
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            print("Loaded existing credentials from token.pickle.")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Refreshed expired credentials.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file('C:\\Users\\abhin\\OneDrive\\Desktop\\fluxy\\engine\\client_secret_847628883490-119tgn331uonmcb1p57b632q1gjrdbo2.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
            print("Obtained new credentials.")
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            print("Saved credentials to token.pickle.")
    service = build('gmail', 'v1', credentials=creds)
    print("Gmail service built successfully.")
    return service

def fetch_emails(service, num_emails=10):
    print(f"Fetching {num_emails} emails...")
    try:
        results = service.users().messages().list(userId="me", maxResults=num_emails).execute()
        messages = results.get("messages", [])
        email_texts = []
        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
            email_snippet = msg_data.get("snippet", "")
            email_texts.append(email_snippet)
        print(f"Fetched {len(email_texts)} emails.")
        return email_texts
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

def train_spam_detector():
    print("Starting spam detector training...")
    try:
        df = pd.read_csv("C:\\Users\\abhin\\OneDrive\\Desktop\\fluxy\\engine\\spam.csv", encoding="latin-1")[['v1', 'v2']]
        print("CSV file read successfully.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None, None

    df.columns = ['label', 'text']
    print("Columns renamed successfully.")

    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    print("Labels mapped successfully.")

    try:
        df['text'] = df['text'].apply(clean_text)
        print("Text cleaned successfully.")
        # Filter out empty or very short rows
        df = df[df['text'].str.strip() != ""]
        df = df[df['text'].str.len() > 2]
        print("Filtered out empty and very short text rows.")
        print(df['text'].head())  # Print first few entries to check cleaned text
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return None, None

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(df['text'])
        print("Text vectorized successfully.")
    except Exception as e:
        print(f"Error vectorizing text: {e}")
        return None, None

    try:
        y = df['label']
        model = MultinomialNB()
        model.fit(X, y)
        print("Model trained successfully.")
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None

    return model, vectorizer

# Authenticate and fetch emails
service = authenticate_gmail()
email_texts = fetch_emails(service)
print("Fetched Emails:", email_texts)

# Train the spam detector
model, vectorizer = train_spam_detector()
if model and vectorizer:
    print("Spam detector trained successfully.")

    # Test the spam detector with fetched emails
    email_texts_cleaned = [clean_text(text) for text in email_texts]
    email_texts_vectorized = vectorizer.transform(email_texts_cleaned)
    predictions = model.predict(email_texts_vectorized)
    
    for text, prediction in zip(email_texts, predictions):
        print(f"Email: {text} -> Prediction: {'Spam' if prediction else 'Ham'}")
else:
    print("Spam detector training failed.")
