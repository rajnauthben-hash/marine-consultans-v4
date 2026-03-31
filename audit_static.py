from __future__ import annotations

import argparse
import contextlib
import re
import subprocess
import threading
import urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parent
ROUTES = [
    "/",
    "/index.html",
    "/about.html",
    "/products.html",
    "/services.html",
    "/support.html",
    "/industries.html",
    "/news.html",
    "/contact.html",
    "/quote.html",
    "/privacy.html",
    "/terms.html",
    "/404.html",
    "/favicon.ico",
]


def find_chrome() -> str | None:
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


@contextlib.contextmanager
def local_server(port: int):
    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(ROOT), **kwargs)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def fetch_status(url: str) -> int:
    with urllib.request.urlopen(url) as response:
        return response.status


def dump_dom(chrome: str, url: str, timeout: int) -> str:
    result = subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--blink-settings=imagesEnabled=false",
            f"--timeout={timeout * 1000}",
            f"--virtual-time-budget={timeout * 1000}",
            "--dump-dom",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=timeout + 45,
    )
    return result.stdout


def scrub_dom(dom: str) -> str:
    dom = re.sub(r"<script.*?</script>", "", dom, flags=re.I | re.S)
    dom = re.sub(r"<style.*?</style>", "", dom, flags=re.I | re.S)
    return dom


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the generated static deployment output.")
    parser.add_argument("--port", type=int, default=8030)
    parser.add_argument("--timeout", type=int, default=7)
    args = parser.parse_args()

    chrome = find_chrome()
    if not chrome:
        raise SystemExit("Chrome or Edge was not found. Unable to run browser-backed audit.")

    with local_server(args.port) as base_url:
        print(f"Serving static output from {base_url}")

        route_failures: list[str] = []
        for route in ROUTES:
            url = urljoin(base_url, route)
            status = fetch_status(url)
            print(f"{route} -> {status}")
            if status != 200:
                route_failures.append(route)

        if route_failures:
            raise SystemExit(f"Route audit failed: {route_failures}")

        dom_issues: list[str] = []
        checked_internal_links: set[str] = set()
        pages_for_dom = [
            "/index.html",
            "/about.html",
            "/products.html",
            "/services.html",
            "/support.html",
            "/industries.html",
            "/news.html",
            "/contact.html",
            "/quote.html",
            "/privacy.html",
            "/terms.html",
        ]

        for route in pages_for_dom:
            url = urljoin(base_url, route)
            dom = scrub_dom(dump_dom(chrome, url, args.timeout))
            if "{{DATA:SCREEN:" in dom:
                dom_issues.append(f"{route}: unresolved Stitch placeholders in live DOM")

            hash_links = re.findall(r'href=\"#\"', dom, flags=re.I)
            if hash_links:
                dom_issues.append(f"{route}: {len(hash_links)} live hash links remained after JS")

            for href in re.findall(r'href=\"([^\"]+)\"', dom, flags=re.I):
                if href.startswith(("mailto:", "tel:", "https://", "http://")):
                    continue
                normalized = urlparse(urljoin(url, href))._replace(fragment="").geturl()
                checked_internal_links.add(normalized)

        link_failures: list[str] = []
        for link in sorted(checked_internal_links):
            status = fetch_status(link)
            if status != 200:
                link_failures.append(f"{link} -> {status}")

        print(f"Checked internal browser links: {len(checked_internal_links)}")

        if dom_issues:
            for issue in dom_issues:
                print(issue)
            raise SystemExit("DOM audit failed.")

        if link_failures:
            for issue in link_failures:
                print(issue)
            raise SystemExit("Internal link audit failed.")

        print("Static audit passed.")


if __name__ == "__main__":
    main()
