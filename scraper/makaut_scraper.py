import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import time
from urllib.parse import urljoin
import urllib3

from utils.hash_util import generate_hash
from core.sources import URLS
from scraper.date_extractor import extract_date
from scraper.pdf_processor import get_date_from_pdf

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger("SCRAPER")

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
})

STRICT_BLOCKLIST = [
    "about us", "contact", "directory", "staff", "genesis", "vision", 
    "mission", "campus", "library", "login", "register", "sitemap", 
    "disclaimer", "university", "chancellor", "vice-chancellor", "registrar",
    "home", "administration", "committees", "affiliated", "regulations", 
    "academics", "schools", "programmes", "syllabus", "calendar", "moocs", 
    "ph.d.", "aicte", "ugc", "mhrd", "aishe", "nptel", "swayam", "fee", 
    "scholarship", "entrance", "happening", "seminar", "workshop", "events", 
    "students", "placements", "results", "alumni", "gallery", "hostel", "sports"
]

def build_item(title, url, source_name, date_context=None):
    """
    STRICT 2026 GATEKEEPER:
    1. Check for 2026 in Title/Context (Regex)
    2. Check for 2026 in PDF Metadata/Text
    3. If no 2026 date found, discard the notice.
    """
    if not title or not url: 
        return None
    
    # 1. Filter out static noise
    if any(k in title.lower() for k in STRICT_BLOCKLIST):
        return None

    # 2. Extract Date (Regex First)
    real_date = extract_date(title)
    if not real_date and date_context:
        real_date = extract_date(date_context)
    
    # 3. PDF Deep Scan (Local Only - No AI)
    if not real_date and ".pdf" in url.lower():
        real_date = get_date_from_pdf(url)

    # 4. FINAL 2026 VALIDATION
    # Only keep the notice if we verified it is from 2026
    if real_date and real_date.year == 2026:
        return {
            "title": title.strip(),
            "source": source_name,
            "source_url": url,
            "pdf_url": url if ".pdf" in url.lower() else None,
            "content_hash": generate_hash(title, url),
            "published_date": real_date,
            "scraped_at": datetime.utcnow()
        }
    
    # Notice is either old or could not be verified; discard it.
    return None

def parse_generic_links(base_url, source_name):
    data = []
    seen = set()
    verify_ssl = False if "makautexam" in base_url else True
    try:
        r = SESSION.get(base_url, timeout=30, verify=verify_ssl)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        main_body = soup.find("div", {"id": "content"}) or soup.find("div", class_="content") or soup.find("table") or soup
        for a in main_body.find_all("a"):
            title = a.get_text(" ", strip=True)
            href = a.get("href")
            if not title or not href: continue
            full_url = urljoin(base_url, href)
            if not full_url.startswith(("http:", "https:")): continue
            context_text = a.parent.get_text(" ", strip=True) if a.parent else ""
            h = generate_hash(title, full_url)
            if h in seen: continue
            seen.add(h)
            item = build_item(title, full_url, source_name, context_text)
            if item:
                data.append(item)
    except Exception as e:
        logger.error(f"Scrape error on {base_url}: {e}")
    return data

def scrape_source(source_key, source_config):
    url = source_config["url"]
    source_name = source_config["source"]
    try:
        return parse_generic_links(url, source_name)
    except Exception as e:
        logger.warning(f"{source_key} failed: {e}")
    return []

def scrape_all_sources():
    all_data = []
    for key, config in URLS.items():
        logger.info(f"SCRAPING SOURCE: {key}")
        source_data = scrape_source(key, config)
        all_data.extend(source_data)
    return all_data