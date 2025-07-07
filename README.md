# Product Recommender for Flipkart Books

This project is a complete pipeline for scraping book data from Flipkart, cleaning and processing the text, vectorizing product descriptions, and recommending similar products based on content, price, and ratings.

---

## 📁 Project Structure

```
product_recommender/
├── data/                # Data folder (not tracked by git)
├── model/               # Pickled models (not tracked by git)
├── scripts/             # All Python scripts
├── README.md            # This file
├── .gitignore           # Ignore data/model files
├── requirements.txt     # All dependencies
```

---

## 🚀 Features

- **scraper.py**: Scrapes product listings from Flipkart, supports pagination and duplicate filtering.
- **cleaner.py**: Cleans and tokenizes product descriptions using NLTK.
- **vectorizer.py**: Converts cleaned descriptions into TF-IDF vectors and saves the model.
- **recommender.py**: Recommends similar products, factoring in content similarity, price, and ratings.

---

## 🔧 Setup Instructions

1. **Clone the repo**
    ```bash
    git clone https://github.com/yourusername/product_recommender.git
    cd product_recommender
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Pipeline (Step by Step)**

    1. **Scrape Data**
        ```bash
        python scripts/scraper.py
        ```
        - Scrapes books from Flipkart and saves raw data to `data/raw_products_all_pages.csv`.

    2. **Clean Data**
        ```bash
        python scripts/cleaner.py
        ```
        - Cleans descriptions, saves processed data to `data/processed_data.csv`.

    3. **Vectorize Data**
        ```bash
        python scripts/vectorizer.py
        ```
        - Creates TF-IDF vectors and saves the model to `model/tfidf_model.pkl`.

    4. **Run the Recommender**
        ```bash
        python scripts/recommender.py
        ```
        - Start the interactive recommendation system.

---

## 📝 Notes

- **Data and model folders are gitignored:** To keep the repository lightweight and avoid sharing large or sensitive files.
- **Flipkart structure may change:** If scraping fails, check for changes in the site’s HTML and update class names.
- **NLTK first-run:** The cleaner script downloads necessary NLTK resources.

---

## 📚 Example Usage

When running `recommender.py`, you’ll see sample products. Enter a product name to get recommendations. Type `'quit'` to exit.

---

## 📄 License

[MIT License](LICENSE) (or your choice)

---

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the project!
