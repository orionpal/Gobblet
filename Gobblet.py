# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 22:56:04 2018

@author: Orion Palaquibay
"""
import Board
#All game actions will be done on main game board, when it is called the game will play until someone wins
class GobbletGame:
    def __init__(self, PlayerW, PlayerB):
        self.PlayerW = PlayerW
        self.PlayerB = PlayerB
        self.GameBoard = Board(PlayerW, PlayerB)
        self.Holding = None
        self.fromBoard = False
    
    def holdInvP(self, stacknum):
        if (self.fromBoard==False):
            self.Holding = self.GameBoard.currentPlayer.getTopPiece(stacknum)
        else:
            print("you're holding a piece from the board")
        
    def holdBoardP(self, x, y):
        if (self.fromBoard==False):
            if (self.GameBoard.pieceAt(x, y).Color==self.GameBoard.currentPlayer.Color):
                self.Holding = self.GameBoard.grabFromBoard(x, y)
                self.fromBoard = (x, y)
            else:
                print("that's not your piece")
        else:
            print("you're already holding a piece from the board")
        
    def makeMove(self, x, y):
        if (self.fromBoard==False):
            if (self.GameBoard.movFromInv(self.Holding, x, y)):
                self.GameBoard.nextTurn()
                self.Holding = None
                return True
            return False
        if (self.fromBoard!=False):
            if (self.fromBoard[0]!=x and self.fromBoard[1]!=y):
                if (self.GameBoard.movFromBoard(self.Holding, x, y)):
                    self.GameBoard.nextTurn()
                    self.Holding = None
                    self.fromBoard = False
                    return True
        return False
    def winner(self):
        return self.GameBoard.checkWin()
#-------------------------------------------------------------------

