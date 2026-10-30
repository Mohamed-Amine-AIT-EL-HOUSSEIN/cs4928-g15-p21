# Event A agreement and reconciliation

Application: `spring-netflix-oss-microservices`.

|Table|Items|Agreement|Observed Po|Chance Pe|Cohen kappa|
|---|---:|---:|---:|---:|---:|
|A: reference items (TP/FN)|52|100.0%|1.000000|0.526627|1.000000|
|B: tool items (MATCH/FP)|34|100.0%|1.000000|0.889273|1.000000|

Label or effective matching-ID conflicts: **0**.

N/A/NA matching-ID placeholders normalised to empty in memory: A=22, B=0. Original workbooks are never edited.

Kappa quantifies agreement between the supplied labels; it does not by itself establish independence or validate the reference architecture.

## Input versions

- A: `eventA\rater1_counts.xlsx`
  SHA256 `ef5fbbaf71e8e449e985a8c77be9d2b33a209fc967b7e930119d2a78f6d9983c`
- B: `eventA\rater2_counts.xlsx`
  SHA256 `92791eac1b32c8da02fdc6f3cf6f721d5bf6987a9d377c51c22fe2731e1bab36`

## Final-label rule

Both submitted labels and matching IDs agree for every item. No disputed decisions or tie-breaker actions were required. The consolidated labels are in [final_labels.csv](final_labels.csv); they do not replace the original A/B sheets.

Final labels preserve the decisions shared by the two submitted sheets. No independent adjudication was needed because no conflicting labels or matching IDs were found.

## Metric calculation

TP = reference-table TP count; FN = reference-table FN count; FP = tool-table FP count. MATCH is not counted as a second TP.

Precision = TP/(TP+FP); recall = TP/(TP+FN); F1 = 2TP/(2TP+FP+FN). Undefined denominators are empty in metrics.csv, not zero.

Re-run from repository root: `python scripts/analyse_eventA.py` (Python 3.10+ and openpyxl).
