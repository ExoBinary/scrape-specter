from fastapi import FastAPI, HTTPException
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from modules.spider import PyppeteerSpider
from modules.database import create_tables
from multiprocessing import Process, Manager, freeze_support
from urllib.parse import urlparse
import re

app = FastAPI()

# Declare the manager and lock_dict as global variables to initialize them later
manager = None
lock_dict = None

def run_crawler(domain, lock_dict):
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(PyppeteerSpider, start_urls=[domain])
        process.start()
        process.join()  # Wait for the crawling process to finish before releasing the lock.
    except Exception:
        raise HTTPException(status_code=500, detail="Server Error. Please report this issue.")
    finally:
        lock_dict[domain] = False  # Ensure the lock is released even if an exception occurs.

@app.post("/crawl/")
async def crawl(url: str):
    global lock_dict

    # Validate and format the URL
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Validate the URL using regex
    if not re.match(r'(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    # Extract the domain from the URL
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Acquire the lock for the domain
    if domain in lock_dict and lock_dict[domain]:
        return {"detail": f"Crawling initiated for domain: {domain}"}
    lock_dict[domain] = True

    # Run the crawler in a separate process using the extracted domain
    p = Process(target=run_crawler, args=(domain, lock_dict))
    p.start()

    return {"detail": f"Crawling initiated for domain: {domain}"}

if __name__ == "__main__":
    import uvicorn
    freeze_support()  # Add freeze_support for multiprocessing on Windows

    # Initialize the manager and lock_dict inside the main guard
    manager = Manager()
    lock_dict = manager.dict()

    # Call create_tables to ensure all tables are created
    create_tables()

    uvicorn.run(app, host="0.0.0.0", port=8039)