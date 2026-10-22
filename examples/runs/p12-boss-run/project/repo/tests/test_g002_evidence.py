"""E0 inventory and bounded evidence selection; no product or bot changes.

Run from repo: python3 -m unittest discover -s tests
Inventory IDs use module.class.method; group headers supply module.class.
To select existing evidence, import emit_rows from a later evidence test.
Selection never changes the collection being evaluated by that test.
"""
import json
from pathlib import Path
import unittest

from source_id import source_id


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def emit_rows(target, columns, rows, start=1, stop=None, excluded=()):
    """Print a numbered, explicitly bounded window over already evaluated rows.

    Callers must evaluate/assert their complete target collection before calling.
    This helper reports selection and completeness, not criterion success.
    Numbers are one-based inclusive. Empty collections are supported.
    Missing END or numbered rows in collected output means incomplete evidence.
    """
    rows = list(rows)
    if start < 1 or (stop is not None and stop < start):
        raise ValueError("invalid one-based inclusive evidence window")
    last = len(rows) if stop is None else min(stop, len(rows))
    selected = list(enumerate(rows, 1))[start - 1:last]
    metadata = {
        "target": target, "source_id": source_id(),
        "columns": columns, "total": len(rows), "shown": len(selected),
        "window": [start, last],
        "unshown_before": min(start - 1, len(rows)),
        "unshown_after": max(0, len(rows) - max(last, start - 1)),
        "excluded": list(excluded),
        "meaning": "display only; assertions and conditions belong to caller",
    }
    print("EVIDENCE_BEGIN " + json.dumps(metadata, ensure_ascii=False, sort_keys=True))
    for number, row in selected:
        print(f"{number:03d} " + json.dumps(row, ensure_ascii=False, sort_keys=True))
    print("EVIDENCE_END " + json.dumps({
        "target": target, "total": len(rows), "shown": len(selected),
    }, sort_keys=True))


class EvidenceToolTest(unittest.TestCase):
    def test_bounded_selection_reports_missing_ranges(self):
        import contextlib
        import io

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            emit_rows("tool-self-check", ["value"], [[1], [2], [3]], 2, 2,
                      excluded=["outside target"])
        lines = output.getvalue().splitlines()
        metadata = json.loads(lines[0].split(" ", 1)[1])
        self.assertEqual((metadata["total"], metadata["shown"]), (3, 1))
        self.assertEqual((metadata["unshown_before"], metadata["unshown_after"]), (1, 1))
        self.assertEqual(lines[1], "002 [2]")
        self.assertTrue(lines[-1].startswith("EVIDENCE_END "))
        with self.assertRaises(ValueError):
            emit_rows("invalid", [], [], 0)

    def test_inventory_all_files_and_discovered_ids(self):
        root = Path(__file__).resolve().parent.parent
        files = sorted((root / "tests").glob("*.py"))
        loader = unittest.TestLoader()
        # Use a fresh loader, and inspect without executing the discovered tests.
        suite = loader.discover(str(root / "tests"))
        ids = [case.id() for case in flatten(suite)]
        self.assertEqual(loader.errors, [])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn(self.id(), ids)
        source_files = [
            "game.py", "session.py", "play.py", "run_driver.py",
            "bots.py", "source_id.py",
        ] + [str(path.relative_to(root)) for path in files]
        print("INVENTORY_BEGIN source=" + source_id())
        print("columns: F number path; G module.class; I number method; "
              "full test ID = current G + '.' + method")
        for number, path in enumerate(files, 1):
            print(f"F {number:02d} {path.relative_to(root)}")
        group = None
        for number, test_id in enumerate(sorted(ids), 1):
            parent, method = test_id.rsplit(".", 1)
            if parent != group:
                print("G " + parent)
                group = parent
            print(f"I {number:03d} {method}")
        print("IDENTIFIED_FILES " + json.dumps(source_files))
        print(f"INVENTORY_END files={len(files)} ids={len(ids)} "
              f"shown_files={len(files)} shown_ids={len(ids)} "
              "excluded=non-Python-files; unshown=none")


if __name__ == "__main__":
    unittest.main()
