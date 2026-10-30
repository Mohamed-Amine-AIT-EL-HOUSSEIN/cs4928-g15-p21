# Event A transfer comparison and design implications

## Study and evidence

Held-out case: **App 6, spring-netflix-oss-microservices** (paper Table 1 #6), replication package commit `1b8994471e9df0d32e22b31415eead8511078125`.

The [preregistered prediction](https://github.com/Mohamed-Amine-AIT-EL-HOUSSEIN/cs4928-g15-p21/blob/c126ca8e10258b35252605aad634c93e97a61acd/eventA/prediction.md) is preserved. We audit published Code2DFD outputs against the supplied reference architecture, using the frozen [counting rule](../docs/counting_rule.md); this is not a fresh execution of Code2DFD. The input/item specification is embedded in [analyse_eventA.py](../scripts/analyse_eventA.py). Each consolidated label includes its source location.

## Agreement and consolidated labels

Both submitted sheets contain 52 reference items and 34 tool-output items. All 86 labels and effective matching IDs agree. Cohen's kappa is **1.000 for Table A** and **1.000 for Table B**, calculated separately. A's 22 `N/A` matching-ID placeholders are interpreted as empty references only in memory; the original workbooks are unchanged.

There are **zero label/matching-ID conflicts**. No tie-breaker decision or disputed-label resolution was necessary. [final_labels.csv](results/final_labels.csv) consolidates the coincident labels, with empty matching IDs for FN/FP and evidence explanations. It does not replace the original A/B workbooks.

Kappa describes agreement between the supplied labels; it does not by itself establish independence or validate the reference architecture. See [agreement.md](results/agreement.md).

## M2 versus Event A

M2 uses the four frozen applications; Event A uses one different application. The comparison is descriptive and scope-dependent, not a controlled estimate of a universal tool-performance change. M2 evidence: [frozen result CSV](https://github.com/Mohamed-Amine-AIT-EL-HOUSSEIN/cs4928-g15-p21/blob/c1a9b2b0d997fa189dfe11109caebf61310bb8f4/results/m2_results.csv). Event A: [metrics.csv](results/metrics.csv).

|Scope|M2 TP / FP / FN|Event A TP / FP / FN|M2 P / R / F1|Event A P / R / F1|
|---|---|---|---|---|
|Components|53 / 1 / 1|11 / 0 / 0|0.981 / 0.981 / 0.981|1.000 / 1.000 / 1.000|
|Connections|92 / 4 / 27|21 / 2 / 3|0.958 / 0.773 / 0.856|0.913 / 0.875 / 0.894|
|Endpoints|23 / 6 / 18|0 / 0 / 17|0.793 / 0.561 / 0.657|n/a / 0.000 / 0.000|
|All characteristics|168 / 11 / 46|32 / 2 / 20|0.939 / 0.785 / 0.855|0.941 / 0.615 / 0.744|

TP is counted from the reference table once; MATCH rows are not additional TPs. Undefined precision (no reported endpoints) is n/a, not zero. Overall Event A F1 is `2*32/(2*32+2+20) = 64/86 = 0.744186`.

Component recovery is complete under the frozen rule. Connection F1 increases descriptively by about 0.038, while connection precision falls from 0.958 to 0.913 and recall rises from 0.773 to 0.875. The lower overall F1 therefore must not be reported as a decline in every characteristic. The raw output contains no `Endpoints` entries; all 17 reference endpoints are unreported under the frozen evaluation. This documents absent output information, not absence of APIs in the application.

## Test of the preregistered prediction

|Registered expectation or challenge|Observed result|Interpretation|
|---|---|---|
|FN-dominated errors|20 FN and 2 FP overall; connections have 3 FN and 2 FP|Supported as a count-based observation; 17 of the FNs concern endpoints.|
|Component/connection precision approximately 1; any such FP challenges prediction|Component FP=0, connection FP=2; connection P=0.913|The explicit FP challenge is triggered.|
|Overall F1 within 0.855 ± 0.10|F1=0.744186, difference from registered 0.855 is -0.110814; lower bound=0.755|The F1-band challenge is triggered.|
|Expected kappa ≥0.8; challenge kappa <0.6|Both table kappas=1.000|Numerical expectation met for agreement between the supplied labels.|
|Missed connections mainly service-to-service and infrastructure links|Two missing directed service links and one missing composite-to-broker link|The observed edge types are consistent with this broad description; their causal mechanism has not been established from source code.|

The original prediction's background statement that all M2 component/connection errors were FNs is factually inaccurate: M2 already had one component FP and four connection FPs. This clarification is recorded separately without rewriting the preregistration. Event A's FPs challenge the new near-zero-FP prediction; they are not the first FPs in the M2 evidence.

**Decision: partial transfer, with the preregistered overall-F1 and FP expectations challenged.** The original M2 bounded-reproduction result is retained. A negative transfer result is an observed research outcome, not a reason to retune labels after execution.

## Traceable connection errors

Ground-truth lines refer to `tool_comparison/groundtruth_textual/spring-netflix-oss-microservices.txt` at the pinned replication commit. JSON pointers refer to the corresponding raw Code2DFD JSON; the fixed replication repository contains both files under the paths described above.

|IDs|Observed discrepancy|Locatable evidence and interpretation|
|---|---|---|
|G025, FN|`card_statement_composite -> card_service` not reported|Reference L28; no corresponding sender/receiver/direction in `/information_flows`.|
|G026, FN|`card_statement_composite -> statement_service` not reported|Reference L29; no matching directed flow.|
|G028, FN|`card_statement_composite -> rabbitmq` not reported|Reference L31; no matching directed flow. A broker-related missing edge is observed; why recovery omitted it is not proven here.|
|T020, FP|`monitor -> rabbitmq` has no reference edge|JSON `/information_flows/8`; reference Connections L15–38. Even assuming monitor aliases monitor_dashboard does not supply this reference edge.|
|T021, FP|`turbine -> rabbitmq` is an extra direction|JSON `/information_flows/9`; reference G017/L20 is `rabbitmq -> turbine`. Correct direction is separately recovered by T034 (`/information_flows/32`), so G017 remains TP.|
|G036–G052, FN|17 reference endpoints unreported|Reference L41–44; no service in raw JSON has an `Endpoints` tagged-value entry.|

These are evidence-backed discrepancies against the supplied reference, not proof that every reference decision is infallible. No author-processed labels were used in this analysis.

## Software-design and maintainability implications

### Concrete design pressure

An evaluation pipeline must distinguish directed-edge semantics and information coverage. A report that exposes only one overall F1 can obscure that connection F1 improved while endpoint output was absent. An undirected or swapped-endpoint representation can also obscure the T021 discrepancy.

### Alternatives and proportionate response

|Response|Benefit|Trade-off|
|---|---|---|
|Keep the frozen evaluator and add no new structure|Preserves comparability and avoids speculative refactoring|Requires readers to interpret raw outputs; coverage omissions can remain unclear.|
|Keep the frozen evaluator, add explicit per-characteristic coverage/status metadata, and verify directed edges|Makes absent output distinguishable from zero reported items; makes sender/receiver errors auditable|Adds metadata and verification responsibilities, but does not require changing scientific labels or the original score.|
|Introduce an Adapter layer for multiple output formats|Could isolate format variation if multiple tools/formats are actually supported|No comparative evidence here establishes that a multi-tool abstraction is currently needed; it adds implementation and maintenance cost.|

**Recommended implication:** retain the frozen first result and favour explicit coverage metadata plus small directed-edge verification at the input/evaluation boundary. Keep reading/parsing, matching judgements and metric calculation as separate responsibilities. Require a directed `(sender, receiver)` key, and ensure `(a,b)` differs from `(b,a)`. If this recommendation is implemented later, keep its output separate from this frozen Event A run.

Suggested future verification: a reverse-edge fixture must not match; a file without endpoint information must expose unavailable coverage rather than imply that the application has no endpoints; each reported number must trace to its G/T inputs. These are proposed checks, not claims that a refactoring experiment was performed here. The supplied analysis script verifies workbook completeness, pairing and scoring; it does not implement or evaluate a new architecture-recovery tool.

## Limitations and reproduction

- One held-out application cannot establish general performance across systems.
- Both evaluations use the supplied ground truth; matching it does not independently validate that ground truth.
- Missing endpoints in the published artifact cannot establish their absence in the running application.
- Error mechanisms beyond the observed reference/raw-output discrepancies require source/configuration evidence.
- Perfect label agreement does not establish that the reference is correct or that errors are absent.

From repository root, install `openpyxl` in the chosen Python environment and run:

```text
python scripts/analyse_eventA.py
```

The script reads the existing `eventA/rater1_counts.xlsx` and `eventA/rater2_counts.xlsx`, verifies the pinned item specification, and regenerates the agreement report (including any conflicts), consolidated labels and metrics in `eventA/results/`. It does not modify original workbooks, M2 files or prediction.md.
