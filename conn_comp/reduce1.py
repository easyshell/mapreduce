#!/usr/bin/env python
import math
import sys
import os

class reducer:
    def __init__(self):
        self.belong = None
        self.last_key = None
        self.next_set_tag = None
        self.contact = set()
    
    def _next_set_tag(self, set_tag):
        set_tag = set_tag.split("-")
        next_round = int(set_tag[1]) + 1
        return str(set_tag[0]) + "-" + str(next_round)

    def _fetch(self, key, val, cls=False):
        if cls == True:
            self.contact = set()
            self.belong = None
        if not self.belong:
            self.belong = int(val[0])
        else:
            self.belong = min(self.belong, int(val[0]))
        self.contact.add(val[0])
        if val[-1].startswith("set"):
            self.next_set_tag = self._next_set_tag(val[-1])

    def _output(self):
        if not self.next_set_tag:
            self.next_set_tag = "set-1" 
        if int(self.last_key) > int(self.belong):
            self.contact.add(self.last_key)
            for rela in self.contact:
                if int(rela) != int(self.belong):
                    print '%s\t%s\t%s' % (rela, self.belong, self.next_set_tag)
        else:
            for rela in self.contact:
                print '%s\t%s\t%s' % (rela, self.last_key, self.next_set_tag)

    def reduce(self):
        for line in sys.stdin:
            tokens = line.replace("\n", "").split("\t")
            key = tokens[0]
            val = tokens[1:]
            if self.last_key and key != self.last_key:
                self._output()
                self._fetch(key, val, cls=True)
            else:
                self._fetch(key, val)
            self.last_key = key
        if self.last_key:
            self._output()

def main():
    rd = reducer()
    rd.reduce()

if __name__ == '__main__':
    main()

