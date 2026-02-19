<p align="center">
  <img src="assets/banner.svg" alt="Google Maps Scraper" width="900">
</p>

<p align="center">
  <strong>Extract business data from Google Maps — names, addresses, phone numbers, websites and hours in one command.</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-575ECF?style=flat-square" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.9%2B-575ECF?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+"></a>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-575ECF?style=flat-square" alt="Platform">
  <a href="https://www.selenium.dev/"><img src="https://img.shields.io/badge/Selenium-4.15%2B-575ECF?style=flat-square&logo=selenium&logoColor=white" alt="Selenium"></a>
  <a href="https://github.com/SoCloseSociety/GoogleMapScraper/stargazers"><img src="https://img.shields.io/github/stars/SoCloseSociety/GoogleMapScraper?style=flat-square&color=575ECF" alt="GitHub Stars"></a>
  <a href="https://github.com/SoCloseSociety/GoogleMapScraper/issues"><img src="https://img.shields.io/github/issues/SoCloseSociety/GoogleMapScraper?style=flat-square&color=575ECF" alt="Issues"></a>
  <a href="https://github.com/SoCloseSociety/GoogleMapScraper/network/members"><img src="https://img.shields.io/github/forks/SoCloseSociety/GoogleMapScraper?style=flat-square&color=575ECF" alt="Forks"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#key-features">Features</a> &bull;
  <a href="#configuration">Configuration</a> &bull;
  <a href="#faq">FAQ</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

---

## What is Google Maps Scraper?

**Google Maps Scraper** is a free, open-source **Google Maps data extraction tool** built with Python and Selenium. It lets you scrape business information from any Google Maps search — names, addresses, phone numbers, websites, and opening hours — into clean CSV files.

Need to build a lead list, research local businesses, or gather market data? This scraper automates what would take hours of manual copy-pasting. Provide a search query or URL, and get a ready-to-use CSV.

### Who is this for?

- **Sales Teams** building lead lists of local businesses
- **Market Researchers** analyzing business density by area
- **Real Estate Agents** studying commercial activity in neighborhoods
- **Startup Founders** doing competitive landscape analysis
- **SEO Agencies** auditing local business listings
- **Data Analysts** collecting location-based business data

### Key Features

- **Single Command** - Provide a search query or URL, get a CSV
- **Two-Phase Scraping** - Collects all place links first, then extracts details
- **Crash-Safe** - Progress saved after each extraction; interrupt and resume anytime
- **Headless Mode** - Run without a visible browser window
- **Smart Scrolling** - Automatically detects when all results are loaded
- **Anti-Detection** - Randomized delays, clean browser fingerprint
- **CLI-First** - Fully scriptable with argparse options
- **Lightweight** - Only 4 dependencies, no bloat
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Free & Open Source** - MIT license, no API key required

---

