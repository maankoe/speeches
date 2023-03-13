from pathlib import Path

HTML = "html"
TEXT = "txt"
COVID_SPEECHES = "covid_speeches"
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def write_bytes(file_path: Path, payload: bytes):
    with open(file_path, "wb") as f:
        f.write(payload)


def write_text(file_path: Path, payload: str):
    with open(file_path, "w") as f:
        f.write(payload)