# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:30:16 2017

@author: kalifou
"""

class QueryParser(object):

    def __init__(self, query_id, query_text, relevant_docs=None):
        self.query_id = query_id  # ID of the current query       
        self.query_text = query_text # text contained in the query
        self.relevant_docs = relevant_docs # dict of {doc_id : (themes, score)...} of docs relevant to the query
        
    def nextQuery():
        pass

class EvalMeasure(object):
    """Abstract class for query evaluation""" 
    def __init__(self):
        pass
    
    def eval(self,l):
        pass
    
class Eval_P(EvalMeasure):
    """Class for query evaluation using precision-recall""" 
    pass

class Eval_AP(EvalMeasure):
    """Class for query evaluation using average precision-recall""" 
    pass
    
class EvalIRModel(object):

    def __init__(self):
        pass