## Quick Start

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **Python** | Version 3.9 or higher ([Download](https://www.python.org/downloads/)) |
| **Google Chrome** | Latest version ([Download](https://www.google.com/chrome/)) |

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/SoCloseSociety/GoogleMapScraper.git
cd GoogleMapScraper

# 2. (Recommended) Create a virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Search by query
python main.py -q "restaurants+paris" -o my_results

# Search by full Google Maps URL
python main.py -u "https://www.google.com/maps/search/dentist+london/" -o dentists
```

The scraper will:
1. Open Chrome and search Google Maps
2. Scroll through all results and collect every place link
3. Visit each place and extract business details
4. Save everything to CSV files

#### All CLI Options

```bash
python main.py --help
```

| Option | Description | Default |
|--------|-------------|---------|
| `-u, --url URL` | Full Google Maps search URL | None |
| `-q, --query QUERY` | Search query (spaces replaced with +) | None |
| `-o, --output NAME` | Base name for output CSV files | `output` |
| `--headless` | Run Chrome without visible browser window | Off |
| `--links-only` | Only collect links, skip detail extraction | Off |
| `--from-links CSV` | Skip link collection, extract from existing CSV | None |

#### Examples

```bash
# Headless mode (no browser window)
python main.py -q "bakery+tokyo" -o bakeries --headless

# Collect links only (fast reconnaissance)
python main.py -q "gym+berlin" -o gyms --links-only

# Resume from a previous links file (skip Phase 1)
python main.py --from-links gyms_links.csv -o gyms
```

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

## Data Extracted

| Field | Description |
|-------|-------------|
| **Name** | Business name |
| **Address** | Full street address |
| **Phone** | Phone number |
| **Website** | Business website URL |
| **Schedule** | Opening hours |

---

## Configuration

You can adjust these constants at the top of `main.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `DEFAULT_DELAY` | `(2, 4)` | Random delay range between requests (seconds) |
| `PAGE_LOAD_TIMEOUT` | `15` | Max wait for page elements (seconds) |
| `SCROLL_PAUSE` | `1.5` | Pause between scrolls (seconds) |
| `MAX_SCROLL_STALLS` | `15` | Stop scrolling after N stalls with no new links |

---

## Project Structure

```
GoogleMapScraper/
├── main.py              # Main scraper script
├── requirements.txt     # Python dependencies
├── assets/
│   └── banner.svg       # Project banner
├── LICENSE              # MIT License
├── README.md            # This file
├── CONTRIBUTING.md      # Contribution guidelines
└── .gitignore           # Git ignore rules
```

---

## Troubleshooting

### Chrome driver issues

The scraper uses `webdriver-manager` to automatically download the correct ChromeDriver. If you encounter issues:

```bash
pip install --upgrade webdriver-manager
```

### No results found

If the scraper doesn't find any links:
1. Try using a full Google Maps URL with `-u` instead of a query
2. Make sure Chrome is up to date
3. Try without `--headless` to see what's happening

### Google Maps UI changes

Google occasionally updates its interface. If the scraper breaks:
1. Check the [Issues](https://github.com/SoCloseSociety/GoogleMapScraper/issues) page
2. Open a new issue with the error message

---

## FAQ

**Q: Is this free?**
A: Yes. Google Maps Scraper is 100% free and open source under the MIT license.

**Q: Do I need a Google Maps API key?**
A: No. This tool uses browser automation (Selenium), so no API key is needed.

**Q: How many businesses can I scrape?**
A: The tool scrapes all results returned by Google Maps for your search. Just be mindful of Google's usage policies.

**Q: Can I resume a failed scrape?**
A: Yes! Use `--from-links` to resume from a previously saved links CSV.

**Q: Does it work on Mac / Linux?**
A: Yes. Fully cross-platform on Windows, macOS, and Linux.

**Q: Can I run it without a browser window?**
A: Yes. Use `--headless` mode.

---

## Alternatives Comparison

| Feature | Google Maps Scraper | Manual Copy-Paste | Google Places API | Outscraper |
|---------|--------------------|--------------------|-------------------|------------|
| Price | **Free** | Free | $0.02/request | $2.50/1000 |
| Bulk extraction | Yes | No | Yes | Yes |
| Crash recovery | Yes | N/A | N/A | N/A |
| Open source | Yes | N/A | No | No |
| API key required | No | No | Yes | Yes |
| Cross-platform | Yes | Yes | Any | Web only |
| Headless mode | Yes | N/A | N/A | N/A |

---

## Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) before submitting a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Disclaimer

This tool is provided for **educational and research purposes only**. Scraping Google Maps may violate Google's Terms of Service. You are solely responsible for how you use this tool. The authors are not responsible for any misuse or consequences arising from the use of this software.

---

<p align="center">
  <strong>If this project helps you, please give it a star!</strong><br>
  It helps others discover this tool.<br><br>
  <a href="https://github.com/SoCloseSociety/GoogleMapScraper">
    <img src="https://img.shields.io/github/stars/SoCloseSociety/GoogleMapScraper?style=for-the-badge&logo=github&color=575ECF" alt="Star this repo">
  </a>
</p>

<br>

<p align="center">
  <sub>Built with purpose by <a href="https://soclose.co"><strong>SoClose</strong></a> &mdash; Digital Innovation Through Automation & AI</sub><br>
  <sub>
    <a href="https://soclose.co">Website</a> &bull;
    <a href="https://linkedin.com/company/soclose-agency">LinkedIn</a> &bull;
    <a href="https://twitter.com/SoCloseAgency">Twitter</a> &bull;
    <a href="mailto:hello@soclose.co">Contact</a>
  </sub>
</p>
