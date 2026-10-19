"""Shared helpers for the G15 M2 reproduction (CS4928, project P21).

Reads ONLY:
  - the ground truth:      tool_comparison/groundtruth_textual/<app>.txt
  - Code2DFD raw output:   tool_comparison/results/recovery_correctness/raw_results/Code2DFD/<app>-code2DFD-raw.json
The paper's own labels (processed_results/) are read only by paper_counts(),
which score.py calls in the comparison step, after both raters have finished.
"""
import json
import re
from pathlib import Path

APPS = [  # frozen M1 sample (workbook row G15, column F)
    "microservice-kafka",
    "spring-petclinic-microservices",
    "piggymetrics",
    "blog-microservices",
]
CHARS = ["component", "connection", "endpoint"]

RAW_DIR = Path("tool_comparison/results/recovery_correctness/raw_results/Code2DFD")
GT_DIR = Path("tool_comparison/groundtruth_textual")
PROCESSED_DIR = Path("tool_comparison/results/recovery_correctness/processed_results/code2DFD")

QUOTED = re.compile(r'"([^"]*)"')


def _split_endpoint_line(line):
    """'svc: "/a", "/b"' -> [('svc', '/a'), ('svc', '/b')]"""
    svc, _, rest = line.partition(":")
    return [(svc.strip(), ep) for ep in QUOTED.findall(rest)]


def ground_truth(repo, app):
    """Return list of (characteristic, item_text) from the ground-truth file."""
    text = (Path(repo) / GT_DIR / f"{app}.txt").read_text(encoding="utf-8")
    items, section = [], None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        if low.startswith("components:"):
            section = "component"; continue
        if low.startswith("connections:"):
            section = "connection"; continue
        if low.startswith("endpoints:"):
            section = "endpoint"; continue
        if section == "endpoint":
            items += [("endpoint", f"{s}: {e}") for s, e in _split_endpoint_line(line)]
        elif section:
            items.append((section, " ".join(line.split())))
    return items


def tool_output(repo, app):
    """Return list of (characteristic, item_text) exactly as Code2DFD reported them.

    No matching or renaming is done here: deciding whether a tool item matches
    a ground-truth item is the raters' job (see docs/counting_rule.md).
    """
    path = Path(repo) / RAW_DIR / f"{app}-code2DFD-raw.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    items, seen = [], set()

    def add(ch, txt):
        if (ch, txt) not in seen:
            seen.add((ch, txt)); items.append((ch, txt))

    for svc in data.get("microservices", {}).values():
        add("component", svc["servicename"])
    for ext in data.get("external_components", {}).values():
        add("component", ext["name"])
    for flow in data.get("information_flows", {}).values():
        add("connection", f'{flow["sender"]} -> {flow["receiver"]}')
    for svc in data.get("microservices", {}).values():
        for key, val in svc.get("tagged_values", []):
            if key == "Endpoints":
                # stored as a stringified Python list, e.g. "['/a', '/b']"
                for ep in re.findall(r"'([^']*)'", str(val)):
                    add("endpoint", f'{svc["servicename"]}: {ep.strip(chr(34))}')
    return items


def paper_counts(repo, app):
    """TP/FP/FN per characteristic as published by the authors (processed_results).

    Only used AFTER both raters have finished (comparison step).
    """
    path = Path(repo) / PROCESSED_DIR / f"{app}-code2DFD-processed.txt"
    text = path.read_text(encoding="utf-8")
    counts = {c: {"TP": 0, "FP": 0, "FN": 0} for c in CHARS}
    section = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        head = line.rstrip(":").lower()
        if head in ("components", "connections", "endpoints", "fp"):
            section = {"components": "component", "connections": "connection",
                       "endpoints": "endpoint", "fp": "fp"}[head]
            continue
        if section in ("component", "connection"):
            lab = line.split()[0]
            if lab in ("TP", "FN", "FP"):
                counts[section][lab] += 1
        elif section == "endpoint":
            m = re.match(r"(TP|FN|FP)\((\d+)\)", line)
            if m:
                counts["endpoint"][m.group(1)] += int(m.group(2))
        elif section == "fp":
            ch = "connection" if "->" in line else "component"
            counts[ch]["FP"] += 1
    return counts


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else None
    return p, r, f
