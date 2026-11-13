"""Compare two Code2DFD results: components, connections (directed) and external components.

Each input is either Code2DFD's dict output (output/results/dict_*.txt, a Python literal)
or a JSON file with the same three keys (the replication package's *-code2DFD-raw.json).

usage: python compare_runs.py OLD NEW [--json out.json]
"""
import ast
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if path.endswith(".json"):
        return json.loads(text)
    # literal_eval only reads literals (dicts, sets, tuples...), it never runs code
    return ast.literal_eval(text)


def summarise(result):
    services = {s.get("servicename") or s.get("name") for s in result["microservices"].values()}
    flows = {(f["sender"], f["receiver"]) for f in result["information_flows"].values()}
    external = {e.get("name") for e in result["external_components"].values()}
    return {"components": services, "connections": flows, "external_components": external}


def diff(old, new):
    out = {}
    for key in old:
        out[key] = {
            "old_count": len(old[key]),
            "new_count": len(new[key]),
            "added": sorted(new[key] - old[key]),
            "removed": sorted(old[key] - new[key]),
        }
    # a connection whose reverse exists on the other side = same pair, direction flipped
    flipped = sorted(f for f in out["connections"]["added"] if (f[1], f[0]) in old["connections"])
    out["connections"]["direction_flipped"] = flipped
    return out


def main():
    args = sys.argv[1:]
    json_out = None
    if "--json" in args:
        i = args.index("--json")
        json_out = args[i + 1]
        del args[i:i + 2]
    old, new = (summarise(load(p)) for p in args)
    result = diff(old, new)
    for key, d in result.items():
        print(f"{key}: {d['old_count']} -> {d['new_count']}")
        for item in d["added"]:
            print(f"  + {' -> '.join(item) if isinstance(item, tuple) else item}")
        for item in d["removed"]:
            print(f"  - {' -> '.join(item) if isinstance(item, tuple) else item}")
        for item in d.get("direction_flipped", []):
            print(f"  ~ reversed: {' -> '.join(item)}")
    same = all(not d["added"] and not d["removed"] for d in result.values())
    print("IDENTICAL" if same else "DIFFERENT")
    if json_out:
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=list)


if __name__ == "__main__":
    main()
