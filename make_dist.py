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
                yield s[0]
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

def optimize_score(tile_count, text_dist, N=98, P=180, M=15):
    score_dist = {ch: [ct, 1] for ch, ct in tile_count.items()}
    rem = P - len(score_dist)
    BUCKET_COUNT = 15
    mxf = max(text_dist.values())
    mnf = min(text_dist.values())
    w = math.log(mxf - mnf) / math.sqrt(BUCKET_COUNT)
    temp_buckets = []
    for i in range(BUCKET_COUNT + 1):
        temp_buckets.append([])
    for l, f in text_dist.items():
        bk = max(0, min(int((math.log(f) - math.log(mxf)) / w), BUCKET_COUNT))
        temp_buckets[bk].append(l)
        score_dist[l][1] += bk
        rem -= bk * score_dist[l][0]
    buckets = []
    for b in temp_buckets:
        if b:
            buckets.append(sorted(b, key=text_dist.get))
    while rem > 0:
        mb = None
        md = 0.0
        for b in buckets:
            d = 0.0
            for ch in b:
                ct, sc = score_dist[ch]
                f = text_dist[ch]
                d += abs(ct / N - sc * f) - abs(ct / N - (sc + 1) * f)
            d /= len(b)
            if not mb or d > md:
                mb = b
                md = d
        for ch in mb:
            score_dist[ch][1] += 1
            rem -= score_dist[ch][0]
            if rem == 0:
                break
    score_dist['[blank]'] = [2,0]
    return score_dist

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', action='store')
    parser.add_argument('-d', '--digraph', action='store', default='')
    args = parser.parse_args()

    with open(args.infile) as fin:
        d = count(fin.read(), args.digraph)
        print(d)
        t = optimize_count(d)
        print(t)
        print(sorted(t.items(), key=lambda x: x[1], reverse=True))
        s = optimize_score(t, d)
        print(s)
