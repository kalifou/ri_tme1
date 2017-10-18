# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 18:43:53 2017

"""
import Weighter

class IRmodel(object):
    
    def __init__(self):
        pass

    def getScores(self,query):
        pass

    def getRanking(self,query):
        pass

class Vectoriel(object):

    def __init__(self,normalized,index):
        self.normalized = normalized
        self.weighter = Weighter(index)

    def getScores(self,query):

        if self.normalized :
            pass

        else :
            pass