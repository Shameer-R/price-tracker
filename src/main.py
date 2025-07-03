from bs4 import BeautifulSoup
import requests

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

def get_product_price_from_url(website_url):
    if get_website_name_from_url(website_url) == "BestBuy":
        
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        request_content = requests.get(website_url, headers={'User-Agent': agent}, timeout=3)
        
        soup = BeautifulSoup(request_content.content, 'html5lib')
        
        price_tag = soup.find(id="large-customer-price").text.strip()
        price_text = convert_price_tag_to_string(price_tag)
        
        return float(price_text)