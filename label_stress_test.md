# Label stress test (Milestone 2)

Eight posts written to sit on my label boundaries (AI-generated, not real
posts), each classified with the definitions in the README. The point was to
find where the definitions don't give a clean answer. These posts are not in
labels.csv.

| # | Post | First pass | Clean? | What it exposed |
|---|---|---|---|---|
| 1 | "Wemby 8 blocks tonight. Unreal." | reaction | yes | Fact plus feeling, no claim beyond it |
| 2 | "Wemby 8 blocks tonight. DPOY is already locked." | analysis? hot_take? | **no** | Is a one-game stat enough support for a season claim? |
| 3 | "Heat are winning because Spo finally stopped playing two bigs together." | analysis? hot_take? | **no** | Is a rotation change a "checkable fact"? |
| 4 | "Lakers are frauds." | hot_take | yes | |
| 5 | "Lakers are frauds, 2-6 against teams over .500." | analysis | yes | |
| 6 | "LMAO the Celtics blew a 22 point lead again, this team is cooked" | reaction? analysis? | **no** | Heated tone plus a fact plus a one-word verdict |
| 7 | "Refs gave Miami 40 free throws. Rigged." | analysis | yes, after #6 | Same shape as #6 |
| 8 | "Giannis is averaging 30 since Doc's comments, the motivation is real" | analysis? reaction? | **no** | Looks like the "undefeated since X" joke format |

## What I tightened

- **#2:** `analysis` means *supported*, not *well supported*. I don't judge
  whether the fact is enough; I only check that it's there and offered as support.
  Otherwise two labellers would split on every thin-evidence post.
- **#3:** I widened "checkable fact" to name lineups, rotations, injuries and quotes,
  not only stats.
- **#6:** Tone never decides. A verdict word ("cooked", "rigged", "frauds")
  is a claim, so a fact behind it makes the post `analysis`.
- **#8:** In an "X since Y" post, if Y is a basketball cause (a coach's
  comment, a lineup change, a returning player), it's `analysis`. If Y is not
  basketball (a statue, an ad, an election), it's `reaction`.

After these changes, all eight have a single answer.
