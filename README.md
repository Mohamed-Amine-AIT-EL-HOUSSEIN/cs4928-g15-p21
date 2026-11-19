# G15 / P21 — Static Architecture Recovery for Microservices (Code2DFD)

CS4928 Theory and Practice of Software Design, group G15, project pack P21.

Study: Schneider et al., *Comparison of static analysis architecture recovery tools for microservice applications*, Empirical Software Engineering 30:128 (2025).
Replication package: <https://github.com/M3SOulu/EMSE2025SAR-Replication> at commit `1b8994471e9df0d32e22b31415eead8511078125` (used throughout).

## Results at a glance

| Stage | Question | Result | Evidence |
|---|---|---|---|
| M2 (RQ1) | Do two independent raters reproduce Code2DFD's P/R/F1 on 4 apps? | **REPRODUCED.** Pooled P 0.939, R 0.785, F1 0.855, identical to the paper's per-item counts in every cell; kappa 1.00 (393/393 items) | [`docs/M2_record.md`](docs/M2_record.md), [`results/m2_summary.md`](results/m2_summary.md) |
| Event A (RQ2, transfer) | Does the result transfer to a held-out app (App 6, spring-netflix-oss-microservices)? | **Partial transfer.** F1 0.744 (outside the preregistered 0.755–0.955); components 1.000, connections 0.894, endpoints 0/17 reported; kappa 1.00 | [`eventA/comparison.md`](eventA/comparison.md) |
| M4 (RQ2, design) | Smallest justified change to our evaluation pipeline | Separate audit script (`scripts/m4_audit.py`) for endpoint coverage and connection direction; Adapter layer rejected | [`m4/M4_design_record.md`](m4/M4_design_record.md) |
| Event B | Can the M4 design see a new architectural link? | Code2DFD found the new link; frozen M4 could not show it. Option B (`--before/--after` mode, 74 lines, 3 new tests) makes it visible in 1 command instead of 7 manual steps. Week 9 decision **partly supported** | [`eventB/response.md`](eventB/response.md) |

## Research questions (frozen at M1, see [`docs/M1_plan.md`](docs/M1_plan.md))

- **RQ1.** When two of us independently count TP/FP/FN on Code2DFD's published outputs for four benchmark apps, how well do our counts agree, and how close do the resulting precision/recall/F1 get to what the paper reports?
- **RQ2.** How accurately does Code2DFD recover the architecture of a new microservice app outside the original dataset, and what's the cheapest design for adding new apps or tool formats: manual counting, one script per tool, or an Adapter per tool feeding a shared matcher?

## Repository map

```
docs/
  M1_plan.md            RQs, sample, method, expectations (tag M1_PLAN) + known deviation
  counting_rule.md      labelling rule, approved by all 5 members 19/10/2026
  M2_record.md          M2 audit record: inputs, raters, deviations D-01..D-04, threats, AI use
  evidence/             git logs showing rater independence
count_sheets/           M2 rater sheets (rater1, rater2) and agreed labels
results/                M2 outputs: agreement, conflicts, P/R/F1 vs paper, decision
eventA/                 Event A: prediction, rater sheets, comparison, results/
m4/                     M4 design record and audit output
eventB/                 Event B: predictions, Code2DFD before/after runs, option A walk-through,
                        decision, response, setup notes, Dockerfile
scripts/                build_sheets, check_sheet, score (M2); build_sheets_eventA,
                        analyse_eventA (Event A); m4_audit (M4 + Event B option B)
tests/                  unit tests for m4_audit.py
```

## Milestone tags

| Tag | Commit | Date | Meaning |
|---|---|---|---|
| `M1_PLAN` | `97053f2` | 19/10/2026 | Preregistration frozen before counting |
| `M2_REPRO` | `c1a9b2b` | 20/10/2026 | Bounded reproduction complete |
| `PRE_EVENT_A` | `c1a9b2b` | 20/10/2026 | Frozen state before Change Event A |
| `PRE_EVENT_B` | `09a3143` | 11/11/2026 | Frozen M4 state before Change Event B |
| `FINAL` | `ba83f5c` | 19/11/2026 | Final submission |

Predictions were committed before the work they predict: Event A `c126ca8` (before any App 6 counting), Event B `e7b8371` (before any Code2DFD run).

## How to reproduce

### Requirements

- Python 3.10 or later (tested on 3.13 and 3.14), `openpyxl` (`pip install openpyxl`)
- A clone of the replication package at the pinned commit:

