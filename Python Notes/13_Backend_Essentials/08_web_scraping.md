# Web Scraping with BeautifulSoup

### Simple Explanation (Hinglish)
Internet se automatically data extract karne ko **Web Scraping** kehte hain. Jaise Amazon se product prices nikalna, ya news websites se headlines collect karna. **BeautifulSoup** HTML ko parse karne mein help karta hai.

### Theory (Clear + Structured)
- **BeautifulSoup**: Library for parsing HTML and XML documents.
- **requests**: Library for making HTTP requests.
- **HTML Tags**: Elements like `<div>`, `<a>`, `<p>` that structure web pages.
- **Selectors**: Methods to find elements (`find()`, `find_all()`, CSS selectors).

### Examples with Hinglish Comments

```python
# Pehle install karo: pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

# Website se HTML fetch karna
url = "https://books.toscrape.com/"
response = requests.get(url)

# Check if request successful
if response.status_code == 200:
    print("Website successfully fetched!")
else:
    print(f"Failed to fetch website. Status code: {response.status_code}")

# HTML parse karna
soup = BeautifulSoup(response.text, 'html.parser')
# # 'html.parser' built-in parser hai

# Saare book titles nikalna
book_titles = soup.find_all('h3')
# # Saare <h3> tags dhundh liye

print("\nBook Titles:")
for i, title in enumerate(book_titles[:5], 1):
    # Text extract karna
    book_name = title.a['title']
    print(f"{i}. {book_name}")

# Price nikalna
prices = soup.find_all('p', class_='price_color')
# # class_='price_color' wale <p> tags dhundho

print("\nPrices:")
for price in prices[:5]:
    print(price.text)

# Advanced: Specific element dhundhna
first_book = soup.find('article', class_='product_pod')
if first_book:
    title = first_book.h3.a['title']
    price = first_book.find('p', class_='price_color').text
    print(f"\nFirst Book: {title} - {price}")

# All links nikalna
links = soup.find_all('a')
print(f"\nTotal links on page: {len(links)}")

# Real-world example: Scraping with error handling
def scrape_books(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status
        
        soup = BeautifulSoup(response.text, 'html.parser')
        books = []
        
        for article in soup.find_all('article', class_='product_pod'):
            title = article.h3.a['title']
            price = article.find('p', class_='price_color').text
            books.append({'title': title, 'price': price})
        
        return books
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Testing
scraped_books = scrape_books("https://books.toscrape.com/")
print(f"\nScraped {len(scraped_books)} books successfully!")
```

### Common Mistakes
1. **Website ka robots.txt check na karna**: Hamesha `/robots.txt` check karo ki scraping allowed hai ya nahi.
2. **Rate limiting**: Bahot tezi se requests mat bhejo, warna IP ban ho sakti hai. `time.sleep()` use karo.
3. **HTML structure change**: Websites apna structure change kar sakti hain, isliye error handling zaroori hai.

### Interview Notes
1. **Legal aspects**: Always check `robots.txt` and terms of service before scraping.
2. **Alternatives**: Some websites offer official APIs - prefer those over scraping.

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Scrape all headings (h1, h2, h3) from any news website.
2. **(Basic)** Extract all links (`<a>` tags) from a webpage and print their `href` attributes.
3. **(Medium)** Scrape product names and prices from an e-commerce demo site (like books.toscrape.com).
4. **(Medium)** Find elements in a page by class name and filter them based on their text content.
5. **(Hard)** Build a scraper that paginates through multiple pages (at least 3 pages) and saves the scraped data to a CSV file.
