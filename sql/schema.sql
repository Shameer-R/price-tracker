CREATE TABLE IF NOT EXISTS product (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS website (
    website_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS price_history (
    price_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES product(product_id),
    website_id INT NOT NULL REFERENCES website(website_id),
    price DECIMAL (10, 2) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)