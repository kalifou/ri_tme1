# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 13:03:11 2017

@author: kalifou
"""
from Index import Index
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from IRmodel import Okapi
from EvalMeasure import EvalIRModel

if __name__ == "__main__":
    
# This code is running but I need to check the results
    
#    parser = ParserCACM()
#    textRepresenter = PorterStemmer()         
#    fname = "data/cacm/cacm.txt"
#    I = Index(parser,textRepresenter)
#    I.indexation(fname)
#    
#    print 'before building okapi'
#    o = Okapi(I)
#    print 'okapi built'
#    
#    queryExample = {'techniqu' : 1, 'accelerat' : 1}
#    
#    scores = o.getRanking(query=queryExample)
#    print "Docs's ranking : ",scores
    
##########################################################
# This eval gives poor results : I will investigate a bit later
    fname = "data/cacm/cacm.txt"
    query_file = "data/cacm/cacm.qry"
    relevance_file = "data/cacm/cacm.rel"
    
    type = "Okapi"
    eval_platform = EvalIRModel(fname,query_file,relevance_file,type=type)
    eval_platform.eval()
    