from pathlib import Path

UPLOADS = Path("/srv/app/uploads").resolve()

def safe_path(filename: str) -> Path:
    p = (UPLOADS / filename).resolve()
    if not p.is_relative_to(UPLOADS):          # Python 3.9+
        raise ValueError("invalid file name")
    return p
