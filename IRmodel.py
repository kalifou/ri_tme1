# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:43:53 2017

"""
import numpy as np
import sys
from Weighter import TF, TF_IDF,  Binary,Log_plus
from RandomWalk import *
from QueryParser import QueryParser

class IRmodel(object):
    
    def __init__(self):
        pass
    def getName(self):
        pass
    def getIndex(self):
        pass
    def getScores(self,query):
        """compute doncument's scores for a given query"""
        pass

    def getRanking(self,query):
        """Generic Ranking (ordered by desc) all the documents using how they score on the query"""
        
#        scores = self.getScores(query)        
#        list_of_sorted_scores = list( (int(key),value) for key, value \
#                            in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
#        
#        # Now add all docs without any score at the end of the list
#        docs_with_score = [ int(k) for k in scores.keys()]
#
#        all_doc_ids = [ int(k) for k in self.getIndex().docs.keys()]
#        #print "type id :",type(all_doc_ids[0])
#        no_score = list( set(all_doc_ids).difference(set(docs_with_score)))
#        #print "len ALL, NO, WITH",len(all_doc_ids),len(no_score),len(docs_with_score)
#        for doc_id in no_score:
#            list_of_sorted_scores.append((int(doc_id), -sys.maxint))
#   
#        return list_of_sorted_scores
        
        scores = self.getScores(query)        
        list_of_sorted_scores = list( (int(key),value) for key, value \
                            in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
        
        # Now add all docs without any score at the end of the list
        docs_with_score = scores.keys()

        all_doc_ids = [ int(k) for k in self.getIndex().docs.keys()]
        #print "type id :",type(all_doc_ids[0])
        no_score = list( set(all_doc_ids).difference(set(docs_with_score)))
        #print "len ALL, NO, WITH",len(all_doc_ids),len(no_score),len(docs_with_score)
        for doc_id in no_score:
            list_of_sorted_scores.append((doc_id, -sys.maxint))
        #print list_of_sorted_scores
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
                #doc_score[str(doc_id)] = doc_score.get(str(doc_id), 0) + weights_query[stem] * w_stem
                doc_score[int(doc_id)] = doc_score.get(int(doc_id), 0) + weights_query[stem] * w_stem
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
                doc_score[int(doc_id)] /= (query_norm * self.Weighter.norm.get(doc_id,100000))
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
        
        #pre-compute corpus language model
        self.corpus_prob = {}
        for stem in self.Index.stems.keys():
            docs_with_stem = self.Index.getTfsForStem(stem)
            self.corpus_prob[stem] = sum(docs_with_stem.values()) / self.corpus_size
        
    def getIndex(self):
        return self.Index
    
    def getName(self):
        return "Language Model"
    
    def getScores(self,query):
        """Calculating a score for all documents with respect to the stems of query """
        doc_scores = {}
        for doc_id in self.Index.docFrom.keys():
            doc_score = 0
            doc_tfs = self.Index.getTfsForDoc(doc_id)
            doc_length = sum(doc_tfs.values())
            for q_stem,q_tf in query.items():
                #add corpus prob in any case
                in_log = (1 - self.l_term) * self.corpus_prob[q_stem]
                #add doc prob if stem in current doc
                if doc_tfs.has_key(str(q_stem)):    
                    in_log += self.l_term * (doc_tfs[str(q_stem)] / float(doc_length))
                    #print in_log
                if in_log < 0:
                    print "SHOOOOOOOOOULD NOT HAPPEN"
                doc_score += q_tf * np.log(in_log)
            if doc_score == 0:
                print "ERROR SCORE = 0, EVERY DOC SHOULD HAVE A NEG SCORE"
            doc_scores[int(doc_id)] = doc_score
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
            scores[int(doc_id)] = self.f(query,doc_id)
        #print "scores :",scores
        return scores
        
class RankModel(IRmodel):
    def __init__(self, I, n=300, K=100,d=.85):
        self.n = n
        self.K = K
        self.Index = I
        self.Index.get_all_doc_ids()
        self.d = d
    def getName(self):
        return "PageRank"
        
    def getIndex(self):
        return self.Index
        
#    def getRanking(self,query):
#        """Generic Ranking (ordered by desc) all the documents using how they score on the query"""
#        
#        scores = self.getScores(query)        
#        list_of_sorted_scores = list( (int(key),value) for key, value \
#                            in sorted(scores.iteritems(),reverse=True, key=lambda (k,v): (v,k)))
#        
#        # Now add all docs without any score at the end of the list
#        docs_with_score = scores.keys()
#        ids_ = self.getIndex().all_ids_
#        #all_ids.remove('')
#        all_doc_ids = [ int(float(k)) for k in ids_] 
#        no_score = list( set(all_doc_ids).difference(set(docs_with_score)))
#        #print "len ALL, NO, WITH",len(all_doc_ids),len(no_score),len(docs_with_score)
#        for doc_id in no_score:
#            list_of_sorted_scores.append((doc_id, -sys.maxint))
#        #print list_of_sorted_scores
#        return list_of_sorted_scores  
        
    def getScores(self,query):
        w = TF_IDF(self.Index)
        model = Vectoriel(self.Index,True, w)
        P, Succ, Index_P, Counter_Index_P, N_pgs = select_G_q(self.n, self.K, query, model, self.Index)
        pr = PageRank(N_pgs, self.d) 
        A = get_A(P, Succ, N_pgs)  
        pr.randomWalk(A)
        return pr.get_result(Counter_Index_P)
        
class HitsModel(IRmodel):
    def __init__(self, I, n=100, K=20):
        self.n = n
        self.K = K
        self.Index=I
    def getName(self):
        return "Hits"
        
    def getIndex(self):
        return self.Index
        
    def getScores(self,query):
        w = TF_IDF(self.Index)
        model = Vectoriel(self.Index,True, w)
        P, Succ, Index_P, Counter_Index_P, N_pgs = select_G_q(self.n, self.K, query, model, self.Index)
        hts = Hits(N_pgs)
        hts.randomWalk(P, Succ, Index_P)
        return hts.get_result(Counter_Index_P)

class MetaModel(IRmodel):
    
    def __init__(self, listFeaturers, I, query_file, relevance_file, alpha=1e-1, l=1e-1):
        self.listFeaturers = listFeaturers
        self.Index = I #?
        self.theta = np.random.rand(len(self.listFeaturers.listFeaturers),1)
        self.lmbda = l
        self.alpha = alpha
        self.all_doc_ids = [ int(k) for k in self.getIndex().docs.keys()]
        self.query_file = query_file
        self.relevance_file = relevance_file
        self.query_parser = QueryParser(self.query_file, self.relevance_file)  
        
    def getName(self):
        return "MetaModel"
        
    def getIndex(self):
        return self.Index
        
    def f_theta(self,d,q):
        x_d_q = np.array(self.listFeaturers.getFeatures(d,q))
        return x_d_q.dot(self.theta)
        
    def getScores(self,query):
        scores = {}
        d_keys = self.listFeaturers.listFeaturers[0].model.getScores(query).keys()
        
        for d in d_keys:
            scores[int(d)] = self.f_theta(int(d),query)[0]
        return scores
        
    def train(self, tmax=1,eps = 1e-1):                
        #########################################################
        #TODO : add stochasticity : no random sampling of Query q,
        #########################################################
        
        #for it in range(tmax):
        q = self.query_parser.nextQuery()
        query_nb = 0
        diff=1e+6
        old_theta = np.copy(self.theta)
        
        while (q != -1) and diff > eps:
            if query_nb % 10 == 0:
                print "Query #",query_nb
                print "Grad theta :",diff
            #i = np.random.randint(0,n_queries)
            #q = queries[i]
            
            ## relevants & irrelevants docs 
            relevants = np.array(q.getRelevantDocs())[:,0]
            if relevants == []:
                    print "query ignored: no relevant docs"
                    q = self.query_parser.nextQuery()
                    continue
            irrelevants = list(set(self.all_doc_ids).difference(set(relevants)))
            
            n_relevants = len(relevants)
            n_irrelevants = len(irrelevants)
            
            i_d = np.random.randint(0,n_relevants)
            d_relevant = relevants[i_d]
            
            i_d_prime = np.random.randint(0,n_irrelevants)
            d_irrelevant = irrelevants[i_d_prime]
            
            diff_f_theta = 1. - self.f_theta(d_relevant,q.getTf()) + self.f_theta(d_irrelevant,q.getTf())
            
            if diff_f_theta > 0.:
                x_d_q = np.array(self.listFeaturers.getFeatures(d_relevant,q.getTf())).reshape(self.theta.shape)
                x_d_prime_q = np.array(self.listFeaturers.getFeatures(d_irrelevant,q.getTf())).reshape(self.theta.shape)
                self.theta += self.alpha*(x_d_q-x_d_prime_q)
            
            # Regularizing Theta
            self.theta = (1.-2.*self.lmbda*self.alpha)*self.theta
            query_nb+=1
            
            diff = np.abs(np.sum(old_theta-self.theta))
            old_theta = np.copy(self.theta)
            
        # Done with training the model
        print "Training achieved with Grad_theta < ",eps," !"
        print "Number of queries required :",query_nb