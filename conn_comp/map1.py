#!/usr/bin/env python

import os
import re
import sys
import math

def main():
    bothway = os.environ.get('bothway')
    for line in sys.stdin:
        val = line.strip().replace("\n","").split("\t")
        print line.strip().replace("\n", "")
        if bothway == "True":
            if (len(val) == 2):
                rev = [val[1], val[0]]
                print '%s\t%s' % (rev[0], rev[1])
            else:
                rev = [val[1], val[0], val[2]]
                print '%s\t%s\t%s' % (rev[0], rev[1], rev[2])
            
if __name__ == '__main__':
    main()
