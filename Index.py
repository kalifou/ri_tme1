# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:32:12 2017

@author: kalifou
"""

class Index(object):

    def __init__(self,name,docs,stems,docFrom,parser,textRepresenter):
        self.name = name
        self.docs = docs
        self.stems = stems
        self.docFrom = docFrom
        self.parser = parser
        self.textRepresenter = textRepresenter

    def indexation(self,source_file):
        """Building Indexes and Inversed Indexes"""
    
        self.parser.initFile(source_file)
        
        doc = self.parser.nextDocument()
        print doc.getText()
        # Getting the Bow
        Bow = self.textRepresenter.getTextRepresentation(doc.getText()) 
        key = None 
        print Bow
        #others = doc.get(key)   
        
        # enregister others dans docFrom
        index = None
        inversed_index =  None
        #        while True:
        #            
        #            next = self.parser.nextDocument(source_file)
        #            text_representation = self.textRepresenter.getTextRepresentation(next)        
        #            
        #            index = None
        #            inversed_index =  None
        #            
        return index,inversed_index

    def getTfsForDoc(self,source_file):
        index,_ = self.indexation(source_file)
        stem_tf = None
        return stem_tf
        
    def getTfsForStem(self,source_file):
        _,inversed_index = self.indexation(source_file)
        doc_tf = None        
        return doc_tf

    def getStr(self,source_file):
        str = None
        return str            
    