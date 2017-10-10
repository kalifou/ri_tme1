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
        self.stems = {}
        self.docFrom = {}
        self.parser = parser
        self.textRepresenter = textRepresenter
        self.index_file = None
        self.inv_index_file = None

    def indexation(self,source_file):
        """Building Indexes and Inversed Indexes"""
        
        self.parser.initFile(source_file)
        
        self.index_file = 'index.txt'
        #if file not built, create it
        #if not os.path.isfile('./index.txt'):
        index = open("index.txt", "wb+")
        
        #store the size needed for each stem to write them in inverted index
        stem_length = {}
            
            
        while True:
             #gather data from doc and update dictionary
             doc = self.parser.nextDocument()
             if (doc == None):
                 index.close()
                 break
             # Getting the Bow                    
             bow = self.textRepresenter.getTextRepresentation(doc.getText())
             str_bow = str(bow)
             doc_id = doc.getId()
             self.docs[doc_id] = (index.tell(), len(str_bow))
             
             #stores  the source,position and length of document as   [source_path, position, length]
             self.docFrom[doc_id] = doc.get("from").split(';')
             #store in file
             index.write(str_bow)
             
             #STEP 1 for inv index: gather size needed for each term
             for stem,val in bow.iteritems():
                 stem_length[stem] = stem_length.get(stem,0)+ len("(" + str(doc_id) + ":" + str(val) + ");")
        
        #STEP 2 for inv index: compute positions in txt file for each stem
        cur_pos = 0
        pos = {}
        for stem,length in stem_length.iteritems():
            pos[stem] = cur_pos + length
            cur_pos = pos[stem]
            
            #populate stems dictionary
            self.stems[stem] = (pos[stem],stem_length[stem])
        
        
        #STEP 3 for inv index: perform 2nd pass over docs to write in file
        self.inv_index_file = "inv_index.txt"
        inv_index = open(self.inv_index_file, "wb+")
         
        self.parser.initFile(source_file)
        while True:
             #gather data from doc and update dictionary
             doc = self.parser.nextDocument()
            
             if (doc == None):
                 inv_index.close()
                 break
             doc_id = doc.getId()
             bow = self.textRepresenter.getTextRepresentation(doc.getText())
             for stem,val in bow.iteritems():
                 inv_index.seek(pos[stem])
                 str_wrt ="(" + str(doc_id) + ":" + str(val) + ");"
                 inv_index.write(str_wrt)
                 pos[stem] = pos.get(stem,0)+ len(str_wrt)
             
        
        
            
    #Return bow representation of a document given its ID
    def getTfsForDoc(self,doc_id):
        pos, size = self.docs[doc_id]
        index = open(self.index_file,'r')
        index.seek(pos)
        bow = index.read(size)
        index.close()
        return ast.literal_eval(bow)
    
    def getTfsForStem(self,stem):
        inv_index = open(self.inv_index_file,"r")
        pos, length = self.stems[stem]
        inv_index.seek(pos)
        ret = inv_index.read(length)
        inv_index.close()
        return ret

    def getStrDoc(self,doc_id): 
        source_path, position, length = self.docFrom[doc_id];
        source_file = open(source_path,'r')
        source_file.seek(int(position))
        doc = source_file.read(int(length))
        source_file.close()
        return doc
    