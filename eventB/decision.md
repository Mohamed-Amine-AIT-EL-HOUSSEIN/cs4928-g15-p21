# Event B – Part 2: options and decision (M1–M2)

G15 / P21. Part 2 by Mohamed Amine AIT EL HOUSSEIN.

## Input from Part 1

- Code2DFD detects the new link `statement-service -> card-service` (P1 confirmed).
- The frozen M4 audit does not show it, because it reads only the Event A human labels (P2, P3 confirmed).
- Option A (no structural change) needs **7 manual steps** (9 under the full two-rater rule) to make the link visible ([evidence.md](evidence.md)).

## Decision rule (pre-registered in [predictions.md](predictions.md), commit `e7b8371`)

More than 3 manual steps → implement option B; Week 9 verdict "partly supported".
**7 > 3, so option B applies.** The rule was applied as written; nothing was re-decided after seeing the evidence.

## Options

| Option                             | Response                                                                                                                                                                                                                                           | Main trade-off                                                                                                                                               |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A. No structural change            | Keep M4 as it is; re-label by hand after every change                                                                                                                                                                                              | No new code, but 7–9 manual steps per change, and the audit still never names the new link                                                                   |
| **B. Small extension (chosen)**    | Add an optional `--before/--after` mode to `scripts/m4_audit.py` that compares two Code2DFD outputs **by sender → receiver name** and names every added/removed component and connection, flagging whether each is already in the reference labels | Makes the change visible in one command; adds a second place where names are normalised, and new items still need a human label before they count in metrics |
| C. Adapter layer / modify Code2DFD | Parser per tool feeding a shared matcher, or change Code2DFD itself                                                                                                                                                                                | Would automate more, but designs for several tools when we study one (speculative generality); highest cost and risk                                         |

## Decision

**Option B.** It answers the pressure (the change is named without manual archaeology) at the smallest cost, and keeps the Week 9 choice of a separate audit script.

Design choices that follow from Part 1 evidence:

- **Match by name, never by ID**: adding one link renumbered 14 of 23 connections in Code2DFD's output.
- **Default behaviour unchanged**: without `--before/--after`, the audit output is identical to the frozen `m4/results/audit.json`.
- **No frozen file changed**: M2 and Event A results are not touched.

**Accepted trade-off:** new links are _named_ automatically, but still need a human label before they enter precision/recall/F1. We accept this because labelling is the study's method (two raters, frozen counting rule); automating it would change the method, not just the tooling.
