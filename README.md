# NYC Taxi Pipeline

A lightweight ETL pipeline for ingesting NYC taxi trip data into PostgreSQL.

## Overview

This project uses Docker Compose to run:

- `pgdatabase` — PostgreSQL database for storing taxi data
- `pgadmin` — pgAdmin web interface for database administration

The ingest script downloads a CSV file from a remote URL, converts date columns, and loads the data into PostgreSQL in chunks.

## Requirements

- Docker
- Docker Compose
- Internet access for downloading dataset files

## Setup

1. Open a terminal in this folder:
   ```bash
   cd nyc-taxi-pipeline
   ```

2. Start the services:
   ```bash
   docker compose up -d
   ```

3. Verify services are running:
   ```bash
   docker compose ps
   ```

## Default Access

pgAdmin is available at:

- `http://localhost:8080`

Login credentials:

- Email: `admin@admin.com`
- Password: `root`

PostgreSQL connection values:

- Host: `localhost`
- Port: `5432`
- User: `root`
- Password: `root`
- Database: `ny_taxi`

## Ingest Data

Use the script to load a CSV file into PostgreSQL.

Example:

```bash
docker run -it --network=nyc-taxi-pipeline_default \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
```

If you run the script directly in the container environment, use the same credentials and host name `pgdatabase`.

## How It Works

- Connects to PostgreSQL using SQLAlchemy
- Reads the remote CSV in chunks for memory efficiency
- Converts `tpep_pickup_datetime` and `tpep_dropoff_datetime` to datetime
- Creates or replaces the destination table
- Appends each chunk to the table

## Notes

- The pipeline currently assumes the CSV contains `tpep_pickup_datetime` and `tpep_dropoff_datetime` columns.
- The first chunk is used to create the table schema, then all chunks are appended.
- If you need to change credentials or ports, update `docker-compose.yml` and restart the services.

## Troubleshooting

- If pgAdmin returns authentication errors, restart Docker Compose and clear browser cookies for the forwarded URL.
- If the container is using an obsolete `version` field warning, the current compose file is still valid but can be updated to the newer format later.
## 🛠️ Technologies
- **Python 3.12+** with `uv` for fast dependency management
- **PostgreSQL 17** for robust data storage
- **Docker & Docker Compose** for containerization and orchestration
- **Pandas & SQLAlchemy** for efficient data manipulation and ETL
- **Click** for user-friendly CLI argument parsing