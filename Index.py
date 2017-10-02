# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:32:12 2017

@author: kalifou
"""
import ast
import os
class Index(object):

    def __init__(self,name,docs,stems,docFrom,parser,textRepresenter):
        self.name = name
        self.docs = {}
        self.stems = stems
        self.docFrom = docFrom
        self.parser = parser
        self.textRepresenter = textRepresenter
        self.index_file = None

    def indexation(self,source_file):
        """Building Indexes and Inversed Indexes"""
        
        self.parser.initFile(source_file)
        
        self.index_file = 'index.txt'
        #if file not built, create it
        if not os.path.isfile('./index.txt'):
            index = open("index.txt", "w+")
            
            
            #print doc.getText()
            # Getting the Bow
            #Bow = self.textRepresenter.getTextRepresentation(doc.getText()) 
            #others = doc.get(key) 
            while True:
                 #gather data from doc and update dictionary
                 doc = self.parser.nextDocument()
                 if (doc == None):
                     break
                 bow = str(self.textRepresenter.getTextRepresentation(doc.getText()))
                 key = doc.getId()
                 self.docs[key] = (index.tell(), len(bow))
                 
                 #store in file
                 index.write(bow)
            index.close()
            

        # enregister others dans docFrom
        #index = None
        #inversed_index =  None
        #        while True:
        #            
        #            next = self.parser.nextDocument(source_file)
        #            text_representation = self.textRepresenter.getTextRepresentation(next)        
        #            
        #            index = None
        #            inversed_index =  None
        #            
        #return index,inversed_index 
        #NOTE: I think it returns nothing but rather update self.docs, stems,..
        #

    #Return bow representation of a document given its ID
    def getTfsForDoc(self,doc_id):
        pos, size = self.docs[doc_id]
        index = open(self.index_file,'r')
        index.seek(pos)
        bow = index.read(size)
        return ast.literal_eval(bow)
        
    def getTfsForStem(self,source_file):
        _,inversed_index = self.indexation(source_file)
        doc_tf = None        
        return doc_tf

    def getStr(self,source_file):
        str = None
        return str            
    