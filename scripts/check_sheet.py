"""Check a filled count sheet for mistakes BEFORE committing it.

Usage (from the G15 repo root):
    python scripts/check_sheet.py count_sheets/rater1_counts.xlsx

It only reports problems (by row ID). It never prints your labels or any
totals, so running it does not reveal or change any judgement.
"""
import sys
from collections import Counter

from openpyxl import load_workbook

from common import APPS

VALID = {"G": {"TP", "FN"}, "T": {"MATCH", "FP"}}


def check(path):
    wb = load_workbook(path)  # formulas are read as text, so they are detected
    problems = 0
    for app in APPS:
        ws = wb[app[:31]]
        rows = {}
        for row in ws.iter_rows():
            rid = row[0].value
            if isinstance(rid, str) and rid[:1] in "GT" and rid[1:].isdigit():
                rows[rid] = {"char": row[1].value, "label": row[3].value,
                             "link": row[4].value, "extra": [c.value for c in row[6:12]]}
        issues = []
        for rid, r in rows.items():
            lab, link = r["label"], r["link"]
            if isinstance(lab, str) and lab.startswith("="):
                issues.append(f"{rid}: Label is a formula - type the value instead")
                continue
            if isinstance(link, str) and link.startswith("="):
                issues.append(f"{rid}: matching-ID cell is a formula - type the value instead")
            lab = (lab or "").strip().upper()
            link = (str(link).strip().upper() if link else "")
            if not lab:
                issues.append(f"{rid}: Label is empty")
                continue
            if lab not in VALID[rid[0]]:
                issues.append(f"{rid}: '{lab}' is not allowed here (use {' or '.join(sorted(VALID[rid[0]]))})")
                continue
            needs_link = lab in ("TP", "MATCH")
            if needs_link and not link:
                issues.append(f"{rid}: {lab} but no matching ID in column E")
            if not needs_link and link:
                issues.append(f"{rid}: {lab} but column E has an ID ({link}) - remove it or change the label")
            if needs_link and link:
                other = rows.get(link)
                if other is None:
                    issues.append(f"{rid}: points to {link}, which does not exist on this tab")
                elif other["char"] != r["char"]:
                    issues.append(f"{rid}: points to {link}, which is a different characteristic")
                else:
                    back = str(other["link"] or "").strip().upper()
                    if back != rid:
                        issues.append(f"{rid}: points to {link}, but {link} points to '{back or 'nothing'}' (pairs must point at each other)")
            if any(v not in (None, "") for v in r["extra"]):
                issues.append(f"{rid}: something is written in column G or later - delete helper columns")
        # one-to-one: no ID used twice
        used = Counter(str(r["link"]).strip().upper() for r in rows.values()
                       if r["link"] and (r["label"] or "").strip().upper() in ("TP", "MATCH"))
        for target, n in used.items():
            if n > 1:
                issues.append(f"{target} is used as a match {n} times (rule §4: one-to-one)")
        status = "OK" if not issues else f"{len(issues)} problem(s)"
        print(f"\n[{app}] {status}")
        for i in issues:
            print("   - " + i)
        problems += len(issues)
    print("\nRESULT:", "no problems found - sheet is ready" if problems == 0
          else f"{problems} problem(s) to fix, then run this again")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    check(sys.argv[1])
