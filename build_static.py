from __future__ import annotations

import struct
from pathlib import Path

import server


ROOT = Path(__file__).resolve().parent


def write_page(destination: Path, body: str) -> None:
    destination.write_text(body, encoding="utf-8")
    print(f"Wrote {destination.relative_to(ROOT)}")


def write_favicon(destination: Path) -> None:
    width = height = 16
    blue = (0x28, 0x16, 0x00, 0xFF)
    orange = (0x00, 0x6A, 0xEB, 0xFF)
    white = (0xFF, 0xFF, 0xFF, 0xFF)

    pixels = bytearray()
    for y in range(height - 1, -1, -1):
        for x in range(width):
            if x < 8:
                color = blue
            else:
                color = orange
            if 3 <= x <= 12 and 3 <= y <= 12 and abs(x - y) <= 1:
                color = white
            pixels.extend(color)

    mask = b"\x00\x00\x00\x00" * height
    dib_header = struct.pack(
        "<IIIHHIIIIII",
        40,
        width,
        height * 2,
        1,
        32,
        0,
        len(pixels) + len(mask),
        0,
        0,
        0,
        0,
    )
    image_data = dib_header + pixels + mask
    icon_header = struct.pack("<HHH", 0, 1, 1)
    directory_entry = struct.pack("<BBBBHHII", width, height, 0, 0, 1, 32, len(image_data), 22)
    destination.write_bytes(icon_header + directory_entry + image_data)
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

    favicon = ROOT / "favicon.ico"
    write_favicon(favicon)
    written.add(favicon)

    print(f"Generated {len(written)} static pages.")


if __name__ == "__main__":
    main()
