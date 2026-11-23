# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter reads comments from r/nba, Reddit's main NBA discussion community, and sorts each one into `analysis`, `hot_take` or `reaction`. An `analysis` post backs a claim with a checkable fact. A `hot_take` argues, compares or predicts with nothing checkable behind it. A `reaction` is a cheer, vent or joke about the moment. The point is to separate the comments that bring evidence from the much larger volume of confident takes and noise. In my reading, about one post in eight was `analysis`.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:** A claim about basketball backed by at least one specific, checkable fact (a stat, a record, a standing, a named result, a lineup or injury status, or a quote) offered as support for the claim.

**Example 1:**
> Absolutely hilarious to me that Miami are now tied for fourth in the east after the entire internet said they were done one week into a six month long 82 game season.

**Example 2:**
> Good game, we are definitely missing Duren. Our paint defense is so weak right now, all we can do is foul lol

### `hot_take`

**Definition:** A claim about basketball that goes past a bare verdict (it gives a reason, compares, ranks or predicts) but offers no checkable fact behind it.

**Example 1:**
> For real, i dont like the heat but i respect spo a TON! No way he doesn't adjust some stuff

**Example 2:**
> Giannis looking quite smart and great on defense, contrary to everything the idiots on this sub have been saying. No one feels embarassed to side with Glenn Rivers?

### `reaction`

**Definition:** An immediate cheer, vent, joke or bare verdict about the game or moment ("refs are garbage", "Kat is that guy") with no reason, comparison or prediction attached.

**Example 1:**
> LFG KNICKS BABY!!!!!!!

**Example 2:**
> Heat Culture is back baby

### Out of scope

Posts about the subreddit itself, the broadcast, the schedule or the mods, and replies that mean nothing without the comment above them (like "7-2*" or "I feel the same about Mazzulla."), are not collected. They were about a third of my reading, and the model only ever sees one post at a time.

### The hardest boundary

**Which two labels:** `analysis` and `reaction`. A post quotes a real number in an excited or joking tone, for example "70 total FTs is crazy work. GG Pistons I hope next time we see each other both teams are fully healthy."

**The decision rule I used every time:**
A fact makes a post `analysis` only if it supports a claim that goes past the fact itself: why something happened, what it means, or what comes next. A post that states a fact and only reacts to it ("crazy", "lmao", "GG") is `reaction`, and so is a number inside a joke with a non-basketball cause ("6-2 since fixing the Wade statue"). Tone never decides: "blew a 22 point lead again, this team is cooked" is `analysis`, because "cooked" is a claim and the blown lead supports it. `analysis` means supported, not right. A one-game stat behind a season-long claim still counts.

Under this rule, "70 total FTs is crazy work" is `reaction`, and the Duren post is `analysis`, because it uses the missing player to explain the loss.

**The second boundary, `hot_take` vs `reaction`**, showed up while labelling, not in the stress test. Ref complaints and hype like "Refs totally ruined the game" or "This team is clutch asff" fit both definitions as first written. The rule: a bare verdict shouted about the moment is `reaction`. Once it adds a reason ("That's not a foul. Where is jakobe supposed to put his feet."), a comparison, a ranking or a prediction ("Raps have no idea who to go to when they need a bucket. No closer."), it's `hot_take`. A description of a disputed play ("he was standing still") is a reason, not a checkable fact, because fans watching the same replay disagree on it.

The stress test that shaped these rules is in [label_stress_test.md](label_stress_test.md).


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Comments copied by hand from three public r/nba threads in November 2026: a Heat discussion thread after their early-season turnaround, the Knicks–Raptors post-game and late-game thread (a close game decided by a disputed flagrant foul), and a thread about Klay Thompson's preseason shooting (7/26 FG, 3/20 from three). The Klay thread was chosen on purpose because the first two were short on `analysis`. A script (`tools/parse_reddit_paste.py`) strips usernames, timestamps, flair and buttons, and keeps every post whole. Usernames are not stored in the repo.

279 posts were collected. 70 were left out as out of scope, each with its reason in `excluded_posts.csv`: replies that mean nothing without the comment above them, questions, posts about the subreddit or other fans, a chain of song-lyric quotes, NFL talk and one near-duplicate. That leaves 209 rows.

**How I labelled them:** Every row was pre-labelled by Claude using the definitions and decision rules above. The note column says so on every row, and marks 22 rows `HARD` with the reason. **I did not do the 20-post cold pass**, so no rows are marked `cold`. 20 randomly drawn posts are in `cold_labels.csv`, still unlabelled. I have also not yet read and corrected every pre-label. Until I do, these labels measure Claude's reading of my rules, not mine.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `analysis` | 34 | 16% |
| `hot_take` | 82 | 39% |
| `reaction` | 93 | 44% |
| **Total** | 209 | 100% |

