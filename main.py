# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:57:37 2017

@author: kalifou
"""

from Index import Index
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from Weighter import Binary, TF, TF_IDF, Log, Log_plus
from IRmodel import Vectoriel
from QueryParser import QueryParser
from EvalMeasure import Eval_P, Eval_AP
import numpy as np
import sys
import os.path
import pickle
import matplotlib.pyplot as plt


def test_weighter():
    parser = ParserCACM()
    textRepresenter = PorterStemmer()         
    fname = "data/cacm/cacm.txt"
    I = Index(parser,textRepresenter)
    I.indexation(fname)
    weighters = [Binary(I), TF(I), TF_IDF(I), Log(I), Log_plus(I)]
    for i,w in enumerate(weighters):
        print "Test of weighter" + str(i)
        print "getDocWeightsForDoc"
        print w.getDocWeightsForDoc("20")
        print "getDocWeightsForStem"
        print w.getDocWeightsForStem("accelerat")
        print "getDocWeightsForQuery"
        print w.getWeightsForQuery(I.getTfsForDoc("20"))

def plotInterpolatedPrecisionRecall(recall, inter_prec):
    plt.plot(recall, inter_prec)  

def testQuery(query_tf, models ):
    print "query : ", query_tf
    query_results = []
    for i,m in enumerate(models):
        print "Test of model " + str(i)
        query_results.append(m.getRanking(queryExample))
        print "get top 3 documents = ", '[%s]' % ', '.join(map(str, query_results[i][0:3] ))
    return query_results
    

if __name__ == "__main__":
    
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
        
    sys.stdout.write("Done!\n")
    sys.stdout.flush()
    
    sys.stdout.write("Creating weighters...")
    sys.stdout.flush()
    
    if os.path.isfile('Vectoriel.p'):
        models = pickle.load( open( "Models.p", "rb" ) )
    else:
        weighters = [Binary(I), Log_plus(I)]#, TF(I), TF_IDF(I), Log(I)] # Log_plus(I)]
        models = [Vectoriel(True, w) for w in weighters]
        pickle.dump( models, open( "Models.p", "wb" ) )
    
    sys.stdout.write("Done!\n")
       
    
    queryExample = {'techniqu' : 1, 'accelerat' : 1}
    query_results = testQuery(queryExample, models)