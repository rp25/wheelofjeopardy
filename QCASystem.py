"""
Created on Mon Aug  5 14:00:51 2019
@author: Rajan
"""


import gameDatabase
import gameLogic
import QAL

class QCASystem:
    def __init__(self, name):
        self.name = name    
        self.db = gameDatabase.database('')
        self.gL = gameLogic.gameLogic()

    #add players after db is loaded since it clears players and high scores
    def loadDefaultQCA(self, path = 'default2.p'):
        self.db.loadDB(path)
        
    def addCategory(self, newCat):
         for cat in self.db.categories:
             if(newCat == cat):
                 print('Category already exists!')
                 return False
         self.db.setCategories(newCat)
         return True
             
    #list insert use index system
    def addQA(self, cat, newQAL, level): 
        try:
            self.db.categories[cat].pop(level - 1)
            self.db.categories[cat].insert(level - 1, newQAL)
        except Exception as e:
            print(e)
  
    def addNewPlayer(self, newPlayer): 
         self.db.setPlayers(newPlayer)
             
if __name__ == '__main__':      
    #exec(open("./QAL.py").read())
    a = QCASystem('sys')
    a.loadDefaultQCA()
#    a.addCategory('V')
#    a.addQA('V', ('Q?', 'A', False))
#    print(a.db.getQCA())

