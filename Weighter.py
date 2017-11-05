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
        if stem_tf == -1:#unknown stem
            return {}
        return stem_tf
        
    def getWeightsForQuery(self,query):        
        """Returning a dictionnary of present keys valued to 1 """  
        pass
    def idf_term(self,stem):
        """getting the inverse doc freq for term"""
        idf = self.idf_stem.get(stem,0)
        if idf == 0:
            print "UNKNOWN STEM"
        return idf
        
    def idf_query(self,query):
        """getting the inverse doc freq for each term of the query"""        
        w = dict()
        for t in query.keys():                        
            w[t] = self.idf_term(t)
        return w
        
class Binary(Weighter):
        
    def getWeightsForQuery(self,query):      
        weights = dict()
        for stem in query.keys():
            weights[stem]=1
        return weights
        
class TF(Weighter):
    def getWeightsForQuery(self,query):    
        return query

class TF_IDF(TF):
    def getWeightsForQuery(self,query): 
        return self.idf_query(query)
                        
class Log(TF):
    def getDocWeightsForDoc(self,doc_id):
        doc_tf = self.index.getTfsForDoc(doc_id)
        return dict((stem, 1 + np.log(tf)) for stem,tf in doc_tf.items())

    def getWeightsForQuery(self,query):
        return self.idf_query(query)
        
    def getDocWeightsForStem(self,stem):
        stem_tfs = self.index.getTfsForStem(stem)  
        if stem_tfs == -1:#unknown stem
            return {}
            
        return dict((doc_id, 1 + np.log(tf)) for doc_id,tf in stem_tfs.items())

class Log_plus(TF):
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