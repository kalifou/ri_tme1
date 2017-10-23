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


def test_weighter():
    parser = ParserCACM()
    textRepresenter = PorterStemmer() 
    name = None
    docs = None
    stems = None
    docsFrom = None         
    fname = "data/cacm/cacm.txt"
    I = Index(name,docs,stems,docsFrom,parser,textRepresenter)
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
    parser = ParserCACM()
    textRepresenter = PorterStemmer()
    
    name = None
    docs = None
    stems = None
    docsFrom = None         
    fname = "data/cacm/cacm.txt"
    
    print "Indexing database ..."
    I = Index(name,docs,stems,docsFrom,parser,textRepresenter)
    I.indexation(fname)
    
    #print I.getTfsForDoc("20")
    #print I.getStrDoc("20")  
    #print I.getTfsForStem("techniqu")
    # Test for our different implementations of weighter
    
    #Log_plus instanciation not returning, must be because of idf computation
    weighters = [Binary(I), TF(I), TF_IDF(I), Log(I)] # Log_plus(I)
    models = [Vectoriel(False, w) for w in weighters]
    
    queryExample = {'techniqu' : 1, 'accelerat' : 1}
    for i,m in enumerate(models):
        print "Test of model " + str(i)
        #print "getScores = ",m.getScores(queryExample)
        query_result = m.getRanking(queryExample)
        print "get top 3 documents = ", '[%s]' % ', '.join(map(str, query_result[0:3] ))
        #print "\n\n getRanking = ",m.getRanking(I.getTfsForDoc("20"))
    
    