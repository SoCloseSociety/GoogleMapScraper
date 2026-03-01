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

import argparse
import csv
import logging
import os
import sys
time
random
socket

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from user_agent import generate_user_agent

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_DELAY = (2, 4)          # Random delay range between requests (seconds)
PAGE_LOAD_TIMEOUT = 15          # Max wait for page elements (seconds)
SCROLL_PAUSE = 1.5              # Pause between scrolls (seconds)
MAX_SCROLL_STALLS = 15          # Stop scrolling after N stalls with no new links

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("soclose-gmaps")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def check_internet(host="one.one.one.one", port=80, timeout=3):
    """Return True if we can reach the internet."""
    try:
        addr = socket.gethostbyname(host)
        conn = socket.create_connection((addr, port), timeout)
        conn.close()
        return True
    except OSError:
        return False

def create_driver(headless=False):
    """Create and return a configured Chrome WebDriver instance."""
    opts = Options()
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--lang=en")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )
    opts.add_experimental_option("useAutomationExtension", False)

    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)

    if not headless:
        driver.maximize_window()

    driver.set_page_load_timeout(30)
    return driver

def random_delay(bounds=DEFAULT_DELAY):
    """Sleep for a random duration within *bounds*."""
    time.sleep(random.uniform(*bounds))

# ---------------------------------------------------------------------------
# Phase 1 — Collect place links
# ---------------------------------------------------------------------------

def collect_links(driver, url):
    """Scroll through Google Maps results and collect all place links.

    Returns a sorted list of unique Google Maps place URLs.
    """
    log.info("Phase 1 — Collecting place links ...")
    driver.get(url + "&hl=en")

    # Wait for the results feed to load
    try:
        WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
        )
    except TimeoutException:
        log.error("Timed out waiting for the results feed. Check your URL.")
        return []

    feed = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')

    links = set()
    stall_count = 0

    while True:
        prev_count = len(links)

        # Parse current page source
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/maps/place/" in href:
                links.add(href)

        new_count = len(links)
        log.info(f"  Links found: {new_count}")

        if new_count == prev_count:
            stall_count += 1
            if stall_count >= MAX_SCROLL_STALLS:
                log.info("  No new results — stopping scroll.")
                break
        else:
            stall_count = 0

        # Scroll the feed container
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", feed
        )
        time.sleep(SCROLL_PAUSE)

    log.info(f"Phase 1 complete — {len(links)} links collected.")
    return sorted(links)

# ---------------------------------------------------------------------------
# Phase 2 — Extract business details
# ---------------------------------------------------------------------------

def extract_details(driver, link):
    """Visit a single place link and extract business information.

    Returns a dict with keys: name, address, website, phone, schedule.
    Returns an empty dict on failure.
    """
    driver.get(link + "&hl=en")

    try:
        WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
    except TimeoutException:
        log.warning(f"  Timeout loading: {link[:80]}...")
        return {}

    soup = BeautifulSoup(driver.page_source, "html.parser")

    data = {
        "name": None,
        "address": None,
        "website": None,
        "phone": None,
        "schedule": None,
    }

    # Business name
    h1 = soup.find("h1")
    if h1:
        data["name"] = h1.get_text(strip=True)

    # Information panel
    for div in soup.find_all("div", attrs={"aria-label": True}):
        label = div["aria-label"]

        if "Information for" in label:
            # Address
            btn = div.find("button", attrs={"data-item-id": "address"})
            if btn:
                data["address"] = btn.get_text(strip=True)

            # Website
            a_tag = div.find("a", attrs={"data-item-id": "authority"})
            if a_tag and a_tag.get("href"):
                data["website"] = a_tag["href"]

            # Phone
            for button in div.find_all("button", attrs={"aria-label": True}):
                if "Phone" in button["aria-label"]:
                    data["phone"] = button.get_text(strip=True)
                    break

        elif "opening hours" in label.lower() or "open hours" in label.lower():
            parts = label.split(".")
            if parts and len(parts[0]) > 0:
                data["schedule"] = parts[0].replace(",", " -> ")

    return data

def scrape_details(driver, links, output_path):
    """Iterate through all links, extract details, and save to CSV.

    Progress is saved after each extraction (crash-safe).
    """
    log.info(f"Phase 2 — Extracting details for {len(links)} places ...")
    results = []

    for i, link in enumerate(links, 1):
        log.info(f"  [{i}/{len(links)}] Scraping ...")

        try:
            data = extract_details(driver, link)
            if data and data.get("name"):
                results.append(data)
                log.info(f"    -> {data["name"]}")
            else:
                log.warning("    -> No data extracted")
        except WebDriverException as exc:
            log.error(f"    -> WebDriver error: {exc}")

        # Save progress after each extraction (crash-safe)
        if results:
            df = pd.DataFrame(results)
            df.to_csv(output_path, index=False, encoding="utf-8")

        random_delay()

    log.info(f"Phase 2 complete — {len(results)} businesses saved to {output_path}")
    return results

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

BANNER = r""
  ____         ____ _
 / ___|  ___  / ___| | ___  ___  ___
 \___ \ / _ \| |   | |/ _ \/ __|/ _ \
  ___) | (_) | |___| | (_) \__ \  __/
 |____/ \___/ \____|_|\"# noqa
       Google Maps Scraper — Light
"


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="SoClose Google Maps Scraper — extract business data from Google Maps.",
        epilog="Example:  python main.py -q 'restaurants+paris' -o results",
    )
    parser.add_argument(
        "-u", "--url",
        help="Full Google Maps search URL.",
    )
    parser.add_argument(
        "-q", "--query",
        help="Search query (spaces replaced with +). Builds the URL for you.",
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Base name for output CSV files (default: output).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode (no visible browser window).",
    )
    parser.add_argument(
        "--links-only",
        action="store_true",
        help="Only collect links — skip detail extraction.",
    )
    parser.add_argument(
        "--from-links",
        metavar="CSV",
        help="Skip link collection and extract details from an existing links CSV.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if not check_internet():
        log.error("No internet connection. Exiting...")
        sys.exit(1)

    driver = create_driver(headless=args.headless)

    try:
        if args.url or args.query:
            links = collect_links(driver, args.url or f'https://www.google.com/maps/search/{args.query.replace(" ", "+")}')
        elif args.from_links:
            with open(args.from_links, newline='') as csvfile:
                reader = csv.reader(csvfile)
                links = [row[0] for row in reader]
        else:
            log.error("No URL or query provided. Exiting...")
            sys.exit(1)

        if not args.links_only:
            output_path = f"{args.output}.csv"
            scrape_details(driver, links, output_path)
    finally:
        driver.quit()
