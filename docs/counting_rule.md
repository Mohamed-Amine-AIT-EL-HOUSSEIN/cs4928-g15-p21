# Counting rule — G15 / P21 (M2 reproduction)

**Status:** APPROVED and frozen. Any change after this is a deviation.
Approved by: Mohamed Amine AIT EL HOUSSEIN, Yiwen Li, Zhuoya Zhang, Zexu Wang, Eoin Walsh Date: 19/10/2026 Commit: see git log for this file

Once approved and committed, this file does not change. Any later change is a deviation (see `docs/M2_record.md`).

---

## 1. What each rater looks at

**Use only:**
- `groundtruth_textual/<app>.txt` (the ground truth)
- `raw_results/Code2DFD/<app>-code2DFD-raw.json` (the tool output)
- your own count sheet (`count_sheets/raterN_counts.xlsx`)

**Do not open** `processed_results/` or `merged_results/`. They contain the paper's own labels.
**Do not discuss** any item with the other rater until both sheets are committed.

---

## 2. Matching names (applies to components, connections and endpoints)

Two names are **the same** if they are identical after:
- ignoring upper/lower case;
- treating `-`, `_` and a space as the same character.

Example: `config-server` = `config_server` = `Config Server`.

If the names differ in any other way, decide whether they clearly name the **same service** (for example `config` vs `config_server`).
- Same service → match. **Write the reason in Note.**
- Not sure → no match. **Write the reason in Note.**

---

## 3. Table A: ground-truth items (TP or FN)

| Characteristic | Label **TP** when… | Otherwise |
|---|---|---|
| Component | Code2DFD reports a component with the same name (rule 2) | **FN** |
| Connection | Code2DFD reports a connection whose **sender and receiver** both match (rule 2), **in the same direction** | **FN** |
| Endpoint | Code2DFD reports the same path **on the same service** | **FN** |

For every TP, write the matching tool item ID (`T…`) in column E.

---

## 4. Table B: Code2DFD output items (MATCH or FP)

- **MATCH**: the item is a ground-truth item under rule 3. Write the `G…` ID in column E.
- **FP**: the item is not in the ground truth.

Specific cases:
- **Self-connection** (`A -> A`): FP, unless the ground truth lists it.
- **Wrong direction** (`B -> A` when the ground truth has `A -> B`): FP for table B, and the ground-truth item `A -> B` is FN unless the right direction also appears.
- **One-to-one:** one tool item can match at most one ground-truth item, and the reverse.

---

## 5. Endpoints: formatting artefacts

Code2DFD stores endpoints as a text string, for example `'/"order'`.
A path counts as **the same path** if it differs from the ground truth **only** by:
- stray quote characters (`"` or `'`);
- a missing or extra `/` between two path segments.

Any other difference, such as a different word or a different parameter name, means **not the same path**. Write the reason in Note.

---

## 6. Resolving disagreements (after both sheets are committed)

1. Run `python scripts/score.py agreement`. It lists every conflict.
2. Both raters discuss each conflict and pick one label, using rules 2–5.
3. If they cannot agree, a **third group member** decides.
4. Write the outcome after `RESOLUTION:` in the Note column of `agreed_counts.xlsx`.

---

## 7. Agreement measure (bounded decision, made before counting)

- Cohen's kappa is calculated **separately** for table A (TP/FN) and table B (MATCH/FP), over all 4 apps.
- The M1 threshold (kappa ≥ 0.6) is applied to the **lower** of the two values.
- Reason: pooling both tables into one kappa would inflate agreement, because the table already fixes which labels are possible.
