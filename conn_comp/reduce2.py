#!/usr/bin/env python
import math
import sys
import os

class reducer:
    def __init__(self):
        self.value_count = 0
        self.last_key = None

    def _fetch(self, key, val, cls=False):
        if cls == True:
            self.value_count = 0
        self.value_count += 1

    def _output(self):
        if self.value_count > 1:
            print(self.last_key)

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

