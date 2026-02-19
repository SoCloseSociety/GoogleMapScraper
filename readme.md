<p align="center">
  <img src="https://img.shields.io/badge/SoClose-Community%20Edition-blueviolet?style=for-the-badge" alt="SoClose Community Edition" />
  <img src="https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+" />
  <img src="https://img.shields.io/github/license/SoCloseSociety/GoogleMapScraper?style=for-the-badge" alt="MIT License" />
  <img src="https://img.shields.io/github/stars/SoCloseSociety/GoogleMapScraper?style=for-the-badge" alt="Stars" />
</p>

<h1 align="center">Google Maps Scraper — Light Edition</h1>

<p align="center">
  <strong>A lightweight, open-source Google Maps scraper built by the <a href="https://soclose.com">SoClose</a> community.</strong><br/>
  Extract business names, addresses, phone numbers, websites, and opening hours from any Google Maps search — in a single command.
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-output">Output</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## Why This Tool?

Need to build a lead list, research local businesses, or gather market data? This scraper automates what would take hours of manual copy-pasting from Google Maps into a clean CSV file you can open in Excel, Google Sheets, or any CRM.

**This is the Light Edition** — simple, single-file, easy to understand and extend. Built for the SoClose community to learn from, improve, and use.

---

## Features

- **Single command** — provide a search query or URL, get a CSV
- **Two-phase scraping** — collects all place links first, then extracts details
- **Crash-safe** — progress is saved after each extraction; interrupt and resume anytime
- **Headless mode** — run without a visible browser window (servers, CI, etc.)
- **Smart scrolling** — automatically detects when all results are loaded
- **Anti-detection** — randomized delays, clean browser fingerprint
- **CLI-first** — fully scriptable with `argparse` options
- **Lightweight** — only 4 dependencies, no bloat

### Data Extracted

| Field        | Description                        |
| ------------ | ---------------------------------- |
| **Name**     | Business name                      |
| **Address**  | Full street address                |
| **Phone**    | Phone number                       |
| **Website**  | Business website URL               |
| **Schedule** | Opening hours                      |

---

## Quick Start

### Prerequisites

- **Python 3.9+** — [Download](https://www.python.org/downloads/)
- **Google Chrome** — [Download](https://www.google.com/chrome/)

### Installation

```bash
# Clone the repository
git clone https://github.com/SoCloseSociety/GoogleMapScraper.git
cd GoogleMapScraper

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run your first scrape

```bash
python main.py -q "restaurants+paris" -o my_results
```

This will:
1. Open Chrome and search Google Maps for "restaurants paris"
2. Scroll through all results and collect every place link
3. Visit each place and extract business details
4. Save everything to `my_results_details.csv`

---

## Usage

```
usage: main.py [-h] [-u URL] [-q QUERY] [-o OUTPUT] [--headless] [--links-only] [--from-links CSV]

SoClose Google Maps Scraper — extract business data from Google Maps.

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Full Google Maps search URL.
  -q QUERY, --query QUERY
                        Search query (spaces replaced with +). Builds the URL for you.
  -o OUTPUT, --output OUTPUT
                        Base name for output CSV files (default: output).
  --headless            Run Chrome in headless mode (no visible browser window).
  --links-only          Only collect links — skip detail extraction.
  --from-links CSV      Skip link collection and extract details from an existing links CSV.
```

### Examples

```bash
# Search by query
python main.py -q "plumber+new+york" -o plumbers_ny

# Search by full Google Maps URL
python main.py -u "https://www.google.com/maps/search/dentist+london/" -o dentists

# Headless mode (no browser window)
python main.py -q "bakery+tokyo" -o bakeries --headless

# Collect links only (fast reconnaissance)
python main.py -q "gym+berlin" -o gyms --links-only

# Resume from a previous links file (skip Phase 1)
python main.py --from-links gyms_links.csv -o gyms
```

---

## Output

The scraper produces two CSV files:

**`{output}_links.csv`** — All place URLs discovered

| link                                        |
| ------------------------------------------- |
| https://www.google.com/maps/place/Café+... |
| https://www.google.com/maps/place/Resto+... |

**`{output}_details.csv`** — Extracted business data

| name          | address            | website             | phone          | schedule             |
| ------------- | ------------------ | ------------------- | -------------- | -------------------- |
| Le Petit Café | 12 Rue de Rivoli   | https://example.com | +33 1 23 45 67 | Monday -> 9AM–10PM   |
| Chez Marcel   | 8 Avenue Montaigne | https://marcel.fr   | +33 1 98 76 54 | Tuesday -> 10AM–11PM |

---

## How It Works

```
┌──────────────────────────────────────────────────────┐
│                    PHASE 1                           │
│         Scroll & Collect Place Links                 │
│                                                      │
│  Google Maps URL ──> Scroll feed ──> Extract /maps/  │
│                      place/ links ──> Save CSV       │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                    PHASE 2                           │
│         Visit Each Place & Extract Details           │
│                                                      │
│  For each link ──> Load page ──> Parse HTML ──>      │
│  Extract name, address, phone, website, schedule     │
│  ──> Append to CSV (crash-safe)                      │
└──────────────────────────────────────────────────────┘
```

---

## Configuration

You can adjust these constants at the top of [main.py](main.py):

| Constant             | Default  | Description                                      |
| -------------------- | -------- | ------------------------------------------------ |
| `DEFAULT_DELAY`      | `(2, 4)` | Random delay range between requests (seconds)    |
| `PAGE_LOAD_TIMEOUT`  | `15`     | Max wait for page elements (seconds)             |
| `SCROLL_PAUSE`       | `1.5`    | Pause between scrolls (seconds)                  |
| `MAX_SCROLL_STALLS`  | `15`     | Stop scrolling after N stalls with no new links  |

---

## Contributing

We welcome contributions from the SoClose community and beyond! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick contribution ideas:**
- Add new data fields (ratings, reviews count, category)
- Add export formats (JSON, Excel)
- Improve anti-detection
- Add proxy support
- Translate the README
- Write tests

---

## Disclaimer

This tool is provided **for educational and research purposes only**. Scraping Google Maps may violate Google's Terms of Service. You are solely responsible for how you use this tool and any consequences that may arise. The authors and the SoClose community assume no liability for misuse.

Always respect website terms of service and local regulations regarding data collection.

---

## License

[MIT License](LICENSE) — Free to use, modify, and distribute.

---

<p align="center">
  Built with care by the <a href="https://soclose.com"><strong>SoClose</strong></a> community.<br/>
  Star this repo if it helped you!
</p>
