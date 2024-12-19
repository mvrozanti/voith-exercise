![CI](https://github.com/mvrozanti/voith-exercise/actions/workflows/ci.yml/badge.svg)

# Time Series Data API with Flyway

This project is a Dockerized API for accessing and managing cryptocurrency time series data. It includes a MySQL database, a Python FastAPI application, and Flyway for database migrations.

---

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Optional: `curl` or a similar HTTP client for testing API endpoints.

---

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

### Managing Migrations
#### Creating a New Migration

Add a new migration file to the `migrations/` folder. Follow Flyway's naming convention:

`V<version>__<description>.sql`

Example:

-- File: `migrations/V3__add_price_index.sql`
```
CREATE INDEX idx_price ON historical_data (price);
```

#### Running Migrations Manually

If Flyway has not applied migrations (e.g., after adding a new migration), start the Flyway service:

```
docker-compose up flyway
```

### Testing the API
#### Health Check

Verify the API is running:

```
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

#### Query Time Series Data

Fetch time series data using a GET request:

```
curl "http://localhost:8000/timeseries?coin_id=api3&start=2024-12-15&end=2024-12-18"
```

Expected response:

```json
{
  "source": "database",
  "data": [
    {"coin_id": "bitcoin", "timestamp": "2024-01-01T00:00:00", "price": 50000.0, "volume": 1000.0}
  ]
}
```

#### Verifying the Import

After running the script, you can verify the imported data:

    docker exec -i mysql mysql -uroot -prootpass -e "SELECT * FROM historical_data LIMIT 5;" timeseries_db

## License

This project is licensed under the MIT License. See LICENSE for details.
