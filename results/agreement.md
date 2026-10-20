# Inter-rater agreement (Cohen's kappa)

Table A = ground-truth items (TP/FN). Table B = Code2DFD output items (MATCH/FP).

| Scope | Table | Items | % agree | kappa |
|---|---|---|---|---|
| microservice-kafka | A | 31 | 100.0 | 1.00 |
| microservice-kafka | B | 24 | 100.0 | 1.00 |
| spring-petclinic-microservices | A | 50 | 100.0 | 1.00 |
| spring-petclinic-microservices | B | 45 | 100.0 | 1.00 |
| piggymetrics | A | 64 | 100.0 | 1.00 |
| piggymetrics | B | 64 | 100.0 | 1.00 |
| blog-microservices | A | 69 | 100.0 | 1.00 |
| blog-microservices | B | 46 | 100.0 | 1.00 |
| ALL 4 APPS | A | 214 | 100.0 | 1.00 |
| ALL 4 APPS | B | 179 | 100.0 | 1.00 |

**Kappa used by the decision rule (lower of A and B, all apps): 1.00**
(threshold >= 0.6; expected in M1: >= 0.8)

Note: kappa is n/a when both raters gave every item the same label (no variation), so % agreement is reported alongside it.

Conflicts to resolve: 0 (see results/conflicts.csv)
