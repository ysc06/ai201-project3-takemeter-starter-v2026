# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

Overall accuracy on the held-out test split is at least **0.65** on every one of the three seeds (42, 7, 2024).

**Why this target:** I plan to keep each label between 25% and 40% of the file, so always guessing the biggest label scores about 0.40. The test split is only about 30 posts, so each post is worth about 3 points of accuracy. 0.65 means getting about 20 of 30 right, which is clearly better than guessing without assuming a DistilBERT trained on about 140 posts will be great. It has to hold on the worst of three seeds, which is why it isn't 0.75.

---

## 2.

Per-label F1 on the test split, every seed: `hot_take` and `reaction` at least **0.60**, `analysis` at least **0.50**.

**Why this target:** `analysis` will be my smallest label. In my reading it was only about 1 post in 8, so even with targeted collection I expect about 8 to 10 of them in the test split, and one post flipping moves its F1 by about 0.1. It also sits on my hardest boundary (a fact in a heated or joking post), so I expect the model to confuse it with `reaction`. The two bigger labels get the stricter bar.

---

## 3.

In `labels.csv`, no label is more than **40%** of the rows and no label is less than **25%**.

**Why this target:** Left to natural rates, r/nba would give me mostly jokes and hype, with `analysis` around 12%. The course's 70% cap would allow a nearly empty label. 25% of 200 rows is 50 `analysis` posts, about 8 in the test split. The notebook calls that the minimum it can measure, so going lower would make criterion 2 untestable.

---

## 4.

When I label the 30 staff posts under the staff taxonomy, `agreement.py` reports agreement of at least **0.70** (21 of 30).

**Why this target:** The staff set was built with deliberately ambiguous posts, and it uses someone else's wording, close to mine but not the same. Three labels by chance would agree about a third of the time. 21 of 30 says I apply a written rule consistently, and it allows for about one post in three being honestly arguable. Below that, I'd suspect my own 200 labels are inconsistent too.

---

## 5.

On every seed, accuracy on the model's most confident third of test predictions is at least **0.15** higher than on its least confident third (`accuracy_most_confident_third` minus `accuracy_least_confident_third` in results.json).

**Why this target:** The use case is triage: trust the confident calls and check the unsure ones by hand. That only works if confidence means something. With about 10 posts per third, one post is 0.10, so 0.15 is the smallest gap that's more than a single lucky post. I expect unsure predictions to cluster on the `analysis`/`reaction` boundary.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
