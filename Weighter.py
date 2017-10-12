# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:18:29 2017

@author: kalifou
"""
#import Index
import numpy as np

    
class Weighter(object):
    """Class """
    def __init__(self,index):
        self.index = index
        self.N = len(self.index.docs)        
        
    def getDocWeightsForDoc(self,idDoc):
        """returning the stem present in doc with associated freq """
        pass
    def getDocWeightsForStem(self,stem):
        """returning the docs where stem is present with associated freq """
        pass
    def getWeightsForQuery(self,query):        
        """Returning a dictionnary of present keys valued to 1 """  
        pass
    def idf_term(self,t):
        """getting the inverse doc freq for each term of the query""" 
        v = self.index.getTfsForStem(t)    
        N_t = float(len(v))
        return np.log(self.N / N_t)
        
    def idf_query(self,query):
        """getting the inverse doc freq for each term of the query"""        
        w = dict()
        for t in query.keys():            
            w[t] = self.idf_term(t)
    
class Binary(Weighter):
    
    def getDocWeightsForDoc(self,idDoc):        
        return self.index.getTfsForDoc(idDoc)
        
    def getDocWeightsForStem(self,stem):        
        return self.index.getTfsForStem(stem)
        
    def getWeightsForQuery(self,query):      
        d = dict()
        for k in query.keys():
            d[k]=1
        return d
        
class TF(Weighter):
    def getWeightsForQuery(self,query):    
        return query

class TF_IDF(Weighter):
    def getWeightsForQuery(self,query): 
        return self.idf_query(query)
                        
class Log(Weighter):
    def getDocWeightsForDoc(self,idDoc):
        d = self.index.getTfsForDoc(idDoc)
        return dict((k, 1 + np.log(v)) for k,v in d.items())

    def getWeightsForQuery(self,query):
        return self.idf_query(query)

class Log_plus(Weighter):
    def getDocWeightsForDoc(self,idDoc):
        tf = self.index.getTfsForDoc(idDoc)        
        return dict((k, (1 + np.log(v)) * self.idf_term(k)) for k,v in tf.items())

    def getWeightsForQuery(self,query):
        idf_q = self.idf_query(query)    
        return dict((k, (1 + np.log(self.index.getTfsForStem(k))) * v ) for k,v in idf_q.items())