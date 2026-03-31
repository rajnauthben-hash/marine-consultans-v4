from __future__ import annotations

from pathlib import Path

import server


ROOT = Path(__file__).resolve().parent


def write_page(destination: Path, body: str) -> None:
    destination.write_text(body, encoding="utf-8")
    print(f"Wrote {destination.relative_to(ROOT)}")


def main() -> None:
    written = set()

    for route, page in server.PAGE_SOURCES.items():
        if route == "/":
            continue
        destination = ROOT / route.lstrip("/")
        body = server.transform_html(route, page["source"], page["title"])
        write_page(destination, body)
        written.add(destination)

    for route, body in server.EXTRA_PAGES.items():
        destination = ROOT / route.lstrip("/")
        write_page(destination, body)
        written.add(destination)

    not_found = server.extra_page(
        "Page Not Found | Marine Consultants",
        "Page Not Found",
        "The requested page does not exist in this export. Use the links below to return to the main site.",
    )
    write_page(ROOT / "404.html", not_found)
    written.add(ROOT / "404.html")

    print(f"Generated {len(written)} static pages.")


if __name__ == "__main__":
    main()
