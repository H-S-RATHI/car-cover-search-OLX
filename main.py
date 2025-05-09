import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv

def scrape_olx(search_url, output_file):
    """
    Scrapes OLX search results using Selenium with Chrome browser
    Args:
        search_url (str): The URL of the OLX search page
        output_file (str): Path to the output CSV file
    """
    # Setup Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    items = []
    
    try:
        print("Opening Chrome browser and fetching data from OLX...")
        driver.get(search_url)
        
        # Wait for items to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-aut-id="itemBox"]'))
        )
        
        # Find all item boxes
        item_boxes = driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemBox"]')
        
        for item in item_boxes:
            try:
                title = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemTitle"]').text
                price = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemPrice"]').text
                location = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemLocation"]').text
                link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                
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
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == '__main__':
    SEARCH_URL = 'https://www.olx.in/items/q-car-cover'
    OUTPUT_FILE = 'olx_car_cover_results.csv'
    scrape_olx(SEARCH_URL, OUTPUT_FILE)
