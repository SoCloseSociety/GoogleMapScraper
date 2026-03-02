#!/usr/bin/env python3
""
SoClose Google Maps Scraper — Light Edition
A lightweight, community-driven Google Maps data scraper.
https://github.com/SoCloseSociety/GoogleMapScraper

Usage:
    python main.py -q "restaurants+paris" -o results
    python main.py -u "https://www.google.com/maps/search/..." -o results
    python main.py --from-links results_links.csv -o results
"

def check_internet(host="one.one.one.one", port=None, timeout=3):
    """Return True if we can reach the internet."""
    try:
        addr = socket.gethostbyname(host)
        if not port:
            port = random.randint(1024, 65535)
        conn = socket.create_connection((addr, port), timeout)
        conn.close()
        return True
    except OSError:
        return False

# ... (rest of the file remains unchanged)
