# CLAUDE.md -- GoogleMapScraper

## 1. Project Identity

**Name:** GoogleMapScraper -- Google Maps Business Data Extractor
**Role:** CLI tool to extract business data (name, address, phone, website, hours) from Google Maps search results using a two-phase approach (collect links then scrape details).
**Author:** SoClose Society (https://soclose.co)
**License:** MIT

### Stack

- **Language:** Python 3.9+
- **Browser:** Selenium 4.15+ with webdriver-manager
- **Parsing:** BeautifulSoup4
- **Data:** pandas
- **Architecture:** Monolithic (single main.py, 368 LOC)

### Architecture

```
Phase 1: Scroll Google Maps feed -> Collect /maps/place/ links -> Save CSV
Phase 2: Visit each link -> Parse HTML -> Extract 5 fields -> Append CSV (crash-safe)
```

### Critical Files

- `main.py` -- All logic (368 LOC, monolithic)
- No config files -- constants hardcoded at top of main.py

## 2-5. Standard Workflow

- Enter plan mode for non-trivial tasks
- Test with a small query first (`-q "restaurants+paris"`)
- Verify both phases complete and CSV has data
- Track tasks in `tasks/todo.md`, lessons in `tasks/lessons.md`

## 6. Project-Specific Rules

### Dev Commands
```bash
pip install -r requirements.txt
python main.py -q "restaurants+paris" -o results      # Search query
python main.py -u "https://maps.google.com/..." -o results  # Direct URL
python main.py --headless -q "plumber+london"          # Headless mode
python main.py --links-only -q "cafes+berlin"          # Phase 1 only
python main.py --from-links results_links.csv          # Phase 2 only
```

### Config (hardcoded in main.py)
- DEFAULT_DELAY=(2,4), PAGE_LOAD_TIMEOUT=15
- SCROLL_PAUSE=1.5, MAX_SCROLL_STALLS=15
- No .env file needed

### Known Fragile Areas
- Google Maps DOM changes can break extraction
- Google consent popup handling -- may need updating per region
- Anti-bot: Google can serve CAPTCHAs for automated access

## 7. Core Principles

- Simplicity First, No Laziness, Minimal Impact
- Never use em dashes (use -- instead)
- Never reduce scroll delays

## Neo Connector (auto)
Ce projet expose `NEO_CONNECTOR.md` : le manifeste machine-lisible de TOUS ses
endpoints/auth/env, consommé par NeoBot pour se câbler automatiquement.
- ÉTAT ACTUEL : ce repo est un OUTIL CLI pur (Selenium scraper, aucune API HTTP). Il ne
  doit PAS être câblé comme outil HTTP Neo. Le manifeste documente cette absence.
- RÈGLE : à chaque ajout/suppression/modif d'un endpoint, d'une auth ou d'une env var,
  régénère le manifeste via `/neo-connector` (ou le prompt dans .claude/skills/neo-connector).
- Ne jamais éditer NEO_CONNECTOR.md à la main : il est généré.
- Le hook pre-commit (.git/hooks/pre-commit) avertit si des routes ont changé sans MAJ du manifeste.
