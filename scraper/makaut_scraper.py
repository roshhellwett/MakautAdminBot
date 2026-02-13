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

# Robust User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/121.0.0.0 Safari/537.36"
]

async def build_item(title, url, source_name, date_context=None):
    if not title or not url: return None
    
    # 1. Forensic Noise Filtering
    BLOCKLIST = ["about us", "contact", "home", "back", "gallery", "archive", "click here"]
    if len(title) < 3 or any(k in title.lower() for k in BLOCKLIST): 
        return None

    # 2. Date Discovery (Title -> Context -> PDF)
    real_date = extract_date(title) 
    if not real_date and date_context:
        real_date = extract_date(date_context)
    
    # 3. Deep Scan (PDF Header Analysis)
    if not real_date and ".pdf" in url.lower():
        # Only deep scan if it looks like a notice (avoid huge files)
        real_date = await get_date_from_pdf(url)

    # 4. Validity Check (Academic Year Window)
    if real_date and real_date.year in [TARGET_YEAR, TARGET_YEAR - 1]:
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
        await asyncio.sleep(random.uniform(2, 5)) # Polite Delay
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT, verify=verify, follow_redirects=True) as client:
            r = await client.get(source_config["url"], headers=headers)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            
            items = []
            
            # STRATEGY 1: Table Row Scan (Best for MAKAUT tables)
            rows = soup.find_all("tr")
            if len(rows) > 5:
                logger.info(f"🔎 {source_key}: Scanning {len(rows)} table rows...")
                for row in rows:
                    link = row.find("a", href=True)
                    if link:
                        # Pass the ENTIRE row text as context (contains date column)
                        full_row_text = row.get_text(" ", strip=True)
                        full_url = urljoin(source_config["url"], link["href"])
                        
                        item = await build_item(
                            link.get_text(strip=True), 
                            full_url, 
                            source_config["source"], 
                            full_row_text
                        )
                        if item: items.append(item)
            
            # STRATEGY 2: Fallback (Div/List based sites)
            if not items:
                logger.info(f"⚠️ {source_key}: No table rows found, trying fallback scan...")
                container = soup.find("div", {"id": "content"}) or soup.body
                for a in container.find_all("a", href=True):
                    full_url = urljoin(source_config["url"], a["href"])
                    # Use parent paragraph/div as context
                    context = a.parent.get_text(strip=True) if a.parent else ""
                    item = await build_item(
                        a.get_text(strip=True), 
                        full_url, 
                        source_config["source"], 
                        context
                    )
                    if item: items.append(item)

            if items:
                logger.info(f"✅ {source_key}: Successfully extracted {len(items)} notices.")
            else:
                logger.warning(f"⚠️ {source_key}: Found links but NO VALID DATES extracted.")
                
            return items

    except Exception as e:
        logger.error(f"❌ Source Failure [{source_key}]: {e}")
        return []
            #@academictelebotbyroshhellwett