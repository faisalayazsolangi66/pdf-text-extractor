# PDF Text Extractor

Extract text from a PDF file using [pypdf](https://pypdf.readthedocs.io/).
Extracts every page by default, or a selected range with
`--pages` (for example `1-3` or `1,4-5`). Output goes to a text
file with `-o`, or to standard output when no output file is
given. Pages that contain only scanned images have no extractable
text and are reported as empty.

## Requirements

- Python 3
- pypdf (see `requirements.txt`)

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py report.pdf
python3 main.py report.pdf -o report.txt
python3 main.py report.pdf -o first-pages.txt --pages 1-3
```

## Example

```bash
$ python3 main.py report.pdf -o report.txt
Extracted 5 page(s) from report.pdf -> report.txt

$ head -3 report.txt
Annual Report 2026
Revenue grew 12% year over year.
```

## License

MIT — see [LICENSE](LICENSE).
