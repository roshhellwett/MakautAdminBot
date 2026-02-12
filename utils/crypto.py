import hashlib

def generate_notice_hash(title: str, url: str) -> str:
    """
    Forensic Fingerprinting: Generates a unique SHA-256 hash.
    Used for global deduplication across all university sources.
    """
    raw = f"{title.strip().lower()}|{url.strip().lower()}"
    return hashlib.sha256(raw.encode()).hexdigest()