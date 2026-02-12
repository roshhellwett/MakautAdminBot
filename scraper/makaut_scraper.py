import httpx
import random
import logging
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

from utils.hash_util import generate_hash
from core.sources import URLS
from core.config import SSL_VERIFY_EXEMPT, TARGET_YEAR, REQUEST_TIMEOUT
from scraper.date_extractor import extract_date
from scraper.pdf_processor import get_date_from_pdf

logger = logging.getLogger("SCRAPER")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/121.0.0.0 Safari/537.36"
]

async def build_item(title, url, source_name, date_context=None):
    if not title or not url: return None
    
    # Forensic noise reduction [cite: 33]
    BLOCKLIST = ["about us", "contact", "home", "back", "gallery"]
    if any(k in title.lower() for k in BLOCKLIST): return None

    # Multi-stage Date Inference
    real_date = extract_date(title) or (extract_date(date_context) if date_context else None)
    
    # PDF Content Fallback
    if not real_date and ".pdf" in url.lower():
        real_date = await get_date_from_pdf(url)

    if real_date and real_date.year == TARGET_YEAR:
        return {
            "title": title.strip(),
            "source": source_name,
            "source_url": url,
            "pdf_url": url if ".pdf" in url.lower() else None,
            "content_hash": generate_hash(title, url),
            "published_date": real_date,
            "scraped_at": datetime.utcnow()
        }
    return None

async def scrape_source(source_key, source_config):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    verify = not any(domain in source_config["url"] for domain in SSL_VERIFY_EXEMPT)
    
    try:
        await asyncio.sleep(random.uniform(1, 3)) # Stealth Jitter 
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, verify=verify) as client:
            r = await client.get(source_config["url"], headers=headers)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Context-aware scraping
            items = []
            container = soup.find("div", {"id": "content"}) or soup.find("table") or soup
            for a in container.find_all("a", href=True):
                full_url = urljoin(source_config["url"], a["href"])
                item = await build_item(a.get_text(strip=True), full_url, source_config["source"], a.parent.get_text())
                if item: items.append(item)
            return items
    except Exception as e:
        logger.error(f"Source Failure {source_key}: {e}")
        return []
            #@academictelebotbyroshhellwett