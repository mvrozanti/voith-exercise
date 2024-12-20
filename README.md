![CI](https://github.com/mvrozanti/voith-exercise/actions/workflows/ci.yml/badge.svg?branch=master)

# Time Series Data API with Flyway

This project is a Dockerized API for accessing and managing cryptocurrency time series data. It includes a MySQL database, a Python FastAPI application, and Flyway for database migrations.

---

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Optional: `curl` or a similar HTTP client for testing API endpoints.

---

## Project Structure

```
.
├── API-Time-Series-Exercise.pdf
├── data
│   └── historical_data_last_4_days.csv
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── migrations
│   └── V1__initial_schema.sql
├── README.md
├── requirements.txt
├── scripts
│   └── import-data.sh
├── tests
│   ├── __init__.py
│   └── test_timeseries_service.py
└── voith_exercise
    ├── controllers
    │   └── timeseries_controller.py
    ├── db.py
    ├── __init__.py
    ├── main.py
    ├── models
    │   └── historical_data.py
    ├── repositories
    │   └── timeseries_repository.py
    └── services
        └── timeseries_service.py
```

## Getting Started

### Clone the Repository
```bash
git clone https://github.com/mvrozanti/voith-exercise
cd voith-exercise
```

### Build and Start Services

Start all services - MySQL database, API, Flyway and Redis:

```
docker-compose up --build
```

### Importing Data for Demo Purposes

To quickly populate the database with data for demonstration purposes, I provide a script to import a sample CSV file into the historical_data table:

```
bash scripts/import-data.sh
```

After running the script, you can verify the imported data:

    docker exec -i mysql mysql -uroot -prootpass -e "SELECT * FROM historical_data LIMIT 5;" timeseries_db

## Using the API
### Basic Fetch Data for a Coin

Fetch all available data for cardano:

    curl "http://localhost:8000/api/v1/data/timeseries/cardano"

Response:

```json
{
  "coin_id": "cardano",
  "timestamps": ["2024-12-18T00:00:00", ...],
  "prices": [1.11, ...],
  "volumes": [99999, ...]
}
```

### Fetch Data with Filters
Fetch data for cardano within a specific date range:

    curl "http://localhost:8000/api/v1/data/timeseries/cardano?start_date=2024-12-18&end_date=2024-12-18"

Response:

```json
{
  "coin_id": "cardano",
  "timestamps": ["2024-12-18T00:00:00", ...],
  "prices": [1.11, ...],
  "volumes": [99999, ...]
}
```


Fetch data for zcash with price and volume filters:

    curl "http://localhost:8000/api/v1/data/timeseries/zcash?min_price=0&max_price=10000&min_volume=0&max_volume=49919727"

Response:

```json
{
  "coin_id": "zcash",
  "timestamps": ["2024-12-18T00:00:00", ...],
  "prices": [1.11, ...],
  "volumes": [99999, ...]
}
```


### Fetch Summary Statistics
Get summary statistics for bitcoin within a specific date range:

    curl "http://localhost:8000/api/v1/data/timeseries/bitcoin/stats?start_date=2024-12-18&end_date=2024-12-19" 

Response:
```json
{
  "coin_id": "bitcoin",
  "stats": {
    "avg_price": 104203.55827765404,
    "total_volume": 131901766571096.0
  }
}
```


### Fetch Paginated Data
Fetch the first 10 records for ethereum:

    curl "http://localhost:8000/api/v1/data/timeseries/ethereum/paginated?limit=10&offset=0"

Response:

```json
{
  "coin_id": "ethereum",
  "stats": {
    "avg_price": 104203.55827765404,
    "total_volume": 131901766571096.0
  }
}
```

Fetch the next 10 records for ethereum:

    curl "http://localhost:8000/api/v1/data/timeseries/ethereum/paginated?limit=10&offset=10"

Response:

```json
{
  "coin_id": "ethereum",
  "timestamps": [
    "2024-12-16T17:44:00",
    ...
  ],
  "prices": [
    3993.54,
    ...
  ],
  "volumes": [
    41066171468.0,
    ...
  ]
}
```

### Error Cases
Fetch data for a non-existent coin:

    curl "http://localhost:8000/api/v1/data/timeseries/unknown_coin"

Response:

```json
{"detail":"No data found for the given criteria"}
```

Fetch data with invalid filters (e.g., negative limit):

    curl "http://localhost:8000/api/v1/data/timeseries/bitcoin/paginated?limit=-5&offset=0"

Response:

```json
{ "detail": "Limit must be greater than 0." }
```

### Health Check

Verify that the API is running:

curl "http://localhost:8000/health"

Response:

```json
{ "status": "ok" }
```

## Managing Migrations
### Creating a New Migration

Add a new migration file to the `migrations/` folder. Follow Flyway's naming convention:

`V<version>__<description>.sql`

Example:

-- File: `migrations/V3__add_price_index.sql`
```
CREATE INDEX idx_price ON historical_data (price);
```

### Running Migrations Manually

If Flyway has not applied migrations (e.g., after adding a new migration), start the Flyway service:

```
docker-compose up flyway
```

## To-do

- Integrate Swagger via FastAPI, providing examples
- Add linting tools (flake8 or pylint)
- Create a Postman Collection and hook it up to the GitHub Actions workflow
- Add logging and monitoring (e.g., Prometheus, Grafana)

## License

This project is licensed under the MIT License. See LICENSE for details.
