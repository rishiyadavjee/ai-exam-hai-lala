#!/usr/bin/env python3
"""
Data Mining assignment solver (Q1-Q5).

Usage:   python3 solve.py <d>      d = last digit of enrollment number (0-9)
Example: python3 solve.py 7
         python3 solve.py 7 > answers_d7.txt

Only the Python standard library is used (Python 3.8+).
Every question ends with a VERIFY block: a second-method check you can quote
in your "verification note".
"""
import sys
import math
import statistics
from itertools import combinations
from collections import Counter


# ----------------------------------------------------------------- helpers
def f4(x):
    return f"{x:.4f}"


def med(v):
    v = sorted(v)
    n = len(v)
    m = n // 2
    return v[m] if n % 2 else (v[m - 1] + v[m]) / 2


def hdr(t):
    print("\n" + "=" * 74 + "\n" + t + "\n" + "=" * 74)


def fmt(s):
    return "{" + ", ".join(s) + "}"


# ---------------------------------------------------------------------- Q1
def q1(d):
    hdr("Q1  PREPROCESSING")
    X = 45 + 5 * d
    data = sorted([5, 7, 12, 14, 18, 18, 22, 25, 27, 30, 41, X])
    n = len(data)
    print(f"X = 45 + 5*{d} = {X}")
    print("Data (sorted):", data)

    print("\n(a) Equal-depth bins, depth 4")
    for i in range(0, n, 4):
        b = data[i:i + 4]
        m = sum(b) / len(b)
        lo, hi = b[0], b[-1]
        bnd = [lo if (v - lo) <= (hi - v) else hi for v in b]  # tie -> lower
        print(f" Bin{i // 4 + 1}: {b}")
        print(f"   smoothing by means      : {', '.join([f4(m)] * len(b))}")
        print(f"   smoothing by boundaries : {bnd}   (min={lo}, max={hi})")

    print("\n(b) Normalising 41 (all 12 values)")
    mn, mx = min(data), max(data)
    mu = sum(data) / n
    sd = math.sqrt(sum((v - mu) ** 2 for v in data) / n)  # population SD
    mm = (41 - mn) / (mx - mn)
    z = (41 - mu) / sd
    print(f" min={mn}, max={mx}, mean={f4(mu)}, population SD={f4(sd)}")
    print(f" min-max = (41-{mn})/({mx}-{mn}) = {f4(mm)}")
    print(f" z-score = (41-{f4(mu)})/{f4(sd)} = {f4(z)}")

    print("\n(c) IQR outlier rule")
    lowh, upph = data[: n // 2], data[n // 2:]
    Q1, Q3 = med(lowh), med(upph)
    iqr = Q3 - Q1
    lf, uf = Q1 - 1.5 * iqr, Q3 + 1.5 * iqr
    print(f" lower half={lowh} -> Q1={f4(Q1)}")
    print(f" upper half={upph} -> Q3={f4(Q3)}")
    print(f" IQR={f4(iqr)}, fences=[{f4(lf)}, {f4(uf)}]")
    out = X > uf or X < lf
    print(f" X={X} is {'an OUTLIER' if out else 'NOT an outlier'} "
          f"({'>' if X > uf else '<=' } upper fence {f4(uf)})")

    d2 = data[:]
    d2.remove(X)
    n2 = len(d2)
    mn2, mx2 = min(d2), max(d2)
    mu2 = sum(d2) / n2
    sd2 = math.sqrt(sum((v - mu2) ** 2 for v in d2) / n2)
    mm2 = (41 - mn2) / (mx2 - mn2)
    z2 = (41 - mu2) / sd2
    print(f"\n Without X (n={n2}): min={mn2}, max={mx2}, mean={f4(mu2)}, SD={f4(sd2)}")
    print(f" min-max of 41 = {f4(mm2)}      z-score of 41 = {f4(z2)}")

    print("\n Damage measure = relative change |with X - without X| / |without X|")
    dm_abs, dz_abs = abs(mm - mm2), abs(z - z2)
    dm_rel, dz_rel = dm_abs / abs(mm2), dz_abs / abs(z2)
    print(f" min-max: {f4(mm)} vs {f4(mm2)} -> abs change {f4(dm_abs)}, relative {f4(dm_rel)} ({dm_rel * 100:.2f}%)")
    print(f" z-score: {f4(z)} vs {f4(z2)} -> abs change {f4(dz_abs)}, relative {f4(dz_rel)} ({dz_rel * 100:.2f}%)")
    worse = "min-max" if dm_rel > dz_rel else "z-score"
    print(f" Extra measure (compression): the 11 normal values (5..41) fill only {f4((41 - mn) / (mx - mn))} of the [0,1] min-max range "
          f"(1.0000 without X); under z-score their SD-scaled spread shrinks by factor {f4(sd2 / sd)}.")
    print(f" => Trust {worse} LESS with X left in (larger relative damage).")
    if worse == "min-max":
        print(" Reason: min-max uses only min & max, so one extreme X stretches the range and squeezes")
        print("         every other value toward 0; z-score also moves (mean, SD pulled by X) but all")
        print("         12 values contribute, so the damage is spread out.")
    else:
        print(" Reason: X drags the mean up AND inflates the SD, and both enter every z-score, so the")
        print("         z-score of 41 shifts more (relative) than its min-max value; min-max is hurt")
        print("         only through the max.")
    print(" (Verdict depends on the damage measure you pick; state it, quantify it, justify it.)")

    print("\nVERIFY (second method)")
    print(f" statistics.pstdev -> {f4(statistics.pstdev(data))} (hand formula gave {f4(sd)})")
    print(f" mean check: sum={sum(data)}, sum/12={f4(sum(data) / 12)}")


# ---------------------------------------------------------------------- Q2
def q2(d):
    hdr("Q2  ASSOCIATION RULES (Apriori)")
    base = {
        1: {"Rice", "Dal", "Oil"},
        2: {"Rice", "Tea", "Sugar"},
        3: {"Dal", "Oil", "Tea"},
        4: {"Rice", "Dal", "Oil", "Tea"},
        5: {"Rice", "Dal", "Sugar"},
        6: {"Dal", "Oil", "Tea", "Sugar"},
        7: {"Rice", "Dal", "Oil", "Sugar"},
        8: {"Tea", "Sugar"},
    }
    rm = [1, 2, 3, 5, 6, 7, 8][d % 7]
    T = {k: v for k, v in base.items() if k != rm}
    N = len(T)
    MIN = 3
    print(f"d mod 7 = {d % 7} -> delete T{rm}. Remaining TIDs: {list(T)}  (N={N}, min support count={MIN})")
    for k, v in T.items():
        print(f"  T{k}: {sorted(v)}")

    def cnt(s):
        return sum(1 for t in T.values() if set(s) <= t)

    def gen(L):
        """join step (shared first k-1 items) + Apriori prune step"""
        Ls = set(L)
        ok, pr = [], []
        for a, b in combinations(L, 2):
            if a[:-1] == b[:-1]:
                c = a + (b[-1],)
                bad = [s for s in combinations(c, len(c) - 1) if s not in Ls]
                (pr if bad else ok).append((c, bad) if bad else c)
        return ok, pr

    items = sorted({i for t in T.values() for i in t})
    C, pruned, k = [(i,) for i in items], [], 1
    freq = {}
    while True:
        print(f"\nC{k}:")
        for c, bad in pruned:
            print(f"   {fmt(c)}  PRUNED by Apriori property (infrequent subset {fmt(bad[0])})")
        L = []
        for c in C:
            n = cnt(c)
            if n >= MIN:
                L.append(c)
                freq[c] = n
                print(f"   {fmt(c)}  count={n}  keep")
            else:
                print(f"   {fmt(c)}  count={n}  PRUNED after counting (<{MIN})")
        print(f"L{k} = " + (", ".join(f"{fmt(c)}:{freq[c]}" for c in L) if L else "(empty)"))
        nxt, pr = gen(L) if len(L) >= 2 else ([], [])
        if not nxt:
            print(f"\nC{k + 1}:")
            for c, bad in pr:
                print(f"   {fmt(c)}  PRUNED by Apriori property (infrequent subset {fmt(bad[0])})")
            if len(L) < 2:
                why = f"L{k} has {len(L)} itemset(s); join needs two itemsets sharing {k - 1} item(s) -> no C{k + 1}"
            elif pr:
                why = f"every C{k + 1} candidate pruned by Apriori property -> nothing to count"
            else:
                why = f"no two L{k} itemsets share their first {k - 1} item(s) -> C{k + 1} empty"
            print(f"   (empty)\nSTOP: {why}.")
            break
        C, pruned, k = nxt, pr, k + 1

    print(f"\n(b) Rule {{Dal, Oil}} -> {{Rice}}")
    a, c_, ac = cnt(("Dal", "Oil")), cnt(("Rice",)), cnt(("Dal", "Oil", "Rice"))
    sup, conf = ac / N, ac / a
    lift = conf / (c_ / N)
    print(f" count(Dal,Oil,Rice)={ac}, count(Dal,Oil)={a}, count(Rice)={c_}, N={N}")
    print(f" support    = {ac}/{N} = {f4(sup)}")
    print(f" confidence = {ac}/{a} = {f4(conf)}")
    print(f" lift       = {f4(conf)}/{f4(c_ / N)} = {f4(lift)}")
    print(f" confidence if independent = P(Rice) = {c_}/{N} = {f4(c_ / N)}")
    verdict = ("lift > 1: positive correlation, interesting" if lift > 1 else
               "lift = 1: independent, NOT interesting" if abs(lift - 1) < 1e-12 else
               "lift < 1: negative correlation, NOT interesting (high confidence is misleading)")
    print(f" => {verdict}")

    print("\n(c) Closed / maximal frequent itemsets")
    for s in sorted(freq, key=lambda x: (len(x), x)):
        sup_ = [t for t in freq if len(t) > len(s) and set(s) < set(t)]
        closed = not any(freq[t] == freq[s] for t in sup_)
        maximal = not sup_
        tag = ", ".join(x for x, y in (("CLOSED", closed), ("MAXIMAL", maximal)) if y) or "-"
        print(f"  {fmt(s):28s} count={freq[s]}  {tag}")

    print("\nVERIFY (second method): brute force over all 2^5-1 itemsets")
    brute = {}
    for r in range(1, 6):
        for s in combinations(items, r):
            if cnt(s) >= MIN:
                brute[s] = cnt(s)
    print(f" Apriori frequent set == brute-force frequent set: {brute == freq}")


# ---------------------------------------------------------------------- Q3
RAW = [
    (1, "High", "N", "Fair", "No"), (2, "High", "N", "Good", "No"),
    (3, "High", "Y", "Fair", "Yes"), (4, "Low", "Y", "Fair", "Yes"),
    (5, "Low", "Y", "Good", "No"), (6, "Low", "N", "Good", "Yes"),
    (7, "High", "Y", "Good", "Yes"), (8, "Low", "N", "Fair", "No"),
    (9, "Low", "Y", "Fair", "Yes"), (10, "High", "N", "Fair", "Yes"),
]
ATTR = ["Income", "Student", "Credit"]
CLS = ["Yes", "No"]
XQ = ("Low", "Y", "Good")


def ent(c):
    n = sum(c)
    return -sum(x / n * math.log2(x / n) for x in c if x) if n else 0.0


def gini(c):
    n = sum(c)
    return 1 - sum((x / n) ** 2 for x in c) if n else 0.0


def nb_stats(data):
    N = len(data)
    st = {}
    for c in CLS:
        rows = [r for r in data if r[4] == c]
        st[c] = dict(Nc=len(rows), prior=len(rows) / N,
                     cnts=[sum(1 for r in rows if r[j] == XQ[j - 1]) for j in (1, 2, 3)])
    return st


def nb_scores(st):
    K = [len({r[j] for r in RAW}) for j in (1, 2, 3)]
    uns, sm = {}, {}
    for c, s in st.items():
        u = s["prior"]
        m = s["prior"]
        for i in range(3):
            u *= (s["cnts"][i] / s["Nc"]) if s["Nc"] else 0
            m *= (s["cnts"][i] + 1) / (s["Nc"] + K[i])
        uns[c], sm[c] = u, m
    return uns, sm, K


def q3(d):
    hdr("Q3  CLASSIFICATION")
    rm = d + 1
    data = [r for r in RAW if r[0] != rm]
    N = len(data)
    print(f"Delete record #{rm}. Remaining {N} records: {[r[0] for r in data]}")
    cc = [sum(1 for r in data if r[4] == c) for c in CLS]
    H = ent(cc)
    print(f"Class counts: Yes={cc[0]}, No={cc[1]}   Info(D) = {f4(H)}")
    print(f"Gini(D) = {f4(gini(cc))}")

    print("\n(a)+(b) Information gain and weighted Gini")
    res, maxdiff = {}, 0.0
    for j, a in enumerate(ATTR, 1):
        E = G = Ealt = 0.0
        print(f" -- {a}")
        for v in sorted({r[j] for r in RAW}):
            sub = [r for r in data if r[j] == v]
            c = [sum(1 for r in sub if r[4] == k) for k in CLS]
            n = len(sub)
            e, g = ent(c), gini(c)
            E += n / N * e
            G += n / N * g
            if n:  # alt formula: H = log2 n - (1/n) sum c log2 c
                Ealt += n / N * (math.log2(n) - sum(x * math.log2(x) for x in c if x) / n)
            print(f"    {v:5s} n={n} (Yes={c[0]}, No={c[1]})  entropy={f4(e)}  gini={f4(g)}")
        res[a] = (H - E, G)
        maxdiff = max(maxdiff, abs(E - Ealt))
        print(f"    Info_{a}={f4(E)}   Gain={f4(H - E)}   weighted Gini={f4(G)}")
    r_ig = max(res, key=lambda a: res[a][0])
    r_gi = min(res, key=lambda a: res[a][1])
    ties_ig = [a for a in res if abs(res[a][0] - res[r_ig][0]) < 1e-12]
    ties_gi = [a for a in res if abs(res[a][1] - res[r_gi][1]) < 1e-12]
    print(f" Root by information gain : {r_ig}" + (f"  (TIE among {ties_ig})" if len(ties_ig) > 1 else ""))
    print(f" Root by weighted Gini    : {r_gi}" + (f"  (TIE among {ties_gi})" if len(ties_gi) > 1 else ""))
    print(f" Same root? {'YES' if r_ig == r_gi else 'NO'}")

    print(f"\n(c) Naive Bayes, X = {XQ}")
    st = nb_stats(data)
    uns, sm, K = nb_scores(st)
    for c in CLS:
        s = st[c]
        print(f" P({c}) = {s['Nc']}/{N} = {f4(s['prior'])}")
        for i, a in enumerate(ATTR):
            print(f"   P({a}={XQ[i]} | {c}) = ({s['cnts'][i]}+1)/({s['Nc']}+{K[i]}) = {f4((s['cnts'][i] + 1) / (s['Nc'] + K[i]))}")
        print(f"   smoothed score({c}) = {f4(sm[c])}")
    pred0 = max(sm, key=sm.get)
    print(f" Predicted class (smoothed): {pred0}   (Yes={f4(sm['Yes'])}, No={f4(sm['No'])})")

    print("\n(d) Zero counts (unsmoothed) for X's attribute values")
    zeros = [(c, ATTR[i], XQ[i]) for c in CLS for i in range(3) if st[c]["cnts"][i] == 0]
    for c in CLS:
        print(f"   class {c}: counts {dict(zip([f'{ATTR[i]}={XQ[i]}' for i in range(3)], st[c]['cnts']))}")
    print("   zero counts:", ", ".join(f"count({a}={v}, {c})=0" for c, a, v in zeros) if zeros else "none")
    print("   unsmoothed scores:", {c: f4(uns[c]) for c in CLS})

    if any(uns[c] == 0 for c in CLS):
        print("   A class score is ALREADY exactly 0 -> no extra deletion needed.")
        print("   (Smoothing step above gives it a small non-zero score.)")
    else:
        rest = [r[0] for r in data]
        cands = []
        for k in (1, 2):
            for combo in combinations(rest, k):
                nd = [r for r in data if r[0] not in combo]
                if any(sum(1 for r in nd if r[4] == c) == 0 for c in CLS):
                    continue
                u, _, _ = nb_scores(nb_stats(nd))
                zc = [c for c in CLS if u[c] == 0]
                if len(zc) == 1:
                    cands.append((combo, zc[0]))
            if cands:
                break  # prefer the fewest deletions
        print(f"   Minimal deletions that zero exactly one class: {len(cands)} option(s)")
        for combo, zc in cands[:10]:
            print(f"     delete {list(combo)} -> unsmoothed score of class {zc} = 0")
        if cands:
            combo, zc = cands[0]
            nd = [r for r in data if r[0] not in combo]
            st2 = nb_stats(nd)
            u2, s2, _ = nb_scores(st2)
            print(f"\n   CHOSEN: delete records {list(combo)}  (remaining {len(nd)})")
            for c in CLS:
                s = st2[c]
                print(f"    class {c}: Nc={s['Nc']}, prior={f4(s['prior'])}, counts for X={s['cnts']}")
            print(f"    unsmoothed scores: { {c: f4(u2[c]) for c in CLS} }")
            print(f"    smoothed scores  : { {c: f4(s2[c]) for c in CLS} }")
            pred1 = max(s2, key=s2.get)
            print(f"    predicted class now {pred1}; before {pred0} -> "
                  f"{'CHANGED' if pred1 != pred0 else 'unchanged'}")
        else:
            print("   No 1- or 2-record deletion makes exactly one class score 0.")

    print("\nVERIFY (second method)")
    print(f" Info_A via log2(n)-sum(c*log2 c)/n formula vs entropy formula: max diff = {maxdiff:.2e}")
    print(f" Priors sum to 1: {sum(st[c]['prior'] for c in CLS)}")


# ---------------------------------------------------------------------- Q4
P = {"A": (1, 2), "B": (2, 1), "C": (2, 4), "D": (6, 5), "E": (7, 7), "F": (8, 5), "G": (4, 3)}


def md(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def assign(Pts, c):
    return {k: (1 if md(p, c[0]) < md(p, c[1]) else 2) for k, p in Pts.items()}  # tie -> 2


def newcent(Pts, asg, old):
    out = []
    for k in (1, 2):
        m = [Pts[p] for p in Pts if asg[p] == k]
        out.append((sum(x for x, _ in m) / len(m), sum(y for _, y in m) / len(m)) if m else old[k - 1])
    return out


def dbscan(Pts, eps, minpts):
    nb = {k: [q for q in Pts if md(Pts[k], Pts[q]) <= eps] for k in Pts}
    core = {k for k in Pts if len(nb[k]) >= minpts}
    cid, comps, seen = {}, [], set()
    for k in sorted(core):
        if k in seen:
            continue
        comp, stack = {k}, [k]
        seen.add(k)
        while stack:
            u = stack.pop()
            for v in nb[u]:
                if v in core and v not in seen:
                    seen.add(v)
                    comp.add(v)
                    stack.append(v)
        comps.append(comp)
    label = {}
    for k in Pts:
        if k in core:
            label[k] = "core"
        elif any(q in core for q in nb[k]):
            label[k] = "border"
        else:
            label[k] = "noise"
    for i, comp in enumerate(comps, 1):
        for p in comp:
            cid[p] = i
    for k in Pts:  # border -> first cluster (by core-name order) it touches
        if label[k] == "border":
            for i, comp in enumerate(comps, 1):
                if any(q in comp for q in nb[k]):
                    cid[k] = i
                    break
    return nb, label, cid


def show_dbscan(Pts, eps, minpts):
    nb, label, cid = dbscan(Pts, eps, minpts)
    for k in Pts:
        print(f"   {k}{Pts[k]}: N_eps={nb[k]} size={len(nb[k])}  -> {label[k].upper()}"
              + (f" (cluster {cid[k]})" if k in cid else ""))
    cl = {}
    for k, i in cid.items():
        cl.setdefault(i, []).append(k)
    for i in sorted(cl):
        print(f"   cluster {i}: {sorted(cl[i])}")
    print(f"   noise: {[k for k in Pts if label[k] == 'noise']}")
    return nb, label, cid


def q4(d):
    hdr("Q4  CLUSTERING (Manhattan distance)")
    names = [("A", "D"), ("B", "E"), ("C", "F")][d % 3]
    print(f"d mod 3 = {d % 3} -> initial centroids {names[0]} (cluster 1) and {names[1]} (cluster 2)")
    cent = [P[names[0]], P[names[1]]]

    print("\n(a) K-means, k=2")
    hist = []
    for it in (1, 2):
        asg = assign(P, cent)
        print(f" Iteration {it}: centroids c1=({f4(cent[0][0])}, {f4(cent[0][1])}), c2=({f4(cent[1][0])}, {f4(cent[1][1])})")
        for k, p in P.items():
            d1, d2 = md(p, cent[0]), md(p, cent[1])
            print(f"   {k}{p}: d1={d1:.4f}, d2={d2:.4f} -> cluster {asg[k]}" + ("  (tie -> higher)" if d1 == d2 else ""))
        new = newcent(P, asg, cent)
        print(f"   C1={sorted(p for p in P if asg[p] == 1)}  C2={sorted(p for p in P if asg[p] == 2)}")
        print(f"   new centroids: c1=({f4(new[0][0])}, {f4(new[0][1])})  c2=({f4(new[1][0])}, {f4(new[1][1])})")
        hist.append((asg, new))
        cent = new
    asg1, asg2 = hist[0][0], hist[1][0]
    asg3 = assign(P, cent)
    if asg1 == asg2:
        conv = "CONVERGED: iteration 2 assignments are identical to iteration 1, so centroids did not move."
    elif asg3 == asg2:
        conv = ("CONVERGED: iteration 2 assignments changed vs iteration 1, but a 3rd assignment pass "
                "with the iteration-2 centroids gives the same clusters, so centroids stay fixed.")
    else:
        conv = "NOT converged: a 3rd assignment pass still changes cluster membership."
    print(f" {conv}")
    final_km = asg2
    final_c = cent

    print("\n(b) DBSCAN eps=3, minPts=4 (point counts itself, dist <= eps)")
    nb4, lab4, cid4 = show_dbscan(P, 3, 4)

    print("\n(c) DBSCAN eps=3, minPts=3")
    nb3, lab3, cid3 = show_dbscan(P, 3, 3)
    ch = [k for k in P if lab3[k] != lab4[k]]
    print("   Labels that change (minPts 4 -> 3):",
          ", ".join(f"{k}: {lab4[k]} -> {lab3[k]}" for k in ch) if ch else "none")
    km = {1: sorted(p for p in P if final_km[p] == 1), 2: sorted(p for p in P if final_km[p] == 2)}
    print(f"   K-means final clusters: C1={km[1]}, C2={km[2]}")
    forced = [k for k in P if lab3[k] == "noise" or lab4[k] == "noise"]
    print(f"   Points K-means forces into a cluster but DBSCAN calls noise (some minPts): {forced}")
    print("   K-means assigns every point to some cluster (no noise concept, spherical/ L1-ball shapes,")
    print("   needs k). DBSCAN finds density-connected regions of any shape and leaves sparse points as noise.")

    best = None
    for x in range(-3, 16):
        for y in range(-3, 16):
            H = (x, y)
            d1, d2 = md(H, final_c[0]), md(H, final_c[1])
            near = min(d1, d2)
            P2 = dict(P)
            P2["H"] = H
            if (dbscan(P2, 3, 4)[1]["H"] == "noise" and dbscan(P2, 3, 3)[1]["H"] == "noise"):
                if best is None or (near, x, y) < best[0]:
                    best = ((near, x, y), H, d1, d2)
    if best:
        _, H, d1, d2 = best
        cl = 1 if d1 < d2 else 2
        print(f"\n   New point H = {H}")
        print(f"   Manhattan to final centroids: d(H,c1)={d1:.4f}, d(H,c2)={d2:.4f} -> K-means puts H in cluster {cl}")
        dists = {k: md(H, p) for k, p in P.items()}
        print(f"   Distances to data points: {dists}")
        print(f"   Nearest data point at {min(dists.values())} > eps=3, so |N_eps(H)|=1 (itself only)")
        print("   -> not core, no core neighbour -> NOISE for both minPts=4 and minPts=3")

    print("\nVERIFY (second method)")
    tot_x = sum(p[0] for p in P.values())
    tot_y = sum(p[1] for p in P.values())
    n1 = sum(1 for k in P if final_km[k] == 1)
    n2 = len(P) - n1
    # weighted centroid identity uses the cluster assignment that produced the centroids (iteration 2)
    cx = n1 * cent[0][0] + n2 * cent[1][0]
    cy = n1 * cent[0][1] + n2 * cent[1][1]
    print(f" weighted centroid identity sum(n_k*c_k) == sum(points): "
          f"({cx:.4f},{cy:.4f}) vs ({tot_x},{tot_y})")
    sym = all((q in nb4[k]) == (k in nb4[q]) for k in P for q in P)
    print(f" DBSCAN neighbourhood relation symmetric: {sym}")


# ---------------------------------------------------------------------- Q5
def q5(d):
    hdr("Q5  EVALUATION")
    TP, FP, FN, TN = 30, 20, 10 + 2 * d, 940 - 2 * d
    tot = TP + FP + FN + TN
    print(f"TP={TP}, FP={FP}, FN=10+2*{d}={FN}, TN=940-2*{d}={TN}  (total={tot})")
    acc = (TP + TN) / tot
    prec = TP / (TP + FP)
    rec = TP / (TP + FN)
    f1 = 2 * prec * rec / (prec + rec)
    print("\n(a)")
    print(f" accuracy  = (TP+TN)/total = {TP + TN}/{tot} = {f4(acc)}")
    print(f" precision = TP/(TP+FP)    = {TP}/{TP + FP} = {f4(prec)}")
    print(f" recall    = TP/(TP+FN)    = {TP}/{TP + FN} = {f4(rec)}")
    print(f" F1        = 2PR/(P+R)     = {f4(f1)}")

    print("\n(b) Model that never flags fraud (predict all negative)")
    base = (FP + TN) / tot
    print(f" actual frauds = TP+FN = {TP + FN}; actual legit = FP+TN = {FP + TN}")
    print(f" accuracy = {FP + TN}/{tot} = {f4(base)};  recall = 0/{TP + FN} = {f4(0.0)};  precision = 0/0 (undefined)")
    print(f" Do-nothing model gets {f4(base)} accuracy vs your model {f4(acc)} -> only {f4(acc - base)} apart,")
    print(f" while recall is {f4(rec)} vs 0. Fraud is rare ({(TP + FN) / tot * 100:.1f}%), so accuracy is")
    print(" dominated by the majority class and hides the missed frauds.")

    print("\n(c) Change: lower the decision threshold (e.g. 0.5 -> 0.3)")
    print(" Moves: recall UP (FN down, TP up), precision DOWN (FP up), accuracy usually slightly down,")
    print(" F1 may move either way (use F2 to weight recall).")
    print(" Cost: more false alarms -> more manual review, blocked genuine cards, customer annoyance.")
    print(" Alternatives: track recall / F2 instead of accuracy; oversample fraud (SMOTE) or class weights.")

    print("\nVERIFY (second method)")
    print(f" F1 via 2TP/(2TP+FP+FN) = {f4(2 * TP / (2 * TP + FP + FN))}  (matches {f4(f1)})")


# -------------------------------------------------------------------- main
def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or not 0 <= int(sys.argv[1]) <= 9:
        sys.exit("Usage: python3 solve.py <d>   (d = last digit of enrollment number, 0-9)")
    d = int(sys.argv[1])
    print(f"DATA MINING ASSIGNMENT  --  d = {d}")
    for q in (q1, q2, q3, q4, q5):
        q(d)


if __name__ == "__main__":
    main()
