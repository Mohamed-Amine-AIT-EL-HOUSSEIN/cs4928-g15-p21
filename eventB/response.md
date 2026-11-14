# Event B – response and conclusion (M5–M6)

G15 / P21. Part 1: Zexu Wang. Part 2: Mohamed Amine AIT EL HOUSSEIN.

## What changed (pre-Event-B `PRE_EVENT_B` → post-response)

| Evidence                  | Before (frozen M4)                     | After (option B)                                                       |
| ------------------------- | -------------------------------------- | ---------------------------------------------------------------------- |
| Files changed             | –                                      | 2: `scripts/m4_audit.py`, `tests/test_m4_audit.py`                     |
| Lines added               | –                                      | 33 in the audit, 41 in tests (74 total)                                |
| Automated tests           | 3 (pass)                               | 6 (pass)                                                               |
| Steps to see the new link | 7 manual steps (9 under the full rule) | **1 command**                                                          |
| Is the new link named?    | No                                     | Yes: `statement_service -> card_service`, `in_reference_labels: false` |
| Frozen results changed    | –                                      | None (M2 F1 0.855, Event A F1 0.744 unchanged)                         |
| Default audit output      | `m4/results/audit.json`                | Identical when `--before/--after` are not given                        |

Command (output in [runs/m4_audit_optionB.json](runs/m4_audit_optionB.json)):

```
python scripts/m4_audit.py --before eventB/runs/before/dict_fernandoabcampos_spring-netflix-oss-microservices.txt --after eventB/runs/after/dict_fernandoabcampos_spring-netflix-oss-microservices.txt --out eventB/runs/m4_audit_optionB.json
```

## Predictions vs outcomes ([predictions.md](predictions.md))

| Prediction                                                                                        | Outcome                                                                         |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| P1: Code2DFD detects the new link, right direction, nothing else changes                          | **Confirmed** (Part 1)                                                          |
| P2: frozen M4 does not show it without re-labelling                                               | **Confirmed** (Part 1)                                                          |
| P3: the pressure hits M4's inputs, not its checks                                                 | **Confirmed**: the fix adds a new input path; the existing checks are unchanged |
| P4: option A > 3 manual steps; option B costs 1–2 files, < ~80 lines, 2–3 tests, 0 frozen changes | **Confirmed**: 7 steps; 2 files, 74 lines, 3 new tests, 0 frozen changes        |
| P5: Week 9 decision partly supported                                                              | **Confirmed** (below)                                                           |

## Conclusion: Week 9 decision **partly supported**

- **Supported:** a small, separate audit script was the right shape. It absorbed the new pressure with an optional mode and 33 lines, with no Adapter layer and no change to Code2DFD.
- **Not supported:** reading _only_ human labels made architectural change invisible. M4 needed a second input (the tool's own output) to answer Event B.

## Trade-off / anti-pattern risk

- **Avoided:** speculative generality. An Adapter layer (option C) was rejected again, because there is still one tool.
- **Introduced:** duplicated knowledge. Name normalisation (case, `-`, `_`, space) now lives in two functions in `m4_audit.py`. If the counting rule's §2 changes, both must change (shotgun-surgery risk). Kept because merging them would touch the frozen M4 check.
- **Remaining:** new links are named automatically but still need a human label before they count in metrics (accepted, see [decision.md](decision.md)).

## AI use

Claude drafted the option B code, tests and this write-up. Checked, not taken on trust: all 6 tests run; the default audit output was compared with the frozen `m4/results/audit.json` and is identical; the change report on the real runs names exactly the one link Part 1 found.
