from fastapi import FastAPI, HTTPException
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from modules.spider import PyppeteerSpider
from modules.database import create_tables
from multiprocessing import Process, Manager, freeze_support
from urllib.parse import urlparse
import re
import uvicorn

# Initialize FastAPI application
app = FastAPI()

# Declare global variables for manager and lock dictionary
manager = None
lock_dict = None

def run_crawler(domain, lock_dict):
    """
    Run the Scrapy crawler in a separate process.

    :param domain: Domain to crawl.
    :param lock_dict: Dictionary to manage domain locks.
    """
    try:
        # Initialize and start Scrapy crawler process
        process = CrawlerProcess(get_project_settings())
        process.crawl(PyppeteerSpider, start_urls=[domain])
        process.start()
        process.join()
    except Exception:
        # In case of any exception, raise HTTP 500 error
        raise HTTPException(status_code=500, detail="Server Error. Please report this issue.")
    finally:
        # Release the domain lock after crawling is finished or an exception occurs
        lock_dict[domain] = False

@app.post("/crawl/")
async def crawl(url: str):
    """
    API endpoint to initiate web crawling.

    :param url: URL to crawl.
    :return: Response indicating the crawling initiation status.
    """
    global lock_dict

    # Ensure URL starts with http or https
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Validate URL format
    if not re.match(r'(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    # Extract domain from URL
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Check and set lock for the domain
    if domain in lock_dict and lock_dict[domain]:
        return {"detail": f"Crawling initiated for domain: {domain}"}
    lock_dict[domain] = True

    # Initiate crawling in a separate process
    p = Process(target=run_crawler, args=(domain, lock_dict))
    p.start()

    return {"detail": f"Crawling initiated for domain: {domain}"}

if __name__ == "__main__":
    # Ensure proper multiprocessing support on Windows
    freeze_support()

    # Initialize the manager and lock dictionary
    manager = Manager()
    lock_dict = manager.dict()

    # Create database tables if they don't exist
    create_tables()

    # Start the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=8039)