#import itertools
#from string import ascii_lowercase as alphabet
#import sys
from itertools import chain

import argparse

parser = argparse.ArgumentParser(description = "Search for word ladders.")

parser.add_argument('-1', dest='start', action='store', help='Start word.', required=True)
parser.add_argument('-2', dest='goal', action='store', help='End word.', required=True)
parser.add_argument('-d', dest='dict', action='store', help='Dictionary to use.')
parser.add_argument('-s', dest='step', action='store', help='Changed letters between words', type=int, default=1)

args = parser.parse_args()

print(f"{args.start} -> {args.goal}")

def nCk(l, s):
    combs = []
    if s == 1:
        return l

    for i, c in enumerate(l[:-s + 1]):
        for sc in nCk(l[i + 1:], s - 1):
            if type(sc) is list:
                combs.append([c]+sc)
            else:
                combs.append([c]+[sc])

    return combs

def replace_all(w, r):
    if type(r) is int:
        r=[r]

    for l in r:
        w = w[:l] + "." + w[l+1:]

    return w

def candidates(root):
    cand = {}
    for br in root:
        cand[br] = {w for w in words for r in rungs if w != br and replace_all(w, r) == replace_all(br, r) }
    return cand

def printPath(alls, allg):
    for meet in alls.keys() & allg.keys():
        path = [ start ]

        t = meet
        while (t in alls and t != start):
            path.insert(1, t)
            t = alls[t]

        t = allg[meet]
        while (t in allg and t != goal):
            path.append(t)
            t = allg[t]

        path.append(goal)
        print(path)

word_len = len(args.start)
start = args.start.lower()
goal = args.goal.lower()

rungs = nCk(list(range(0, word_len)), args.step)

if args.dict is None:
    wordlist = "words"
elif args.dict == "nederlands" or args.dict == "dutch" or args.dict == "NL":
    wordlist = "nederlands"
elif args.dict == "deutsch" or args.dict == "german" or args.dict == "DE":
    wordlist = "ngerman"
else:
    wordlist = args.dict

with open('/usr/share/dict/' + wordlist, 'r') as f:
    words = f.read()

words = [x.lower() for x in words.split('\n') if len(x) == word_len]

s = { }
g = { }
alls = {}
allg = {}

s["s0"] = candidates([start])
g["s0"] = candidates([goal])

for w in s[f"s0"]:
    for c in s[f"s0"][w]:
        if not c in alls:
            alls.update({ c: w })

for w in g[f"s0"]:
    for c in g[f"s0"][w]:
        if not c in allg:
            allg.update({ c: w })

for i in range(0, 2):
    s[f"s{i + 1}"] = {}
    g[f"s{i + 1}"] = {}

    for w in g[f"s{i}"]:
        g[f"s{i + 1}"].update(candidates(g[f"s{i}"][w]))
    for w in g[f"s{i + 1}"]:
        for c in g[f"s{i + 1}"][w]:
            if not c in allg:
                allg.update({ c: w })

    if alls.keys() & allg.keys():
        printPath(alls, allg)
        exit()

    for w in s[f"s{i}"]:
        s[f"s{i + 1}"].update(candidates(s[f"s{i}"][w]))
    for w in s[f"s{i + 1}"]:
        for c in s[f"s{i + 1}"][w]:
            if not c in alls:
                alls.update({ c: w })

    if alls.keys() & allg.keys():
        printPath(alls, allg)
        exit()

