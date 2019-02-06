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
        self.curMove = [-1,-1,-1,-1,-1] #will have form (x1, y1, x2, y2, stacknum)
        self.lastMove = [-1,-1,-1,-1,-1] #will have form (x1, y1, x2, y2, stacknum)
    
    def currentPlayer(self):
        return self.GameBoard.currentPlayer
    def opposition(self):
        if (self.GameBoard.currentPlayer=='W'):
            return self.GameBoard.PlayerB
        return self.GameBoard.PlayerW
    
    def checkWin(self, color):
        return self.GameBoard.checkWin(color)
    
    def pieceAt(self, x, y):
        return self.GameBoard.pieceAt(x, y)
    
    def holdInvP(self, stacknum):
        if (self.fromBoard==False):
            self.Holding = self.GameBoard.currentPlayer.getTopPiece(stacknum)
            self.curMove[4] = stacknum
            return True
        else:
            #print("you're holding a piece from the board")
            return False
        
    def holdBoardP(self, x, y):
        if (self.fromBoard==False):
            if (self.GameBoard.pieceAt(x, y).Color==self.GameBoard.currentPlayer.Color):
                self.Holding = self.GameBoard.grabFromBoard(x, y)
                self.fromBoard = (x, y)
                self.curMove[0] = x
                self.curMove[1] = y
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
                self.curMove[2] = x
                self.curMove[3] = y
                self.lastMove = self.curMove
                self.GameBoard.nextTurn()
                self.Holding = Board.Piece('X', -1)
                self.curMove = [-1,-1,-1,-1,-1]
                return True
            return False
        else:
            if (self.fromBoard[0]!=x or self.fromBoard[1]!=y):
                if (self.GameBoard.movFromBoard(self.Holding, x, y)):
                    self.curMove[2] = x
                    self.curMove[3] = y
                    self.lastMove = self.curMove
                    self.GameBoard.nextTurn()
                    self.Holding = Board.Piece('X', -1)
                    self.fromBoard = False
                    self.curMove = [-1,-1,-1,-1,-1]
                    return True
        return False
    
    def undoMove(self, lastMove):
        self.GameBoard.nextTurn() #change to player that made move
        piece = self.GameBoard.GBoard[lastMove[3]][lastMove[2]].pop()
        if (lastMove[0]==-1): #if move was from invintory
            self.GameBoard.currentPlayer.Inv[lastMove[4]-1].append(piece)
            self.lastMove = [-1,-1,-1,-1,-1]
            self.curMove = [-1,-1,-1,-1,-1]
        else: #if move was from board
            self.GameBoard.GBoard[lastMove[1]][lastMove[0]].append(piece)
            self.lastMove = [-1,-1,-1,-1,-1]
            self.curMove = [-1,-1,-1,-1,-1]
    def winner(self):
        return self.GameBoard.checkWin()
#-------------------------------------------------------------------

