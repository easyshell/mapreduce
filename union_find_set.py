import os
import sys
import math
import copy
import numpy
import logging
import logging.config
import logging.handlers
from operator import itemgetter, attrgetter

formatter = logging.Formatter('%(asctime)s - %(levelname)s: - %(message)s')
log_rank_progress = logging.getLogger('rank_progress')
handle_rank_progress = logging.FileHandler('rank_progress.txt', 'w')
handle_rank_progress.setFormatter(formatter)
log_rank_progress.addHandler(handle_rank_progress)
log_rank_progress.setLevel(logging.INFO)

log_rank_record = logging.getLogger('rank_record')
handler_rank_record = logging.FileHandler('rank_record.txt', 'w')
handler_rank_record.setFormatter(formatter)
log_rank_record.addHandler(handler_rank_record)
log_rank_record.setLevel(logging.INFO)

class union_find:
    def __init__(self, input_file, max_node_count=7500000):
        self.input_file = input_file
        self.node_count = 0
        self.url2id = {}
        self.id2url = {}
        self.union_find_set = range(max_node_count)
        self._build_union_find_set()
     
    def _get_node_count(self):
        return self.node_count

    def _id2url(self, idx):
        return self.id2url[idx]

    def _belong_find(self, idx):
        if self.union_find_set[idx] == idx:
            return idx
        root = self._belong_find(self.union_find_set[idx])
        self.union_find_set[idx] = root
        return root

    def _merge(self, ida, idb):
        idar = self._belong_find(ida); idbr = self._belong_find(idb)
        #print "%d\t%d\n" % (idar, idbr)
        if (idar != idbr):
            self.union_find_set[idar] = idbr

    def _build_union_find_set(self):
        with open(self.input_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n','').split('\t')
                url1 = line[0]; url2 = line[1]
                if not url1 in self.url2id:
                    self.url2id[url1] = self.node_count
                    self.id2url[self.node_count] = url1
                    self.node_count += 1
                if not url2 in self.url2id:
                    self.url2id[url2] = self.node_count
                    self.id2url[self.node_count] = url2
                    self.node_count += 1
                id1 = self.url2id[url1]; id2 = self.url2id[url2]
                self._merge(id1, id2)
            f.close()
            
    def print_alongs(self, outdir="/home/kimi/kimi/unicom_component/output"):
        for i in range(0, self.node_count):
            rooti = self._belong_find(i)
            with open(outdir+"/"+str(rooti), 'ab') as f:
                f.write(self._id2url(i)+"\n")
                f.close()
        
def main():
    weibo_file = "/home/kimi/kimi/unicom_component/weibo.500" 
    uf = union_find(weibo_file)
    uf.print_alongs()

if __name__ == '__main__':
    main()
