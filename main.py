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

def check_internet(host="one.one.one.one", port=80, timeout=3):
    """Return True if we can reach the internet."""
    try:
        addr = socket.gethostbyname(host)
        conn = socket.create_connection((addr, port), timeout)
        conn.close()
        return True
    except OSError:
        return False

# New function to generate a dynamic host name
def get_dynamic_host():
    import random
    hosts = ['one.one.one.one', '8.8.8.8', '9.9.9.9']  # Example list of safe hosts
    return random.choice(hosts)

# Update check_internet to use the dynamic host name
def check_internet(host=None, port=80, timeout=3):
    if not host:
        host = get_dynamic_host()
    try:
        addr = socket.gethostbyname(host)
        conn = socket.create_connection((addr, port), timeout)
        conn.close()
        return True
    except OSError:
        return False

# Update the rest of the code to use the new check_internet function
# (No changes needed for other parts of the code as it already uses check_internet)
