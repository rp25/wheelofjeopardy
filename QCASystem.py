# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:00:51 2019

@author: Rajan
"""


import pandas as pd
import gameDatabase
import gameLogic
import QAL
    
class QCASystem:
    def __init__(self, name):
        self.name = name    
        self.db = gameDatabase.database('newDefault')
        self.gL = gameLogic.gameLogic()

    #add players after db is loaded since it clears players and high scores
    def loadDefaultQCA(self, path = 'newDefault.p'):
        self.db.loadDB(path)
        
    def addCategory(self, newCat):
         for cat in self.db.categories:
             if(newCat == cat):
                 print('Category already exists!')
                 return False
         db.setCategories(category)
         return True
             
    #list insert use index system
    def addQA(self, cat, QAL, level): 
        try:
            db.categories[cat].pop(level - 1)
            db.categories[cat].insert(level - 1, QAL)
        except Except as e:
            print(e)
  
    def addNewPlayer(self, newPlayer): 
         db.setPlayers(newPlayer)
             
if __name__ == '__main__':             
    a = QCASystem('sys')
    a.loadDefaultQCA()
#    a.addCategory('V')
#    a.addQA('V', ('Q?', 'A', False))
#    print(a.db.getQCA())
