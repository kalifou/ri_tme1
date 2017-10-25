# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:30:16 2017

@author: kalifou, portelas
"""
from TextRepresenter import PorterStemmer
from ParserCACM import ParserCACM
import numpy as np

class Query(object):
    def __init__(self, query_id, query_text, query_tf, relevant_docs=None):
        self.query_id = query_id  # ID of the current query       
        self.query_text = query_text # text contained in the query
        self.query_tf = query_tf
        self.relevant_docs = relevant_docs # dict of {doc_id : (themes, score)...} of docs relevant to the query
        
    def getId(self):
        return self.query_id
    
    def getText(self):
        return self.query_text
    
    def getTf(self):
        return self.query_tf
    
    def getRelevantDocs(self):
        return self.relevant_docs

class QueryParser(object):
    """Class for query reading from file""" 
    def __init__(self, query_file, relevance_file):
        self.query = open(query_file, 'r')
        self.textRepresenter = PorterStemmer()
        
        #init boolean to be able to close source files
        self.already_closed = False
        
        #Create parser to read query_file
        #WARNING WILL ONLY WORK ON CACM DATASET TODO FIND SOLUTION
        self.parser = ParserCACM()
        self.parser.initFile(query_file)
        
        #Build a dictionary (query_id, list of relevant documents)
        #TODO ASK IF OK TO LOAD ALL THIS, SHOULD WE NOT READ ONE BY ONE ?  
        self.relevant_docs = {}
        with open(relevance_file, 'r') as f:
            for line in f:
                data = line.split(" ")
                query_id = int(data[0])
                if(not self.relevant_docs.has_key(query_id)):
                    self.relevant_docs[query_id] = []
                #A list is added per relevant doc for later use of couple (themes, score) 
                self.relevant_docs.get(query_id).append([ data[1], None, None])
                
    def nextQuery(self):
        """Return next Query object"""
        
        query_data = self.parser.nextDocument()
        
        if (query_data == None):
            if( not self.already_closed ):
                self.query.close()
                self.already_closed = True
                return -1
        
        query_id = query_data.getId()
        query_text = query_data.getText()
        query_tf = self.textRepresenter.getTextRepresentation(query_text)
        return Query(query_id, query_text, query_tf, np.array(self.relevant_docs[int(query_id)]))


class EvalMeasure(object):
    """Abstract class for query evaluation""" 
    def __init__(self):
        pass
    
    def eval(self,l):
        pass
   
class Eval_P(EvalMeasure):
    """Class for query evaluation using precision-recall""" 
    def __init__(self):
        pass
    
    def getRecall(self, i, relevant_docs, doc_list):
        """Compute recall for given query and sorted (document, score) list"""
        return len(np.intersect1d(relevant_docs[:,0], doc_list)) / len(relevant_docs)
         
    def evaluation(self, Query, retrieved_doc):
        relevant_doc = np.array(Query.getRelevantDocs())
        #Compute precision-recall
        recall = []
        interpoled_precision = []
        for i in xrange(len(retrieved_doc)):
            interpoled_precision.append(0)
            recall.append(self.getRecall(i, relevant_doc, retrieved_doc))
        return recall, interpoled_precision

class Eval_AP(EvalMeasure):
    """Class for query evaluation using average precision-recall""" 
    pass
    
class EvalIRModel(object):

    def __init__(self):
        pass