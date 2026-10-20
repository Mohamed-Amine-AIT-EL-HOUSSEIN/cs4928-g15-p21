# M2 record — G15 / P21 bounded reproduction

Fill every `____` before tagging `M2_REPRO`. Delete nothing that was already committed; add new lines instead.

---

## 1. Input identity

| Item                | Value                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Study               | Schneider et al., _Comparison of static analysis architecture recovery tools for microservice applications_, EMSE 30:128 (2025) |
| Replication package | https://github.com/M3SOulu/EMSE2025SAR-Replication                                                                              |
| Commit used         | `1b8994471e9df0d32e22b31415eead8511078125`                                                                                      |
| Accessed            | 12/10/2026 (local clone at the commit above)                                                                                    |
| Tool                | Code2DFD (published raw outputs; the tool was not re-run for RQ1)                                                               |
| Apps (frozen M1)    | microservice-kafka, spring-petclinic-microservices, piggymetrics, blog-microservices                                            |
| Characteristics     | components, connections, endpoints                                                                                              |
| Ground-truth items  | 214 (kafka 31, petclinic 50, piggymetrics 64, blog 69)                                                                          |
| Tool-output items   | 179 (kafka 24, petclinic 45, piggymetrics 64, blog 46)                                                                          |
| Raters              | Rater 1: Mohamed Amine AIT EL HOUSSEIN · Rater 2: Zexu Wang                                                                     |
| Counting rule       | `docs/counting_rule.md`, approved by the group 19/10/2026 (commit `49a475d`)                                                    |

## 2. Environment

| Item     | Value                                                                                                                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OS       | Windows 10/11                                                                                                                                                                                     |
| Python   | 3.14.3                                                                                                                                                                                            |
| openpyxl | 3.1.5                                                                                                                                                                                             |
| Note     | Windows 260-character path limit caused a partial checkout of the replication repo. Fixed with `git config core.longpaths true` and a re-checkout of the same commit. No input file was modified. |

## 3. Execution route

```
python scripts/build_sheets.py <replication-repo>          # blank count sheets
# rater 1 and rater 2 fill their sheets independently, then commit
python scripts/check_sheet.py count_sheets/raterN_counts.xlsx   # structural check (blanks, formulas, broken pairs)
python scripts/score.py agreement                         # kappa + conflicts
# group resolves conflicts in count_sheets/agreed_counts.xlsx, then commits
python scripts/score.py score <replication-repo>          # P/R/F1 + comparison + decision
```

How each rater worked:

- **Rater 1 (M. A. Ait El Houssein):** an XLOOKUP helper column suggested exact-name matches (rule §2 normalisation: case, `-`, `_`, space). Each suggested ID was typed manually into column E and verified with Ctrl+F before accepting. All labels were entered manually; helper columns were deleted before commit.
- **Rater 2 (Zexu Wang):** counted manually, without a helper column.
- Both sheets passed `scripts/check_sheet.py` (no blanks, no formulas, all TP/MATCH pairs consistent) before agreement was computed.

## 4. Raw evidence (never edited after commit)

