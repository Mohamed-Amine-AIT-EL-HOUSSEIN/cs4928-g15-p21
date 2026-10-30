# Event A — prediction (written before counting)

## Held-out case
App 6: spring-netflix-oss-microservices (paper Table 1 #6), replication repo @1b89944.
Rule: first Table 1 app not used at M2 whose results no member has seen.

## Method
Unchanged M2 method (docs/counting_rule.md, scripts/score.py, 2 independent raters + tie-breaker). No retuning after results. New raters, same rule.

## Prediction
M2 baseline: F1 0.855, kappa 1.00; all component/connection errors were FNs (mainly service-to-service calls and logging/broker links).
1. Errors stay FN-dominated; component/connection precision ≈ 1.00.
2. Missed connections are mainly service-to-service and infrastructure links.
3. F1 within ±0.10 of M2.
4. Kappa ≥ 0.8.

## Would challenge M2
F1 off by >0.10, component/connection FPs appear, missed connections fall outside the M2 categories, or kappa < 0.6.

Note: committed by a rater before counting; based only on M2 results. Nobody saw App 6 results beforehand.
