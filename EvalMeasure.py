# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 14:20:28 2017

@author: kalifou
"""
import numpy as np
import sys
import matplotlib.pyplot as plt
from Weighter import Binary, TF, TF_IDF, Log, Log_plus
from IRmodel import Vectoriel, Okapi, LanguageModel
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from Index import Index
from QueryParser import QueryParser

def intersection(l1,l2):
    """Intersection between list l1 & l2"""
    return list(set(l1).intersection(l2))


def removeUnknownStems(Query,Index):
    """Remove unknown stem from query tf"""
    query_tf = Query.getTf()
    for stem in query_tf.keys():
        #if unknown stem remove from query
        if not Index.stems.has_key(stem):
                print "Unknown stem removed: " + stem
                query_tf.pop(stem)

        
class EvalMeasure(object):
    """Abstract class for query evaluation""" 
    def __init__(self):
        pass
    
    def evaluation(self, Query, retrieved_doc):
        """ Evaluate the list l of docs"""
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
        
        interpoled_precision = [max(precision[i:]) for i in xrange(len(precision))]
        return recall, interpoled_precision,precision

class Eval_AP(EvalMeasure):
    """Class for query evaluation using average precision-recall""" 
    def __init__(self):
        pass
    
    def evaluation(self, Query, retrieved_doc):
        relevant_doc = np.array(Query.getRelevantDocs())[:,0]
        retrieved = retrieved_doc[:,0]
        precisions = []
                
        for i,doc in enumerate(xrange(len(retrieved))):
            
            #if current doc is relevant, add current precision
            if str(doc) in relevant_doc:
                precisions.append(self.getNumRecall(relevant_doc, retrieved[0:i+1]) / (i+1))
                
        #average precision
        return 0 if len(precisions) == 0 else sum(precisions) / float(len(precisions))
 
class EvalIRModel(object):
    
    def plot_(self,recall, interpolated_prec,precision):
        """Plotting Both : simple & interpolated precision - recall curve"""
        fig = plt.figure() #(figsize=(9,7))
        fig.suptitle('Precision - Recall',fontsize=15)
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.plot(recall,precision, 'b-',label="precision")
        plt.plot(recall,interpolated_prec, 'r',label="interpolated precision")
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()
        
    def __init__(self, index_file, query_file, relevance_file,type="Vectoriel"):
        """ type = Vectoriel | Okapi"""
        
        parser = ParserCACM()
        textRepresenter = PorterStemmer()
        I = Index(parser,textRepresenter)
        I.indexation(index_file)
        I.parser = None
        
        self.Index = I
        
        if type  == "Vectoriel":
            weighters = [Binary(I), TF(I), TF_IDF(I), Log(I), Log_plus(I)]     
            self.models = [Vectoriel(True, w) for w in weighters]
        if type == "LanguageModel":
            self.models = [LanguageModel(I,0.9)]
        else :
            self.models = [Okapi(I)]
            
        self.query_file = query_file
        self.relevance_file = relevance_file
        self.query_parser = QueryParser(self.query_file, self.relevance_file)  
    
    def eval_std(self):  
        """ Evaluate the a set of query using a set of different Vector Models 
            Todo : calculate mean & std of each model on the whole query dataset
            DRAFT !
        """
        
        sys.stdout.write("Evaluation of our models ...")
        print '\n'
        Eval = Eval_P()
        EvalAP = Eval_AP()
        
        recall_model_i = dict() # {model_i:(recall,mean)}
        prec_model_i = dict()
        
        for i,m in enumerate(self.models):
            query_result = 0
            self.query_parser = QueryParser(self.query_file, self.relevance_file)
            Q = self.query_parser.nextQuery()
        
            while (Q != -1):
                
                print "\n\nModel : ", m.getName()
                query_result = m.getRanking(Q.getTf())
                recall, interpolated_prec,precision = Eval.evaluation(Q, query_result)
                #Display first 10 values to see performances
                print 'recall :', recall[0:10]
                print 'precision : ',precision[0:10]
                print 'inter_precision : ',interpolated_prec [0:10]
                self.plot_(recall, interpolated_prec,precision) 
                average_precision = EvalAP.evaluation(Q, query_result)
                print 'AP: ', average_precision
                Q = self.query_parser.nextQuery()
                
            recall_model_i[i] = ()
            prec_model_i[i] = ()
        
    def eval(self): 
        """ Ploting Interpolated Precision-recall for a set of models """
        
        sys.stdout.write("Evaluation of our models ...")
        print '\n'
        Eval = Eval_P()
        EvalAP = Eval_AP()
        
        query_result = 0
        Q = self.query_parser.nextQuery()
        while (Q != -1):
            removeUnknownStems(Q, self.Index)
            for i,m in enumerate(self.models):
                print "\n\nModel : ", m.getName()
                query_result = m.getRanking(Q.getTf())
                recall, interpolated_prec,precision = Eval.evaluation(Q, query_result)
                #Display first 10 values to see performances
                print 'recall :', recall[0:10]
                print 'precision : ',precision[0:10]
                print 'inter_precision : ',interpolated_prec [0:10]
                self.plot_(recall, interpolated_prec,precision) 
                average_precision = EvalAP.evaluation(Q, query_result)
                print 'AP: ', average_precision
            Q = self.query_parser.nextQuery()