| File                                            | What it is                                                         | Commit                       |
| ----------------------------------------------- | ------------------------------------------------------------------ | ---------------------------- |
| `count_sheets/rater1_counts.xlsx`               | Rater 1 (Mohamed Amine AIT EL HOUSSEIN) labels                     | `1e81ead` (20/10/2026 13:17) |
| `count_sheets/rater2_counts.xlsx`               | Rater 2 (Zexu Wang) labels                                         | `b3af920` (20/10/2026 03:15) |
| `docs/evidence/*.txt`                           | Git logs showing Rater 1 committed before pulling Rater 2's sheet  | `73b1a2c`                    |
| `results/agreement.md`, `results/conflicts.csv` | Kappa + list of disagreements                                      | `e6647e2`                    |
| `count_sheets/agreed_counts.xlsx`               | Resolved labels (0 conflicts, so identical to both raters' labels) | `e6647e2`                    |
| `results/m2_results.csv`, `results/m2_summary.md` | P/R/F1 vs paper + decision | (commit with M2_REPRO) |

## 5. Derived results

- `results/m2_results.csv`: TP/FP/FN and P/R/F1 per app × characteristic, ours vs paper
- `results/m2_summary.md`: summary table + decision rule outcome

## 6. Comparison and status

**Inter-rater agreement:** 393/393 items identical (100%). Cohen's kappa = 1.00 for table A (214 items) and table B (179 items), on every app and pooled. Conflicts to resolve: 0.

**Paper baseline for these 4 apps** (recomputed by `score.py` from `processed_results/code2DFD/`):

|                               | P     | R     | F1    |
| ----------------------------- | ----- | ----- | ----- |
| Pooled, all 3 characteristics | 0.939 | 0.785 | 0.855 |

**Our result (pooled, all 3 characteristics):** P 0.939, R 0.785, F1 0.855, kappa 1.00

| App | Our F1 | Paper F1 | diff |
| --- | --- | --- | --- |
| microservice-kafka | 0.764 | 0.764 | 0.000 |
| spring-petclinic-microservices | 0.926 | 0.926 | 0.000 |
| piggymetrics | 0.906 | 0.906 | 0.000 |
| blog-microservices | 0.783 | 0.783 | 0.000 |

**Status:** REPRODUCED

**Why (frozen M1 rule, `results/m2_summary.md`):**

- PASS: pooled P/R/F1 within ±0.05 (differences 0.000 / 0.000 / 0.000)
- PASS: every app's F1 within ±0.10 (all differences 0.000)
- PASS: kappa ≥ 0.60 (kappa = 1.00)

**Observation:** our TP/FP/FN counts are identical to the paper's in every app × characteristic cell (pooled TP 168, FP 11, FN 46; see `results/m2_results.csv`). Our counting rule (§2 name normalisation, §4 self-connections, §5 endpoint formatting) therefore produced the same judgements as the authors' unpublished matching. The paper's labels were opened only by `score.py` in this final step, after both rater sheets and the agreement results were committed (`1e81ead`, `b3af920`, `e6647e2`).

## 7. Deviations from M1

| ID   | Date       | What changed                                                                                                                                                                                                                 | Why                                                                | Effect on interpretation                                                                                                                                                                                                                         |
| ---- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| D-01 | Week 5 (M1) | The 4 apps were not chosen with the project pack's default rule ("first 3 eligible items in stable order"). They were chosen in Week 5 by a group member who was neither a rater nor the tie-breaker, from an AI assistant's suggestion, to give a mix of sizes and easy/hard cases: piggymetrics (largest app; endpoint FPs), spring-petclinic-microservices (well-structured reference case), microservice-kafka (asynchronous Kafka messaging, a different connection type), blog-microservices (low connection recall, a hard case). | Aim was diversity of app size and connection type. The choice was partly informed by the paper's published per-app results. | **Selection was not blind to the paper's results**, which the pack's rule is meant to prevent. The sample is deliberately diverse rather than representative. Because the selector was not a rater, neither rater was given the paper's per-app results before counting. Reported as the main threat (§8).
| D-02 | 19/10/2026 | Clarified how kappa is computed (counting rule §7): separately for table A and table B; the M1 threshold applies to the lower value. Decided **before** counting.                                                            | M1 did not say how kappa would be computed over two kinds of item. | None on P/R/F1. Makes the kappa check stricter.                                                                                                                                                                                                  |
| D-03 | 19/10/2026 | The M1 expected values (P≈0.96, R≈0.81, F1≈0.88) were approximate. The decision rule compares against the baseline recomputed from `processed_results` (P 0.939, R 0.785, F1 0.855). The M1 expectation itself is unchanged. | M1 says the comparison is "vs paper's processed_results".          | The expectation and the baseline differ by up to 0.03; the rule uses the baseline.                                                                                                                                                               |
| D-04 | 20/10/2026 | Rater 2 committed their sheet (`b3af920`, 20/10/2026 03:15) before Rater 1 had finished; the group rule was to upload only after both raters had finished.                                                                   | Coordination slip.                                                 | Rater 1 did not open or pull that file before committing their own sheet (`1e81ead`, 20/10/2026 13:17); the local reflog and remote log saved in `docs/evidence/` show no pull in between. Independence is preserved; recorded for transparency. |

## 8. Key threat to validity

Agreement was perfect (393/393 items, kappa = 1.00). Rater 1 used an exact-name lookup helper with manual verification; Rater 2 counted fully by hand. 332 of 393 rows (84%) are exact-name matches after rule §2 normalisation, so most items were straightforward; on the 61 rows that required judgement (48 ground-truth + 13 tool-output rows), the raters also agreed. Because both our counts and the paper's come from human matching against the same ground truth, the exact match shows the counting is reproducible on these apps; it does not independently validate the ground truth itself. Remaining threats: **sample selection (D-01)**: the 4 apps were chosen with knowledge of the paper's per-app results, so the sample is diverse but not blind or representative, but the selector was neither rater nor tie-breaker, and both raters counted without the paper's results; Rater 2 confirmed he never opened `processed_results/` or `merged_results/`. The sample is also small (4 of 17 apps), and our matching rules (counting rule §2 and §5) may differ from the authors' unpublished rules, so a difference from the paper may reflect the rules rather than the tool.

## 9. AI-use note (only material influence)

- **Sample choice (Week 5):** the 4 apps were picked by a non-rater group member from an AI assistant's suggestion, partly informed by the paper's per-app results; the group accepted it (see D-01).
- The count-sheet builder, checker, scoring script, counting rule draft and this template were drafted with Claude (AI). The group reviewed and approved the counting rule and kit on 19/10/2026.
- While building and testing the scoring script, the AI read the paper's published labels (`processed_results/`). **The raters did not.** The scoring script was tested on simulated labels, and reproduced the paper's own numbers exactly when fed the paper's counts.
- **Done by the group, not by AI:** the research questions, the bounded sample and the decision rule (M1); review and approval of the counting rule; **all 393 labels on each rater sheet, decided by two group members independently**; verification of every suggested match (Rater 1, Ctrl+F); interpretation of the result. The AI-drafted scripts only build blank sheets, check sheet structure and compute kappa/P/R/F1 from the raters' labels; they make no labelling decisions.
- **Verification of AI-drafted code by the group:** the checker was run on both rater sheets before agreement was computed; one result was recalculated by hand from `count_sheets/agreed_counts.xlsx` (microservice-kafka: TP 21, FP 3, FN 10 → F1 = 2×21 / (2×21 + 3 + 10) = 0.764) and matched `score.py`. Checked by: Mohamed Amine AIT EL HOUSSEIN, 20/10/2026 (TP 21, FN 10, FP 3, F1 0.7636; matches `score.py`)

## 10. Evidence chain example (for the coordinator)

> Pooled F1 0.855 (`results/m2_summary.md`) → `results/m2_results.csv`, row POOLED/all → `count_sheets/agreed_counts.xlsx` (labels) → `count_sheets/rater1_counts.xlsx` + `rater2_counts.xlsx` → `raw_results/Code2DFD/<app>-code2DFD-raw.json` + `groundtruth_textual/<app>.txt` @ commit `1b89944`.

## 11. Workbook entries (row G15)

- **Column I, reproduction result:** REPRODUCED. Code2DFD on 4 apps (components, connections, endpoints): pooled P 0.939, R 0.785, F1 0.855, identical to the paper's per-app counts (all F1 differences 0.000). Inter-rater kappa 1.00 (393/393 items).
- **Column J, evidence link:** `https://github.com/Mohamed-Amine-AIT-EL-HOUSSEIN/cs4928-g15-p21` tag `M2_REPRO`
