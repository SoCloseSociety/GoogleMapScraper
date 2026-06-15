# NEO_CONNECTOR -- GoogleMapScraper
- service: googlemapscraper
- base_url_prod: N/A (no network service -- local CLI tool)
- auth: none (no server, no API)
- env_required: [] (none -- all config is hardcoded constants in main.py)
- generated_at:

## Summary verdict
**This project exposes NO HTTP API.** It is a pure command-line Selenium scraper
(`main.py`, monolithic). It MUST NOT be wired into NeoBot as an HTTP tool. There are
no routes, webhooks, SSE, WebSocket, cron, or queue endpoints to call. The only entry
point is the local CLI invoked via `python main.py ...`, which launches a Chrome
WebDriver and writes CSV files to disk.

Proof (files read in full):
- `main.py` -- imports only `argparse, csv, logging, os, sys, time, random, socket,
  selenium, webdriver_manager, bs4, pandas`. No web framework (no Flask/FastAPI/
  aiohttp/Express/uvicorn). Single guarded entry: `if __name__ == "__main__": main()`.
- `requirements.txt` -- `beautifulsoup4, selenium, webdriver-manager, pandas`. No
  server/runtime dependency.
- `CLAUDE.md` -- declares "Architecture: Monolithic (single main.py)", "No .env file
  needed", "CLI tool".
- Repo-wide grep for `flask|fastapi|aiohttp|@app.|@router|express|app.(get|post)|
  uvicorn|webhook|websocket|listen(|createServer|os.environ|getenv|.env` -> no matches.

## Endpoints
None. No HTTP/webhook/SSE/WS/cron/queue endpoints exist in this repo.

## CLI interface (informational only -- NOT a network endpoint)
The only invocable surface is the local CLI. Argument parser proven in
`main.py:parse_args()` (lines 267-301). Provide exactly one of `--url`/`--query`/
`--from-links`.

| arg | type | required | description |
|-----|------|----------|-------------|
| `-u` / `--url` | string | one-of | Full Google Maps search URL. |
| `-q` / `--query` | string | one-of | Search query (spaces -> `+`); builds the URL. |
| `--from-links` | path (CSV) | one-of | Skip Phase 1; extract details from an existing `*_links.csv`. |
| `-o` / `--output` | string | no (default `output`) | Base name for output CSV files. |
| `--headless` | flag | no | Run Chrome with no visible window. |
| `--links-only` | flag | no | Phase 1 only (collect links, skip detail extraction). |

Behaviour (proven in `main()` lines 304-364):
- Phase 1 `collect_links()` -> writes `<output>_links.csv` (column: `link`).
- Phase 2 `scrape_details()` -> writes `<output>_details.csv` (columns: name, address,
  website, phone, schedule); CSV re-written after each place (crash-safe).
- Long-running and synchronous: blocking Selenium run, random 2-4s delay per place, no
  job/poll/result async pattern, no return value over any wire.
- Exit codes: `sys.exit(1)` on no input arg, file-not-found (`--from-links`), or no
  internet (`check_internet()`); otherwise returns 0.

## Flows
No network flow. Local two-phase pipeline:
1. Build search URL from `-q`/`-u` (or load links from `--from-links`).
2. `check_internet()` -> launch Chrome WebDriver (`create_driver`).
3. Phase 1: scroll `div[role="feed"]`, harvest `/maps/place/` links -> `*_links.csv`.
4. Phase 2: visit each link, parse `<h1>` + info panel -> `*_details.csv`.

## Gaps
None affecting connectivity. The absence of an API is definitive, not uncertain:
the conclusion is proven by the full read of `main.py` + `requirements.txt` + a
repo-wide grep that returned zero web-framework / env-var matters.

If a remote-callable interface is ever wanted, it would have to be added (e.g. a
FastAPI wrapper exposing `generate -> poll -> result`) -- it does not exist today.

## Recap
- Endpoints found: 0 HTTP / 0 webhook / 0 SSE / 0 WS / 0 cron / 0 queue.
- CLI commands: 1 entry point (`python main.py`) with 6 args.
- Already covered in NeoBot integrations.py: N/A (not an HTTP service).
- New endpoints to wire: 0. Do NOT add Neo HTTP tools for this repo.
