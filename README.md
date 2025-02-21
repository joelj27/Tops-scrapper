##Top Scraper - Product Data Extraction
#Overview
      The Top Scraper project was developed to extract product listing data from an e-commerce platform. Since the product data flows through an API, I opted not to use Scrapy for this project. Instead, the script uses the requests library to retrieve the product listings and the BeautifulSoup library to parse the HTML data.

#Approach Used for Scraping
  Identify Product Categories:
      Gather all the product categories that need to be scraped.
      Identify the corresponding category IDs.
  Extract Product Listings:
      For each category, retrieve the listing of products available.
  Extract Detailed Product Information:
    For each product, extract the detailed data by accessing the product's individual URL.
Libraries Used:
  requests for sending HTTP requests and fetching the data.
  BeautifulSoup (from bs4) for parsing and extracting data from HTML.
Dependencies Required to Run the Script
  To run the script, the following dependencies must be installed:
    beautifulsoup4==4.13.3
    nested_lookup==0.2.25
    requests==2.32.3
    tqdm==4.67.1
    concurrent
    nested-lookup
How to Run the Script (Step by Step)
  Install the required dependencies by running:
      pip install -r requirements.txt
  Run the script using the following command:
      python main.py
Sample Output (First 5 Products)
Below is an example of the first 5 products fetched:
