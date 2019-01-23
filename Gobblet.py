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
        self.GameBoard = Board.Board(PlayerW, PlayerB)
        self.Holding = Board.Piece('X', -1)
        self.fromBoard = False
    
    def currentPlayer(self):
        return self.GameBoard.currentPlayer
    
    def checkWin(self, color):
        return self.GameBoard.checkWin(color)
    
    def pieceAt(self, x, y):
        return self.GameBoard.pieceAt(x, y)
    
    def holdInvP(self, stacknum):
        if (self.fromBoard==False):
            self.Holding = self.GameBoard.currentPlayer.getTopPiece(stacknum)
            return True
        else:
            #print("you're holding a piece from the board")
            return False
        
    def holdBoardP(self, x, y):
        if (self.fromBoard==False):
            if (self.GameBoard.pieceAt(x, y).Color==self.GameBoard.currentPlayer.Color):
                self.Holding = self.GameBoard.grabFromBoard(x, y)
                self.fromBoard = (x, y)
                return True
            else:
                #print("that's not your piece")
                return False
        else:
            #print("you're already holding a piece from the board")
            return False
        
    def makeMove(self, x, y):
        if (self.fromBoard==False):
            if (self.GameBoard.movFromInv(self.Holding, x, y)):
                self.GameBoard.nextTurn()
                self.Holding = Board.Piece('X', -1)
                return True
            return False
        elif (self.fromBoard!=False):
            if (self.fromBoard[0]!=x or self.fromBoard[1]!=y):
                if (self.GameBoard.movFromBoard(self.Holding, x, y)):
                    self.GameBoard.nextTurn()
                    self.Holding = Board.Piece('X', -1)
                    self.fromBoard = False
                    return True
        return False
    def winner(self):
        return self.GameBoard.checkWin()
#-------------------------------------------------------------------

