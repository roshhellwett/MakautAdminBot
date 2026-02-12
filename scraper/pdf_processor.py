import logging
import pdfplumber
import requests
import io
from scraper.date_extractor import extract_date

logger = logging.getLogger("PDF_PROCESSOR")

def get_date_from_pdf(pdf_url):
    """
    FREE EXTRACTION ONLY:
    Strictly searches for 2026 dates in Metadata and Local Text.
    """
    try:
        # Download PDF into memory
        response = requests.get(pdf_url, timeout=15, verify=False)
        if response.status_code != 200: 
            return None
        pdf_bytes = io.BytesIO(response.content)

        with pdfplumber.open(pdf_bytes) as pdf:
            # --- STEP 1: METADATA CHECK (FREE) ---
            meta_date = pdf.metadata.get('CreationDate')
            if meta_date and "2026" in meta_date:
                # Format: D:20260212...
                raw_str = meta_date[2:10]
                try:
                    from datetime import datetime
                    found_dt = datetime.strptime(raw_str, "%Y%m%d")
                    return found_dt
                except: 
                    pass

            # --- STEP 2: LOCAL TEXT SCAN (FREE) ---
            # Search only the first 1000 characters for a 2026 date
            if len(pdf.pages) > 0:
                first_page_text = pdf.pages[0].extract_text()
                if first_page_text:
                    found_date = extract_date(first_page_text[:1000])
                    if found_date and found_date.year == 2026:
                        return found_date

    except Exception as e:
        logger.error(f"❌ PDF Local Scan Error: {e}")
    
    return None