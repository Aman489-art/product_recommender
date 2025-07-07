import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download(['punkt', 'stopwords', 'wordnet'])
nltk.download('punkt_tab')


def clean_text(text):
    # Lowercase + remove special chars
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    
    # Tokenize and lemmatize
    tokens = nltk.word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    return " ".join([
        lemmatizer.lemmatize(token) 
        for token in tokens 
        if token not in stop_words and len(token) > 2
    ])

def process_data(raw_path="/home/aman_mi_938/Documents/product_recommmender/data/raw_products_all_pages.csv"):
    df = pd.read_csv(raw_path)
    df['clean_desc'] = df['description'].apply(clean_text)
    df.to_csv("/home/aman_mi_938/Documents/product_recommmender/data/processed_data.csv", index=False)
    print("Done")
process_data(raw_path="/home/aman_mi_938/Documents/product_recommmender/data/raw_products_all_pages.csv")
