"""Generate resume-print.pdf from index.html (zero margins, background colors).

Requires: pip install playwright==1.63.0 (CI pins this version; see .github/workflows/generate-pdf.yml)
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent

with sync_playwright() as p:
    try:
        browser = p.chromium.launch()  # CI: bundled chromium
    except Exception:
        browser = p.chromium.launch(channel="chrome")  # local: system chrome
    page = browser.new_page()
    page.goto((ROOT / "index.html").as_uri())
    page.wait_for_timeout(1000)  # let JS compute dynamic durations
    page.pdf(
        path=str(ROOT / "resume-print.pdf"),
        prefer_css_page_size=True,
        print_background=True,
        margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
    )
    browser.close()

print("resume-print.pdf generated")
