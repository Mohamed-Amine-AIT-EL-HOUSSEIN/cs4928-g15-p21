# M2 record — G15 / P21 bounded reproduction

Fill every `____` before tagging `M2_REPRO`. Delete nothing that was already committed; add new lines instead.

---

## 1. Input identity

| Item | Value |
|---|---|
| Study | Schneider et al., *Comparison of static analysis architecture recovery tools for microservice applications*, EMSE 30:128 (2025) |
| Replication package | https://github.com/M3SOulu/EMSE2025SAR-Replication |
| Commit used | `1b8994471e9df0d32e22b31415eead8511078125` |
| Accessed | ____ |
| Tool | Code2DFD (published raw outputs; the tool was not re-run for RQ1) |
| Apps (frozen M1) | microservice-kafka, spring-petclinic-microservices, piggymetrics, blog-microservices |
| Characteristics | components, connections, endpoints |
| Ground-truth items | 214 (kafka 31, petclinic 50, piggymetrics 64, blog 69) |

## 2. Environment

| Item | Value |
|---|---|
| OS | Windows ____ |
| Python | ____ (`python --version`) |
| openpyxl | ____ (`pip show openpyxl`) |
| Note | Windows 260-character path limit caused a partial checkout of the replication repo. Fixed with `git config core.longpaths true` and a re-checkout of the same commit. No input file was modified. |

## 3. Execution route

```
python scripts/build_sheets.py <replication-repo>          # blank count sheets
# rater 1 and rater 2 fill their sheets independently, then commit
python scripts/score.py agreement                         # kappa + conflicts
# group resolves conflicts in count_sheets/agreed_counts.xlsx, then commits
python scripts/score.py score <replication-repo>          # P/R/F1 + comparison + decision
```

## 4. Raw evidence (never edited after commit)

| File | What it is | Commit |
|---|---|---|
| `count_sheets/rater1_counts.xlsx` | Rater 1 (____) labels | ____ |
| `count_sheets/rater2_counts.xlsx` | Rater 2 (____) labels | ____ |
| `results/agreement.md`, `results/conflicts.csv` | Kappa + list of disagreements | ____ |
| `count_sheets/agreed_counts.xlsx` | Resolved labels | ____ |

## 5. Derived results

- `results/m2_results.csv`: TP/FP/FN and P/R/F1 per app × characteristic, ours vs paper
- `results/m2_summary.md`: summary table + decision rule outcome

## 6. Comparison and status

**Paper baseline for these 4 apps** (recomputed by `score.py` from `processed_results/code2DFD/`):

| | P | R | F1 |
|---|---|---|---|
| Pooled, all 3 characteristics | 0.939 | 0.785 | 0.855 |

**Our result:** P ____  R ____  F1 ____  kappa ____
**Status:** ____ (REPRODUCED / NOT REPRODUCED / INCONCLUSIVE-BLOCKED)
**Why:** ____ (copy the PASS/FAIL lines from `results/m2_summary.md`)

## 7. Deviations from M1

| ID | Date | What changed | Why | Effect on interpretation |
|---|---|---|---|---|
| D-01 | ____ | The 4 apps were not chosen with the project pack's default rule ("first 3 eligible items in stable order"). They were chosen by: ____ | ____ | The sample may not represent the other 13 apps. Reported as a threat. |
| D-02 | ____ | Clarified how kappa is computed (counting rule §7): separately for table A and table B; the M1 threshold applies to the lower value. Decided **before** counting. | M1 did not say how kappa would be computed over two kinds of item. | None on P/R/F1. Makes the kappa check stricter. |
| D-03 | ____ | The M1 expected values (P≈0.96, R≈0.81, F1≈0.88) were approximate. The decision rule compares against the baseline recomputed from `processed_results` (P 0.939, R 0.785, F1 0.855). The M1 expectation itself is unchanged. | M1 says the comparison is "vs paper's processed_results". | The expectation and the baseline differ by up to 0.03; the rule uses the baseline. |

## 8. Key threat to validity

____ (1–2 lines). Candidates:
- **Small, non-random sample:** 4 of 17 apps (see D-01).
- **Counting rule:** our matching rules (counting rule §2 and §5) may differ from the authors' unpublished rules, so disagreement with the paper may reflect the rules rather than the tool.
- **Ground truth not audited:** we reuse the authors' ground truth as correct.

## 9. AI-use note (only material influence)

- The count-sheet builder, scoring script, counting rule draft and this template were drafted with Claude (AI). The group reviewed and approved them on ____.
- While building and testing the scoring script, the AI read the paper's published labels (`processed_results/`). **The raters did not.** The scoring script was tested on simulated labels, and reproduced the paper's own numbers exactly when fed the paper's counts.

## 10. Evidence chain example (for the coordinator)

> Pooled F1 ____ (`results/m2_summary.md`) → `results/m2_results.csv`, row POOLED/all → `count_sheets/agreed_counts.xlsx` (labels) → `count_sheets/rater1_counts.xlsx` + `rater2_counts.xlsx` → `raw_results/Code2DFD/<app>-code2DFD-raw.json` + `groundtruth_textual/<app>.txt` @ commit `1b89944`.

## 11. Workbook entries (row G15)

- **Column I, reproduction result:** ____
- **Column J, evidence link:** `<group repo URL>` tag `M2_REPRO`
