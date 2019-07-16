# -*- coding: utf-8 -*-
import pickle
import numpy as np
import random

# gamelogic object will hold 12 predefined sectors and handle all game related logics associated with each sector. 
class gamelogic:
    
    def __init__(self):
        # For the mininum system - read the category data from the QCAsystem (6 sectors)
        self.sectors = ['category 1', 'category 2', 'category 3', 'category 4', 'category 5', 'category 6', 
        'lose', 'free', 'bankrupt', 'pchoice', 'ochoice', 'double']
        
    # Return a randomized sector when the player spins the wheel 
    def getOneSector(self):
        random_pick = random.choice(self.sectors)
        
        # For the skeletal system - return the random_pick from the list
        # For the minumum system - return the random_pick by calling its sub function 
        return random_pick
    
    # Return the name of the sector and one category randomly selected   
    def getCategories(self):
        # Read the category data from the QCAsystem (6 sectors)
        # Randomize the category data and select one to return
        pass
        
    # Return the name of the sector and allow the player to use the "FreeTurn" token if exists
    def loseTurn(self):
        pass
        
    # Return the name of the sector and reward the player with a "FreeTurn" token
    def freeTurn(self):
        pass
        
    # Return the name of the sector and take away oall of the player's current score (stored in the QCAsystem). Do not allow "Free Turn" token to be used
    def bankrupt(self):
        pass
        
    # Return the name of the sector and allow the player to choose a category to answer
    def playerChoice(self):
        pass
        
    # Return the name of the sector and allow the player's opponent to select a category     
    def opponentChoice(self):
        pass
        
    # Return the name of the sector and double the score stored in the QCAsystem   
    def doubleScore(self):
        pass