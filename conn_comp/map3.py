#!/usr/bin/env python

import os
import re
import sys
import math

def main():
    for line in sys.stdin:
        val = line.strip().replace("\n","").split("\t")
        print '%s\t%s\t%s\t%s' % (val[0], val[1], val[2], "left")
        print '%s\t%s\t%s\t%s' % (val[1], val[0], val[2], "right")
if __name__ == '__main__':
    main()
