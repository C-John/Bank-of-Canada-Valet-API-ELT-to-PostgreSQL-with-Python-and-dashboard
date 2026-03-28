# Currency ELT & Analytics Dashboard
A containerized data pipeline that extracts CAD exchange rates from the Bank of Canada Valet API, transforms the data in PostgreSQL, and serves a Flask-based visualization dashboard.

## Technical Architecture
* **Infrastructure:** Docker & Docker Compose (Containerized Architecture)
* **Database:** PostgreSQL 15 (Relational Data Storage)
* [cite_start]**Backend:** Python 3.11, Flask, Psycopg3 
* **ELT Process:** Automated Python scripts for extraction and SQL for transformation
* **Environment:** WSL2 (Ubuntu) native Docker engine

## Configuration
Create a `.env` file in the root directory with:
```env
DB_NAME=currency_db_elt
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=db
DB_PORT=5432
```

## How to Run
1. **Start Docker:** `sudo service docker start`

2. **Build & Launch:** 

    In your `bash` Terminal:
    ```bash
    docker compose up --build
    ```
3. **Populate DB:**

    In a second `bash` Terminal not running the flask service:
    ```bash
    docker exec -it valet_app python main.py
    ```
4. **Dashboard:**

    Open a `web browser` and navigate to `URL`:
    ```URL
    http://localhost:5000
    ```
5. **Stop & Clean Up:**

    In your `bash` Terminal:
    ```bash
    docker compose down
    ```

### Legal & Copyright
**Copyright (c) 2026 Calder Henry. All rights reserved.**
*This repository is for portfolio demonstration purposes. No part of this code may be used, modified, or redistributed without explicit permission.*