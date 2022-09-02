import argparse
import csv
import logging

from data_providers import ISBNAPI


def read_csv_file(filename):
    result = []
    with open(filename, newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";", )
        for row in reader:
            result.append(row)
    return result

def main():
    parser = argparse.ArgumentParser(description='Obtain book data based on ISBN')
    parser.add_argument(
        "--zotero-host", action="store", required=True,
        help="Zotero host ('authorize' header value in web library)"
    )
    parser.add_argument(
        "--input", action="store", required=True,
        help="Path to input CSV file (must contain 'ISBN' header)"
    )
    parser.add_argument(
        "--output", action="store", required=True,
        help="Path to output CSV file"
    )
    parser.add_argument(
        "--log-level", action="store", default="critical",
        help="Logging level"
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level.upper())
    log = logging.getLogger(__name__)

    csv_data = read_csv_file(args.input)
    isbn_api = ISBNAPI(zotero_host=args.zotero_host)

    for row in csv_data:
        if (isbn := row.get("ISBN/ISSN")) and not row.get("Tytul"):
            try:
                data = isbn_api.fetch(isbn)
            except ValueError:
                log.info("Failed to find any data for %s", isbn)
                continue
            row["Tytul"] = data.title
            row["Wydawnictwo"] = data.publisher
            row["Liczba stron"] = data.pages_number
            row["Wydanie"] = data.issue_number
            row["Miejsce"] = data.place
            row["Rok"] = data.year
            for idx, author in enumerate(data.authors, start=1):
                row[f"Imie{idx}"] = author.get("first_name", "")
                row[f"Nazwisko{idx}"] = author.get("last_name", "")

    with open(args.output, "w") as fh:
        fieldnames = csv_data[0].keys()
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(csv_data)

if __name__ == '__main__':
    main()
