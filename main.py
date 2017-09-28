# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:57:37 2017

@author: kalifou
"""

from Index import Index
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from Document import Document

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
    # Squelette code
    #with open(None, "") as idx:
    #    idx.tell()
    #    idx.write()
    #    idx.seek()