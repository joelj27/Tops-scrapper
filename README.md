### Top Scraper - Product Data Extraction
   A Python script to scrape product data from an e-commerce platform using requests and BeautifulSoup. The script fetches product listings from categories via the API and extracts detailed product information by accessing individual product URLs.

## Approach
#Identify Product Categories:
Collect all relevant product categories and their corresponding category IDs.
# Scrape Product Listings:
Retrieve product listings for each category.
# Extract Detailed Product Information:
Access product URLs and scrape detailed data for each product.
## Libraries Used:
requests: To send HTTP requests and fetch data.
BeautifulSoup (bs4): To parse and extract data from HTML content.
##Requirements
      Ensure the following dependencies are installed:

      beautifulsoup4==4.13.3
      nested_lookup==0.2.25
      requests==2.32.3
      tqdm==4.67.1
      concurrent
      nested-lookup
      Setup & Usage
## Setup & Usage
# Install required dependencies:
      pip install -r requirements.txt
      python main.py
Sample Output:

Excel public file url : https://docs.google.com/spreadsheets/d/1JTzZKCDyhbypaqfYR3G70LzbAc4u5Tdo5Ju4ojtv08U/edit?usp=sharing

#Note: Quantity is extracted from the title with the use of LLM.
