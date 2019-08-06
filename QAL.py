# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:57:21 2019

@author: Rajan
"""

#This class creates a QAL object (Question, Answer, Level)
class QAL:
    #Each QAL object requires a question, answer and level
    def __init__(self, question, answer, level):
        self.question = question
        self.answer = answer
        self.level = level
        #This will be used during gamepaly so show that a Q/A pair has already been used
        self.used = False
        #Records the freq
        self.freq = 0
        
    #Used to modify a question    
    def setQuestion(self, question):
        self.question = question
    
    #Used to modify an answer
    def setAnswer(self, answer):
        self.answer = answer
    
    #Used to modify a level    
    def setLevel(self, level):
        self.level = level
    
    #Modify when a certain QAL object has been used
    def setUsed(self, used):
        self.used = used
        
    #Increment by one when a QAL object is used    
    def setFreq(self, freq):
        self.freq = freq
        
    #Returns question from obj    
    def getQuestion(self):
        return self.question
    
    #Returns answers from obj
    def getAnswer(self):
        return self.answer
    
    #Returns level from obj 
    #This will be used to determine the amount of points a QAL is worth
    def getLevel(self):
        return self.level
    
    #Once a question is used in a game this 
    def getUsed(self):
        self.used
        
    #Amy be used to get how frequently a QAL has been selected    
    def getFreq(self):
        return self.freq
        
    