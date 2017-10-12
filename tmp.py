# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:33:04 2017

@author: kalifou
"""

s= '(1:2);(2:2);(2:3);'
import numpy as np
def dict_from_string(str):
    t = str[:-1].split(';')
    d = {}
    for e in t:
        [id,freq] = e[1:-1].split(':')
        d[int(id)] = int(freq)
    return d

#q = dict_from_string(s)
#print len(q),q.



q = {1:2,2:3,3:4}
print q, dict((k, 1 + np.log(v)) for k,v in q.items())