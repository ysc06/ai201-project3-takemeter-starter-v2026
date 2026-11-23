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
BUTTONS = re.compile(r"^(Upvote|Vote|Downvote|Reply|Award|Share|-?\d+(\.\d+)?[kK]?)+$")
LINK_ONLY = re.compile(r"^\[[^\]]*\]\(https?://[^)]*\)(•\[[^\]]*\]\(https?://[^)]*\))?$")
JUNK = re.compile(r"^(Collapse video player|\d+:\d+ / \d+:\d+|\[deleted\]|\[removed\]|•?\s*\d+[smhdwy] ago|Continue this thread|View more comments|\d+ more repl(y|ies))$")
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
        if not s or LINK_ONLY.match(s) or JUNK.match(s): continue
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


# ── New-Reddit page format (no links; "•" and "5d ago" on their own lines) ──
import hashlib
AGO = re.compile(r"^(Edited )?\d+\s*(mo|min|hr|yr|[smhdwy])s? ago$")
STOP = re.compile(r"^(View more comments|Community Info Section)$")
SKIP_PLAIN = re.compile(r"^(u/\S+ avatar|\d+ more repl(y|ies)|Upvote|Downvote|Reply|Award|Share|-?\d+(\.\d+)?[kK]?|•)$")

def text_id(text):
    return "t" + hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]

def parse_plain(lines):
    L = [l.rstrip("\n") for l in lines]
    S = [l.strip() for l in L]
    n = len(S)
    def is_header(i):  # username, "•", "Nd ago"
        return i + 2 < n and S[i] and S[i + 1] == "•" and AGO.match(S[i + 2])
    posts, cur, i, head = [], [], 0, False
    if "Comments Section" in S:          # skip the thread's own post, sort bar etc.
        i = S.index("Comments Section") + 1
    def is_ad(i):                        # promoted comment: name, "•", "Ad"
        return i + 2 < n and S[i + 1] == "•" and S[i + 2] == "Ad"
    def flush():
        if cur:
            t = " / ".join(cur); posts.append({"comment_id": text_id(t), "text": t})
    while i < n:
        s = S[i]
        if STOP.match(s): break
        if is_ad(i):                     # skip the ad up to the next real comment
            flush(); cur = []; i += 3
            while i < n and not is_header(i) and not STOP.match(S[i]): i += 1
            continue
        if is_header(i):
            flush(); cur = []; i += 3
            while i + 1 < n and S[i] == "•" and AGO.match(S[i + 1]): i += 2
            head = True; continue
        if s == "Upvote":
            flush(); cur = []; head = False; i += 1; continue
        if not s or SKIP_PLAIN.match(s): i += 1; continue
        if head and (s.startswith(("emoji:", ":")) or s in TEAMS or FLAIR.match(s)
                     or (len(s.split()) <= 3 and s.split()[-1] in TEAMS)
                     or s.startswith("Profile Badge") or s.endswith("Bandwagon")):
            i += 1; continue
        head = False; cur.append(s); i += 1
    flush()
    seen, out = set(), []
    for p in posts:
        if p["text"] not in seen: seen.add(p["text"]); out.append(p)
    return out

def parse_any(path):
    lines = open(path, encoding="utf-8").readlines()
    return parse(lines) if any("/comment/" in l for l in lines) else parse_plain(lines)
