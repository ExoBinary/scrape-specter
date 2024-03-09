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

The API will be available at `http://localhost:8039`.

### Using the API

To initiate a scraping task, send a POST request to the `/crawl/` endpoint with the target URL:

```
curl -X 'POST'
'http://localhost:8039/crawl/'
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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

MIT License

Copyright (c) 2024 ExoBinary

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request