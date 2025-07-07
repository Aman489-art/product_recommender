import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_all_pages(base_url, max_pages=50):
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_products = []
    seen_products = set()
    
    for page in range(1, max_pages + 1):
        # Add pagination parameter to URL
        url = f"{base_url}&page={page}"
        print(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.find_all(class_="slAVV4")
            
            if not data:
                print(f"No products found on page {page}. Stopping.")
                break
                
            print(f"Found {len(data)} products on page {page}")
            
            for item in data:
                try:
                    name = item.find(class_="wjcEIp").get_text(strip=True) if item.find(class_="wjcEIp") else "N/A"
					if name in seen_products:  # Skip duplicates
						continue
					seen_products.add(name)
                    price = item.find(class_="Nx9bqj").get_text(strip=True) if item.find(class_="Nx9bqj") else "N/A"
                    description = item.find(class_="NqpwHC").get_text(strip=True) if item.find(class_="NqpwHC") else "N/A"
                    rating_elem = item.find(class_="XQDdHH")
                    ratings = rating_elem.get_text(strip=True) if rating_elem else "No Rating"
                    
                    all_products.append({
                        'name': name,
                        'price': price,
                        'description': description,
                        'ratings': ratings,
                        'page': page
                    })
                    
                except Exception as e:
                    print(f"Error processing item on page {page}: {e}")
                    continue
                    
            # Respectful delay between requests
            time.sleep(2)
            
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
            continue
            
    return pd.DataFrame(all_products)

if __name__ == "__main__":
    base_url = "https://www.flipkart.com/books/fiction-books/pr?sid=bks,wbi"
    df = scrape_all_pages(base_url, max_pages=50)  # Adjust max_pages as needed
    
    if not df.empty:
        df.to_csv("/home/aman_mi_938/Documents/product_recommmender/data/raw_products_all_pages.csv", index=False)
        print(f"Successfully saved {len(df)} products from {df['page'].nunique()} pages to CSV")
        print("Page distribution:")
        print(df['page'].value_counts().sort_index())
    else:
        print("No products scraped. Check the website structure or network connection.")
