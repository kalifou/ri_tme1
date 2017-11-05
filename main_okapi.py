# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 13:03:11 2017

@author: kalifou
"""
from Index import Index
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from Okapi import Okapi

if __name__ == "__main__":
    
    parser = ParserCACM()
    textRepresenter = PorterStemmer()         
    fname = "data/cacm/cacm.txt"
    I = Index(parser,textRepresenter)
    I.indexation(fname)
    
    print 'before building okapi'
    o = Okapi(I)
    print 'okapi built'
    
    queryExample = {'techniqu' : 1, 'accelerat' : 1}
    docs = o.L.keys()
    for doc_id in docs :
        print 'doc_id : ',doc_id
        score = o.f(queryExample,doc_id)
        print "Query's score : ",score