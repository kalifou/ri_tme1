# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 22:32:40 2017

@author: kalifou
"""
import numpy as np
from Index import *
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer


class RandomWalk(object):
    def __init__(self,index):
        self.index = index

    def randomWalk(self):
        raise NotImplementedError('Always abstract class') 
    
class PageRank(object):
    
    def __init__(self,index, N_pages, d, P):
        """
        d : proba to randomly click on a link/page
        N_pages : Number of Web pages
        index : contains 
        P : {j from V | j->i  from E}
        """
        self.index = index
        self.d = d
        self.N_pages = N_pages
        self.P = P
        self.mu =  None
        self.eps = 1e-4
        
    def randomWalk(self, A):
        
        self.mu = np.zeros((self.N_pages,1)) + 1./self.N_pages 
        # indices : position dans la le graphe        
        
        print 'mu', self.mu
        sum = 1.
        cpt=0
        while(sum > self.eps):
            prec = self.mu
            self.mu = ((1.-self.d)/self.N_pages) + self.d * np.dot(A,self.mu )
            print self.mu
            sum = np.sum(abs(self.mu-prec))
            print "sum",sum
            print cpt
            cpt+=1
            
    def get_mu(self):
        return self.mu
        
        
    def create_graph(index):
        N_pgs = 0.
        A = np.random.rand(N_pgs,N_pgs)
        P = None
        
        return A,P

class Hits(object):
    def __init__(self,index, N_pages, d, P):
        pass
        
    def randomWalk(self, A):
        pass        
        
if __name__ == "__main__":
    index = None
    
    d = 0.6
    
    ## Constructing the graph!
    print "Building Index..."
    parser = ParserCACM()
    textRepresenter = PorterStemmer() 
    fname = "data/cacm/cacm.txt"
    I = Index(parser,textRepresenter)
    I.indexation(fname)
    
    Docs = I.docs
    Docs_id = Docs.keys()
    N_pgs = len(Docs_id)
    Index_P = { id:idx for idx,id in enumerate(Docs_id)}
    Counter_Index_P = { idx:id for idx,id in enumerate(Docs_id)}
    
    print "Building Pi..."
    Succ = { Index_P[p]:(I.getLinksForDoc(p),len(I.getLinksForDoc(p))) for p in Docs_id }
    P = {}
    for e in Succ:
        succ_e,l_e = Succ[e]
        for s in succ_e:    
            if Index_P.get(s,"Unknown_Doc_id") not in P:
                P[Index_P.get(s,"Unknown_Doc_id")] = []
            P[Index_P.get(s,"Unknown_Doc_id")].append(e)
        
    print "Building Matrix A..."
    A = np.zeros((N_pgs,N_pgs))
    for i in range(N_pgs):
        for j in range(N_pgs):
            Pi= P.get(i,[])
            Succ_j,lj = Succ[j] 
            
            if lj==0:  #j is isolated
                A[i][j] = 1./N_pgs
                
            elif j in Pi: # j precedes i
                A[i][j] = 1./lj
                
            else : # j & i are not connected
                A[i][j] = 0.
    
    print "Starting PageRank..."   
    print "Number of pages :", N_pgs       
    pr = PageRank(I, N_pgs, d, P) 
    pr.randomWalk(A)
    mu = pr.get_mu()
    print mu
    
    