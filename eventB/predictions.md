# Pre-registered Event B Predictions – Group G15, Project P21

These predictions are based on the existing Event A results, Code2DFD's documented extractors, and the frozen M4 implementation. They represent expectations before implementing the planned change, not confirmed experimental outcomes.

## P1. Will Code2DFD detect the new link? In the right direction?

**Prediction:** Code2DFD is likely to detect the new connection from `statement-service` to `card-service` in the correct direction, and no other connections will appear or disappear.

**Reasoning:** The new communication uses Spring `RestTemplate`, which is explicitly supported in Code2DFD's default configuration. The `getForObject()` call also contains the target service URL, providing a recognizable communication pattern for the RestTemplate extractor.

**Confidence:** Medium.

**What would prove it wrong:** The post-change JSON contains no connection from `statement-service` to `card-service`, or reports the connection in the reverse direction, or any other connection is added or removed compared with the pre-change run.

## P2. Will the M4 audit show the new link without manual re-labelling?

**Prediction:** No. The frozen M4 audit will not independently identify the new link without updated human labels.

**Reasoning:** M4 reads `final_labels.csv` and `metrics.csv`, not Code2DFD's raw JSON output. Its checks depend on manually prepared labels and metrics. Therefore, even if Code2DFD detects the new connection, M4 cannot automatically discover it.

**Confidence:** High.

**What would prove it wrong:** M4 reports the new connection using only its original inputs, without modifying the labels or metrics.

## P3. Which part of the M4 design does this pressure affect, and why?

**Prediction:** The pressure primarily affects the input and evidence boundary of M4, rather than its existing checking logic.

**Reasoning:**
- Endpoint coverage checks depend on the supplied metrics.
- Direction checks depend on matched connection pairs in the human-labelled CSV.
- Neither check independently reads the architecture recovered by Code2DFD.

Consequently, M4 can audit the quality of prepared results but cannot independently detect architectural changes.

**Confidence:** High.

**What would prove it wrong:** M4 automatically detects and compares the new connection using the original, unchanged inputs.

## P4. Expected cost and decision rule

**Prediction:** Option A (no change) will need manual re-labelling to make the new link visible in M4. We expect this to take **more than 3 manual steps**:

1. Open both Code2DFD JSON outputs (before and after).
2. Find the new flow.
3. Add label rows for it.
4. Recompute the metrics.

**Decision rule (fixed now, before any Event B work):**

| Outcome | Response | Week 9 verdict |
|---|---|---|
| Option A needs **≤ 3 manual steps** | Keep **A** (no structural change) | Supported |
| Option A needs **> 3 manual steps** | Implement **B**: a before/after comparison of Code2DFD JSON outputs | Partly supported |

**Expected cost of option B:**

| Item | Expected |
|---|---|
| Files changed | 1–2 |
| Lines added | < ~80 |
| New tests | 2–3 |
| Changes to M2 or Event A results | 0 |

**Confidence:** Medium.

**Proven wrong if:** option B needs a new module or class structure (Adapter-like), or touches frozen M2 / Event A results.

## P5. Expected verdict on the Week 9 decision

**Prediction: Partly supported.**

The Week 9 decision to choose a separate audit script over modifying Code2DFD remains justified.

**Reasoning:** M4 successfully separates quality auditing from the architecture-recovery tool. However, Event B is expected to expose a limitation: the audit cannot independently observe new architectural changes because it relies on manually prepared inputs.

Modifying Code2DFD or introducing an adapter layer would be disproportionate at this stage. A small extension to M4 could be considered if automated change visibility becomes a requirement.

**Confidence:** Medium-high.

**What would prove it wrong:** If the separate audit approach cannot provide reliable evidence of the new connection even after updating its inputs, the original design decision may need revision.

---

## Realistic Response Options

| Option | Response | Main trade-off |
|---|---|---|
| A. No structural change | Keep M4 unchanged and update its CSV inputs manually. | Minimal implementation cost, but continued manual dependency. |
| B. Small audit extension | Add a comparison between Code2DFD's before-and-after JSON outputs and the labelled results. | Better change visibility, but introduces additional parsing and testing. |
| C. Adapter layer / modify Code2DFD | Integrate architectural output directly into the audit process. | Greater automation, but increased complexity and maintenance cost. |

### Recommended Option: A – No Structural Change for Event B

The existing M4 design already provides the necessary checks once its inputs are updated. Implementing additional functionality before demonstrating that the current approach is insufficient would introduce unnecessary complexity.

**Important distinction:** Event B should test whether the architecture-recovery tool detects the new link and whether M4 can make that change visible. These are two separate questions. A successful Code2DFD detection does not automatically mean M4 can independently audit it.
