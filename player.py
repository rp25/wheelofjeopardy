# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 09:35:10 2019

@author: Rajan
"""

#The player class will hold all information regarding a team or player
class player:
    #Each player must have a unique name
    def __init__(self, name):
        self.name = name    
        self.score = 0
        self.highscore = 0
        
    #Returns the name of the player    
    def getName(self):
        return self.name
    
    #Returns the current score of the player
    def getScore(self):
        return self.score
    
    #Returns the highest score the player has achieved 
    def getHighScore(self):
        return self.highscore
  
    #Checks to see if current score is greater than the highest score
    #Sets highscore to current score if true
    def setHighScore(self):
        if(self.score > self.highscore):
            self.highscore = self.score    
    
    #Sets score and check if current score is a highscore
    def setScore(self, score):
        self.score = score
        self.setHighScore()
        