```bash
git clone https://github.com/M3SOulu/EMSE2025SAR-Replication.git
cd EMSE2025SAR-Replication && git checkout 1b8994471e9df0d32e22b31415eead8511078125 && cd ..
```

On Windows, run `git config --global core.longpaths true` first, otherwise some files are not checked out (see `docs/M2_record.md` §2).

All commands below run from the root of this repository. `<REPL>` is the path to the replication clone.

### M2: bounded reproduction (RQ1)

```bash
python scripts/check_sheet.py count_sheets/rater1_counts.xlsx   # structural check of a rater sheet
python scripts/score.py agreement                                # kappa + conflicts -> results/agreement.md
python scripts/score.py score <REPL>                             # P/R/F1 vs paper -> results/m2_results.csv, m2_summary.md
```

Expected: `Status: REPRODUCED`, pooled F1 0.855, kappa 1.00. `score.py score` is the only step that reads the paper's own labels (`processed_results/`), and it runs after both rater sheets are committed. To regenerate blank sheets: `python scripts/build_sheets.py <REPL>` (overwrites `count_sheets/`).

### Event A: held-out app

```bash
python scripts/analyse_eventA.py
```

Reads `eventA/rater1_counts.xlsx` and `eventA/rater2_counts.xlsx` and regenerates `eventA/results/` (agreement, final labels, metrics). Expected: overall F1 0.744, kappa 1.00 for both tables. Blank sheets: `python scripts/build_sheets_eventA.py <REPL>` (writes to `eventA/`, does not touch M2 sheets).

### M4: evaluation audit

```bash
python -m unittest discover -s tests -v
python scripts/m4_audit.py                  # -> m4/results/audit.json
```

Expected: all tests pass; 17 reference endpoints, 0 reported; 42 matched connection rows checked; Event A F1 unchanged at 0.744.

### Event B: change visibility

Compare the two Code2DFD runs and run the option B audit on them:

```bash
python eventB/scripts/compare_runs.py eventB/runs/before/dict_fernandoabcampos_spring-netflix-oss-microservices.txt eventB/runs/after/dict_fernandoabcampos_spring-netflix-oss-microservices.txt
python scripts/m4_audit.py --before eventB/runs/before/dict_fernandoabcampos_spring-netflix-oss-microservices.txt --after eventB/runs/after/dict_fernandoabcampos_spring-netflix-oss-microservices.txt --out eventB/runs/m4_audit_optionB.json
```

Expected: connections 23 → 24, the only change is `+ statement-service -> card-service`.

Re-running Code2DFD itself (the study's fork at `39763f4`, inside the Linux container in `eventB/tools/Dockerfile.code2dfd`) is described step by step in [`eventB/setup_notes.md`](eventB/setup_notes.md) and [`eventB/evidence.md`](eventB/evidence.md). The "before" run reproduces the study's own Code2DFD output for App 6 exactly.

### Notes on re-running

- Regenerated files can differ from the committed ones only in path separators (`\` vs `/`) and line endings, because the original runs were on Windows. All numbers are identical.
- Frozen results (`results/`, `eventA/results/`, `m4/results/audit.json`) are evidence; if you re-run to check, discard the regenerated copies (`git checkout -- .`) rather than committing them.

## Deviations, threats and AI use

- **Sample selection (D-01):** the 4 M2 apps (paper Table 1 #3, #5, #15, #16) were not chosen by the pack's "first 3 in stable order" rule; the choice came from an AI suggestion partly informed by the paper's per-app results. Raters did not see those results. See `docs/M1_plan.md` and `docs/M2_record.md` §7–8.
- **RQ2 scope:** the planned run on a new app outside the dataset (ewolff/microservice-consul) was not carried out. Transfer was tested on a held-out dataset app (Event A) and on a changed snapshot of it (Event B).
- **Known limitations:** `eventB/known_limitations.md` (M4 direction check only covers matched rows).
- **AI use** is recorded where it influenced a decision: `docs/M2_record.md` §9, `m4/M4_design_record.md` §6, `eventB/evidence.md` and `eventB/response.md` ("AI use"). All labels were made by group members; AI-drafted scripts compute statistics from those labels and were checked by tests and hand calculation.

The original M2 kit instructions are kept in [`docs/M2_kit_guide.md`](docs/M2_kit_guide.md).
