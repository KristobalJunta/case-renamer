#!/usr/bin/env python3

import sys
import re


class Line:
    lnum = 0
    lcont = ''

    def __init__(self, lnum, lcont):
        self.lnum = lnum
        self.lcont = lcont


if len(sys.argv) < 2:
    print("Specify file name")
    exit(1)

fname = sys.argv[1]
f = open(fname)
lines = []
ln = 0
for line in f.readlines():
    lines.append(Line(ln, line))
    ln += 1
f.close()

caselines = list(filter(lambda s: 'case' in s.lcont, lines))
initlines = list(filter(lambda s: 'initcreate' in s.lcont, lines))
nextlines = list(filter(lambda s: 'next' in s.lcont, lines))

casenum = 1
newlines = lines

for c in caselines:
    oldnum = re.search('\d+', c.lcont)[0]

    nl = re.sub('\d+', str(casenum), c.lcont)
    newlines[c.lnum] = Line(c.lnum, nl)

    oldinit = list(filter(lambda s: oldnum in s.lcont, initlines))
    oldnext = list(filter(lambda s: oldnum in s.lcont, nextlines))

    for l in oldinit:
        nl = re.sub('\d+', str(casenum), l.lcont)
        newlines[l.lnum] = Line(l.lnum, nl)
    for l in oldnext:
        nl = re.sub('\d+', str(casenum), l.lcont)
        newlines[l.lnum] = Line(l.lnum, nl)

    casenum += 1

newfname = fname+'.new.cpp'
nf = open(newfname, 'w')
nf.write("".join(list(map(lambda s: s.lcont, newlines))))
nf.close()
