# M2 result - Code2DFD on 4 benchmark apps

| Scope | Our P | Our R | Our F1 | Paper P | Paper R | Paper F1 | diff F1 |
|---|---|---|---|---|---|---|---|
| microservice-kafka | 0.875 | 0.677 | 0.764 | 0.875 | 0.677 | 0.764 | 0.000 |
| spring-petclinic-microservices | 0.978 | 0.880 | 0.926 | 0.978 | 0.880 | 0.926 | 0.000 |
| piggymetrics | 0.906 | 0.906 | 0.906 | 0.906 | 0.906 | 0.906 | 0.000 |
| blog-microservices | 0.978 | 0.652 | 0.783 | 0.978 | 0.652 | 0.783 | 0.000 |
| POOLED | 0.939 | 0.785 | 0.855 | 0.939 | 0.785 | 0.855 | 0.000 |

## Decision rule (frozen in M1)

- PASS: Pooled P/R/F1 within +/-0.05 (diffs P/R/F1 = [0.0, 0.0, 0.0])
- PASS: Every app F1 within +/-0.10 ({'microservice-kafka': 0.0, 'spring-petclinic-microservices': 0.0, 'piggymetrics': 0.0, 'blog-microservices': 0.0})
- PASS: Kappa >= 0.60 (kappa = 1.00)

## Status: **REPRODUCED**

Per-characteristic numbers: results/m2_results.csv
