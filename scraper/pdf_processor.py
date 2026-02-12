import logging
import pdfplumber
import httpx
import io
import asyncio
import random
from datetime import datetime
from scraper.date_extractor import extract_date
from core.config import SSL_VERIFY_EXEMPT, REQUEST_TIMEOUT

logger = logging.getLogger("PDF_PROCESSOR")

# Production-grade User Agents to mimic real browser behavior
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def _process_pdf_sync(pdf_bytes):
    """Synchronous CPU-bound PDF parsing executed in a separate thread to prevent event loop lag."""
    try:
        with pdfplumber.open(pdf_bytes) as pdf:
            if not pdf.pages:
                return None
            
            # 1. Metadata Intelligence (Primary Check)
            # Many university PDFs include a CreationDate metadata field
            meta_date = pdf.metadata.get('CreationDate')
            if meta_date:
                try:
                    # Clean metadata string (format usually: D:YYYYMMDDHHMMSS)
                    clean_meta = meta_date.replace("D:", "")[:8]
                    return datetime.strptime(clean_meta, "%Y%m%d")
                except Exception:
                    pass

            # 2. Forensic Header Area Scan (Targeted Search)
            # Scans only the top 25% of the first page where dates usually reside
            p = pdf.pages[0]
            header_area = (0, 0, p.width, p.height * 0.25)
            header_text = p.within_bbox(header_area).extract_text()
            
            found_date = extract_date(header_text)
            if found_date:
                return found_date
            
            # 3. Deep Page Scan (Fallback)
            # Full text extraction from the first page
            return extract_date(p.extract_text())
            
    except Exception as e:
        logger.error(f"⚠️ Internal PDF Parsing Error: {e}")
        return None

async def get_date_from_pdf(pdf_url):
    """Asynchronous wrapper for PDF acquisition with browser-mimicry headers."""
    # Targeted SSL exemption for legacy university servers
    verify = not any(domain in pdf_url for domain in SSL_VERIFY_EXEMPT)
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/pdf,application/xhtml+xml,text/html;q=0.9,*/*;q=0.8",
        "Referer": "https://makautwb.ac.in/",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    try:
        # Using follow_redirects=True to handle university session routing
        async with httpx.AsyncClient(verify=verify, timeout=REQUEST_TIMEOUT, follow_redirects=True) as client:
            response = await client.get(pdf_url, headers=headers)
            
            if response.status_code != 200:
                logger.warning(f"📡 PDF Download Failed ({response.status_code}): {pdf_url}")
                return None
            
            # Use BytesIO to keep the file in memory and avoid disk I/O bottlenecks
            pdf_bytes = io.BytesIO(response.content)
            
            # Offload heavy CPU parsing to a thread to keep bot command responsiveness 100%
            return await asyncio.to_thread(_process_pdf_sync, pdf_bytes)

    except Exception as e:
        logger.error(f"🛑 PDF Acquisition Critical Error: {e} | URL: {pdf_url}")
        return None
        #@academictelebotbyroshhellwett