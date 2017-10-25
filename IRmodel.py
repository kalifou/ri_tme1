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

class Vectoriel(IRmodel):

    def __init__(self,normalized,Weighter):
        self.normalized = normalized
        self.Weighter = Weighter

    def getScores(self,query):
        """Calculating a score for all documents with respect to the stems of query """
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
        
        
        #Not needed, we want a sparse encoding
        '''
        # Getting all ids of docs without any score
        docs_with_score = doc_score.keys()
        all_doc_ids = self.Weighter.index.docs.keys()
        no_score = list( set(all_doc_ids) - set(docs_with_score))
        for doc_id in no_score:
            doc_score[doc_id] = 0
        '''
        
        return doc_score
    
    def getRanking(self,query):
        """Ranking (ordered by desc) all the documents using how they score on the query"""
        
        scores = self.getScores(query)        
        list_of_sorted_scores = list( (key,value) for key, value in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
        #print "\n Normal scores :\n", scores
        #print "\n Sorted scores :\n", list_of_sorted_scores
        return np.array(list_of_sorted_scores)