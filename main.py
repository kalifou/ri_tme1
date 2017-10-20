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
    print "coucou"
    parser = ParserCACM()
    textRepresenter = PorterStemmer()
    
    name = None
    docs = None
    stems = None
    docsFrom = None         
    fname = "data/cacm/cacm.txt"
    print "coucou"
    I = Index(name,docs,stems,docsFrom,parser,textRepresenter)
    I.indexation(fname)
    print "cucu"
    #print I.getTfsForDoc("20")
    #print I.getStrDoc("20")
    #stems checked  : iter  solut wegstein converg procedur exampl (ok),
    #fails for techniqu discuss with "((" appearing  &  ( missing 
    # seems like we overwrite at the wrong position : try to read the inv_index.txt, the head is incomplete/ unreadable. 
    
    #print I.getTfsForStem("techniqu")
    
    
    # Test for our different implementations of weighter
    weighters = [ Log_plus(I)] #[Binary(I), TF(I), TF_IDF(I), Log(I), Log_plus(I)]
    models = [Vectoriel(False, w) for w in weighters]
    
    for i,m in enumerate(models):
        print "Test of model " + str(i)
        print "getScores = ",m.getScores(I.getTfsForDoc("20"))
        print "\n\n getRanking = ",m.getRanking(I.getTfsForDoc("20"))
    
    