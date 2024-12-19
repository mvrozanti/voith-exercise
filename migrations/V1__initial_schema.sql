CREATE TABLE historical_data (
    coin_id VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    price DOUBLE,
    volume DOUBLE,
    PRIMARY KEY (coin_id, timestamp)
);