`analysis` is below the 25% floor in my criterion 3. I left it there rather than inventing posts or cutting real ones to hit the number. Even the stats thread was only about 30% `analysis`, which is itself a finding about this community.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "It's only the preseason, but 3/20 is crazy from arguably the 2nd best shooter of all time"
>
> *Could have been:* `analysis` or `reaction`
>
> *I chose, because:* `reaction`. The stat is real, but the post only reacts to it ("crazy"). It doesn't use the number to argue anything beyond the number. This is the same call as "70 total FTs is crazy work" from my reading.

**2.**
> *The post:* "Anyone remember that time the Knicks fleeced the Raptors in a trade and then curb stomped them 15 times in a row?"
>
> *Could have been:* `reaction` or `analysis`
>
> *I chose, because:* `analysis`. It reads like trash talk, but "fleeced" is a claim and the 15-game streak is a checkable fact offered for it. My rule says tone never decides.

**3.**
> *The post:* "Knicks would've won regardless but cmon man no way you think someone should get a flagrant for standing still while contesting"
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* `hot_take`. "Standing still" sounds like a fact, but it's a description of a disputed play: in the same thread, fans watching the same replay said he moved his foot. A checkable fact has to be something two people looking it up would agree on.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42. Trained on Apple Silicon (`mps`, torch 2.14.1), which `results.json` records.

**Anything I changed from the defaults, and why:** Nothing.

**Split sizes:** 145 train / 32 val / 32 test. The test split has 5 `analysis`, 13 `hot_take` and 14 `reaction`. **`analysis` has fewer than 8 test examples**, so its per-label score is decided by a handful of posts and will swing between seeds. That traces straight back to it being 16% of the file.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

Most of this unit was done by Claude, at my request. Claude drafted the Milestone 1 reading notes from posts I pasted, and wrote the label definitions, the decision rules, all five criteria in `criteria.md`, the stress test, the parsing scripts and most of this README. I copied the Reddit threads myself and ran the notebook myself.

**Moment 1**

- *What I asked for:* Eight posts written to sit on the label boundaries, then classified with the definitions (`label_stress_test.md`).
- *What came back:* Four of the eight didn't classify cleanly, for example "Wemby 8 blocks tonight. DPOY is already locked." and "LMAO the Celtics blew a 22 point lead again, this team is cooked".
- *What I changed:* `analysis` now means *supported*, not *well supported*. Tone never decides. Lineups, injuries and quotes count as facts. An "X since Y" post is `analysis` only when Y is a basketball cause.

**Moment 2**

- *What I asked for:* Pre-labels for the Knicks–Raptors thread.
- *What came back:* Ref complaints like "Refs totally ruined the game" and hype like "This team is clutch asff" fit both `hot_take` and `reaction` as the definitions were first written.
- *What I changed:* I added a second decision rule. A bare verdict about the moment is `reaction`, and a reason, comparison, ranking or prediction makes it `hot_take`. I updated the `hot_take` and `reaction` definitions here and in `label_definitions.txt` to match.

**Pre-labelling disclosure:** All 209 labels in `labels.csv` are Claude's pre-labels, and every row's note says so. I did not do the 20-post cold pass. I have not yet read and corrected each pre-label.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

Written before the baseline was run: the trained model will beat the zero-shot baseline on `reaction`, because ref vents and hype are short, repetitive and well represented in training, but lose to it on `analysis`, which the trained model never predicted on any seed, while the baseline at least reads the phrase "checkable fact" in the definition.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.625 | 0.750 | 0.562 | MISSED |
| 2. Per-label F1 (`analysis` ≥ 0.50; others ≥ 0.60) | see target | a 0.00 · h 0.56 · r 0.76 | a 0.00 · h 0.73 · r 0.90 | a 0.00 · h 0.61 · r 0.61 | MISSED |
| 3. Every label 25–40% of labels.csv | 25–40% | a 16% · h 39% · r 44% | same file | same file | MISSED |
| 4. Staff agreement | ≥ 0.70 | 1.00 (30/30) | not seed-dependent | not seed-dependent | MET |
| 5. Confident third beats unsure third by | ≥ 0.15 | +0.40 | +0.40 | +0.20 | MET |

Macro F1 was 0.442 / 0.543 / 0.407. Accuracy spread across seeds is **0.19**, nearly twice the 10-point line where a dataset is too small or lopsided for a stable measure. All three runs were on Apple Silicon (`mps`, torch 2.14.1).

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42 (the one section 7 prints):

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 0 | 4 | 1 |
| **hot_take** | 0 | 7 | 6 |
| **reaction** | 0 | 1 | 13 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

