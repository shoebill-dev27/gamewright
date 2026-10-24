"""Source identification for measurements: a short hash over the executed source set."""

import hashlib
from pathlib import Path

_NAMES = ("game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py")


def source_id():
    """12 hex digits over game, session, play, run_driver, bots, source_id and tests/*.py.

    Reads files only. The BUILD string alone does not identify a source set.
    """
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    files = [root / name for name in _NAMES] + sorted((root / "tests").glob("*.py"))
    for path in files:
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        try:
            digest.update(path.read_bytes())
        except OSError:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()[:12]
