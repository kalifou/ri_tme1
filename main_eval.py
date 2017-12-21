# -*- coding: utf-8 -*-
from Index import Index
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from Weighter import Binary, TF, TF_IDF, Log, Log_plus
from EvalMeasure import EvalIRModel
import numpy as np
import os.path
import time

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
    t1 = time.time()
    fname = "data/cacm/cacm.txt"
    query_file = "data/cacm/cacm.qry"
    relevance_file = "data/cacm/cacm.rel"
    type = "Vectoriel" # model_type = Vectoriel | Okapi | Language | PageRank
    eval_platform = EvalIRModel(fname,query_file,relevance_file,model_type=type)
    simple_eval = False    
    
    if simple_eval :        
        eval_platform.eval()
    else:
        models_recall, models_inter_prec, models_AP = eval_platform.eval_std()
    print "Exec duration(s) : ",time.time()-t1