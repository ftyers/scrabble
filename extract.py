#!/usr/bin/env python3

import json

def get_lang(line):
    ls = line[2:].strip().split()
    if len(ls) == 3 and ls[1] == 'letter' and ls[2] == 'distribution':
        skip = ['Písmenkovka', 'Scalaparola', 'Scarabeo', 'Alfapet']
        if ls[0] not in skip:
            return ls[0]
    elif ls[0] == 'English' and '(Super)' not in ls:
        return ls[0]
    elif ls[0] == 'Spanish':
        return ls[0] + ' ' + ' '.join(ls[3:])
    elif len(ls) == 4:
        special = [('Dutch', '#1'), ('Hebrew', '#4'), ('Latin', '(Cambridge)'), ('Slovak', '(official)')]
        if (ls[0], ls[3]) in special:
            return ls[0]
    return None

data = {}
lang = None
score = -1
dist = []

with open('Scrabble_letter_distributions') as fin:
    for line in fin:
        if line.strip() == '==Unofficial editions==':
            break
        elif line.startswith('|+'):
            lang = get_lang(line)
            if lang:
                data[lang] = {}
        elif lang and line.startswith('!'):
            if '!!' in line:
                dist = []
                for m in line.split('!!')[1:]:
                    dist.append(int(m.strip().strip('×')))
            else:
                score = int(line[1:].strip())
        elif lang and line.startswith('|') and '||' in line:
            for ls, c in zip(line.split('||')[1:], dist):
                for l in ls.strip().split():
                    data[lang][l] = {'score': score, 'count': c}

print(json.dumps(data))
print(len(data))
print(list(data.keys()))
