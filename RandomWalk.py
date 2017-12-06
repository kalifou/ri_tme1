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
    
class PageRank(RandomWalk):
    
    def __init__(self,N_pages, d):
        """
        d : proba to randomly click on a link/page
        N_pages : Number of Web pages
        index : contains 
        P : {j from V | j->i  from E}
        """
        self.d = d
        self.N_pages = N_pages
        self.eps = 1e-5
        
    def randomWalk(self, A):
        
        self.mu = np.zeros((self.N_pages,1)) + 1./self.N_pages 
        # indices : position dans la le graphe        
        
        sum = 1.
        cpt=0
        while(sum > self.eps):
            prec = self.mu
            self.mu = ((1.-self.d)/self.N_pages) + self.d * np.dot(A,self.mu )
            sum = np.sum(abs(self.mu-prec))
            print "Step : ",cpt,", Sum of abs. error (mu) : ",sum
            cpt+=1
        print "...Converged!"
    def get_mu(self):
        return self.mu

class Hits(RandomWalk):
    def __init__(self,N_pages):
        self.N_pages = N_pages
        
    def randomWalk(self, A):
        self.a = np.zeros((self.N_pages,1)) + 1./self.N_pages 
        self.h = np.zeros((self.N_pages,1)) + 1./self.N_pages 
              

def get_Pre_Succ(I):
    """returns Succ & Prec"""
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
    return P,Succ,Index_P,Counter_Index_P,N_pgs
    
def get_A(P,Succ):
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
    return A
    
if __name__ == "__main__":
    index = None
    
    d = 0.6
    print "Building Index..."
    parser = ParserCACM()
    textRepresenter = PorterStemmer() 
    fname = "data/cacm/cacm.txt"
    I = Index(parser,textRepresenter)
    I.indexation(fname)
    
    # Getting Matrices of Predecessors, Successors, Index & Inv code, Nb Pages 
    P, Succ, Index_P, Counter_Index_P, N_pgs = get_Pre_Succ(I)
    # Getting the incidence Matrix A
    A = get_A(P, Succ)    
    
    print "Starting PageRank..."   
    print "Number of pages :", N_pgs       
    pr = PageRank(N_pgs, d) 
    pr.randomWalk(A)
    mu = pr.get_mu()
    
    