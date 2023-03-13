import requests

from speeches.util.file_util import *


if __name__ == "__main__":
    url_file = DATA_DIR / COVID_SPEECHES / "covid_speeches_urls"
    html_dir = DATA_DIR / COVID_SPEECHES / HTML

    html_dir.mkdir(parents=True, exist_ok=True)

    with open(url_file) as f:
        for line in f:
            url = line[:-1]
            print("Downloading:", url)
            payload = requests.get(url).content
            write_bytes((html_dir / url[url.rindex("/")+1:]).with_suffix(".html"), payload)
