#!/usr/bin/env python3
"""Extract text from a PDF file.

Uses pypdf to pull the text out of every page (or a selected page
range) and writes it to a text file, or prints it to standard
output when no output file is given. Pages that contain only
scanned images have no extractable text and are reported as empty.
"""
import argparse
import sys

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - handled with a clear message
    PdfReader = None


def parse_pages(spec, total):
    """Parse a page spec like '1-3', '2', or '1,4-5' (1-based)."""
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.update(range(int(start), int(end) + 1))
        elif part:
            pages.add(int(part))
    chosen = sorted(page for page in pages if 1 <= page <= total)
    if not chosen:
        raise ValueError(f"no valid pages in range '{spec}' "
                         f"(PDF has {total} page(s))")
    return chosen


def extract(input_path, pages=None):
    """Return [(page_number, text)] for the requested pages."""
    reader = PdfReader(input_path)
    total = len(reader.pages)
    wanted = pages or list(range(1, total + 1))
    result = []
    for number in wanted:
        text = reader.pages[number - 1].extract_text() or ""
        result.append((number, text))
    return result, total


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file.")
    parser.add_argument("input", help="input PDF file")
    parser.add_argument("-o", "--output",
                        help="output text file (default: print to stdout)")
    parser.add_argument("--pages",
                        help="pages to extract, e.g. '1-3' or '1,4-5' "
                             "(default: all pages)")
    parser.add_argument("--page-separator", default="\n--- page {n} ---\n",
                        help="separator printed between pages "
                             "(default: '\\n--- page {n} ---\\n')")
    args = parser.parse_args(argv)

    if PdfReader is None:
        print("error: pypdf is not installed. Run: pip install -r "
              "requirements.txt", file=sys.stderr)
        return 1
    try:
        reader = PdfReader(args.input)
        total = len(reader.pages)
    except FileNotFoundError:
        print(f"error: file not found: {args.input}", file=sys.stderr)
        return 1
    except Exception as exc:  # unreadable / not a PDF
        print(f"error: could not read PDF: {exc}", file=sys.stderr)
        return 1

    try:
        wanted = parse_pages(args.pages, total) if args.pages else None
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    extracted, _ = extract(args.input, wanted)
    empty = [n for n, text in extracted if not text.strip()]
    parts = []
    for number, text in extracted:
        if len(extracted) > 1:
            parts.append(args.page_separator.format(n=number))
        parts.append(text.rstrip("\n"))
    output_text = "\n".join(parts).strip() + "\n"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output_text)
        print(f"Extracted {len(extracted)} page(s) from {args.input} "
              f"-> {args.output}")
    else:
        print(output_text, end="")
    if empty:
        print(f"Note: no extractable text on page(s): "
              f"{', '.join(map(str, empty))} (may be scanned images)",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
