#!/usr/bin/env python3

import unicodedata
from collections import defaultdict
import math

def tokenize(s_, digraphs):
    if not digraphs:
        yield from s_.upper()
    else:
        ls = digraphs.upper().split()
        ls.sort(key=len, reverse=True)
        i = 0
        s = s_.upper()
        while i < len(s):
            for d in ls:
                if s[i:i+len(d)] == d:
                    yield d
                    i += len(d)
                    break
            else:
                yield s[i]
                i += 1

def count(s, digraphs, lim=0.0005):
    dct = defaultdict(lambda: 0)
    N = 0
    for c in tokenize(s, digraphs):
        if len(c) > 1 or unicodedata.category(c)[0] == 'L':
            dct[c] += 1
            N += 1
    ret = {}
    for c in dct:
        d = dct[c] / N
        if d >= lim:
            ret[c] = d
    return ret

def optimize_count(text_dist, N=98):
    rem = N - len(text_dist)
    tile_dist = {c:1 for c in text_dist}
    while rem > 0:
        mc = None
        md = 0.0
        for ch in tile_dist:
            ct = tile_dist[ch]
            rc = text_dist[ch]
            d = abs((ct / N) - rc) - abs(((ct + 1) / N) - rc)
            if not mc or d > md:
                mc = ch
                md = d
        tile_dist[mc] += 1
        rem -= 1
    return tile_dist

def optimize_score(tile_count, text_dist, N=98, BUCKET_COUNT=12):
    score_dist = {ch: [ct, 1] for ch, ct in tile_count.items()}
    mxf = max(text_dist.values())
    mnf = min(text_dist.values())
    w = math.log(mxf - mnf) / math.sqrt(BUCKET_COUNT)
    for l, f in text_dist.items():
        bk = max(0, min(int((math.log(f) - math.log(mxf)) / w), BUCKET_COUNT)-1)
        score_dist[l][1] += bk
    score_dist['[blank]'] = [2,0]
    return score_dist

def table(score_dist):
    t = []
    for i in range(max(x[1] for x in score_dist.values()) + 2):
        l = []
        for j in range(max(x[0] for x in score_dist.values())+1):
            l.append([])
        t.append(l)
    for i in range(len(t)-1):
        t[i+1][0].append(str(i))
    for i in range(len(t[0])-1):
        t[0][i+1].append('×' + str(i+1))
    cols = [0]
    rows = [0]
    for ch, (ct, sc) in score_dist.items():
        t[sc+1][ct].append(ch)
        cols.append(ct)
        rows.append(sc+1)
    cols = sorted(set(cols))
    rows = sorted(set(rows))
    col_w = [0]*len(cols)
    for i, c in enumerate(cols):
        for r in rows:
            col_w[i] = max(col_w[i], len(' '.join(t[r][c])))
    for r in rows:
        l = []
        for c, w in zip(cols, col_w):
            s = ' '.join(sorted(t[r][c]))
            l.append(' '*(w-len(s)) + s)
        print('   '.join(l))

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', action='store')
    parser.add_argument('-d', '--digraph', action='store', default='')
    parser.add_argument('-t', '--tiles', type=int, default=100)
    parser.add_argument('-b', '--buckets', type=int, default=12)
    args = parser.parse_args()

    with open(args.infile) as fin:
        d = count(fin.read(), args.digraph)
        print('distribution:', d)
        t = optimize_count(d, args.tiles-2)
        print('tile count:', t)
        s = optimize_score(t, d, args.tiles-2, args.buckets)
        print('scores:', s)
        print('total score:', sum(x*y for x,y in s.values()))
        table(s)
