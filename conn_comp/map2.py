#!/usr/bin/env python

import os
import re
import sys
import math

def main():
    for line in sys.stdin:
        val = line.strip().replace("\n","").split("\t")
        print(val[0])
            
if __name__ == '__main__':
    main()
