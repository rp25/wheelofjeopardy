# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 10:58:33 2019

@author: Rajan
"""
import pickle


class database:
    #creates a database object with a given name
    def __init__(self, name):
        self.name = name    
        self.categories = {}
        self.allPlayers = []
        self.currentPlayers = []
        self.round = 1    
        self.spin = 0
        
    #Returns the name of the database    
    def getName(self):
        return self.name
    
    #Returns the categories of the database    
    def getCategories(self):
        return self.categories
    
    #Used to modify database name
    def setName(self, name):
        self.name = name
        
    #Used to add categories to the database    
    def setCategories(self, category):
        self.categories[category] = None
        
    #Used to add new players
    #Checks to see if player exists    
    def setPlayers(self, newPlayer):
        for player in self.currentPlayers:
            if(newPlayer.getName() == player.getName()):
                print('Player already exist!')
                return False
            
        self.currentPlayers.append(newPlayer)
        return True
            
    #After game has ended add current players to allplayers
    #Sets score to zero      
    def updateAllPLayer(self):
        for currentPlayer in self.currentPlayers:
            for player in self.allPlayers:
                currentPlayer.setScore(0)
                if(currentPlayer.getName() == player.getName()):
                    index = list.index(player)
                    self.allPlayers.pop(index)
                    self.allPlayers.append(currentPlayer)
                else:
                    self.allPlayers.append(currentPlayer)
                    
    #Used to change round of game
    def setRound(self, roundNum):
        self.round = roundNum
        
    #Used to change spin count of game
    def setSpin(self, spinNum):
        self.spin = spinNum
    
    #Returns current players
    def getCurrentPlayers(self):
        return self.currentPlayers
    
    #Returns current game round
    def getRound(self):
        return self.round
    
    #Returns current spin count
    def getSpin(self):
        return self.spin
    
    #???
    def getNumPlayer(self):
        pass
    
    #Exports database to a pickle file
    def exportDB(self, path):
        database = {'name' : self.name, 'categories' : self.categories, 'allPlayers' : self.allPlayers,
                    'currentPlayers' : self.currentPlayers, 'round' : self.round, 'spin' : self.spin,}
        pickle.dump(database, open(path + self.name + '.p', 'wb'))
    
    #loads database from a pickle file
    def loadDB(self, path):
        
        db = pickle.load(open(path, "rb"))
        self.name = db['name']  
        self.categories = db['categories']
        self.allPlayers = db['allPlayers']
        self.currentPlayers = db['currentPlayers']
        self.round = db['round']
        self.spin = db['spin']
        
