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
from collections import defaultdict
from Index import Index
from QueryParser import QueryParser
import os.path
import pickle

def intersection(l1,l2):
    """Intersection between list l1 & l2"""
    #print 'L1 : ',l1
    #print 'L2 : ',l2
    #print "Inter : ",list(set(l1).intersection(l2))
    assert(isinstance(l1[0],int))
    print "type :", type(l2[0])
    assert(isinstance(l2[0],int))
    return list(set(l1).intersection(l2))


def removeUnknownStems(Query,Index):
    """Remove unknown stem from query tf"""
    query_tf = Query.getTf()
    for stem in query_tf.keys():
        #if unknown stem remove from query
        if not Index.stems.has_key(stem):
                print "Unknown stem removed: " + stem
                query_tf.pop(stem)

def initIndex(database_file):
    """Init Index or load it if previously computed"""
    sys.stdout.write("Indexing database...")
    sys.stdout.flush()
    if os.path.isfile('Index.p'):
       I = pickle.load( open( "Index.p", "rb" ) ) 
    
    else:
        parser = ParserCACM()
        textRepresenter = PorterStemmer()
        I = Index(parser,textRepresenter)
        I.indexation(database_file)
        I.parser = None
        pickle.dump( I, open( "Index.p", "wb" ) )
        
    sys.stdout.write("Done!\n")
    sys.stdout.flush()
    
    return I

def initModels(I,modelType):
    """Init Models of type modelType or load if already computed"""
    
    model_file_name = modelType + '.p'
    
    sys.stdout.write("Creating models...")
    sys.stdout.flush()
    
    if os.path.isfile(model_file_name):
        models = pickle.load( open( model_file_name, "rb" ) )
        
    elif modelType == "Vectoriel":
        weighters = [Binary(I), TF(I), TF_IDF(I), Log(I), Log_plus(I)]
        models = [Vectoriel(Index,True, w) for w in weighters]
        pickle.dump( models, open( model_file_name, "wb" ) )
    
    else:
        print "Unknown model type ABORT THE MISSION"
    
    sys.stdout.write("Done!\n")
    
    return models
        
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
        retrieved = np.array( retrieved_doc ,dtype=int)[:,0]
        recall = []
        precision = []
        N_retrieved = len(retrieved)
        N_relevant = len(relevant_doc)
        #print N_relevant,N_retrieved
        for i in xrange(N_retrieved):
            
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
        retrieved = np.array(retrieved_doc,dtype=int)[:,0]
        precisions = []
                
        for i,doc in enumerate(xrange(len(retrieved))):
            
            #if current doc is relevant, add current precision
            if str(doc) in relevant_doc:
                print "i,rd,retr,nmRecal :",i,relevant_doc,retrieved,self.getNumRecall(relevant_doc, retrieved[0:i+1]) / (i+1.)
                
                precisions.append(self.getNumRecall(relevant_doc, retrieved[0:i+1]) / (i+1))
                
        print "prec :",precisions
        #average precision
        return 0 if len(precisions) == 0 else np.mean(precisions)
 
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
        
    def __init__(self, index_file, query_file, relevance_file,model_type="Vectoriel"):
        """ model_type = Vectoriel | Okapi | Language """

        self.Index = initIndex(index_file)
        self.Index
        
        if model_type  == "Vectoriel":
            self.models = initModels(self.Index,model_type)
            
        elif model_type == "Language":
            self.models = [LanguageModel(self.Index,0.9)]
        else :
            self.models = [Okapi(self.Index)]
            
        self.query_file = query_file
        self.relevance_file = relevance_file
        self.query_parser = QueryParser(self.query_file, self.relevance_file)  
    
    def eval_std(self, verbose=True):  
        """ Evaluate the a set of query using a set of different Vector Models 
            Todo : calculate mean & std of each model on the whole query dataset
            DRAFT !
        """
        
        sys.stdout.write("Evaluation of our models ...")
        print '\n'
        Eval = Eval_P()
        EvalAP = Eval_AP()
        
        models_recall = defaultdict(list)
        models_inter_prec = defaultdict(list)
        models_prec = defaultdict(list)
        models_AP = defaultdict(float)
        
        for i,m in enumerate(self.models):
            
            m_name = m.getName()
            if verbose:
                print "\n\nModel : ", m_name
            
            query_result = 0
            query_nb = 0
            self.query_parser = QueryParser(self.query_file, self.relevance_file)
            Q = self.query_parser.nextQuery()
            query_nb += 1
            while (Q != -1):
                
                query_result = m.getRanking(Q.getTf())
                recall, interpolated_prec, prec = Eval.evaluation(Q, query_result)
                
                #accumulate results
                if not models_recall.has_key(m_name):
                    models_recall[m_name] = np.array(recall)
                    models_inter_prec[m_name] = np.array(interpolated_prec)
                    models_prec[m_name] = np.array(prec)
                    models_AP[m_name] = EvalAP.evaluation(Q, query_result)
                else:
                    print len(recall),len(models_recall[m_name])
                    models_recall[m_name] += np.array(recall)
                    models_inter_prec[m_name] += np.array(interpolated_prec)
                    models_prec[m_name] += np.array(prec)
                    models_AP[m_name] += EvalAP.evaluation(Q, query_result)

                Q = self.query_parser.nextQuery()
                query_nb += 1
               
            #average results for model
            models_recall[m_name] /= query_nb
            models_inter_prec[m_name] /= query_nb
            models_prec[m_name] /= query_nb
            models_AP[m_name] /= query_nb
            
            if verbose:
                self.plot_(models_recall[m_name], models_inter_prec[m_name], models_prec[m_name])
                print 'AP: ',  models_AP[m_name]
            
        return models_recall, models_inter_prec, models_AP
        
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
                print Q.getText() 

                query_result = m.getRanking(Q.getTf())
                recall, interpolated_prec,precision = Eval.evaluation(Q, query_result)
                #Display first 10 values to see performances
                #print 'recall :', recall[0:10]
                #print 'precision : ',precision[0:10]
                #print 'inter_precision : ',interpolated_prec [0:10]
                self.plot_(recall, interpolated_prec,precision) 
                average_precision = EvalAP.evaluation(Q, query_result)
                print 'AP: ', average_precision
            Q = self.query_parser.nextQuery()