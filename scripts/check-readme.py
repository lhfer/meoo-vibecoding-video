#!/usr/bin/env python3
"""Check presentation links and self-contained SVG assets, without network access."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ('README.md', 'docs/case-study.md')
ASSETS = ROOT / 'docs/media/readme'


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, bool]] = []
        self.anchors: set[str] = set()
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        a = dict(attrs)
        for key in ('id', 'name'):
            if a.get(key):
                self.anchors.add(a[key])
        if tag == 'a' and a.get('href'):
            self.links.append((a['href'], False))
        if tag == 'img':
            if not a.get('alt', '').strip():
                self.errors.append('Image has no descriptive alt text')
            if a.get('src'):
                self.links.append((a['src'], True))
        if tag == 'source' and a.get('srcset'):
            for item in a['srcset'].split(','):
                if item.strip():
                    self.links.append((item.strip().split()[0], True))


def check(known: set[str]) -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    for name in DOCUMENTS:
        path = ROOT / name
        if not path.is_file():
            errors.append(f'Missing document: {name}')
            continue
        text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        parser = References()
        parser.feed(text)
        errors.extend(f'{name}: {e}' for e in parser.errors)
        for match in re.finditer(r'(!?)\[([^\]\n]*)\]\(([^\s)]+)\)', text):
            image, label, target = match.groups()
            parser.links.append((target, bool(image)))
            if image and not label.strip():
                errors.append(f'{name}: Markdown image has no alt text')
        for target, image in parser.links:
            count += 1
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                if image:
                    errors.append(f'{name}: Image must be repository-relative: {target}')
                continue
            if not parsed.path:
                if parsed.fragment and unquote(parsed.fragment) not in parser.anchors:
                    errors.append(f'{name}: Missing explicit anchor: {target}')
                continue
            local = (ROOT / unquote(parsed.path).lstrip('/') if parsed.path.startswith('/')
                     else path.parent / unquote(parsed.path)).resolve()
            if not local.is_relative_to(ROOT):
                errors.append(f'{name}: Link escapes repository: {target}')
                continue
            relative = local.relative_to(ROOT).as_posix()
            if not local.exists() and relative not in known:
                errors.append(f'{name}: Missing local target: {target}')
    assets = sorted(ASSETS.glob('*.svg'))
    if len(assets) != 6:
        errors.append(f'Expected 6 presentation SVGs, found {len(assets)}')
    for path in assets:
        raw = path.read_text(encoding='utf-8')
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            errors.append(f'{path.name}: Invalid SVG: {exc}')
            continue
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        if root.find('svg:title', ns) is None or root.find('svg:desc', ns) is None:
            errors.append(f'{path.name}: Missing accessible title/description')
        if not root.get('viewBox'):
            errors.append(f'{path.name}: Missing responsive viewBox')
        if path.stat().st_size > 32_000:
            errors.append(f'{path.name}: Exceeds 32 KB asset budget')
        for node in root.iter():
            tag = node.tag.rsplit('}', 1)[-1]
            if tag in {'script', 'foreignObject', 'image'}:
                errors.append(f'{path.name}: Unsupported or externally dependent element: {tag}')
            for key, value in node.attrib.items():
                key = key.rsplit('}', 1)[-1]
                if key.lower().startswith('on'):
                    errors.append(f'{path.name}: Event handlers are not allowed')
                if key in {'href', 'src'} and not value.startswith('#'):
                    errors.append(f'{path.name}: External dependency: {value}')
        if '@import' in raw or '@font-face' in raw:
            errors.append(f'{path.name}: Imported CSS/fonts are not allowed')
        for value in re.findall(r'url\(([^)]+)\)', raw):
            if not value.strip(' \"\'').startswith('#'):
                errors.append(f'{path.name}: External CSS dependency: {value}')
    return errors, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--known-paths', type=Path,
                        help='Optional fresh, newline-delimited Git tree inventory for a sparse checkout; validates path existence only.')
    args = parser.parse_args()
    known = set(args.known_paths.read_text(encoding='utf-8').splitlines()) if args.known_paths else set()
    errors, count = check(known)
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in errors), file=sys.stderr)
        return 1
    print(f'PASS: {count} references checked; 6 self-contained SVGs parsed; no external image dependencies.')
    if known:
        print('Sparse-checkout mode: unavailable file paths were checked against the supplied tree inventory, not downloaded.')
    print('No HTTP availability, hosted GitHub rendering, GIF decoding, or Skill runtime test was performed by this checker.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
