# Event B – Part 1 evidence (Z1–Z6)

G15 / P21. Part 1 done by Zexu (Nujs-0927) on 2026-11-13, with AI assistance (see "AI use" at the end).

**Order check:** the Event B prediction was committed first (`e7b8371`, 2026-11-12 10:06 UTC, [predictions.md](predictions.md)). Every Code2DFD run below is from 2026-11-13 and comes after it.

## Setup (Z1)

Code2DFD is the study's own fork, [M3SOulu/EMSE2025SAR-code2DFD](https://github.com/M3SOulu/EMSE2025SAR-code2DFD) at `39763f4798b4d779d97656ec7135c98da440a7d7`, the commit pinned in the study's Tools repo. Dependencies were installed unpinned plus `ruamel.yaml` (and `six`, which `plantuml` needs but does not declare). Full details are in [setup_notes.md](setup_notes.md).

Two problems came up, and both were fixed without changing Code2DFD's code:

| Problem | Effect | Fix | Evidence |
|---|---|---|---|
| Code2DFD calls the Unix `find`/`grep`; on Windows `find` is a different program | Crash before any output (`UnicodeDecodeError`) | Run the tool in a Linux container, same Python 3.12 and package versions ([tools/Dockerfile.code2dfd](tools/Dockerfile.code2dfd)) | [runs/discarded/windows_native_FAILED.log](runs/discarded/windows_native_FAILED.log) |
| App 6's config-server reads its config from another repo (`fernandoabcampos/microservices-config`), which Code2DFD clones with `git`; the first image had no `git` | Run finished but **missed 3 connections** (`edge-server -> card-service`, `-> card-statement-composite`, `-> statement-service`) | Config repo cloned beforehand at its last commit `bb5da24` (2016-06-18); the run was discarded | [runs/discarded/no_config_repo/check_vs_study_raw.txt](runs/discarded/no_config_repo/check_vs_study_raw.txt) |

## Runs (Z2, Z3)

App 6 (`spring-netflix-oss-microservices`) was exported byte-exact from the replication package at `1b89944`, the same commit as Event A. Its git tree hash `684425c` is identical to the replication repo's. It was put in its own repo with `git init`.

| Run | App commit | Change | Output |
|---|---|---|---|
| before | `09baaa594d9881be85eb28409ab64514b91d44e1` | none | [runs/before/](runs/before/) |
| after | `c6a56a206070de7f5fc30e835c995fb88b42ed93` | one new file `statement-service/.../service/CardLookup.java` (15 lines) | [runs/after/](runs/after/), diff in [runs/after/app.diff](runs/after/app.diff) |

**The before run reproduces the study's own Code2DFD output for App 6 exactly**: 9 components, 23 connections, 2 external components, the same sets ([runs/before/check_vs_study_raw.txt](runs/before/check_vs_study_raw.txt), compared with `tool_comparison/results/recovery_correctness/raw_results/Code2DFD/spring-netflix-oss-microservices-code2DFD-raw.json` @ `1b89944`). So our setup is faithful, and the before/after difference comes from the change only.

`CardLookup.java` follows prediction P1: statement-service calls card-service with `RestTemplate.getForObject("http://card-service/api/card/" + cardId, String.class)`. Only the file name was given in the task list, so the code was written from P1.

The PlantUML server could not be reached in either run, so no PNG was drawn. The `.puml` files are the diagram source Code2DFD produced; the data outputs are complete.

## Tool

Compared with [scripts/compare_runs.py](scripts/compare_runs.py), which matches components and directed connections by name, not by ID ([runs/before_vs_after.txt](runs/before_vs_after.txt), [runs/before_vs_after.json](runs/before_vs_after.json)):

| | before | after | change |
|---|---|---|---|
| components | 9 | 9 | none |
| connections | 23 | 24 | **+ `statement-service -> card-service`** |
| external components | 2 | 2 | none |

- **The new link is there, in the right direction** (sender `statement-service`, receiver `card-service`), stereotype `restful_http`. Code2DFD's traceability points it at `CardLookup.java#L13`, the `getForObject` line ([runs/after/…_traceability.json](runs/after/fernandoabcampos_spring-netflix-oss-microservices_traceability.json)).
- **Nothing else was added or removed.** No connection changed direction.
- **P1 outcome: confirmed.**
- Side finding: adding one link **renumbered 14 of the 23 existing connections** in Code2DFD's output (for example `statement-service -> discovery-service` moved from `#19` to `#12`). Any label that points at a connection by its JSON index goes stale after a change. Our numbering also differs from the study's raw JSON, which the Event A labels point into.

