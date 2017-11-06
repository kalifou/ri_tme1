# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:43:53 2017

"""
import numpy as np
import sys
from Weighter import TF

class IRmodel(object):
    
    def __init__(self):
        pass
    
    def getScores(self,query):
        """compute doncument's scores for a given query"""
        pass

    def getRanking(self,query):
        """Generic Ranking (ordered by desc) all the documents using how they score on the query"""
        
        scores = self.getScores(query)        
        list_of_sorted_scores = list( (key,value) for key, value \
                            in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
        
        # Now add all docs without any score at the end of the list
        docs_with_score = scores.keys()
        all_doc_ids = self.Weighter.index.docs.keys()
        no_score = list( set(all_doc_ids) - set(docs_with_score))
        for doc_id in no_score:
            list_of_sorted_scores.append((doc_id, -sys.maxint))
              
        return np.array(list_of_sorted_scores)

class Vectoriel(IRmodel):

    def __init__(self,normalized,Weighter):
        self.normalized = normalized
        self.Weighter = Weighter

    def getName(self):
        return self.Weighter.getName()
        
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
        
class Okapi(IRmodel):
    """BM25 - Okapi : classical Probilistic model for Information Retrieval"""
    
    def __init__(self,index):
        """Setting the params"""
        self.k1 = np.random.uniform(1,2)
        self.b = 0.75
        self.Weighter = TF(index)
        self.index = index
        
        # Collecting docs length
        self.L = {}
        self.L_moy = 0.0
        for doc_id in self.index.docFrom.keys():
            self.L[doc_id] = float(self.index.docFrom[doc_id][2])
            self.L_moy += self.L[doc_id]
        self.L_moy = self.L_moy / self.Weighter.N # Check that the mean length is okay !!
        print 'L moy : ',self.L_moy
        
        # Calculating all probabilistic ids for all stems        
        self.idf_probabilistic = self.idf_probabilistic()
        #print 'Proba. IDFs : ',self.idf_probabilistic
        
    def getName(self):
        return "Okapi"
        
    def idf_probabilistic(self):
        """ Probabilistic Inverse Document Frequency
            TODO : add this function to __init__() in Weighter class with a switch parameter 
                   such as probabilistic = True | False 
        """
        idf = {}
        N = self.Weighter.N 
        for stem in self.index.stems.keys():
            tfs = self.index.getTfsForStem(stem)
            df_t = float(len(tfs))
            r = np.log(( N - df_t + .5 ) / ( df_t + .5) )
            idf[stem] = max(0, r)
        return idf
        
    def f(self,q,d):
        """Score measuring how well Query q matches Document d"""
        score = 0.0        
        for t in q:
            num = (self.k1 + 1)*  self.Weighter.getDocWeightsForStem(t).get(d,0.)
            denom = self.k1 * ( (1-self.b) + self.b * self.L[d] / self.L_moy) \
                                + self.Weighter.getDocWeightsForStem(t).get(d,0.)
            #print 'denom :',denom
            score += self.idf_probabilistic.get(t,0.0) * (num / denom)                                        
        return score        
    
    def getScores(self,query):        
        """compute doncument's scores for a given query"""
        scores = {}        
        docs = self.L.keys()
        for doc_id in docs :
            scores[doc_id] = self.f(query,doc_id)
        return scores 