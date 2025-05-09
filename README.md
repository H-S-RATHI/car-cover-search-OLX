# OLX Car Cover Search Scraper

A web scraping tool that searches for car covers on OLX India and extracts product information using Selenium with human-like browsing behavior.

## Overview

This project uses Selenium WebDriver to automate the process of searching for car covers on OLX India. It implements human-like scrolling and browsing patterns to avoid detection as a bot. The scraper extracts product details including:

- Title
- Price
- Product details
- Link to the product page
- Image URL

All data is saved to a JSON file for further analysis or use.

## Features

- **Human-like Browsing**: Implements random scrolling patterns, pauses, and interactions to mimic human behavior
- **Robust Error Handling**: Gracefully handles missing elements and connection issues
- **Detailed Logging**: Provides informative console output during the scraping process
- **JSON Output**: Saves all scraped data in a structured JSON format

## Requirements

- Python 3.6+
- Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
```
git clone <https://github.com/H-S-RATHI/car-cover-search-OLX>
cd car-cover-search-OLX
```

2. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

Run the script with:

```
python main.py
```

By default, the script will:
1. Search for "car cover" on OLX India
2. Scroll through multiple pages of results
3. Extract product information
4. Save the results to `olx_car_cover_results.json`

## Customization

You can modify the following variables in `main.py` to customize the search:

- `SEARCH_URL`: Change to search for different products or apply filters
- `OUTPUT_FILE`: Change the name or location of the output file

## Output Format

The script generates a JSON file with the following structure:

```json
[
    {
        "title": "Product Title",
        "price": "₹ X,XXX",
        "details": "Additional details (e.g., year, kilometers for cars)",
        "link": "https://www.olx.in/item/...",
        "image_url": "https://apollo.olx.in/..."
    },
    ...
]
```

## Notes

- The script includes random delays and scrolling patterns to avoid being detected as a bot
- For debugging purposes, headless mode is disabled by default (can be enabled by uncommenting line 80)
- The script handles various page layouts and element structures on OLX

## License

[Specify your license here]

## Disclaimer

This tool is for educational purposes only. Please respect OLX's terms of service and robots.txt file. Use responsibly and avoid excessive requests that might impact their service.