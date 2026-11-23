#!/usr/bin/env python3
"""Turn text copied from a Reddit thread page into one post per row.

    python tools/parse_reddit_paste.py raw_posts.txt parsed_posts.csv

Strips usernames, timestamps, flair and the Upvote/Reply button row. Keeps the
whole post text, joining its lines with " / ". Writes text and comment_id
(from the permalink, used to drop duplicates when threads are pasted twice).
"""
import csv, re, sys

TEAMS = {"76ers","Bucks","Bulls","Cavaliers","Celtics","Clippers","Grizzlies","Hawks",
 "Heat","Hornets","Jazz","Kings","Knicks","Lakers","Magic","Mavericks","Nets","Nuggets",
 "Pacers","Pelicans","Pistons","Raptors","Rockets","Spurs","Suns","Thunder",
 "Timberwolves","Trail Blazers","Warriors","Wizards","NBA"}
USER = re.compile(r"^\[[^\]]+\]\(https?://(www\.)?reddit\.com/user/[^)]*\)$")
TIME = re.compile(r"^•?\s*\[[^\]]*ago\]\((https?://[^)]*/comment/([a-z0-9]+)/?)\)")
BUTTONS = re.compile(r"^(Upvote|Vote|Downvote|Reply|Award|Share|\d+)+$")
FLAIR = re.compile(r"^(\[[A-Z]{2,4}\].*|Top \d+% (Commenter|Poster)|.*\bFan\b.*)$")

def parse(lines):
    posts, cur, cid, in_head = [], [], None, False
    def flush():
        if cur:
            posts.append({"comment_id": cid or "", "text": " / ".join(cur)})
    for raw in lines:
        line = raw.rstrip("\n")
        s = line.strip()
        m = TIME.match(s)
        if m:
            flush(); cur, cid, in_head = [], m.group(2), True; continue
        if USER.match(s) or BUTTONS.match(s.replace(" ", "")) and s:
            if BUTTONS.match(s.replace(" ", "")): flush(); cur, cid = [], None
            continue
        if not s: continue
        if in_head and (line.startswith(" ") or s in TEAMS or FLAIR.match(s)):
            continue
        in_head = False
        cur.append(s)
    flush()
    seen, out = set(), []
    for p in posts:
        key = p["comment_id"] or p["text"]
        if key not in seen:
            seen.add(key); out.append(p)
    return out

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    posts = parse(open(src, encoding="utf-8"))
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["comment_id", "text"]); w.writeheader(); w.writerows(posts)
    print(f"{len(posts)} posts -> {dst}")
