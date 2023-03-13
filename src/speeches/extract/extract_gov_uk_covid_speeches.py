from bs4 import BeautifulSoup

from speeches.util.file_util import *


if __name__ == "__main__":
    html_dir = DATA_DIR / COVID_SPEECHES / HTML
    txt_dir = DATA_DIR / COVID_SPEECHES / TEXT

    for file in html_dir.iterdir():
        print("Processing:", file)
        with open(file) as f:
            soup = BeautifulSoup(f, "html.parser")
            for para in soup.find_all("div", {"class": "govspeak"}):
                text = para.get_text().replace(u"\u00A0", " ")
                write_text((txt_dir / file.name).with_suffix(".txt"), text)
