# -*- coding: utf-8 -*-
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
import matplotlib.pyplot as plt


def plot_(recall, interpolated_prec,precision):
    """Plotting Both : simple & interpolated precision - recall curve"""
    fig = plt.figure() #(figsize=(9,7))
    fig.suptitle('Precision - Recall',fontsize=15)
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.plot(recall,precision, 'b-',label="precision")
    plt.plot(recall,interpolated_prec, 'r',label="interpolated precision")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()
    
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
    parser = ParserCACM()
    textRepresenter = PorterStemmer()
    I = Index(parser,textRepresenter)
    I.indexation(fname)
    I.parser = None
    weighters = [Log_plus(I)] #,TF_IDF(I)]
    models = [Vectoriel(True, w) for w in weighters]
    sys.stdout.write("Evaluation of weighter's models ...")
    print '\n'
    query_file = "data/cacm/cacm.qry"
    relevance_file = "data/cacm/cacm.rel"
    QueryParser = QueryParser(query_file, relevance_file)
    Eval = Eval_P()
    EvalAP = Eval_AP()
    recall = []
    prec = []
    query_result = 0
    Q = QueryParser.nextQuery()
    while (Q != -1):
        for i,m in enumerate(models):
            print "Model ", i
            query_result = m.getRanking(Q.getTf())
            recall, interpolated_prec,precision = Eval.evaluation(Q, query_result)
            #Display first 15 values to see performances
            print 'recall :', recall[0:10]
            print 'precision : ',precision[0:10]
            print 'inter_precision : ',interpolated_prec [0:10]
            plot_(recall, interpolated_prec,precision) 
            average_precision = EvalAP.evaluation(Q, query_result)
            print 'AP: ', average_precision
        Q = QueryParser.nextQuery()
