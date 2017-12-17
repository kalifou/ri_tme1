# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 17:24:32 2017

@author: kalifou
"""
from IRmodel import Okapi
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
import sys
import os
import pickle
from RandomWalk import *

if __name__ == "__main__":
    index = None
    
    d = 0.6
    fname = "data/cacm/cacm.txt"
    
    sys.stdout.write("Indexing database...")
    sys.stdout.flush()
    if os.path.isfile('Index.p'):
       I = pickle.load( open( "Index.p", "rb" ) ) 
    
    else:
        parser = ParserCACM()
        textRepresenter = PorterStemmer()
        I = Index(parser,textRepresenter)
        I.indexation(fname)
        I.parser = None
        pickle.dump( I, open( "Index.p", "wb" ) )
    
    # Getting Matrices of Predecessors, Successors, Index & Inv code, Nb Pages 
    
#
#    P, Succ, Index_P, Counter_Index_P, N_pgs = pr.get_Pre_Succ(I)
#    # Getting the incidence Matrix A
#    A = pr.get_A(P, Succ)    
#    
#    print "Number of pages :", N_pgs 
#    print "Starting PageRank..."   
#          
#    #pr = PageRank(N_pgs, d) 
#    pr.randomWalk(A)
#    mu = pr.get_mu()
#    
#    hts = Hits(N_pgs,N_iters=100)
#    hts.randomWalk(A, P, Succ, Index_P, Counter_Index_P)
#    
#    print "MAX mu ",max(mu)    
#    print "MAX a ",max(hts.get_a())
    
    #### Graph relevant to query
    n=1000
    K = 10
    q = None
    o = Okapi(I)
    queryExample = {'techniqu' : 1, 'accelerat' : 1}
    P, Succ, Index_P, Counter_Index_P, N_pgs = select_G_q(n, K, queryExample, o, I)
    pr = PageRank(N_pgs, d) 
    A = get_A(P, Succ,N_pgs)  
    print P
    pr.randomWalk(A)
    mu = pr.get_result(Counter_Index_P)
    print "MAX mu ",max(mu)  
#    print "Npages",N_pgs,pr.N_pages
#    print "Random walk for HITS"
#    hts = Hits(N_pgs,N_iters=100)
#    hts.randomWalk(A, P, Succ, Index_P, Counter_Index_P)
#    a = hts.get_result(Counter_Index_P)
#    print a