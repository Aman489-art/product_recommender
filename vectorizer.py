import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

def vectorize_text(data_path="/home/aman_mi_938/Documents/product_recommmender/data/processed_data.csv"):
    df = pd.read_csv(data_path)
    tfidf = TfidfVectorizer(max_features=5000)
    vectors = tfidf.fit_transform(df['clean_desc'])
    joblib.dump(tfidf, "/home/aman_mi_938/Documents/product_recommmender/model/tfidf_model.pkl")
    return vectors
vectorize_text(data_path="/home/aman_mi_938/Documents/product_recommmender/data/processed_data.csv")
