# G15 / P21 — M1 Plan (preregistration)

Copied from the shared workbook 

## RQ1
When two of us independently count TP/FP/FN on Code2DFD's published outputs for four benchmark apps, how well do our counts agree, and how close do the resulting precision/recall/F1 get to what the paper reports?

## RQ2
How accurately does Code2DFD recover the architecture of a new microservice app outside the original dataset, and what's the cheapest design for adding new apps or tool formats: manual counting, one script per tool, or an Adapter per tool feeding a shared matcher?

## Bounded sample
- RQ1: Code2DFD published outputs for 4 dataset apps: piggymetrics, spring-petclinic-microservices, microservice-kafka, blog-microservices (GT: groundtruth_textual/*.txt).
- RQ2: 1 new app: ewolff/microservice-consul @08b0190.

## Method / decision rule
- RQ1: 2 members label each GT item TP/FP/FN independently (components/connections/endpoints); agreement = Cohen's kappa; resolve by discussion. P/R/F1 per app + pooled vs paper's processed_results.
- RQ2: same scoring on the new app; compare manual / script-per-tool / Adapter+shared matcher by new LOC + time to add 1 app or 1 tool.

## Expected result (before execution)
Kappa ≥ 0.8; pooled P≈0.96, R≈0.81, F1≈0.88 (paper data, these 4 apps), ours within ±0.05. New app: overall F1 < 0.86, endpoints weakest. Adapter cheapest once ≥2 tools/apps.

## Non-reproduction
Pooled P/R/F1 off by >0.05, or any app F1 off by >0.10; or kappa < 0.6; or tool won't run on pinned commits.

## Known deviation (recorded 19/10, before any M2 counting)
The P21 pack says to take the first 3 eligible apps in stable order and not to choose by results. These 4 apps (paper Table 1 #3, #5, #15, #16) were suggested by an AI assistant in Week 5 to give a mix of sizes and easy/hard cases; the choice was partly informed by known published results (e.g. blog-microservices for low recall, piggymetrics for its FPs). The aim was a mix of difficulty, not agreement with the paper. The workbook was already frozen, so we keep this sample and treat selection bias as a threat to validity (see M2_record D-01).