6 real `hot_take` posts were called `reaction`, and only 1 went the other way. On this seed the model treats any short opinion about the game as a vent, so it hasn't learned my second rule (a reason or comparison makes it a `hot_take`). The bigger story is the empty first column: the model never predicted `analysis` on any seed. Across all three seeds, 14 of the 15 real `analysis` posts were called `hot_take`.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.65 | MISSED | Seed 2024 (0.562) and seed 42 (0.625) are under; only seed 7 clears it. It has to hold on all three. |
| 2 | Per-label F1 | `analysis` ≥ 0.50, others ≥ 0.60 | MISSED | `analysis` is 0.00 on every seed, against a 0.50 target. `hot_take` also misses on seed 42 (0.56). `reaction` clears 0.60 on all three. |
| 3 | Balance | each label 25–40% | MISSED | `analysis` 16% and `reaction` 44%. This is a property of the file, so it's the same on every seed. |
| 4 | Staff agreement | ≥ 0.70 | MET | 30/30 by `agreement.py`, including all 7 posts staff marked hard. The labeller here is Claude, the same one who pre-labelled `labels.csv`. |
| 5 | Confidence gap | ≥ +0.15 | MET | +0.40, +0.40, +0.20. A generous reading is possible: each third is 10 posts, so seed 2024's gap is two posts. The model's mean confidence is also only 0.41–0.46 against 0.33 for a pure guess, so "confident" here means only slightly less unsure. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criterion 2: `analysis` F1 is 0.00. Cause: too few examples, plus a model that barely trained.** `analysis` is 34 of 209 rows, about 24 in training and 5 in each test split. The model's `analysis` column is empty on all three seeds, so it isn't confusing `analysis` with something else, it has simply never learned to say it. Mean confidence sits at 0.41–0.46, barely above the 0.33 of a three-way guess. With 145 training posts, batch size 16 and 3 epochs, the model gets about 30 weight updates, which isn't enough to pull a minority label out of the majority ones. When `analysis` posts go wrong they go to `hot_take` (14 of 15). That is the pair my definitions separate by one thing only, whether a checkable fact is present.

Is it a labelling problem instead? The agreement check says probably not. The same labeller scored 30/30 against staff, including all 7 deliberately hard posts, so the boundary isn't being applied two different ways. What the check did show is that my `analysis` rule is looser than staff's: mine admits weak, decorative facts, theirs requires the fact to carry the argument. That makes `analysis` vs `hot_take` a **genuinely hard pair** in my taxonomy, on top of the thin label. Caveat: every row in `labels.csv` and all 30 staff labels were labelled by Claude, so this is evidence about that labeller, not about my own labelling.

**Criterion 1: accuracy. Cause: mostly the same thin label.** The 5 `analysis` posts are guaranteed misses on every seed, which costs 0.16 of accuracy on 32 posts before anything else goes wrong. On the other 27 posts the model got 20, 24 and 18 right (0.74, 0.89, 0.67). The 0.19 spread across seeds says a 32-post test split is too small to measure this precisely.

**Criterion 3: balance. Cause: collection, not the model.** r/nba's natural rate of `analysis` is low. Even the stats thread I chose to fix it was about 30% `analysis`. I didn't trim real posts or invent new ones to hit the number.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

My 30 labels are in `my_staff_labels.csv`, saved before seeing the key. They were written by Claude under `data/staff_taxonomy.md`, and Claude also pre-labelled `labels.csv`, so this rate measures the labeller of my dataset.

**Agreement rate:** 30 / 30 = 100%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

None. That includes all 7 posts staff marked `HARD` (sp_005, sp_010, sp_014, sp_019, sp_020, sp_028, sp_029). The two traps were labelled the way staff did. On sp_014 ("Times are down about 3% since the shoe rules changed, so obviously…") the number is decoration, so it's `hot_take`. On sp_028 ("Third DNF this year…") the count is something the writer reports about themselves, not argues from, so it's `reaction`.

**Was the set easy, or is the rule tight?** Partly easy. The 30 posts fall in clean blocks of ten per label, and most of the non-`HARD` posts sit far from any boundary. The 7 hard ones are the real test, and 7 of 7 is good evidence the labeller applies a written rule consistently. That labeller is Claude, which also pre-labelled every row of `labels.csv`.

**What the pattern in my disagreements tells me:**

There are no disagreements to sort into piles (a), (b) or (c). What the check does tell me comes from comparing the two rulebooks, and it matters for the diagnosis:

1. **My labels are probably not inconsistent.** The same labeller applied a stricter written rule perfectly on the posts chosen to trip it up. So "I applied a boundary two ways" is the least likely cause of my `analysis` miss.
2. **Staff rule 1 is stricter than my `analysis` rule.** Staff require the fact to be *load-bearing*. Mine says `analysis` means *supported, not well supported* (stress test, case #2). Under staff rules, some of my `analysis` rows would be `hot_take` with a number in them. "We blew out Detriot and the Rockets. We are rounding into contention mode" is one example. Those rows look almost exactly like `hot_take` posts, and that is the direction the model got wrong 14 times out of 15. My looser rule made `analysis` vs `hot_take` a genuinely hard pair for a model to learn: the only signal is "a fact is somewhere in the post," and it gets that signal from about 24 training examples.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
