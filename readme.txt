# Currency ELT & Analytics Dashboard
A containerized data pipeline that extracts CAD exchange rates from the Bank of Canada Valet API, transforms the data in PostgreSQL, and serves a Flask-based visualization dashboard.

## Technical Architecture
* **Infrastructure:** Docker & Docker Compose (Containerized Architecture)
* **Database:** PostgreSQL 15 (Relational Data Storage)
* **Backend:** Python 3.12, Flask, Psycopg3
* **ELT Process:** Automated Python scripts for extraction and SQL for transformation.
* **Environment:** WSL2 (Ubuntu) native Docker engine.

## Configuration:
Create a .env file in the root directory with:
DB_NAME=currency_db_elt
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=db
DB_PORT=5432

## How to Run
1.  Ensure Docker is running: `sudo service docker start`
2.  Build and launch the containers:
    ```bash
    docker compose up --build
    ```
3.  Populate the database (first run):
    ```bash
    docker exec -it valet_app python main.py
    ```
4.  Access the dashboard at `http://localhost:5000`
