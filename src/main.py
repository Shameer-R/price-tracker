from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path

def convert_price_tag_to_string(price_tag):
    price_tag = price_tag.replace("$", "")
    price_tag = price_tag.replace(",", "")
    
    print(price_tag)
    
    return float(price_tag)

def get_website_name_from_url(website_url):
    if "https://www.bestbuy.com" in website_url:
        return "BestBuy"
    elif "https://www.target.com" in website_url:
        return "Target"
    elif "https://www.walmart.com" in website_url:
        return "Walmart"
    elif "https://www.amazon.com" in website_url:
        return "Amazon"
    else:
        raise ValueError(f"Invalid Website URL: {website_url}")

# Reminder to self: Add mock-based test when product is nearing completion
def get_product_price_from_url(website_url):
    if get_website_name_from_url(website_url) == "BestBuy":
        
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        request_content = requests.get(website_url, headers={'User-Agent': agent}, timeout=3)
        
        soup = BeautifulSoup(request_content.content, 'html5lib')
        
        price_tag = soup.find(id="large-customer-price").text.strip()
        price_text = convert_price_tag_to_string(price_tag)
        
        return float(price_text)
    
# Run tasks on each product
def handle_product(product):
    product_name = product['name']
    product_target_price = product['target_price']
    product_sites = product['sites']
    pass
    
if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    config_path = root_dir / 'products.json'
    
    with open(config_path, 'r') as f:
        parsed_json = json.load(f)
        
    product_list = parsed_json['products']
    
    for product in product_list:
        handle_product(product)