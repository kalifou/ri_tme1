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
from QueryParser import QueryParser, Eval_P
import numpy as np
import sys
import os.path
import pickle


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
        models = pickle.load( open( "Vectoriel.p", "rb" ) )
    else:
        weighters = [Binary(I), TF(I), TF_IDF(I), Log(I)] # Log_plus(I)]
        models = [Vectoriel(False, w) for w in weighters]
        pickle.dump( I, open( "Vectoriel.p", "wb" ) )
    
    sys.stdout.write("Done!\n")
       
    '''
    queryExample = {'techniqu' : 1, 'accelerat' : 1}
    for i,m in enumerate(models):
        print "Test of model " + str(i)
        #print "getScores = ",m.getScores(queryExample)
        query_result = m.getRanking(queryExample)
        print "get top 3 documents = ", '[%s]' % ', '.join(map(str, query_result[0:3] ))
        #print "\n\n getRanking = ",m.getRanking(I.getTfsForDoc("20"))
    '''
    '''
    sys.stdout.write("Evaluation of weighter's models ...")
    query_file = "data/cacm/cacm.qry"
    relevance_file = "data/cacm/cacm.rel"
    QueryParser = QueryParser(query_file, relevance_file)
    Eval = Eval_P()
    Q = QueryParser.nextQuery()
    recall = []
    prec = []
    query_result = 0
    for m in models:
        query_result = m.getRanking(Q.getTf())
        recall, prec = Eval.evaluation(Q, query_result)
        print 'recall :', recall[0:15]
        print 'precision : ',prec[0:15]
    '''