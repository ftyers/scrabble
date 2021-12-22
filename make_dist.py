#!/usr/bin/env python3

import unicodedata
from collections import defaultdict

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

def optimize_score(tile_count, text_dist, P=190):
    score_dist = {c: [n, 1] for c, n in tile_count.items()}
    rem = P - len(score_dist)
    while rem > 0:
        mc = None
        md = 0.0
        for ch, (ct, sc) in score_dist.items():
            f = text_dist[ch]
            d = abs(ct - (sc * f * 100)) - abs(ct - ((sc + 1) * f * 100))
            d /= (sc + 1)
            #d = ct - (sc * f * 100)
            #print(ch, ct, sc, f, d)
            if not mc or d > md:
                mc = ch
                md = d
        score_dist[mc][1] += 1
        rem -= 1
        #print('max:', mc)
        #break
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