## M4 audit

The frozen M4 audit was run as it is: `scripts/m4_audit.py` is unchanged since `PRE_EVENT_B` (`git diff PRE_EVENT_B HEAD -- scripts m4 tests` is empty), with its default inputs. Only `--out` was given, so the frozen `m4/results/audit.json` was not overwritten:

```
python scripts/m4_audit.py --out eventB/runs/m4_audit_after_change.json
```

- Output: [runs/m4_audit_after_change.json](runs/m4_audit_after_change.json). It is **identical** to the frozen `m4/results/audit.json`.
- **It does not show the new link.** M4 reads only `eventA/results/final_labels.csv` and `metrics.csv` (hand-made Event A labels). It never reads Code2DFD's output, so a change to the app cannot reach it.
- **P2 outcome: confirmed.**
- **P3 outcome: confirmed.** The pressure lands on M4's inputs (what it reads), not its checking logic.

## Manual steps (option A: no structural change)

To find out what option A really costs, it was walked through once on **copies** of the Event A inputs, in [optionA/](optionA/). The frozen `eventA/results/` files were not touched. Counting starts, like P4, from the point where both Code2DFD outputs exist.

1. **Find the new flow.** Compare the two outputs by sender and receiver. IDs cannot be used, because 14 of 23 existing flows were renumbered. Result: `statement-service -> card-service`, after-run `#8`.
2. **Add the expected connection to the reference by hand.** It is not in the replication ground truth. Added row `G053` with evidence `CardLookup.java:L13` at app commit `c6a56a2`.
3. **Add the tool-side row.** Added `T035`, `MATCH` with `G053`, pointing into the after run.
4. **Reconcile evidence pointers.** The 23 existing T rows point into the study's raw JSON; the new row points into our after run, which is numbered differently. Either re-point all 23 rows or accept mixed sources. The walk-through accepted mixed sources and noted it in the row.
5. **Recompute `metrics.csv`.** Connection TP goes 21 → 22; overall TP 32 → 33; precision, recall and F1 recomputed.
6. **Save the edited inputs as copies and re-run M4 on them.** The Event A results are frozen.
   ```
   python scripts/m4_audit.py --labels eventB/optionA/final_labels.csv --metrics eventB/optionA/metrics.csv --out eventB/optionA/m4_audit.json
   ```
7. **Interpret the audit.** Only `checked_matched_rows` (42 → 44) and the F1 value (0.744 → 0.75) change ([optionA/m4_audit.json](optionA/m4_audit.json)). **The new link is never named.** To see which link was added, you go back to the CSV.

**Count: 7 manual steps.** It is 9 if steps 2–3 follow the frozen counting rule (two independent raters, then an agreement check). P4 predicted "more than 3"; **outcome: confirmed**. Under the decision rule fixed in [predictions.md](predictions.md) (more than 3 steps → implement option B; Week 9 verdict "Partly supported"), option B applies. That is Part 2.

Also observed: after the walk-through, the audit's field `frozen_overall_F1` reports 0.75. The field only echoes whatever `metrics.csv` it is given, so the name "frozen" can mislead.

## AI use

An AI assistant (Claude) was used for Part 1. It:
- diagnosed the Windows `find`/`grep` failure
- wrote `tools/Dockerfile.code2dfd` and `scripts/compare_runs.py`
- wrote `CardLookup.java` from P1
- did the option A walk-through edits

Checks done, not taken on trust:
- The before run was compared with the study's own output and matched exactly.
- The new link was confirmed in Code2DFD's own traceability file (`CardLookup.java#L13`).
- The M4 code was confirmed unchanged against `PRE_EVENT_B`.
- The frozen files were confirmed unchanged with `git status`.

Where it was wrong: the first container image it built had no `git`. Code2DFD then silently skipped the config repo and lost 3 connections. This was caught from the run log (`git: not found`) and the comparison with the study's output, and the run was discarded.
