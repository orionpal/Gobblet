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
        #self.makeRatedMove()
        self.nLookAhead(1)
        
    def nLookAhead(self, n):
        #dumG = copy.deepcopy(game)
        allMoves = self.moves()
        bestSets = []
        bestRate = -99999
        #O(n)
        for ms in allMoves:
            self.makeListMove(ms)
            lm = self.Game.lastMove
            rate = self.minimax(n, False, -99999, 99999)
            if (rate>bestRate):
                bestSets = []
                bestRate = rate
                bestSets.append(ms)
            elif (rate==bestRate):
                bestSets.append(ms)
            self.Game.undoMove(lm)
        
        if (len(bestSets)==0):
            self.makeRandMove
            return True
        bestSet = random.choice(bestSets)
        self.makeListMove(bestSet)
        return True
            
    def minimax(self, n, isMax, alpha, beta):
        if (n==0):
            if (isMax):
                return self.evaluatePos(self.Game.currentPlayer().Color)
            return self.evaluatePos(self.Game.opposition().Color)
        allMoves = self.moves()
        if (isMax):
            bestRate = -99999
            #O(n)
            for ms in allMoves:
                self.makeListMove(ms)
                lm = self.Game.lastMove
                rate = self.minimax(n-1, False, alpha, beta)
                bestRate = max(bestRate, rate)
                alpha = max(alpha, bestRate)
                self.Game.undoMove(lm)
                if (beta<=alpha):
                    break
            return bestRate
        else:
            bestRate = 99999
            #O(n)
            for ms in allMoves:
                self.makeListMove(ms)
                lm = self.Game.lastMove
                rate = self.minimax(n-1, True,alpha, beta)
                bestRate = min(bestRate, rate)
                beta = min(beta, bestRate)
                self.Game.undoMove(lm)
                if (beta<=alpha):
                    break
            return bestRate
        
            
    def makeRatedMove(self):
        allMovs = self.moves()
        pc = self.Game.currentPlayer().Color
        bestrate = -99999
        bestsets = []
        #O(n)
        for ms in allMovs:
            self.makeListMove(ms)
            lm = self.Game.lastMove
            rate = self.evaluatePos(pc)
            if (rate==bestrate):
                bestsets.append(ms)
            elif (rate>bestrate):
                bestrate = rate
                bestsets = []
                bestsets.append(ms)
            self.Game.undoMove(lm)
            
        bestset = random.choice(bestsets)
        self.makeListMove(bestset)
        return True
            
    #makes a random move set
    def makeRandMove(self):
        allMovs = self.moves()
        Moveset = random.choice(allMovs)
        self.makeListMove(Moveset)
        return True

    #rating for player's position on the dumboard only based on pieces on board
    def evaluatePos(self, color):
        Wrate = 0
        Brate = 0
        if (self.Game.checkWin('W')):
            Wrate = Wrate+99999
        if (self.Game.checkWin('B')):
            Brate = Brate+99999
        #rate decrease for invintory
        for i in range(3):
            Wrate = Wrate - self.Game.PlayerW.getTopPiece(i+1).Size*3
            Brate = Brate - self.Game.PlayerB.getTopPiece(i+1).Size*3
        #rate increase for rows
        for y in range(4):
            WCount = []
            BCount = []
            for x in range(4):
                p = self.Game.pieceAt(x,y)
                if (p.Color=='W'):
                    WCount.append(p)
                elif (p.Color=='B'):
                    BCount.append(p)
            for p in WCount:
                Wrate = Wrate + len(WCount)*p.Size
            for p in BCount:
                Brate = Brate + len(BCount)*p.Size
        #rate increase for columns
        for x in range(4):
            WCount = []
            BCount = []
            for y in range(4):
                p = self.Game.pieceAt(x,y)
                if (p.Color=='W'):
                    WCount.append(p)
                elif (p.Color=='B'):
                    BCount.append(p)
            for p in WCount:
                Wrate = Wrate + len(WCount)*p.Size
            for p in BCount:
                Brate = Brate + len(BCount)*p.Size
        
        #rate increase for diagonals
        WCount = []
        BCount = []
        for i in range(4):
            p = self.Game.pieceAt(i,i)
            if (p.Color=='W'):
                WCount.append(p)
            elif (p.Color=='B'):
                BCount.append(p)
        for p in WCount:
            Wrate = Wrate + len(WCount)*p.Size
        for p in BCount:
            Brate = Brate + len(BCount)*p.Size
        WCount = []
        BCount = []
        for i in range(4):
            p = self.Game.pieceAt(3-i,i)
            if (p.Color=='W'):
                WCount.append(p)
            elif (p.Color=='B'):
                BCount.append(p)
        for p in WCount:
            Wrate = Wrate + len(WCount)*p.Size
        for p in BCount:
            Brate = Brate + len(BCount)*p.Size
        
        if (color=='W'):
            return Wrate-Brate
        elif(color=='B'):
            return Brate-Wrate
        return 0
    #returns all possible move sets for one turn, each element in the returned list is a 
    #tuple with the first element being a grabpiece move and the second being a move to a spot on the board
    def moves(self):
#        #Invintory grab moves
#        self.Game.GameBoard.showBoard()
#        self.Game.PlayerW.ShowInv() 
#        self.Game.PlayerB.ShowInv()
        InvGrab = []
        sizes = []
        dumG = copy.deepcopy(self.Game)
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
                    dumG = copy.deepcopy(self.Game)
        movesets = []
        for i in InvGrab:
            for y in range(4):
                for x in range(4):
                    dumG.holdInvP(i)
                    if (dumG.makeMove(x, y)):
                        movesets.append((-1,-1,x,y,i))
                    dumG = copy.deepcopy(self.Game)
                        
        for coor in BoardGrab:
            for y in range(4):
                for x in range(4):
                    dumG.holdBoardP(coor[0],coor[1])
                    if (dumG.makeMove(x, y)):
                        movesets.append((coor[0],coor[1],x,y,-1))
                    dumG = copy.deepcopy(self.Game)
#        self.Game.GameBoard.showBoard() 
#        self.Game.PlayerW.ShowInv() 
#        self.Game.PlayerB.ShowInv()
        return movesets
    
    
    def holdInvP(self, i):
        self.Game.holdInvP(i)
    def holdBoardP(self, x, y):
        self.Game.holdBoardP(x, y)
    def makeMove(self, x, y):
        self.Game.makeMove(x, y)
    def makeListMove(self, moveList): #moveList has form (x1,y1,x2,y2, stacknum)
        if (moveList[0]==-1): #Grab is from Inv
            self.holdInvP(moveList[4])
            self.makeMove(moveList[2],moveList[3])
        else: #if move was from board
            self.holdBoardP(moveList[0], moveList[1])
            self.makeMove(moveList[2],moveList[3])
        
    