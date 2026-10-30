"""Event A: build blank count sheets for the held-out app.

Reuses build() from build_sheets.py unchanged (same layout, same drop-downs,
same README) and only swaps the app list and the output folder, so the M2
sheets in count_sheets/ are never overwritten.

Usage (from the G15 repo root):
    python scripts/build_sheets_eventA.py <path-to-EMSE2025SAR-Replication>

Creates eventA/rater1_counts.xlsx and eventA/rater2_counts.xlsx.
"""
import sys
from pathlib import Path

import build_sheets

HELD_OUT = ["spring-netflix-oss-microservices"]  # paper Table 1 #6, see eventA/prediction.md

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    repo = sys.argv[1]
    build_sheets.APPS = HELD_OUT  # build() reads the module-level APPS
    out_dir = Path("eventA")
    out_dir.mkdir(exist_ok=True)
    for n in (1, 2):
        sizes = build_sheets.build(repo, f"rater{n}", out_dir / f"rater{n}_counts.xlsx")
    print("Built eventA/rater1_counts.xlsx and eventA/rater2_counts.xlsx")
    for app, (g, t) in sizes.items():
        print(f"  {app:34s} ground-truth items: {g:3d}   tool items: {t:3d}")
