# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 22:56:04 2018

@author: Orion Palaquibay
"""

#Internal Functions of Gobblet Game

class Player:
    #Initiate Player with some name and their Color ('W' or 'B')
    def __init__(self, BorW, Name):
        self.Name = Name
        self.Color = BorW
        self.Inv = [[],[],[]]
        for x in range(3):
            for z in range(4):
                self.Inv[x].append(Piece(self.Color, z))
    #Print the Invintory of the Player to Console
    def ShowInv(self):
        for i in range(3):
            print('stack number ' + str(i+1) + ': ')
            stack = self.Inv[i]
            slen = len(stack)
            for i in range(slen):
                print(stack[slen-i-1].Color + str(stack[slen-i-1].Size))
    #------------------------------------------------------------------------------------------
    #Use these two in conjunction to use valid pieces in the Players Invintory
    def getTopPiece(self, stacknum):
        stack = self.Inv[stacknum-1]
        if (len(stack)==0):
            print("This stack has no pieces")
            return False
        return stack[len(stack)-1]

    def removePiece(self, piece):
        for i in range(3):
            stack = self.Inv[i]
            if (stack[len(stack)-1]==piece):
                self.Inv[i] = stack[:len(stack)-1]
                return piece
        print('This piece is not available for use')
        return piece
#------------------------------------------------------------------------------------------
        
#Basic Piece class with Color ('B' or 'W') and Size (Ranging between 0 and 3)
class Piece:
    def __init__(self, BorW, Size):
        self.Color = BorW
        self.Size = Size
#-----------------------------------------------------------------------------------------

#Board Class Handling Player movements on Board and whose turn it is
class Board:
    def __init__(self, PlayerW, PlayerB):
        self.PlayerW = PlayerW
        self.PlayerB = PlayerB
        #4 x 4 array of arrays, each spot has a stack of pieces, top of the stack is top piece
        self.GBoard = [[[],[],[],[]],
                      [[],[],[],[]],
                      [[],[],[],[]],
                      [[],[],[],[]]]
        #populate the board with ghost pieces of no size and no color
        for y in range(4):
            for x in range(4):
                self.GBoard[y][x].append(Piece("X", -1))
        
        self.currentPlayer = self.PlayerW
        #self.BoardInUse = False
    #---------------------------------------------------------------------------------------------------
    #swaps current player and updates players based on what changed with current player
    def nextTurn(self):
        if (self.currentPlayer.Color=='W'):
            self.PlayerW = self.currentPlayer
            self.currentPlayer = self.PlayerB
        elif (self.currentPlayer.Color=='B'):
            self.PlayerB = self.currentPlayer
            self.currentPlayer = self.PlayerW
    #----------------------------------------------------------------------------------------------------
    def move(self, piece, x, y):
        if (piece.Color!=self.currentPlayer.Color):
            print("This is not your piece")
            return False
        if (self.pieceAt(x, y).Size < piece.Size):
            self.GBoard[y][x].append(piece)
            return True
        print ("The piece here is too big to cover")
        return False
    def movFromBoard(self, piece, x, y):
        return self.move(piece, x, y)
    def movFromInv(self, piece, x, y):
        if (self.partOf3Rule(x,y) or self.pieceAt(x,y).Size==-1):
            if (self.move(piece, x, y)):
                self.currentPlayer.removePiece(piece)
                return True
            return False
        return False
    def grabFromBoard(self, x, y):
        return self.GBoard[y][x].pop()
    #-------------------------------------------------------------------------------------------------
    #checks if current player has won on board
    def checkWin(self):
        color = self.currentPlayer.Color
        #horizontal 4 in a row
        for r in range(4):
            if (self.pieceAt(0,r).Color==color and
                self.pieceAt(1,r).Color==color and
                self.pieceAt(2,r).Color==color and
                self.pieceAt(3,r).Color==color):
                return True
        #vertical 4 in a row
        for c in range(4):
            if (self.pieceAt(c,0).Color==color and
                self.pieceAt(c,1).Color==color and
                self.pieceAt(c,2).Color==color and
                self.pieceAt(c,3).Color==color):
                return True
        #diagonal 4 in a row
        if (self.pieceAt(0,0).Color==color and
            self.pieceAt(1,1).Color==color and
            self.pieceAt(2,2).Color==color and
            self.pieceAt(3,3).Color==color):
            return True
        if (self.pieceAt(3,0).Color==color and
            self.pieceAt(2,1).Color==color and
            self.pieceAt(1,2).Color==color and
            self.pieceAt(0,3).Color==color):
            return True
        return False
    #--------------------------------------------------------------------------------------------------
    def pieceAt(self, x, y):
        return self.GBoard[y][x][len(self.GBoard[y][x])-1]
    #checks for 3 in a row rule
    def partOf3Rule(self, x, y):
        if (self.pieceAt(x,y).Color == self.currentPlayer.Color):
            return False
        return self.partOf3NS(x,y) or self.partOf3WE(x,y) or self.partOf3NW(x,y) or self.partOf3NE(x,y)
    #-------------------------------------------------------------------------------------------------------
    #functions checking 3 in a row vertical, horizontal, and diagonal
    def partOf3NS(self, x, y):
        color = self.pieceAt(x,y).Color
        top = False
        mid = False
        bot = False
        if (y==0):
            top = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y+2).Color==color
        if (y==1):
            top = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y+2).Color==color
            mid = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y-1).Color==color
        if (y==2):
            mid = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y-1).Color==color
            bot = self.pieceAt(x,y-1).Color==color and self.pieceAt(x,y-2).Color==color
        if (y==3):
            bot = self.pieceAt(x,y-1).Color==color and self.pieceAt(x,y-2).Color==color
        return top or mid or bot
    def partOf3WE(self, x, y):
        color = self.pieceAt(x,y).Color
        left = False
        mid = False
        right = False
        if (x==0):
            left = self.pieceAt(x+1,y).Color==color and self.pieceAt(x+2,y).Color==color
        if (x==1):
            left = self.pieceAt(x+1,y).Color==color and self.pieceAt(x+2,y).Color==color
            mid = self.pieceAt(x+1,y).Color==color and self.pieceAt(x-1,y).Color==color
        if (x==2):
            right = self.pieceAt(x-1,y).Color==color and self.pieceAt(x-2,y).Color==color
            mid = self.pieceAt(x+1,y).Color==color and self.pieceAt(x-1,y).Color==color
        if (x==3):
            right = self.pieceAt(x-1,y).Color==color and self.pieceAt(x-2,y).Color==color
        return left or mid or right
    def partOf3NW(self, x, y):
        color = self.pieceAt(x,y).Color
        topleft = False
        mid = False
        botright = False
        if (y==0):
            if (x==0 or x==1):
                topleft = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x+2,y+2).Color==color
        if (y==1):
            if (x==1):
                topleft = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x+2,y+2).Color==color
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
            if (x==0):
                topleft = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x+2,y+2).Color==color
            if (x==2):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
        if (y==2):
            if (x==1):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
            if (x==2):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
                botright = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
            if (x==3):
                botright = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        if (y==3):
            if (x==2 or x==3):
                botright = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        return topleft or mid or botright
    def partOf3NE(self, x, y):
        color = self.pieceAt(x,y).Color
        topright = False
        mid = False
        botleft = False
        if (y==0):
            if (x==2 or x==3):
                topright = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x-2,y+2).Color==color
        if (y==1):
            if (x==2):
                topright = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x-2,y+2).Color==color
                mid = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x+1,y-1).Color==color
            if (x==3):
                topright = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x-2,y+2).Color==color
            if (x==1):
                mid = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x+1,y-1).Color==color
        if (y==2):
            if (x==2):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
            if (x==1):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
                botleft = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
            if (x==0):
                botleft = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        if (y==3):
            if (x==0 or x==1):
                botleft = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        return topright or mid or botleft
