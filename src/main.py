import os
from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / 'products.json'
SCHEMA_PATH = ROOT_DIR / 'sql' / 'schema.sql'

def connect_to_database():
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        
        with open(SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        connection.commit()

        return connection            
    except Exception as e:
        print(f"Failure to connect to database. Error: {e}")
        
def check_if_product_exists_in_database(connection, product_name):
    cursor = connection.cursor()
    
    validation_query = "SELECT 1 FROM product WHERE name = %s"
    
    cursor.execute(validation_query, (product_name,))
    
    result = cursor.fetchone()
    
    return result is not None

def check_if_website_exists_in_database(connection, website_name):
    cursor = connection.cursor()
    
    validation_query = "SELECT 1 FROM website WHERE name = %s"
    
    cursor.execute(validation_query, (website_name,))
    
    result = cursor.fetchone()
    
    return result is not None

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
    
# Make sure websites are already in database
def handle_websites(product_list):
    
    connection = connect_to_database()

    for product in product_list:
        for site in product['sites']:
            website_url = site['url']
            website_name = get_website_name_from_url(website_url)
            
            if check_if_website_exists_in_database(connection, website_name) == True:
                print(f"{website_name} already exists in Database")
            elif check_if_website_exists_in_database(connection, website_name) == False:
                cursor = connection.cursor()
                
                insert_website_query = ("INSERT INTO website (name) VALUES (%s);")
                cursor.execute(insert_website_query, (website_name,))
                
                connection.commit()
                
# Run tasks on each product
def handle_product(product):
    
    connection = connect_to_database()
    
    product_name = product['name']
    product_target_price = product['target_price']
    product_sites = product['sites']
    
    if check_if_product_exists_in_database(connection, product_name) == True:
        print(f"{product_name} already exists in database")
    elif check_if_product_exists_in_database(connection, product_name) == False:
        print(f"{product_name} does not exist in database")
        
        cursor = connection.cursor()
        
        insert_product_query = ("INSERT INTO product (name) VALUES (%s);")
        cursor.execute(insert_product_query, (product_name,))
        
        connection.commit()
        
if __name__ == "__main__":
    with open(CONFIG_PATH, 'r') as f:
        parsed_json = json.load(f)
        
    product_list = parsed_json['products']
    
    handle_websites(product_list)
    
    for product in product_list:
        handle_product(product)