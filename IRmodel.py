# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:43:53 2017

"""
import numpy as np
import sys

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
            #print 'WEIGHTS_QUERY '
            #print weights_query
            query_norm = float(np.sum(np.abs(weights_query.values())))
            #print 'QUERY NORM'
            #print query_norm
        
        for stem in query:
            #get weights of stem for all documents
            weights_stem = self.Weighter.getDocWeightsForStem(stem)
            
            #if unknown stem, dicgtionnary empty, then go to new stem
            if(len(weights_stem) == 0):
                continue
            
            for doc_id, w_stem in weights_stem.items():
                doc_score[doc_id] = doc_score.get(doc_id, 0) + weights_query[stem] * w_stem
           
        if self.normalized:
            #print doc_score.keys()
            for doc_id in doc_score.keys():
                #print 'NORMALIZE ', doc_id
                #print 'QUERY NORM'
                #print query_norm
                #print 'WEIGHTER NORM'
                #print self.Weighter.norm[str(doc_id)]
                #print'PREVIOUS SCORE'
                #print doc_score[doc_id]
                #print 'NEW SCORE'
                doc_score[doc_id] /= (query_norm * self.Weighter.norm[str(doc_id)])
                #print doc_score[doc_id]
         
        return doc_score
    
    def getRanking(self,query):
        """Ranking (ordered by desc) all the documents using how they score on the query"""
        
        scores = self.getScores(query)        
        list_of_sorted_scores = list( (key,value) for key, value in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
        
        # Now add all docs without any score at the end of the list
        docs_with_score = scores.keys()
        all_doc_ids = self.Weighter.index.docs.keys()
        no_score = list( set(all_doc_ids) - set(docs_with_score))
        for doc_id in no_score:
            list_of_sorted_scores.append((doc_id, -sys.maxint))
              
        #print "\n Normal scores :\n", scores
        #print "\n Sorted scores :\n", list_of_sorted_scores
        return np.array(list_of_sorted_scores)