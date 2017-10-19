# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:43:53 2017

"""
import Weighter
import numpy as np

class IRmodel(object):
    
    def __init__(self):
        pass

    
    def getScores(self,query):
        """compute doncument's scores for a given query"""
        pass

    def getRanking(self,query):
        pass

class Vectoriel(object):

    def __init__(self,normalized,Weighter):
        self.normalized = normalized
        self.Weighter = Weighter


    def getScores(self,query):
        doc_score = {}
        
        weights_query = self.Weighter.getWeightsForQuery(query)
        if self.normalized:
            query_norm = np.sum(np.abs(weights_query.values()))
        
        for stem in query:
            #get weights of stem for all documents
            weights_stem = self.Weighter.getDocWeightsForStem(stem)
            
            for doc_id, w_stem in weights_stem.items():
                doc_score[doc_id] = doc_score.get(doc_id, 0) + weights_query[stem] * w_stem
           
        if self.normalized:
            for doc_id in doc_score:
                doc_score[doc_id] /= query_norm * self.Weighter.norm[doc_id]
        
        return doc_score
