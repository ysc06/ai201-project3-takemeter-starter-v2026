#!/usr/bin/env python3
"""Rebuild labels.csv from raw_posts.txt + tools/prelabels.csv.

    python tools/build_labels.py

Posts marked OUT in prelabels.csv go to excluded_posts.csv instead. Posts with
no prelabel yet are listed so they can be labelled. Prints label counts.
"""
import csv, collections, sys
sys.path.insert(0, "tools")
from parse_reddit_paste import parse

posts = parse(open("raw_posts.txt", encoding="utf-8"))
pre = {r["comment_id"]: r for r in csv.DictReader(open("tools/prelabels.csv", encoding="utf-8"))}
keep, out, todo, seen = [], [], [], set()
for p in posts:
    if p["text"] in seen: continue
    seen.add(p["text"])
    r = pre.get(p["comment_id"])
    if r is None: todo.append(p); continue
    (out if r["label"] == "OUT" else keep).append({"text": p["text"], "label": r["label"], "note": r["note"]})
with open("labels.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["text", "label", "note"]); w.writeheader(); w.writerows(keep)
with open("excluded_posts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["text", "reason"]); w.writeheader()
    w.writerows({"text": r["text"], "reason": r["note"]} for r in out)
c = collections.Counter(r["label"] for r in keep); n = len(keep)
print(f"labels.csv: {n} rows | " + ", ".join(f"{k} {v} ({v/n:.0%})" for k, v in sorted(c.items())))
print(f"excluded: {len(out)} | not yet labelled: {len(todo)}")
