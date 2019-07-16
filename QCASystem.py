"""
Created on Mon Jul 15 10:16:26 2019
@author: Rajan
"""

import pandas as pd
import gameDatabase

class QCAL():
    def __init__(self, q, c, a, l):
        self.question = q
        self.category = c
        self.answer = a
        self.level = l
        self.used = False
        self.index = None

class QCASystem:
    
    def __init__(self, name):
        self.name = name    
        self.db = gameDatabase.database('default')

    #add players after db is loaded since it clears players and high scores
    def loadDefaultQCA(self, path = 'default.p'):
        self.db.loadDB(path)
        
    def addCategory(self, cat):
         if(cat not in self.db.getAllCategories()):
             self.db.getQCA()[cat] = []
         else:
             print('Category already exist')
             
    def addQA(self, cat, QA): #('Q', 'A', False)
         if(cat in self.db.getAllCategories()):
             #self.db[cat].append(QA)
             temp = self.db.getQCA()[cat] 
             temp.append(QA)
             self.db.setQCA(cat, temp)

         else:
             print('Category does not exist')
              
    def addNewPlayer(self, newPlayer): #('Q', 'A', False)
         if(newPlayer not in self.db.getAllCurrentPlayers()):
             temp = self.db.getPlayers() 
             temp[newPlayer] = 0
             self.db.setPlayers(temp)
         else:
             print('Player already exist')
             
             
a = QCASystem('sys')
a.loadDefaultQCA()
a.addCategory('V')
a.addQA('V', ('Q?', 'A', False))
print(a.db.getQCA())
