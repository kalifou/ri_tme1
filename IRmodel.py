# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:43:53 2017

"""
import numpy as np
import sys
from Weighter import TF
#from RandomWalk import *
class IRmodel(object):
    
    def __init__(self):
        pass
    
    def getScores(self,query):
        """compute doncument's scores for a given query"""
        pass

    def getRanking(self,query):
        """Generic Ranking (ordered by desc) all the documents using how they score on the query"""
        
        scores = self.getScores(query)        
        list_of_sorted_scores = list( (int(key),value) for key, value \
                            in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
        
        # Now add all docs without any score at the end of the list
        docs_with_score = [ int(k) for k in scores.keys()]

        all_doc_ids = [ int(k) for k in self.getIndex().docs.keys()]
        #print "type id :",type(all_doc_ids[0])
        no_score = list( set(all_doc_ids).difference(set(docs_with_score)))
        #print "len ALL, NO, WITH",len(all_doc_ids),len(no_score),len(docs_with_score)
        for doc_id in no_score:
            list_of_sorted_scores.append((int(doc_id), -sys.maxint))
   
        return list_of_sorted_scores

class Vectoriel(IRmodel):

    def __init__(self, Index,normalized,Weighter):
        self.normalized = normalized
        self.Weighter = Weighter
        self.Index = Index

    def getName(self):
        return self.Weighter.getName()
        
    def getIndex(self):
        return self.Weighter.Index
        
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
                doc_score[str(doc_id)] = doc_score.get(str(doc_id), 0) + weights_query[stem] * w_stem
           
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
                doc_score[doc_id] /= (query_norm * self.Weighter.norm.get(doc_id,100000))
                #print doc_score[doc_id]
         
        return doc_score
        
class RandomModel(IRmodel):
    def __init__(self, Index, lissage_term):
        self.l_term = lissage_term
        self.Index = Index
        self.corpus_size = float(Index.total_corpus_size)
    def getIndex(self):
        return self.Index
    
    def getName(self):
        print "Language Model"
        
    def getScores(self,query):
        return {}
           
class LanguageModel(IRmodel):

    def __init__(self, Index, lissage_term):
        self.l_term = lissage_term
        self.Index = Index
        self.corpus_size = float(Index.total_corpus_size) 
        
    def getIndex(self):
        return self.Index
    
    def getName(self):
        print "Language Model"
        
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
        
class Okapi(IRmodel):
    """BM25 - Okapi : classical Probilistic model for Information Retrieval"""
    
    def __init__(self,Index):
        """Setting the params"""
        self.k1 = 1. #np.random.uniform(1,2)
        self.b = 0.75
        self.Weighter = TF(Index)
        self.Index = Index
        
        # Collecting docs length
        self.L = {}
        self.L_moy = 0.0
        for doc_id in self.Index.docFrom.keys():
            self.L[doc_id] = float(self.Index.docFrom[doc_id][2])
            self.L_moy += self.L[doc_id]
        self.L_moy = self.L_moy / self.Weighter.N # Check that the mean length is okay !!
        print 'L moy : ',self.L_moy
        
        # Calculating all probabilistic ids for all stems        
        self.idf_probabilistic = self.idf_probabilistic()
        #print 'Proba. IDFs : ',self.idf_probabilistic
        
    def getName(self):
        return "Okapi"
    
    def getIndex(self):
        return self.Index
        
    def idf_probabilistic(self):
        """ Probabilistic Inverse Document Frequency
            TODO : add this function to __init__() in Weighter class with a switch parameter 
                   such as probabilistic = True | False 
        """
        idf = {}
        N = self.Weighter.N 
        for stem in self.Index.stems.keys():
            tfs = self.Index.getTfsForStem(stem)
            df_t = float(len(tfs))
            r = np.log(( N - df_t + .5 ) / ( df_t + .5) )
            idf[stem] = max(0, r)
        return idf
        
    def f(self,q,d):
        """Score measuring how well Query q matches Document d"""
        score = 0.0        
        tfs = self.Weighter.getDocWeightsForDoc(d)
        for t in q:
            num = (self.k1 + 1)*  tfs.get(t,0) #getDocWeightsForStem(t).get(d,0.)
            denom = self.k1 * ( (1-self.b) + self.b * (self.L[d] / self.L_moy)) \
                                + tfs.get(t,0) #getDocWeightsForStem(t).get(d,0.)
            #print 'num :',num
            #print 'denom :',denom
            #print "idf prb :",self.idf_probabilistic.get(t,0.0)
            score += self.idf_probabilistic.get(t,0.0) * (num / denom)                                        
        #print "score :",score
        return score        
    
    def getScores(self,query):        
        """compute doncument's scores for a given query"""
        scores = {}        
        docs = self.L.keys()
        for doc_id in docs :
            scores[doc_id] = self.f(query,doc_id)
        #print "scores :",scores
        return scores
        
class RankModel(IRmodel):
    def __init__(self, I, n=1000, K=10):
        self.n = n
        self.K = K
        
    def getScores(query):
        o = Okapi(I)
        P, Succ, Index_P, Counter_Index_P, N_pgs = select_G_q(n, K, query, o, I)
        pr = PageRank(N_pgs, d) 
        A = get_A(P, Succ)  
        pr.randomWalk(A)
        return pr.get_result(Counter_Index_P)
        
class hitsModel(IRmodel):
    def __init__(self, I, n=1000, K=10):
        self.n = n
        self.K = K
        
    def getScores(query):
        o = Okapi(I)
        P, Succ, Index_P, Counter_Index_P, N_pgs = select_G_q(n, K, query, o, I)
        pr = PageRank(N_pgs, d) 
        A = get_A(P, Succ)  
        pr.randomWalk(A)
        return pr.get_result(Counter_Index_P)