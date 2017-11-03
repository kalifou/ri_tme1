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
        
        #Save idf of all stems
        self.idf_stem = {}
        for stem in self.index.stems.keys():
            v = self.index.getTfsForStem(stem)
            N_t = float(len(v))
            self.idf_stem[stem] = np.log(self.N / N_t)
        
        # Save norm of all documents for normalized scores
        self.norm ={}        
        for d in self.index.docs:
            values = self.getDocWeightsForDoc(d).values()
            self.norm[d] = np.sum(np.abs(values))
        
        
        
    def getDocWeightsForDoc(self,idDoc):
        """returning the stem present in doc with associated freq """        
        return self.index.getTfsForDoc(idDoc)
        
    def getDocWeightsForStem(self,stem):
        """returning the docs where stem is present with associated freq """
        stem_tf = self.index.getTfsForStem(stem)
        if stem_tf == -1:
            return {}
        return stem_tf
        
    def getWeightsForQuery(self,query):        
        """Returning a dictionnary of present keys valued to 1 """  
        pass
    def idf_term(self,stem):
        """getting the inverse doc freq for term"""
        #return 0 if unknown stem
        return self.idf_stem.get(stem,0)
        
    def idf_query(self,query):
        """getting the inverse doc freq for each term of the query"""        
        w = dict()
        for t in query.keys():                        
            w[t] = self.idf_term(t)
        return w
        
    def getName(self):
        pass
    
class Binary(Weighter):
        
    def getName(self):
         return " Binary"
    def getWeightsForQuery(self,query):      
        d = dict()
        for k in query.keys():
            d[k]=1
        return d
        
class TF(Weighter):
    def getName(self):
         return " Text Frequency"
    def getWeightsForQuery(self,query):    
        return query

class TF_IDF(TF):
    def getName(self):
         return " Text Frequency - Inverse Document Frequency"
         
    def getWeightsForQuery(self,query): 
        return self.idf_query(query)
                        
class Log(TF):
    def getName(self):
         return " Log"
    def getDocWeightsForDoc(self,idDoc):
        d = self.index.getTfsForDoc(idDoc)
        return dict((k, 1 + np.log(v)) for k,v in d.items())

    def getWeightsForQuery(self,query):
        return self.idf_query(query)
        
    def getDocWeightsForStem(self,stem):
        d = self.index.getTfsForStem(stem)
        
        if d == -1:#unknown stem
            return {}
        return dict((k, 1 + np.log(v)) for k,v in d.items())

class Log_plus(TF):
    def getName(self):
         return " Log +"
    def getDocWeightsForDoc(self,idDoc):
        tf = self.index.getTfsForDoc(idDoc)        
        return dict((k, (1 + np.log(v)) * self.idf_term(k)) for k,v in tf.items())

    def getWeightsForQuery(self,query):
        idf_q = self.idf_query(query)
        return dict((k, (1 + np.log(query[k])) * v ) for k,v in idf_q.items())
        
    def getDocWeightsForStem(self,stem):
        tfs = self.index.getTfsForStem(stem)  
        if tfs == -1:#unknown stem
            return {}
        idf_stem = self.idf_term(stem)
        return dict((k, (1 + np.log(v)) * idf_stem) for k,v in tfs.items())