'''
Created on 10 Aug 2017

@author: chrischne
'''
import json

class Fitness(object):
    '''
    classdocs
    '''
    default_score = 2

    def __init__(self,configfile):
        '''
        Constructor
        '''
        with open(configfile) as data_file:    
            self.score = json.load(data_file)
            #print(self.score)
    
    
    def fitness(self,asps):
        fit = {
            'love': self.default_score,
            'passion': self.default_score,
            'communication': self.default_score
        }
                       
        for asp in asps:
            score = self.getScore(asp)
            
            fit['love'] += score['love']
            fit['passion'] += score['passion']
            fit['communication'] += score['communication']
            
        return fit;

    def getScore(self,asp):
        #try both possibilites
        #sun_conjunciton_mercury
        #mercury_conjunction_sun
        aspstring1 = self.genAspectString(asp['planet1'],asp['aspect'],asp['planet2']);
        aspstring2 = self.genAspectString(asp['planet2'],asp['aspect'],asp['planet1']);

        aspects = self.score['aspects']
        
        if aspstring1 in aspects:
            return aspects[aspstring1]    
        
        elif aspstring2 in aspects:
            return aspects[aspstring2]

        else:
            return self.score['none']; 
        

    def genAspectString(self,p1,asp,p2):
        return p1 + "_" + asp + "_" + p2
    