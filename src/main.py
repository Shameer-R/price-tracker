import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path
import psycopg2
import smtplib
from email.message import EmailMessage

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

ROOT_DIR = Path(__file__).resolve().parent.parent
PRODUCT_JSON_PATH = ROOT_DIR / 'products.json'
CONFIG_PATH = ROOT_DIR / 'config.json'
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

def check_if_price_was_updated_today(connection, product_id, website_id):
    
    cursor = connection.cursor()
    
    select_query = """
    SELECT price_id FROM price_history
    WHERE product_id = %s AND website_id = %s AND timestamp = CURRENT_DATE;
    """
    
    cursor.execute(select_query, (product_id, website_id,))
    
    result = cursor.fetchone()
    
    return result is not None
    

def get_product_id_from_product_name(connection, product_name):
    cursor = connection.cursor()
    
    select_query = "SELECT product_id FROM product WHERE name = %s"
    
    cursor.execute(select_query, (product_name,))
    
    result = cursor.fetchone()
    
    return result[0]

def get_website_id_from_website_name(connection, website_name):
    cursor = connection.cursor()
    
    select_query = "SELECT website_id FROM website WHERE name = %s"
    
    cursor.execute(select_query, (website_name,))
    
    result = cursor.fetchone()
    
    return result[0]

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
                
PricesList = []
                
def product_below_target_price(product_name, website_name, price):
    product_dictionary = {
        "product_name": product_name,
        "website_name": website_name,
        "price": price,
    }
    
    PricesList.append(product_dictionary)

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
        
    product_id = get_product_id_from_product_name(connection, product_name)
    
    for site in product_sites:
        site_url = site['url']
        site_name = get_website_name_from_url(site_url)
        site_id = get_website_id_from_website_name(connection, site_name)
        current_price_from_site = get_product_price_from_url(site_url)
        
        cursor = connection.cursor()
        
        if check_if_price_was_updated_today(connection, product_id, site_id) == True:
            print("Price was already updated today. Overwriting.")
            
            update_price_history_query = """
                UPDATE price_history
                SET price = %s
                WHERE product_id = %s AND website_id = %s AND timestamp = CURRENT_DATE
            """

            cursor.execute(update_price_history_query, (current_price_from_site, product_id, site_id))
            
            connection.commit()
            
        elif check_if_price_was_updated_today(connection, product_id, site_id) == False:
            print("Price was not updated. Creating new entry.")
            
            insert_price_history_query = """
                INSERT INTO price_history (product_id, website_id, price) 
                VALUES (%s, %s, %s);
            """
        
            cursor.execute(insert_price_history_query, (product_id, site_id, current_price_from_site,))
        
            connection.commit()
            
        if current_price_from_site <= product_target_price:
            product_below_target_price(product_name, site_name, current_price_from_site)
            
def send_email_from_bot(email_to, body):
    EMAIL_ADDRESS = "shampricetrackerbot@gmail.com"
    PASSWORD = GMAIL_APP_PASSWORD
    
    msg = EmailMessage()
    msg['Subject'] = "A product you're interested in has gone on sale!"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email_to
    
    msg.set_content(body)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, PASSWORD)
        smtp.send_message(msg)
        print(f"Email sent to {email_to}")


    
if __name__ == "__main__":
    with open(PRODUCT_JSON_PATH, 'r') as f:
        parsed_json = json.load(f)
        
    product_list = parsed_json['products']
    
    handle_websites(product_list)
    
    for product in product_list:
        handle_product(product)
    
    if len(PricesList) > 0:
        
        message_string = ""
        
        for product_dict in PricesList:
            product_name = product_dict['product_name']
            website_name = product_dict['website_name']
            price = product_dict['price']
            
            current_text = f"\n- {product_name} is for sale on {website_name} going for ${price}!\n"
            message_string += current_text
            
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)

        email_list = config.get("emails")
        
        for email in email_list:
            send_email_from_bot(email, message_string)
    