# G15 / P21: M2 bounded reproduction kit

**Goal:** reproduce Code2DFD's precision / recall / F1 on 4 benchmark apps, with 2 independent raters, and compare with the paper.

**Deadline:** M2. Tags `M2_REPRO` and `PRE_EVENT_A`.

---

## Folder layout

```
README.md                  ← this guide
docs/counting_rule.md      ← how to label (approve BEFORE counting)
docs/M2_record.md          ← the audit record (fill as you go)
scripts/common.py          ← reads ground truth + raw tool output
scripts/build_sheets.py    ← makes the blank count sheets
scripts/score.py           ← kappa, P/R/F1, comparison, decision
count_sheets/              ← rater1, rater2, agreed sheets
results/                   ← generated outputs
```

The sheets in `count_sheets/` were already generated from commit `1b89944`. You only need `build_sheets.py` if you want to regenerate them.

---

## Step 0: one-time setup (anyone, 10 min)

1. Create the group repo (GitHub), and copy this folder into it.
2. Install the one library needed:
   ```
   pip install openpyxl
   ```
3. Note the path to your replication repo clone. Below it's written as `<REPL>`, for example:
   `"C:\Users\mek_u\LM121\Theory and Practice of Software Design (CS4928)\EMSE2025SAR-Replication"`
4. Commit: `git add . && git commit -m "M2 kit: scripts, blank sheets, draft counting rule"`

## Step 1: approve the counting rule (whole group, 15 min)

1. Everyone reads `docs/counting_rule.md`.
2. Change anything you disagree with **now**.
3. Fill in "Approved by / Date", then commit.
4. ⚠️ **After this commit, the rule is frozen.**

## Step 2: count (rater 1 and rater 2, separately, about 2–3 h each)

Each rater:
1. Opens **their own** file: `count_sheets/rater1_counts.xlsx` or `rater2_counts.xlsx`.
2. For each app tab, has these 2 files open side by side:
   - `<REPL>/tool_comparison/groundtruth_textual/<app>.txt`
   - `<REPL>/tool_comparison/results/recovery_correctness/raw_results/Code2DFD/<app>-code2DFD-raw.json`
3. Fills **only the yellow cells**:
   - Table A: TP or FN, plus the matching `T…` ID
   - Table B: MATCH or FP, plus the matching `G…` ID
   - Note: a reason for every judgement call
4. Order: kafka → petclinic → piggymetrics → blog (smallest first).
5. Commits **their file alone**:
   `git add count_sheets/rater1_counts.xlsx && git commit -m "Rater 1 counts complete"`

🚫 Don't open `processed_results/` or `merged_results/`.
🚫 Don't talk about items with the other rater until **both** have committed.

## Step 3: agreement (anyone, 5 min)

```
python scripts/score.py agreement
```

- Prints kappa and writes `results/agreement.md` + `results/conflicts.csv`.
- Creates `count_sheets/agreed_counts.xlsx`, with every disagreement **blank and red**.
- Commit: `git add results count_sheets/agreed_counts.xlsx && git commit -m "Agreement + conflicts"`

## Step 4: resolve conflicts (both raters, plus a 3rd if stuck, about 30 min)

1. Open `count_sheets/agreed_counts.xlsx`.
2. For each **red row**:
   - put the agreed label in column D;
   - write the reason after `RESOLUTION:` in the Note column.
3. Commit it.

## Step 5: score and compare (anyone, 5 min)

```
python scripts/score.py score <REPL>
```

- Writes `results/m2_results.csv` + `results/m2_summary.md`.
- Applies the frozen M1 rule and prints **REPRODUCED** or **NOT REPRODUCED**.
- ✅ **Whatever it says is the result.** Don't change anything to get a different answer.
- Commit.

## Step 6: write the record (1 person, 30–45 min)

Fill every `____` in `docs/M2_record.md`:
- environment versions;
- the D-01 reason (how the 4 apps were chosen);
- the key threat;
- the status;
- the evidence chain.

Then fill workbook row G15: **column I** (result) and **column J** (repo link + tag).

## Step 7: tag and push (1 person, 2 min)

```
git add . && git commit -m "M2 complete: bounded reproduction + audit"
git tag -a M2_REPRO -m "M2 bounded reproduction"
git tag -a PRE_EVENT_A -m "Frozen state before Change Event A"
git push && git push --tags
```

⚠️ **After `PRE_EVENT_A`, don't change anything in this state.** Event A work goes in new commits.
