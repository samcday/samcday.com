#!/usr/bin/env python3
"""Dependency-free smoke checks for the static site, not a full HTML validator."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set()
        self.references = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.references.append(attrs[name])


def check():
    for filename in ("index.html", "style.css", "favicon.svg"):
        assert (PUBLIC / filename).is_file(), f"Missing {filename}"
        assert (PUBLIC / filename).stat().st_size, f"Empty {filename}"

    document = (PUBLIC / "index.html").read_text(encoding="utf-8")
    assert document.lstrip().lower().startswith("<!doctype html>"), "Missing HTML doctype"
    page = Page()
    page.feed(document)
    page.close()
    assert {"html", "head", "title", "body", "main"} <= page.tags, "Missing page structure"

    for reference in page.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        if url.path:
            target = (PUBLIC / unquote(url.path).lstrip("/")).resolve()
            assert target.is_relative_to(PUBLIC.resolve()), f"Outside public/: {reference}"
            assert target.is_file(), f"Missing local file: {reference}"
        elif url.fragment:
            assert unquote(url.fragment) in page.ids, f"Missing anchor: {reference}"

    ElementTree.parse(PUBLIC / "favicon.svg")
    assert not (ROOT / "functions").exists(), "This deployment is static-only"
    assert not (PUBLIC / "_worker.js").exists(), "This deployment is static-only"
    print("Static site checks passed")


if __name__ == "__main__":
    check()
