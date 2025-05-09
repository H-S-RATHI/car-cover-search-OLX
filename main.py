import requests
from bs4 import BeautifulSoup
import csv
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    """Creates a requests session with retry strategy and proper headers"""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # number of retries
        backoff_factor=1,  # wait 1, 2, 4 seconds between retries
        status_forcelist=[500, 502, 503, 504]  # HTTP status codes to retry on
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Headers that mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    return session

def scrape_olx(search_url, output_file):
    """
    Scrapes OLX search results for a given query URL and writes them to a CSV file.
    Args:
        search_url (str): The URL of the OLX search page.
        output_file (str): Path to the output CSV file.
    """
    session = create_session()
    items = []
    
    try:
        print("Fetching data from OLX...")
        response = session.get(search_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Each listing is within an <li> with data-aut-id="itemBox"
        for item in soup.find_all('li', {'data-aut-id': 'itemBox'}):
            try:
                title_tag = item.find('span', {'data-aut-id': 'itemTitle'})
                price_tag = item.find('span', {'data-aut-id': 'itemPrice'})
                location_tag = item.find('span', {'data-aut-id': 'itemLocation'})
                link_tag = item.find('a', href=True)

                title = title_tag.get_text(strip=True) if title_tag else ''
                price = price_tag.get_text(strip=True) if price_tag else ''
                location = location_tag.get_text(strip=True) if location_tag else ''
                link = link_tag['href'] if link_tag else ''

                items.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': link,
                })
                
                # Add a small delay between processing items
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error processing an item: {str(e)}")
                continue

        # Write results to CSV file
        if items:
            keys = ['title', 'price', 'location', 'link']
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(items)
            print(f"Successfully scraped {len(items)} items. Results saved to '{output_file}'")
        else:
            print("No items found to scrape!")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == '__main__':
    SEARCH_URL = 'https://www.olx.in/items/q-car-cover'
    OUTPUT_FILE = 'olx_car_cover_results.csv'
    scrape_olx(SEARCH_URL, OUTPUT_FILE)
