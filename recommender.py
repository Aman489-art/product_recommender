import joblib
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity

class EnhancedProductRecommender:
    def __init__(self, data_path="/home/aman_mi_938/Documents/product_recommmender/data/processed_data.csv"):
        # Load data
        self.df = pd.read_csv(data_path)
        
        # Convert price to numeric (handling ₹, $, commas, etc.)
        self.df['price'] = self.df['price'].apply(self._clean_price).astype(float)
        
        # Convert ratings to numeric
        self.df['ratings'] = pd.to_numeric(self.df['ratings'], errors='coerce').fillna(0)
        
        # Normalize price
        self.df['price_norm'] = (self.df['price'] - self.df['price'].min()) / \
                               (self.df['price'].max() - self.df['price'].min())
        
        # Load TF-IDF model and create similarity matrix
        self.tfidf = joblib.load("/home/aman_mi_938/Documents/product_recommmender/model/tfidf_model.pkl")
        self.vectors = self.tfidf.transform(self.df['clean_desc'])
        self.sim_matrix = cosine_similarity(self.vectors)

    def _clean_price(self, price_str):
        """Helper method to clean price strings"""
        if isinstance(price_str, str):
            # Remove all non-digit characters except decimal point
            cleaned = re.sub(r'[^\d.]', '', str(price_str))
            return float(cleaned) if cleaned else 0.0
        return float(price_str)

    def recommend(self, product_name, top_n=5, price_weight=0.3, rating_weight=0.2):
		
        # Get unique products first
        unique_products = self.df.drop_duplicates(subset=['name'])
        matches = unique_products[unique_products['name'].str.lower().str.contains(product_name.lower())]


        """Enhanced recommendations with price and rating considerations"""
        try:
            idx = self.df[self.df['name'] == product_name].index[0]
        except IndexError:
            return f"Product '{product_name}' not found"
            
        content_sim = list(enumerate(self.sim_matrix[idx]))
        combined_scores = []
        
        for i, score in content_sim:
            if i == idx:
                continue
                
            price_sim = 1 - abs(self.df.at[idx, 'price_norm'] - self.df.at[i, 'price_norm'])
            rating_sim = self.df.at[i, 'ratings'] / 5  # Normalize 0-5 to 0-1
            
            combined_score = (
                score * (1 - price_weight - rating_weight) + 
                price_sim * price_weight + 
                rating_sim * rating_weight
            )
            combined_scores.append((i, combined_score))
        
        combined_scores.sort(key=lambda x: x[1], reverse=True)
        sim_indices = [i[0] for i in combined_scores[:top_n]]
        
        return self.df.iloc[sim_indices][['name', 'price', 'description', 'ratings']]

def main():
    recommender = EnhancedProductRecommender()
    
    # Show sample products to help user
    print("Sample products in database:")
    print(recommender.df['name'].head(10).to_string(index=False))
    
    while True:
        product_name = input("\nEnter product name (or 'quit' to exit): ").strip()
        
        if product_name.lower() == 'quit':
            break
            
        # Find closest match (case-insensitive)
        matches = recommender.df[recommender.df['name'].str.contains(product_name, case=False)]
        
        if len(matches) == 0:
            print(f"\nNo products found containing '{product_name}'. Try again.")
        else:
            if len(matches) > 1:
                print("\nMultiple matches found:")
                print(matches[['name']].to_string(index=False))
                continue
                
            # Get exact name from dataframe
            exact_name = matches.iloc[0]['name']
            recs = recommender.recommend(exact_name)
            
            if isinstance(recs, pd.DataFrame):
                print(f"\nRecommended similar to '{exact_name}':")
                print(recs.to_string(index=False))
            else:
                print(recs)

if __name__ == "__main__":
    main()
