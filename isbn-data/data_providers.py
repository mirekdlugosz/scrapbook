import logging
from dataclasses import asdict

from diskcache import Cache
from requests_cache import CachedSession
from xdg import xdg_cache_home

from dto import BookData
from utils import sanitize_string


session = CachedSession(
    "python-isbn-requests",
    use_cache_dir=True,
    allowable_methods=['GET', 'POST'],
)
log = logging.getLogger(__name__)


class GoogleBooksAPI:
    def __init__(self):
        self._url = "https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

    def fetch(self, isbn):
        url = self._url.format(isbn=isbn)
        response = session.get(url)
        books_data = response.json().get('items')
        if not books_data:
            raise ValueError(f"Google Books doesn't know anything about {isbn}")
        if len(books_data) > 1:
            raise ValueError(f"ISBN {isbn} is not unique book identifier in Google Books")
        data = books_data[0].get('volumeInfo')

        authors = []
        for author in data.get("authors", []):
            first_name, last_name = author.rsplit(" ", maxsplit=1)
            authors.append({
                "first_name": sanitize_string(first_name),
                "last_name": sanitize_string(last_name),
            })

        return BookData(
            title=sanitize_string(data.get('title')),
            authors=authors,
            pages_number=data.get('pageCount'),
            year=int(data.get('publishedDate'))
        )


class ZoteroAPI:
    def __init__(self, host):
        self._url = f"https://{host}/Prod//search"
        self._headers = {
            "authority": host,
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,pl;q=0.8",
            "content-type": "text/plain",
            "origin": "https://www.zotero.org",
            "pragma": "no-cache",
            "referer": "https://www.zotero.org/",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        }

    def fetch(self, isbn):
        response = session.post(self._url, data=isbn, headers=self._headers)
        books_data = response.json()
        if not books_data:
            raise ValueError(f"Zotero doesn't know anything about {isbn}")
        if len(books_data) > 1:
            raise ValueError(f"ISBN {isbn} is not unique book identifier in Zotero")
        data = books_data[0]

        authors = []
        for creator in data.get('creators', []):
            authors.append({
                "first_name": sanitize_string(creator.get("firstName")),
                "last_name": sanitize_string(creator.get("lastName")),
            })

        return BookData(
            title=sanitize_string(data.get('title')),
            authors=authors,
            publisher=sanitize_string(data.get('publisher')),
            place=sanitize_string(data.get('place')),
            year=int(data.get('date'))
        )


class ISBNAPI:
    def __init__(self, zotero_host):
        self._google_api = GoogleBooksAPI()
        self._zotero_api = ZoteroAPI(zotero_host)
        self._cache = Cache(directory=(xdg_cache_home() / "python-isbn"))

    def _get_data_using(self, api, isbn):
        try:
            response = api.fetch(isbn)
        except ValueError as e:
            log.info("%s failed to fetch %s:", api.__class__.__name__, isbn, exc_info=True)
            return {}

        data = {
            key: value
            for key, value
            in asdict(response).items()
            if value is not None
        }
        return data

    def fetch(self, isbn):
        isbn = isbn.replace("-", "")
        isbn_data = self._cache.get(isbn)
        if isbn_data:
            log.debug("Cache hit for isbn %s", isbn)
            return BookData(**isbn_data)

        log.info("Cache MISS for isbn %s", isbn)
        google_data = self._get_data_using(self._google_api, isbn)
        zotero_data = self._get_data_using(self._zotero_api, isbn)

        isbn_data = {**google_data, **zotero_data}
        if not isbn_data:
            raise ValueError(f"Failed to find any data for {isbn}")

        if (
            (zotero_authors := zotero_data.get("authors"))
            and (google_authors := google_data.get("authors"))
            and len(zotero_authors) > len(google_authors)
        ):
            log.info(
                "Zotero returned more authors (%s) than Google (%s), using Google data",
                len(zotero_authors),
                len(google_authors),
            )
            isbn_data["authors"] = google_authors

        if len(isbn_data.get("authors")) > 3:
            isbn_data["authors"] = isbn_data.get("authors")[:3]

        self._cache.set(isbn, isbn_data)
        return BookData(**isbn_data)
