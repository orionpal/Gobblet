# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 20:12:28 2019

@author: Orion E. Eman
"""

import Board
import Gobblet
import random
import copy

class AI:
    def __init__(self, Game, memory):
        self.Game = Game
        self.DumGame = copy.deepcopy(self.Game)
        #memory adjustment for more human like interaction
        self.Mem = memory
    def makeRobMove(self):
        self.resetDum()
        #self.makeRandMove()
        self.makeRatedMove()
    def resetDum(self):
        self.DumGame = copy.deepcopy(self.Game)
    
    def makeRatedMove(self):
        allMovs = self.moves()
        pc = self.DumGame.currentPlayer().Color
        
        rate1 = self.evaluatePos1(pc) + self.evaluatePos2(pc)
        bestdiff = 0
        bestset = None
        
        for ms in allMovs:
            self.resetDum()
            for m in ms:
                m(self.DumGame)
            rate2 = self.evaluatePos1(pc) + self.evaluatePos2(pc)
            diff = rate2-rate1
            if (diff>bestdiff):
                bestdiff = diff
                bestset = ms
        if (bestset == None):
            self.makeRandMove()
            return self.Game
        for m in bestset:
            m(self.Game)
        return self.Game
            
    #makes a random move set
    def makeRandMove(self):
        allMovs = self.moves()
        Moveset = random.choice(allMovs)
        for m in Moveset:
            m(self.Game)
        return self.Game

    #rating for player's position on the dumboard only based on pieces on board
    def evaluatePos1(self, color):
        Wrate = 0
        Brate = 0
        
        for y in range(4):
            for x in range(4):
                p = self.DumGame.pieceAt(x,y)
                if (p.Color=='W'):
                    Wrate = Wrate + (p.Size+1)*2
                elif (p.Color=='B'):
                    Brate = Brate + (p.Size+1)*2
        if (color=='W'):
            return Wrate-Brate
        elif(color=='B'):
            return Brate-Wrate
        return (Wrate, Brate)
    #rating for player win
    def evaluatePos2(self, color):
        Wrate = 0
        Brate = 0
        if (self.DumGame.checkWin('W')):
            Wrate = Wrate + 1000
        elif (self.DumGame.checkWin('B')):
            Brate = Brate + 1000
        if (color=='W'):
            return Wrate-Brate
        elif(color=='B'):
            return Brate-Wrate
        return (Wrate, Brate)
    #returns all possible move sets for one turn, each element in the returned list is a 
    #tuple with the first element being a grabpiece move and the second being a move to a spot on the board
    def moves(self):
        self.resetDum()
        #Invintory grab moves
        InvGrab = []
        sizes = []
        #Board grab moves
        BoardGrab = []
        #Grab moves from Inv
        for i in range(3):
            p = self.DumGame.currentPlayer().getTopPiece(i+1)
            if (p.Size not in sizes):
                InvGrab.append(lambda g, i=i: self.holdInvP(i+1, g))
                sizes.append(p.Size)
        #Grab moves from Board
        for y in range(4):
            for x in range(4):
                if (self.DumGame.holdBoardP(x, y)):
                    BoardGrab.append(lambda g, x=x, y=y: self.holdBoardP(x, y, g))
                    self.resetDum()
        movesets = []
        for m in InvGrab:
            for y in range(4):
                for x in range(4):
                    self.resetDum()
                    self.DumGame = m(self.DumGame)
                    if (self.DumGame.makeMove(x, y)):
                        movesets.append((m, lambda g, x=x, y=y: self.makeMove(x, y, g)))
        for m in BoardGrab:
            for y in range(4):
                for x in range(4):
                    self.resetDum()
                    self.DumGame = m(self.DumGame)
                    if (self.DumGame.makeMove(x, y)):
                        movesets.append((m, lambda g, x=x, y=y: self.makeMove(x, y, g)))
        self.resetDum()
        return movesets
    
    def holdInvP(self, i, game):
        game.holdInvP(i)
        return game
    def holdBoardP(self, x, y, game):
        game.holdBoardP(x, y)
        return game
    def makeMove(self, x, y, game):
        game.makeMove(x, y)
        return game