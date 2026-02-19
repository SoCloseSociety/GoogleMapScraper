# Contributing to Google Maps Scraper — Light Edition

Thanks for your interest in contributing! This project is built and maintained by the **SoClose** community. Whether you're fixing a bug, adding a feature, or improving docs — every contribution counts.

## Getting Started

1. **Fork** this repository
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/GoogleMapScraper.git
   cd GoogleMapScraper
   ```
3. Create a **virtual environment** and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Create a **feature branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

## Guidelines

### Code Style

- Keep it simple — this is the **Light Edition**, not an enterprise framework
- Follow existing patterns in the codebase
- Use descriptive variable and function names
- Add docstrings to new functions
- Use `logging` instead of `print()` for output

### Pull Requests

- One feature or fix per PR
- Write a clear description of what changed and why
- Test your changes before submitting
- Keep PRs small and focused

### Commit Messages

Use clear, descriptive commit messages:

```
Add proxy rotation support
Fix CSV encoding issue on Windows
Update README with new usage examples
```

## Ideas for Contributions

Here are some features the community would love to see:

- **New data fields** — ratings, review count, business category, Google Maps place ID
- **Export formats** — JSON, Excel (.xlsx), SQLite
- **Proxy support** — rotate proxies to avoid rate limiting
- **Multi-threading** — scrape multiple places in parallel
- **Search by area** — scrape all businesses in a geographic zone
- **Duplicate detection** — skip places already scraped
- **Tests** — unit tests for parsing logic
- **Docker support** — containerized deployment

## Reporting Bugs

Open an [issue](https://github.com/SoCloseSociety/GoogleMapScraper/issues) with:

- What you expected to happen
- What actually happened
- Steps to reproduce
- Your OS and Python version

## Community

Join the SoClose community at [soclose.com](https://soclose.com) to discuss ideas, get help, and collaborate on projects.

---

Thank you for making this project better!
