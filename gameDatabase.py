# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 10:16:59 2019

@author: Rajan
"""

#standard built in python libraries currently used or maybe used in the future
import pickle
import pandas as pd
import numpy as np

#database objec will hold all game related data including answers, categories, 
# suggested question, scores, high scores, and current players
class database:
    #creates a database object with a given name
    def __init__(self, name):
        self.name = name    
        self.QCA = {}
        #Limit to 3 players
        self.players = {} #only store current game players and score {'player': intScore}
        self.scores = {} #store higest scores for each player from all games  {'player': intScore}
    
    # Returns the name of the database
    def getName(self):
        return self.name
    #Returns a dictionary containing suggested questions, answers, and categories
    def getQCA(self):
        return self.QCA
    #Returns a dictionary of current players and their current score
    def getPlayers(self):
        return self.name
    #Returns a dictionary of highest score for each player from all games played
    def getScores(self):
        return self.scores
    #Allows a function or obj to change the name of the database
    def setName(self, name):
        self.name = name
    #Allows a function or obj to change the suggested questions, answers, and categories dictionary
    def setQCA(self, cat, QAList):
        self.QCA[cat] = QAList
    #Allows a function or object to change the players and their score
    def setPlayers(self, players):
       self.players = players
    #Allows a function or object to change the players and thier high score
    def setScores(self, scores):
        self.scores = scores
    #Function to add new   questions, answers, and categories  
    def addQCA(self, QCA):
        pass
    #Returns all available Categories    
    def getAllCategories(self):
        return self.QCA.keys()
    #Returns all current players
    def getAllCurrentPlayers(self):
        return self.players.keys()
    #loads existing database from previous game or a saved game    
    def loadDB(self, path):
        db = pickle.load(open(path, "rb"))
        self.QCA = db['QCA']
        self.players = db['players']
        self.scores = db['scores']
    #saves database to save game state and resume at a later time        
    def saveDB(self, path):
        database = {'QCA' : self.QCA, 'players' : self.players, 'scores' : self.scores}
        pickle.dump(database, path + self.name + '.p')
