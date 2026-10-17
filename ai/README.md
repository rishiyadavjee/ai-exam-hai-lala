# Data Mining Assignment – Solver (Q1–Q5)

One Python script solves all five questions for any value of `d` (last digit of your enrollment number). Prints full working, every table, and a **VERIFY** block per question (use it for your verification note).

## Files

| File | What |
|---|---|
| `solve.py` | Solver. Standard library only. |
| `answers/answers_d0.txt … answers_d9.txt` | Pre-generated output for every d. Open the one for your digit. |
| `answers_all_d.txt` | All ten outputs in one file. |
| `VIVA.md` | Viva questions + model answers. |
| `README.md` | This file. |

## How to run

Needs Python 3.8+. No `pip install`.

```bash
python3 solve.py 7                  # prints working for d = 7
python3 solve.py 7 > answers_d7.txt # save to file for submission
```

Windows: use `python solve.py 7`.
`d` must be 0–9. Anything else prints usage and exits.

## What each part does

### Q1 Preprocessing
- Sorts data, X = 45 + 5d.
- (a) Equal-depth bins of 4. Bin means. Bin boundaries (value goes to nearer of min/max, tie → lower).
- (b) Min-max of 41 = (41 − min)/(max − min). Z-score = (41 − mean)/SD, **population** SD (÷ n).
- (c) Quartiles = median of lower half / upper half (6 + 6 values). Fences = Q1 − 1.5·IQR, Q3 + 1.5·IQR. Tests X. Removes X, recomputes both normalised values of 41.
  Damage measure used: **relative change** |with X − without X| / |without X|. Also prints a compression measure. Verdict printed. Pick your own measure if you prefer, but state and quantify it.
- VERIFY: `statistics.pstdev` vs hand formula.

### Q2 Apriori
- Deletes transaction by `d mod 7` (0→T1, 1→T2, 2→T3, 3→T5, 4→T6, 5→T7, 6→T8). Keeps original TIDs.
- Join step (share first k−1 items) then prune step. Prints C1, L1, C2, L2, C3, L3 and stop reason.
- Each pruned candidate labelled: **pruned by Apriori property** (names infrequent subset) or **pruned after counting** (gives count).
- (b) support, confidence, lift of {Dal, Oil} → {Rice}. Independent confidence = P(Rice). Interest verdict from lift.
- (c) Closed = no frequent superset with same count. Maximal = no frequent superset.
- VERIFY: brute-force all 31 itemsets, compare with Apriori result.

### Q3 Classification
- Deletes record `d + 1`. Log base 2.
- (a) Info(D), Info_A, Gain per attribute. (b) Weighted Gini per attribute. Reports root for each and flags **ties**.
- (c) Naive Bayes for X = (Low, Y, Good). Laplace: (count + 1)/(class count + distinct values of that attribute). Priors unsmoothed.
- (d) Lists zero counts. Searches all 1-record then 2-record deletions that make exactly one class's unsmoothed score 0. Prints options, picks first, shows smoothed scores and whether prediction changes. If a score is already 0 it says so.
- VERIFY: entropy recomputed with log2(n) − Σc·log2(c)/n.

### Q4 Clustering
- Initial centroids by `d mod 3` (0→A,D; 1→B,E; 2→C,F). Manhattan distance. Ties → cluster 2.
- (a) Two K-means iterations, centroid = coordinate mean. Convergence check by assignment comparison (extra 3rd pass if needed).
- (b) DBSCAN eps 3, minPts 4. Neighbourhood includes the point, dist ≤ eps. Core / border / noise.
- (c) minPts 3, label changes, comparison with K-means, then grid search for new point H: K-means gives it a cluster, DBSCAN calls it noise (checked for **both** minPts 3 and 4).
- VERIFY: weighted centroid identity Σ nₖcₖ = Σ points; neighbourhood symmetry.

### Q5 Evaluation
- FN = 10 + 2d, TN = 940 − 2d. Accuracy, precision, recall, F1.
- Do-nothing model accuracy = (FP + TN)/1000, recall 0. Shows accuracy trap.
- Change suggested: lower threshold. Numbers moved + cost.
- VERIFY: F1 = 2TP/(2TP+FP+FN).

## Before you submit

1. Run with **your** d. Do not copy someone else's file.
2. Write your **own** verification note per question (1–2 lines). Example: *"Checked pstdev with `statistics.pstdev` = 19.2157, matches hand formula."* Use the VERIFY lines.
3. Q1(c) and Q3(a) have judgement parts (damage measure, tie root). Write your reasoning in your own words.
4. Round final answers to 4 decimals (script already does).
5. Check by hand at least one row of each question. Examiner may ask in viva.

## Conventions followed (from the paper)

- Boundary tie → lower boundary. Z-score population SD. Quartiles median-of-halves.
- DBSCAN neighbourhood includes self, distance ≤ eps.
- K-means tie → higher cluster; cluster 1 starts at first named centroid.
- 4 decimal places final, full precision inside.
