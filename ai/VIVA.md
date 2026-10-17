# Viva – Model Answers

Numbers depend on your d. Open your `answers/answers_d<d>.txt` and quote your own values. Answers below give the concept.

---

## General

**Q. What did you do overall?**
Wrote one Python script, parameterised by d. It does all five questions, prints working, and a second-method check per question. I checked at least one step by hand per question.

**Q. Why population SD in z-score?**
Paper said divide by n. Treats the 12 values as the whole population, not a sample.

---

## Q1 Preprocessing

**Q. Equal-depth vs equal-width binning?**
Equal-depth: same number of values per bin (4 here). Equal-width: same interval size. Equal-depth handles skew better; equal-width is hurt by outliers.

**Q. Smoothing by means vs boundaries?**
Means: every value in bin replaced by bin mean. Boundaries: each value replaced by nearer of bin min/max; tie goes to lower boundary (paper rule).

**Q. Min-max formula?**
v' = (v − min)/(max − min) → [0,1]. Z-score: (v − mean)/SD.

**Q. IQR rule?**
Q1 = median of lower half, Q3 = median of upper half, IQR = Q3 − Q1. Outlier if below Q1 − 1.5·IQR or above Q3 + 1.5·IQR. For n = 12: halves are 6 + 6 values.

**Q. Which normalisation do you trust less with X in, and why?**
State measure first: relative change of 41's normalised value when X is removed. Quote your two percentages from the output. Whichever is larger = trust less. Intuition: min-max depends on the single max, so one extreme X squeezes all normal values into a small part of [0,1] (the output shows 41 → only 0.4800-style compression). Z-score uses mean and SD, both pulled by X, but spreads the effect over all values. Honest answer: verdict depends on measure; say which and defend with numbers.

**Q. How to fix outlier effect?**
Remove or cap (winsorise), use robust scaling (median, IQR), or log-transform.

---

## Q2 Association rules

**Q. Apriori property?**
Every subset of a frequent itemset is frequent. So if any (k−1)-subset of a candidate is infrequent, candidate is pruned without counting.

**Q. Two ways a candidate gets pruned?**
(1) Before counting by Apriori property: name the infrequent subset. (2) After counting: its count < min support (3). Both shown in output.

**Q. Join step?**
Two frequent k-itemsets sharing first k−1 items → one (k+1)-candidate. Then prune step.

**Q. Why does the algorithm stop?**
Quote your stop line: either L_k has fewer than two itemsets so no join is possible, or all candidates were pruned / failed the count so L_{k+1} is empty.

**Q. Support, confidence, lift?**
support(A→B) = count(A∪B)/N. confidence = count(A∪B)/count(A). lift = confidence / support(B).

**Q. Confidence if Rice independent of {Dal, Oil}?**
Equals P(Rice) = count(Rice)/N. Compare with rule confidence.

**Q. Is rule interesting?**
Lift > 1 → positive correlation, interesting. Lift = 1 → independent. Lift < 1 → negative correlation, not interesting even if confidence looks decent. Use your lift value.

**Q. Closed vs maximal?**
Closed: no frequent superset with the **same** support. Maximal: **no** frequent superset at all. Every maximal itemset is closed; not the reverse. Maximal set is small summary, closed set keeps support info (lossless).

---

## Q3 Classification

**Q. Information gain formula?**
Gain(A) = Info(D) − Σ (|D_v|/|D|)·Info(D_v). Info = −Σ p·log2 p.

**Q. Gini?**
Gini = 1 − Σ p². Weighted Gini = Σ (|D_v|/|D|)·Gini(D_v). Lower is better.

**Q. Do Gini and IG choose same root?**
Read from your output. Often yes. If two attributes tie, say so and give a tie-break (e.g. first listed attribute, or prefer fewer values). Both measures can tie together.

**Q. Naive Bayes assumption?**
Attributes conditionally independent given class: P(X|C) = ΠP(xi|C). Predict class maximising P(C)·ΠP(xi|C).

**Q. Why smooth? What smoothing used?**
Zero count makes whole product zero. Laplace: (count+1)/(class count + number of distinct values of that attribute). Priors not smoothed (paper rule).

**Q. Zero counts / deleting records?**
List zero counts from (d) line. Deleting record(s) so a (value, class) count becomes 0 makes that class's unsmoothed score exactly 0. Smoothing then gives it a small non-zero score. Say whether predicted class changed (output prints it).

**Q. Why is Gini cheaper than entropy?**
No logarithm. Results nearly always agree.

---

## Q4 Clustering

**Q. K-means steps?**
Pick initial centroids → assign each point to nearest (Manhattan here, tie → cluster 2) → recompute centroid as mean → repeat until assignments stop changing.

**Q. How do you know it converged?**
Assignments in consecutive iterations identical, so centroids stop moving. Quote the CONVERGED line (if iteration 2 changed, a 3rd pass confirms).

**Q. Manhattan distance but mean centroid. Problem?**
Mean minimises squared Euclidean, not Manhattan. Strict L1 version uses median (k-medians). Paper asked for mean update; fine for this question.

**Q. DBSCAN terms?**
Core: ≥ minPts points (including itself) within eps. Border: not core but within eps of a core. Noise: neither.

**Q. What changes when minPts 4 → 3?**
Read your "Labels that change" line. Lower minPts makes more points core; sparse groups that were noise can become clusters.

**Q. K-means vs DBSCAN on this data?**
K-means must put every point in one of k clusters, no noise concept, needs k. DBSCAN finds clusters from density, any shape, no k, leaves sparse points as noise. Use your output: which points differ.

**Q. How did you get H?**
Searched integer grid. Picked H closest to a final centroid such that nearest data point is > eps = 3 away, so neighbourhood is just H itself: not core, not border → noise for minPts 3 and 4. K-means still assigns H to nearest centroid (distances shown).

**Q. DBSCAN drawbacks?**
Sensitive to eps/minPts, struggles with varying density, distance cost in high dimension.

---

## Q5 Evaluation

**Q. Formulas?**
Accuracy (TP+TN)/total. Precision TP/(TP+FP). Recall TP/(TP+FN). F1 = 2PR/(P+R) = 2TP/(2TP+FP+FN).

**Q. Why is "accuracy above 95% so model is good" wrong?**
Fraud is rare. A model that flags nothing scores (FP+TN)/1000 accuracy, which is already near the real model's accuracy, with recall 0. Accuracy mostly measures the majority class. Quote your two accuracies and recall.

**Q. Bank cares about missed fraud. What change?**
Lower decision threshold. Recall ↑ (FN down), precision ↓ (FP up), accuracy slightly ↓. Cost: more false alarms → review workload, blocked genuine customers. Other options: judge by recall / F2 instead of accuracy; oversample fraud or use class weights.

**Q. Precision–recall trade-off?**
Raising threshold: fewer flagged, precision up, recall down. Lowering: opposite.

---

## Likely "trap" questions

- *"Did you just run a script?"* – Yes, but I know every formula above and checked a step by hand; show one on paper (e.g. one entropy value, one support count, one distance).
- *"What if d changes?"* – Rerun `python3 solve.py <d>`; data deletion, X, initial centroids and FN/TN update automatically.
- *"Why tie rules?"* – Paper fixed them so answers are unique: boundary tie → lower, K-means tie → higher cluster.
