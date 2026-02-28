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
    max_attempts = 100  # Add a limit to the number of attempts

    while len(links) < max_attempts:
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
