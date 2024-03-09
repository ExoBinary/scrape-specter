# FastAPI and Scrapy Project

This project integrates FastAPI with Scrapy to create a web scraping API. Users can initiate scraping tasks via an API endpoint, and the results are stored in a PostgreSQL database.

## Features

- **FastAPI Endpoint**: Initiate scraping tasks by sending requests to a FastAPI endpoint.
- **Scrapy Spider**: Leverages Scrapy's PyppeteerSpider to scrape web pages asynchronously.
- **Concurrency Control**: Ensures that the same domain is not scraped concurrently by different users.
- **Database Storage**: Stores the scraped data and domain statuses in a PostgreSQL database.

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- pipenv or virtualenv (optional but recommended for package management)

### Installation

1. Clone the repository:

```
git clone https://github.com/ExoBinary/scrape-specter.git
```

2. Navigate to the project directory:

```
cd scrape-specter
```

3. Install the required Python packages:

```
pip install -r requirements.txt
```

4. Set up the PostgreSQL database and update the `.env` file with your `DATABASE_URL`, for example:

```
DATABASE_URL=postgresql://username:password@localhost/yourdatabase
```

5. Initialize the database tables:

```
python

from modules.database import create_tables
create_tables()
```

### Running the Application

To start the FastAPI application, run:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Using the API

To initiate a scraping task, send a POST request to the `/crawl/` endpoint with the target URL:

```
curl -X 'POST'
'http://localhost:8000/crawl/'
-H 'accept: application/json'
-H 'Content-Type: application/json'
-d '{"url": "https://example.com"}'
```

## Project Structure

- `main.py`: The FastAPI application.
- `modules/spider.py`: Contains the PyppeteerSpider used for scraping.
- `modules/database.py`: Database models and session management.
- `.env`: Environment variables, including the database connection string.

## License

Specify your license.

## Contributing

Instructions for how to contribute to the project.