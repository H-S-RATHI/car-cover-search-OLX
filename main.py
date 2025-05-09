import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv

def scrape_olx(search_url, output_file):
    """
    Scrapes OLX search results using Selenium with Chrome browser
    Args:
        search_url (str): The URL of the OLX search page
        output_file (str): Path to the output CSV file
    """
    # Setup Chrome options
    chrome_options = Options()
    # Add any additional options if needed
    # chrome_options.add_argument('--headless')
    
    # Initialize driver as None so we can check if it's created in the finally block
    driver = None
    items = []
    
    try:
        # Use Selenium's built-in webdriver manager
        # This automatically handles driver compatibility with your browser
        driver = webdriver.Chrome(options=chrome_options)
        
        print("Opening Chrome browser and fetching data from OLX...")
        driver.get(search_url)
        
        # Add a delay to let the page load completely
        time.sleep(5)
        
        print("Page title:", driver.title)
        
        # Wait for items to load with increased timeout
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-aut-id="itemBox3"]'))
            )
        except Exception as e:
            print(f"Timeout waiting for items: {str(e)}")
            # Let's try to get the page source to debug
            print("Page source snippet:", driver.page_source[:500])
        
        # Find all item boxes
        item_boxes = driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemBox3"]')
        print(f"Found {len(item_boxes)} item boxes")
        
        for item in item_boxes:
            try:
                # Initialize default values
                title = "No title available"
                price = "No price available"
                details = "No details available"
                link = "No link available"
                image_url = "No image available"
                
                # Try to get each field individually with proper error handling
                try:
                    title = item.find_element(By.XPATH, './/span[@data-aut-id="itemTitle"]').text
                except Exception:
                    # Try alternative CSS selector
                    try:
                        title = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemTitle"]').text
                    except Exception:
                        pass
                
                try:
                    price = item.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
                except Exception:
                    # Try alternative CSS selector
                    try:
                        price = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemPrice"]').text
                    except Exception:
                        pass
                
                # Try to get details, but make it optional as it may not be present
                try:
                    details = item.find_element(By.XPATH, './/span[@data-aut-id="itemDetails"]').text
                except Exception:
                    try:
                        details = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemDetails"]').text
                    except Exception:
                        pass
                
                try:
                    link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                except Exception:
                    pass
                
                # Get image URL using the XPath you provided
                try:
                    image_url = item.find_element(By.XPATH, './/figure[@data-aut-id="itemImage"]//img').get_attribute('src')
                except Exception:
                    try:
                        image_container = item.find_element(By.CSS_SELECTOR, '[data-aut-id="itemImage"]')
                        image_url = image_container.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    except Exception:
                        pass
                
                items.append({
                    'title': title,
                    'price': price,
                    'details': details,
                    'link': link,
                    'image_url': image_url
                })
                
                # Add a small delay between processing items
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error processing an item: {str(e)}")
                continue
        
        # Write results to CSV file
        if items:
            keys = ['title', 'price', 'details', 'link', 'image_url']
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
        # Only quit the driver if it was successfully created
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error closing browser: {str(e)}")

if __name__ == '__main__':
    SEARCH_URL = 'https://www.olx.in/items/q-car-cover'
    OUTPUT_FILE = 'olx_car_cover_results.csv'
    scrape_olx(SEARCH_URL, OUTPUT_FILE)
