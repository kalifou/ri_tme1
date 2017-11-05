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
        
class LanguageModel(IRmodel):

    def __init__(self, Index, lissage_term):
        self.l_term = lissage_term
        self.Index = Index
        self.corpus_size = float(Index.total_corpus_size)      
        
    def getScores(self,query):
        """Calculating a score for all documents with respect to the stems of query """
        
        doc_scores = {}
        
        #initial score when meeting doc for first time.
        init_score = 0
        
        for stem in query.keys():
            docs_with_stem = self.Index.getTfsForStem(stem)
            corpus_prob = sum(docs_with_stem.values()) / self.corpus_size
            
            #update scores for docs with stem
            for d,stem_tf in docs_with_stem.items():
                
                #if doc had none of previous stems, score = sum of corpus probs
                if not doc_scores.has_key(d):
                    doc_scores[d] = init_score
                    
                doc_prob = stem_tf / float(sum(self.Index.getTfsForDoc(str(d)).values()))
                doc_scores[d] += query[stem] * np.log(self.l_term * doc_prob + (1-self.l_term) * corpus_prob)
            
            #update scores for docs in doc_scores but without this stem
            doc_scores_without_stem = list(set(doc_scores.keys()) - set(docs_with_stem.keys()))
            for d in doc_scores_without_stem:
                doc_scores[d] += (1-self.l_term) * corpus_prob
            
            #update initial score for new documents
            init_score += (1-self.l_term) * corpus_prob

        return doc_scores
        

    
    def getRanking(self,query):
        """Ranking (ordered by desc) all the documents using how they score on the query"""
        
        scores = self.getScores(query)        
        list_of_sorted_scores = list( (key,value) for key, value \
                            in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
        
        # Now add all docs without any score at the end of the list
        docs_with_score = scores.keys()
        all_doc_ids = self.Index.docs.keys()
        no_score = list( set(all_doc_ids) - set(docs_with_score))
        for doc_id in no_score:
            list_of_sorted_scores.append((doc_id, -sys.maxint))
              
        #print "\n Normal scores :\n", scores
        #print "\n Sorted scores :\n", list_of_sorted_scores
        return np.array(list_of_sorted_scores)