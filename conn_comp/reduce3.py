#!/usr/bin/env python
import math
import sys
import os

class reducer:
    def __init__(self):
        self.has_left = False
        self.has_right = False
        self.last_key = None
        self.next_set_tag = None
        self.contact = set()
    
    def _fetch(self, key, val, cls=False):
        #print(val)
        if cls == True:
            self.contact = set()
            self.has_left = False
            self.has_right = False
            self.next_set_tag = None
        if val[-1] == "left":
            self.has_left = True
        if val[-1] == "right":
            self.has_right = True
        self.contact.add(val[0])
        self.next_set_tag = val[1]
    def _output(self):
        if self.has_left and self.has_right:
            for ele in self.contact:
                print '%s\t%s\t%s' % (self.last_key, ele, self.next_set_tag)

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

