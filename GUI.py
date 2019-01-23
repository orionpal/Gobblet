# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 00:27:08 2018

@author: Orion E. Eman
"""
from tkinter import *
from Board import *
from Gobblet import *
import GobbletAI

class GobbletGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.piecePics={
                ('B', 0) : PhotoImage(file="TinyBlack.png"),
                ('B', 1) : PhotoImage(file="SmallBlack.png"),
                ('B', 2) : PhotoImage(file="MediumBlack.png"),
                ('B', 3) : PhotoImage(file="BigBlack.png"),
                ('W', 0) : PhotoImage(file="TinyWhite.png"),
                ('W', 1) : PhotoImage(file="SmallWhite.png"),
                ('W', 2) : PhotoImage(file="MediumWhite.png"),
                ('W', 3) : PhotoImage(file="BigWhite.png"),
                ('X', -1) : PhotoImage(file="Empty.png")
                }
        
        self.init_Game()
        
    def init_Game(self):
        self.master.title("Gobblet")
        self.Game = GobbletGame(Player('W', "White"), Player('B', "Black"))
        self.Computer = GobbletAI.AI(self.Game, 1.0)
        self.init_row1()
        self.init_row2()
        self.init_row3()
        self.init_row4()
        self.init_PlayerW()
        self.init_PlayerB()
        self.updateInv()
        self.updateBoard()
        self.init_Holding()
        self.init_messageBoard()
        self.revealed = 'X'

    def move(self, x, y):
        #print(str(x) + " " + str(y))
        #Try to hold if not already holding something
        if (self.Game.Holding.Size==-1):
            if (self.Game.holdBoardP(x-1, y-1)):
                if (self.Game.checkWin('W')):
                    self.revealed='W'
                elif (self.Game.checkWin('B')):
                    self.revealed='B'
                self.updateHold()
                self.updateBoard()
                return True
        #Try to move
        elif (self.Game.makeMove(x-1,y-1)):
            #self.Computer.updateGame(self.Game)
            self.Computer.makeRobMove()
            self.updateInv()
            self.updateBoard()
            self.clearHold()
            if (self.Game.checkWin('W') and self.Game.checkWin('B')):
                if (self.revealed=='W'):
                    self.updateMessage(self.Game.PlayerW.Name + " has won the game!")
                    return True
                else:
                    self.updateMessage(self.Game.PlayerW.Name + " has won the game!")
                    return True
            elif (self.Game.checkWin('W')):
                self.updateMessage(self.Game.PlayerW.Name + " has won the game!")
                return True
            elif (self.Game.checkWin('B')):
                self.updateMessage(self.Game.PlayerB.Name + " has won the game!")
                return True
            return True
        return False

    def grab(self, player, stacknum):
        if (player.Color!=self.Game.currentPlayer().Color):
            self.updateMessage("Not your piece!")
        elif (self.Game.holdInvP(stacknum)):  
            self.updateHold()
        #print(self.Game.GameBoard)
        
    def clearHold(self):
        if (self.Game.fromBoard==False):
            self.Game.Holding = Board.Piece('X', -1)
            self.updateHold()
        else:
            self.updateMessage("You can't put that back!")
    
    def clearGame(self):
        self.Game = GobbletGame(Player('W', "PlayerW"), Player('B', "PlayerB"))
        self.updateBoard()
        self.updateInv()
        self.updateMessage("Messages will appear here!")
            
    def updateMessage(self, message):
        self.message.config(text = message)
    
    def updateBoard(self):
        for i in range(4):
            p1 = self.Game.GameBoard.pieceAt(i,0)
            p2 = self.Game.GameBoard.pieceAt(i,1)
            p3 = self.Game.GameBoard.pieceAt(i,2)
            p4 = self.Game.GameBoard.pieceAt(i,3)
            self.row1[i].config(image=self.piecePics[(p1.Color, p1.Size)], width=75, height=75)
            self.row2[i].config(image=self.piecePics[(p2.Color, p2.Size)], width=75, height=75)
            self.row3[i].config(image=self.piecePics[(p3.Color, p3.Size)], width=75, height=75)
            self.row4[i].config(image=self.piecePics[(p4.Color, p4.Size)], width=75, height=75)
            
    def updateInv(self):
        for i in range(3):
            pW = self.Game.PlayerW.getTopPiece(i+1)
            pB = self.Game.PlayerB.getTopPiece(i+1)
            self.Winv[i].config(image=self.piecePics[(pW.Color, pW.Size)], width=75, height=75)
            self.Binv[i].config(image=self.piecePics[(pB.Color, pB.Size)], width=75, height=75)
        
    def updateHold(self):
        self.holding.config(image=self.piecePics[(self.Game.Holding.Color, self.Game.Holding.Size)])
        self.cur.config(text="Your Turn: \n" + self.Game.currentPlayer().Name)
        
    def init_PlayerW(self):
        text = Label(self.master, text=self.Game.PlayerW.Name)
        text.place(x=320, y=0)
        self.Winv = []
        for i in range(3):
            self.Winv.append(Button(self.master, text="", command = lambda i=i: self.grab(self.Game.PlayerW, i+1)))
            self.Winv[i].config(width=10, height=5)
            self.Winv[i].place(x=340+(80*i), y=30)
        pass
    def init_PlayerB(self):
        text = Label(self.master, text=self.Game.PlayerB.Name)
        text.place(x=320, y=160)
        self.Binv = []
        for i in range(3):
            self.Binv.append(Button(self.master, text="", command = lambda i=i: self.grab(self.Game.PlayerB, i+1)))
            self.Binv[i].config(width=10, height=5)
            self.Binv[i].place(x=340+(80*i), y=190)
        pass
    def init_Holding(self):
        self.cur = Label(self.master, text="Your Turn: \n" + self.Game.currentPlayer().Name)
        self.cur.place(x=30, y=350)
        hol = Label(self.master, text="Holding Piece: ")
        hol.place(x=100, y=360)
        self.holding = Button(self.master, image=self.piecePics[('X', -1)], width=75, height=75, command = self.clearHold)
        self.holding.place(x=180, y=350)
        
        pass
    def init_messageBoard(self):
        self.message = Label(self.master, text="Messages will appear here!")
        self.message.place(x=350, y=380)
    def init_row1(self):
        self.row1 = []
        for i in range(4):
            self.row1.append(Button(self.master, text="", command = lambda i=i: self.move(i+1,1)))
            self.row1[i].config(width=10, height=5)
            self.row1[i].place(x=80*i, y=0)            
    def init_row2(self):
        self.row2 = []
        for i in range(4):
            self.row2.append(Button(self.master, text="", command = lambda i=i: self.move(i+1,2)))
            self.row2[i].config(width=10, height=5)
            self.row2[i].place(x=80*i, y=80)
    def init_row3(self):
        self.row3 = []
        for i in range(4):
            self.row3.append(Button(self.master, text="", command = lambda i=i: self.move(i+1,3)))
            self.row3[i].config(width=10, height=5)
            self.row3[i].place(x=80*i, y=160)
    def init_row4(self):
        self.row4 = []
        for i in range(4):
            self.row4.append(Button(self.master, text="", command = lambda i=i: self.move(i+1,4)))
            self.row4[i].config(width=10, height=5)
            self.row4[i].place(x=80*i, y=240)
    
def main():
    root = Tk()
    root.geometry("600x450")
    Gobblet = GobbletGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()