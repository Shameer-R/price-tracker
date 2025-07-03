# Price Tracker Bot

A Python-based price tracking bot that monitors product prices on **Best Buy** and sends email alerts when prices drop below target thresholds. The bot stores data in a PostgreSQL database and should be scheduled to run automatically once a day.

---

## Features

- Scrapes product prices from **Best Buy** (currently the only supported website)  
- Stores products, websites, and price history in PostgreSQL  
- Sends email notifications to configured recipients when prices are below target  
- Supports multiple email recipients configured in a JSON file  

---

## Upcoming Plans

- Add support for **Walmart**, **Target**, and **Amazon** price tracking  
- Improve scraping reliability and expand to additional retailers  
- Add more robust error handling and retry logic  

---

## Requirements

- Python 3.8+  
- PostgreSQL database  
- Required Python packages (see `requirements.txt`):  
  - psycopg2  
  - requests  
  - beautifulsoup4  
  - python-dotenv  

---

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/price-tracker-bot.git
   cd price-tracker-bot
2. **Create and activate a virtual environment**

```
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```
pip install -r requirements.txt
```

4. **Set up PostgreSQL**
- Create a database for the bot.
- Update your DATABASE_URL connection string.

5. **Configure environment variables**
Create a .env file locally (do NOT commit):
```
DATABASE_URL=your_postgres_connection_string
GMAIL_APP_PASSWORD=your_gmail_app_password
EMAIL_ADDRESS=your_bot_email_address
```

Add products and emails config
- `products.json`: list of products with target prices and URLs (must be Best Buy URLs currently)
- `config.json`: list of email addresses to notify

## config.json

This JSON file contains the email addresses that will receive price alert notifications. It should have the following format:
```
{
  "emails": [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
  ]
}
```

You can add as many recipient emails as you want inside the "emails" array. The bot reads this file each time it runs and sends alerts to all listed addresses.
