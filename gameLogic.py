# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:06:03 2019

@author: Rajan
"""

import gameDatabase
import player
import random

class gameLogic:
    
    def __init__(self):
        self.defaultSectors = []
        self.db = gameDatabase.database('')
        self.player = player.player()
 
    #check with the team if returning # is sufficient here   
    def getOneSector():
        sector = random.randint(0, 11)
        return sector
       
    #increment the player's turn count
    def freeTurn(self, player):
        player.setTurn(1)
    
    # if the selected sector is 7
    def loseTurn(self, player):
        player.setTurn(-1)
        
    #player loses all points and the turn
    #"free turn" cannot be used    
    def bankrupt(self, player):
        player.setScore(0)
    
    #double the player's score
    def doubleScore(self, player):
        curScore = player.getScore()
        double = curScore*2
        player.setScore(double)
        
    #players to choose which category to answer
    def playerChoice(self, player):
        pass
        #handle in QCAsystem?
    
    #players opponent gets to choose which category to answer
    def opponentChoice(self, player, allPlayers):
        pass
        #handle in QCAsystem?        
    
    #max of 50 spins in each round; max 2 rounds per game
    def changeRound(self):
        curSpin = db.getSpin()
        if (curSpin >= 50): 
          db.setRound(2)
        
    