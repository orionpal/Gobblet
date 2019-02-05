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
        #memory adjustment for more human like interaction
        self.Mem = memory
        
    def makeRobMove(self):
        #self.makeRatedMove(self.Game)
        self.nLookAhead(1, self.Game)
        
    def nLookAhead(self, n, game):
        #dumG = copy.deepcopy(game)
        allMoves = self.moves(game)
        bestSets = []
        bestRate = -99999
        #O(n)
        for ms in allMoves:
            self.makeListMove(ms, game)
            lm = game.lastMove
            count = 0
            rate = self.minimax(n, game, False,count)
            #print(count)
            if (rate>bestRate):
                bestSets = []
                bestRate = rate
                bestSets.append(ms)
            elif (rate==bestRate):
                bestSets.append(ms)
            game.undoMove(lm)
            
        bestSet = random.choice(bestSets)
        self.makeListMove(bestSet, game)
        return game
            
    def minimax(self, n, game, isMax, count):
        if (n==0):
            if (isMax):
                return self.evaluatePos(game.currentPlayer().Color, game)
            return self.evaluatePos(game.opposition().Color, game)
        allMoves = self.moves(game)
        if (isMax):
            rate = -99999
            #O(n)
            for ms in allMoves:
                self.makeListMove(ms, game)
                lm = game.lastMove
                count = count+1
                rate = max(rate, self.minimax(n-1, game, False, count))
                game.undoMove(lm)
            #print(n)
            #print("moves considered: " + str(count))
            return rate 
        else:
            rate = 99999
            #O(n)
            for ms in allMoves:
                self.makeListMove(ms, game)
                lm = game.lastMove
                count = count+1
                rate = min(rate, self.minimax(n-1, game, True, count))
                game.undoMove(lm)
            #print(n)
            #print("moves considered: " + str(count))
            return rate
        
            
    def makeRatedMove(self, game):
        allMovs = self.moves(game)
        pc = game.currentPlayer().Color
        bestrate = -99999
        bestsets = []
        #dumG = copy.deepcopy(game)
        #O(n)
        for ms in allMovs:
            self.makeListMove(ms, game)
            lm = game.lastMove
            rate = self.evaluatePos(pc, game)
            if (rate==bestrate):
                bestsets.append(ms)
            elif (rate>bestrate):
                bestrate = rate
                bestsets = []
                bestsets.append(ms)
            game.undoMove(lm)
            
        bestset = random.choice(bestsets)
        self.makeListMove(bestset, game)
        return game
            
    #makes a random move set
    def makeRandMove(self, game):
        allMovs = self.moves(game)
        Moveset = random.choice(allMovs)
        self.makeListMove(Moveset, game)
        return game

    #rating for player's position on the dumboard only based on pieces on board
    def evaluatePos(self, color, game):
        Wrate = 0
        Brate = 0
        if (game.checkWin('W')):
            Wrate = Wrate+1000
        if (game.checkWin('B')):
            Brate = Brate+1000
        
        for y in range(4):
            for x in range(4):
         #       print (str(x)+", " +str(y))
                p = game.pieceAt(x,y)
                if (p.Color=='W'):
                    Wrate = Wrate + (p.Size+1)*2
                elif (p.Color=='B'):
                    Brate = Brate + (p.Size+1)*2
        #print("Wrate: " + str(Wrate))
        #print("Brate: " + str(Brate))
        
        if (color=='W'):
            return Wrate-Brate
        elif(color=='B'):
            return Brate-Wrate
        return 0
    #returns all possible move sets for one turn, each element in the returned list is a 
    #tuple with the first element being a grabpiece move and the second being a move to a spot on the board
    def moves(self, game):
        #Invintory grab moves
        dumG = copy.deepcopy(game)
        InvGrab = []
        sizes = []
        #Board grab moves
        BoardGrab = []
        #Grab moves from Inv
        for i in range(3):
            p = dumG.currentPlayer().getTopPiece(i+1)
            if (p.Size not in sizes):
                InvGrab.append(i+1)
                sizes.append(p.Size)
        #Grab moves from Board
        for y in range(4):
            for x in range(4):
                if (dumG.holdBoardP(x, y)):
                    BoardGrab.append((x,y))
                    dumG = copy.deepcopy(game)
        movesets = []
        for i in InvGrab:
            for y in range(4):
                for x in range(4):
                    dumG = copy.deepcopy(game)
                    self.holdInvP(i, dumG)
                    if (dumG.makeMove(x, y)):
                        movesets.append((-1,-1,x,y,i))
        for coor in BoardGrab:
            for y in range(4):
                for x in range(4):
                    dumG = copy.deepcopy(game)
                    self.holdBoardP(coor[0],coor[1], dumG)
                    if (dumG.makeMove(x, y)):
                        movesets.append((coor[0],coor[1],x,y,-1))
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
    def makeListMove(self, moveList, game): #moveList has form (x1,y1,x2,y2, stacknum)
        if (moveList[0]==-1): #Grab is from Inv
            self.holdInvP(moveList[4], game)
            self.makeMove(moveList[2],moveList[3], game)
        else: #if move was from board
            self.holdBoardP(moveList[0], moveList[1], game)
            self.makeMove(moveList[2],moveList[3], game)
        
    