# -*- coding: utf-8 -*-
from Index import Index
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
from Weighter import Binary, TF, TF_IDF, Log, Log_plus
from EvalMeasure import EvalIRModel
import numpy as np
import os.path
import time


def plotInterpolatedPrecisionRecall(recall, inter_prec):
    plt.plot(recall, inter_prec)  
    



if __name__ == "__main__":
    t1 = time.time()
    fname = "data/cacm/cacm.txt"
    train_query_file = "data/cacm/cacm_train.qry"
    test_query_file = "data/cacm/cacm_test.qry"
    relevance_file = "data/cacm/cacm.rel"
    
    type = "Okapi" # model_type = Okapi | Language
    if type == "Language":
        eval_platform_language_train = EvalIRModel(fname,train_query_file,relevance_file,model_type="Language")
        eval_platform_language_test = EvalIRModel(fname,test_query_file,relevance_file,model_type="Language")
        #Grid search on language model to find optimal parameter
        grid_language_model = np.arange(0.05,1,0.05) #result = best perfs on test with 0.2
        best_AP = 0
        best_l_term = None
        for l_term in grid_language_model:
            eval_platform_language_train.models[0].l_term = l_term
            _, _, models_AP = eval_platform_language_train.eval_std(verbose=False)
            print "l_term: " + str(l_term) + "giving an AP of: " + str(models_AP["Language Model"])
            if models_AP["Language Model"] > best_AP:
                best_AP = models_AP["Language Model"]
                best_l_term = l_term
        
        #Use best model to find mean AP on test set
        eval_platform_language_test.models[0].l_term = best_l_term
        _, _, models_AP = eval_platform_language_test.eval_std()
        print "Best l_term found on train set:" + str(best_l_term) + ", giving a Mean AP of " + str(models_AP["Language Model"]) + " on test set"
        print "Exec duration(s) : ",time.time()-t1
        
    else: #Okapi
        eval_platform_okapi_train = EvalIRModel(fname,train_query_file,relevance_file,model_type="Okapi")
        eval_platform_okapi_test = EvalIRModel(fname,test_query_file,relevance_file,model_type="Okapi")
        #Grid search on Okapi model to find optimal parameter
        grid_b = np.arange(0.60,0.9,0.05)
        grid_k1 = np.arange(1.,2.1,0.1)
        best_AP = 0
        best_b = None
        best_k1 = None
        for b in grid_b:
            for k1 in grid_k1:
                eval_platform_okapi_train.models[0].b = b
                eval_platform_okapi_train.models[0].k1 = k1
                _, _, models_AP = eval_platform_okapi_train.eval_std(verbose=False)
                print "(b,k1): " +"("+str(b)+","+str(k1)+") giving an AP of: " + str(models_AP["Okapi"])
            if models_AP["Okapi"] > best_AP:
                best_AP = models_AP["Okapi"]
                best_l_term = l_term
        
        #Use best model to find mean AP on test set
        eval_platform_okapi_test.models[0].l_term = best_l_term
        _, _, models_AP = eval_platform_okapi_test.eval_std()
        print "Best (b,k1) found on train set:" +"("+str(best_b)+","+str(best_k1)+ "), giving a Mean AP of " + str(models_AP["Okapi"]) + " on test set"
        print "Exec duration(s) : ",time.time()-t1