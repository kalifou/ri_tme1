# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 22:32:40 2017

@author: kalifou
"""
import numpy as np

class RandomWalk(object):
    def __init__(self,index):
        self.index = index

    def randomWalk(self):
        raise NotImplementedError('Always abstract class') 
    
class PageRank(object):
    def __init__(self,index,N_pages,d,P,L):
        """
        d : proba to randomly click on a link/page
        N_pages : Number of Web pages
        index : contains 
        P : {j from V | j->i  from E}
        L : { }
        """
        self.index = index
        self.d = d
        self.N_pages = N_pages
        self.N_iters = 1e-2   
        self.P = P
        self.L = L
        
    def randomWalk(self):
        
        self.mu = {p:1./self.N_pages for p in self.P}        
        current_page = self.P.values()[0] # Start from the first page        
        self.A = np.zeros((self.N_pages,self.N_pages))
        
        for t in range(1,self.N_iters):

            self.mu[t] = (1.-self.d)/self.N_pages + \
                        self.d * self.mu[t-1]*1. # * self.A
            current_page = None #random_shot() to get p_t+1
    