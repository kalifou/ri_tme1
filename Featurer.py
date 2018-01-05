# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 14:08:27 2018

@author: kalifou
"""

def hash_query(query):
    res= ""
    #print query
    for q in query:
        #print q
        h = str(hash(q))+str(hash(query[q]))
        res+=h
    return res
    
class Featurer(object):
    
    def __init__(self,I):
        """
        params : 
            I : table of index 
        attributes:
            Index : I, param
            features : dict(Q,D2) with queries Q as keys and D2=dict(doc,score) as values.         
        """
        self.Index = I        
        self.features = dict()

    def getFeatures(self,idDoc, query):
        """
        Returns the score of a document with respect to the parameter query.
        """
        features = None
        self.features[idDoc] = features        
        return features
        
class FeaturerModel(Featurer):
    
    def __init__(self,I,model):
        self.Index = I
        self.features = dict()
        self.model = model

    def getFeatures(self,idDoc, query):
        features = self.model.getScores(query) #getRanking(query)   
        query_hash = hash_query(query)
        self.features[query_hash] = features  # hash the query to get an index      
        return features[int(idDoc)]    # How about Unknown idDocs ?!  

class FeaturerList(Featurer):
    """
    returns results of a list of Featurers.
    """
    def __init__(self,listFeaturers):
        self.listFeaturers = listFeaturers
        # Navigate in to find the features by featurer using its index: 
        # dict(featurerIndex,D) with D= dict(queryHash, DictScores) & DictScores= dict(idDoc, Score)
        self.listFeatures= dict( (ft,dict()) for ft in range(len(listFeaturers)))

    def getFeatures(self,idDoc, query):
        features = []
        query_hash = hash_query(query)
        for ft,_ in enumerate(self.listFeatures):            
            fture = self.listFeatures[ft].get(query_hash,None)
            # if the features haven't been gotten before, compute from featurer
            if fture == None:
                r = self.listFeaturers[ft].getFeatures(idDoc,query)
                self.listFeatures[ft] = dict()
                self.listFeatures[ft][query_hash] = self.listFeaturers[ft].features[query_hash]
                #print  "whole feature :",self.listFeatures[ft][query_hash]
            else: 
                #print "whole feature :",fture
                r = fture.get(idDoc,0.)          
            features.append(r)
        return features
    
from Weighter import Binary, TF, TF_IDF, Log, Log_plus
from IRmodel import Vectoriel, Okapi, LanguageModel, RankModel, HitsModel   
import sys
import pickle
import os
from IRmodel import MetaModel

if __name__ == "__main__":

    
    index = None    
    d = 0.6
    fname = "data/cacm/cacm.txt"
    
    sys.stdout.write("Indexing database...")
    sys.stdout.flush()
    if os.path.isfile('Index.p'):
       I = pickle.load( open( "Index.p", "rb" ) ) 
    
    else:
        parser = ParserCACM()
        textRepresenter = PorterStemmer()
        I = Index(parser,textRepresenter)
        I.indexation(fname)
        I.parser = None
        pickle.dump( I, open( "Index.p", "wb" ) )
        
    
    w1 = TF_IDF(I)
    model1 = Vectoriel(I,True, w1)
    w2 = Log_plus(I)
    model2 = Vectoriel(I,True, w2)
    w3 = Log(I)
    model3 = Vectoriel(I,True, w3)
    
    model4 = Okapi(I)
    queryExample = {'techniqu' : 1, 'accelerat' : 1}
    
    f1 = FeaturerModel(I,model1)
    print "\ndone building f1"
    f2 = FeaturerModel(I,model2)
    print "\ndone building f2"
    f3 = FeaturerModel(I,model3)
    print "\ndone building f3"
    
    f4 = FeaturerModel(I,model4)
    print "\ndone building f3"
    
    listFeaturers = FeaturerList([f1,f2,f3,f4])
    print "\ndone building list featurers"
    features = listFeaturers.getFeatures(3132,queryExample)
    print "list of features :\n",features
    
    # check that the data structures are on point => then describe it
    query_file = "data/cacm/cacm.qry"
    relevance_file = "data/cacm/cacm.rel"
    metamodel = MetaModel(listFeaturers,I,query_file,relevance_file)
    scores = metamodel.getScores(queryExample)
    #print "Score by random metamodel ",scores
    metamodel.train()