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
