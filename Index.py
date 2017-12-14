# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:32:12 2017

@author: kalifou
"""
import ast

class Index(object):

    def __init__(self,parser,textRepresenter):
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
          
        #accumulates all tfs to have total size of corpus
        self.total_corpus_size = 0
        
        while True:
             #gather data from doc and update dictionary
             doc = self.parser.nextDocument()
             if (doc == None):
                 index.close()
                 break
             #get the Bow
             bow = self.textRepresenter.getTextRepresentation(doc.getText())
             self.total_corpus_size += sum(bow.values())
             str_bow = str(bow)
             
             #get hyperlinks
             str_links = doc.get("links")
             
             #stores  the source position and length of bow and links for document
             doc_id = doc.getId()
             self.docs[doc_id] = (index.tell(), len(str_bow), len(str_links))
             
             #store source of doc
             self.docFrom[doc_id] = doc.get("from").split(';')
             
             #write in file
             index.write(str_bow)
             index.write(str_links)
             
             #STEP 1 for inv index: gather size needed for each term
             for stem,val in bow.iteritems():
                 stem_length[stem] = stem_length.get(stem,0)+ len("(" + str(doc_id) + ":" + str(val) + ");")
        
        #STEP 2 for inv index: compute positions in txt file for each stem
        cur_pos = 0
        pos = {}
        for stem,length in stem_length.iteritems():
            #populate stems dictionary
            self.stems[stem] = (cur_pos, length)

            #store position where to write stem
            pos[stem] = cur_pos
            
            #next stem will be written at the end of current one
            cur_pos += length
            
           
        
        
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
        pos, bow_size,_ = self.docs[doc_id]
        index = open(self.index_file,'r')
        index.seek(pos)
        bow = index.read(bow_size)
        index.close()
        #print "bow-ast : ",bow, ast.literal_eval(bow)
        return ast.literal_eval(bow)
        
    #return document's hyperlinks list (list of doc_ids)    
    def getLinksForDoc(self,doc_id):
        pos, bow_size, links_size = self.docs[doc_id]
        index = open(self.index_file,'r')
        index.seek(pos + bow_size)
        str_links = index.read(links_size)
        index.close()       
        return str_links.split(';')[0:-1]
        
    #return -1 for unknown stem, tf otherwise
    def getTfsForStem(self,stem):

        if not self.stems.has_key(stem):
            print "Unknown stem:" + stem
            return {}

        inv_index = open(self.inv_index_file,"r")
        pos, length = self.stems[stem]
        inv_index.seek(pos)
        ret = inv_index.read(length)
        inv_index.close()
        return self.dict_from_string(ret)

    def getStrDoc(self,doc_id): 
        source_path, position, length = self.docFrom[doc_id];
        source_file = open(source_path,'r')
        source_file.seek(int(position))
        doc = source_file.read(int(length))
        source_file.close()
        return doc
        
    def dict_from_string(self,str):
        t = str[:-1].split(';')
        d = {}
        for e in t:
            splt = e[1:-1].split(':')
            if len(splt) > 1: 
                [id,freq] = splt #e[1:-1].split(':')
                d[int(id)] = int(freq)
        return d
    