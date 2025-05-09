import time
import os
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def human_like_scroll(driver, scroll_count=10):
    """
    Performs random scrolling with human-like behavior
    Args:
        driver: Selenium webdriver instance
        scroll_count: Number of scroll actions to perform
    """
    print("Starting human-like scrolling...")
    
    # Get the height of the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for i in range(scroll_count):
        # Random scroll amount (between 100 and 800 pixels)
        scroll_amount = random.randint(300, 800)
        
        # Random scroll direction (mostly down, occasionally up)
        direction = 1 if random.random() < 0.9 else -1  # 90% chance to scroll down
        
        # Execute scroll
        driver.execute_script(f"window.scrollBy(0, {direction * scroll_amount});")
        
        # Random pause between scrolls (0.5 to 3 seconds)
        pause_time = random.uniform(0.5, 3)
        print(f"Scroll {i+1}/{scroll_count}: {direction * scroll_amount}px, pausing for {pause_time:.2f}s")
        time.sleep(pause_time)
        
        # Occasionally pause for longer (simulating user reading content)
        if random.random() < 0.2:  # 20% chance
            long_pause = random.uniform(2, 5)
            print(f"Taking a longer pause for {long_pause:.2f}s (reading content)")
            time.sleep(long_pause)
        
        # Check if we've reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height and i > 3:  # Allow a few scrolls before checking
            # Try to scroll a bit more to trigger lazy loading
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Check again
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the bottom of the page, loading more content if available...")
                # Try clicking "load more" button if it exists
                try:
                    load_more = driver.find_element(By.XPATH, "//button[contains(text(), 'Load more')]")
                    load_more.click()
                    time.sleep(3)
                except:
                    # If no load more button, try one more scroll to the bottom
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
        
        last_height = new_height

def scrape_olx(search_url, output_file):
    """
    Scrapes OLX search results using Selenium with Chrome browser
    with human-like scrolling behavior
    Args:
        search_url (str): The URL of the OLX search page
        output_file (str): Path to the output JSON file
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
        
        # Add a delay to let the page load initially
        initial_wait = random.uniform(3, 6)
        print(f"Waiting {initial_wait:.2f}s for initial page load...")
        time.sleep(initial_wait)
        
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
        
        # Perform human-like scrolling to load more content
        # Random number of scrolls between 8 and 15
        scroll_count = random.randint(8, 15)
        human_like_scroll(driver, scroll_count)
        
        # Find all item boxes after scrolling
        item_boxes = driver.find_elements(By.CSS_SELECTOR, '[data-aut-id="itemBox3"]')
        print(f"Found {len(item_boxes)} item boxes after scrolling")
        
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
                
                # Add a small random delay between processing items (0.1 to 0.3 seconds)
                time.sleep(random.uniform(0.1, 0.3))
                
            except Exception as e:
                print(f"Error processing an item: {str(e)}")
                continue
        
        # Write results to JSON file only
        if items:
            # Save to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=4, ensure_ascii=False)
            
            print(f"Successfully scraped {len(items)} items.")
            print(f"Results saved to JSON: '{output_file}'")
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
    OUTPUT_FILE = 'olx_car_cover_results.json'  # Changed to directly use .json extension
    scrape_olx(SEARCH_URL, OUTPUT_FILE)
