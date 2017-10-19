# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:57:37 2017

@author: kalifou
"""

from Index import Index
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from Weighter import *

if __name__ == "__main__":
    
    parser = ParserCACM()
    textRepresenter = PorterStemmer()
    
    name = None
    docs = None
    stems = None
    docsFrom = None         
    fname = "data/cacm/cacm.txt"
    I = Index(name,docs,stems,docsFrom,parser,textRepresenter)
    I.indexation(fname)
    #print I.getTfsForDoc("20")
    #print I.getStrDoc("20")
    #stems checked  : iter  solut wegstein converg procedur exampl (ok),
    #fails for techniqu discuss with "((" appearing  &  ( missing 
    # seems like we overwrite at the wrong position : try to read the inv_index.txt, the head is incomplete/ unreadable. 
    
    #print I.getTfsForStem("techniqu")
    
    
    # Test for our different implementations of weighter
    weighters = [Binary(I), TF(I), TF_IDF(I), Log(I), Log_plus(I)]
    for i,w in enumerate(weighters):
        print "Test of weighter" + str(i)
        print "getDocWeightsForDoc"
        print w.getDocWeightsForDoc("20")
        print "getDocWeightsForStem"
        print w.getDocWeightsForStem("accelerat")
        print "getDocWeightsForQuery"
        print w.getWeightsForQuery(I.getTfsForDoc("20"))
    
    # Squelette code
    #with open(None, "") as idx:
    #    idx.tell()
    #    idx.write()
#    #    idx.seek()
#    
#    w =  B(I)
#    print w.getDocWeightsForDoc("20")
    
    