# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 14:20:28 2017

@author: kalifou
"""
import numpy as np

def intersection(l1,l2):
    """Intersection between list l1 & l2"""
    return list(set(l1).intersection(l2))
    
class EvalMeasure(object):
    """Abstract class for query evaluation""" 
    def __init__(self):
        pass
    
    #def eval(self,l): # TO BE REMOVED ?!
    #    pass 
    
    def evaluation(self, Query, retrieved_doc):
        pass
    
    def getNumRecall(self, relevant_doc, retrieved_doc):
        """Compute recall for given query and sorted (document, score) list"""
        #print "Relevant : ", relevant_doc
        #print "\n\nRetrived : ", retrieved_doc,'\n\n'
        #print "intersect : ", intersection(relevant_doc,retrieved_doc),'\n\n'
        return float(len(intersection(relevant_doc,retrieved_doc)))
    

class Eval_P(EvalMeasure):
    """Class for query evaluation using precision-recall""" 
    def __init__(self):
        pass
        
    def evaluation(self, Query, retrieved_doc):
        relevant_doc = np.array(Query.getRelevantDocs())[:,0]
        retrieved = np.array( retrieved_doc )[:,0]
        recall = []
        precision = []
        N_retrived = len(retrieved)
        N_relevant = len(relevant_doc)
        print N_relevant,N_retrived
        for i in xrange(N_retrived):
            
            numerator = self.getNumRecall(relevant_doc, retrieved[0:i+1])
            precision.append( numerator /(i+1)) # simple precision meas.
            recall.append(  numerator/ N_relevant ) # simple recall meas.
        
        interpoled_precision = [max(precision[0:i+1]) for i in xrange(len(precision))]
        return recall, interpoled_precision,precision

class Eval_AP(EvalMeasure):
    """Class for query evaluation using average precision-recall""" 
    def __init__(self):
        pass
    
    def evaluation(self, Query, retrieved_doc):
        relevant_doc = np.array(Query.getRelevantDocs())[:,0]
        retrieved = retrieved_doc[:,0]
        precisions = []
        
        #print relevant_doc
        for i,doc in enumerate(xrange(len(retrieved))):
            
            #if current doc is relevant, add current precision
            if str(doc) in relevant_doc:
                precisions.append(self.getNumRecall(relevant_doc, retrieved[0:i+1]) / (i+1))
                
        #average precision
        return 0 if len(precisions) == 0 else sum(precisions) / float(len(precisions))
               
class EvalIRModel(object):

    def __init__(self):
        pass