#Gobblet

#All game actions will be done on main game board, when it is called the game will play until someone wins
class Board:
    def __init__(self):
        self.board = [[[],[],[],[]],
                      [[],[],[],[]],
                      [[],[],[],[]],
                      [[],[],[],[]]]
        #populate the board with ghost pieces of no size and no color
        for y in range(4):
            for x in range(4):
                self.board[y][x].append(Piece("X", 0))
        #initialize each player
        self.player1 = Player("W", raw_input("player 1 name: "))
        self.player2 = Player("B", raw_input("player 2 name: "))
        self.currentPlayer = self.player1
        self.BoardInUse = False

    def checkWin():
        #horizontal 4 in a row
        for r in self.board:
            color = r[0][0].BW
            if r[1][0].BW==color and r[2][0].BW==color and r[3][0].BW==color:
                return (True, color)
        #vertical 4 in a row
        for c in self.board[0]:
            color = c[0].BW
            i = self.board[0].index(c)
            if self.board[1][i][0].BW==color and self.board[2][i][0].BW==color and self.board[3][i][0].BW==color:
                return (True, color)
        #2 diagonal 4 in a row
        color1 = self.board[0][0][0].BW
        color2 = self.board[3][0][0].BW
        if self.board[1][1][0].BW==color1 and self.board[2][2][0].BW==color1 and self.board[3][3][0].BW==color1:
            return (True, color1)
        if self.board[2][1][0].BW==color2 and self.board[1][2][0].BW==color2 and self.board[0][3][0].BW==color2:
            return (True, color2)
        return (False, "X")
    
    def usePiece(x,y):
        piece = self.board[4-y][x-1]
        #if you try to use a piece at a spot with no piece or a piece that is not their colorreturn False
        if piece.BW!=self.currentPlayer.BW:
            print "there's either no piece there or it's not your piece"
            return False
        #return the popped piece at spot on board
        return piece.popleft()
    
    def pieceB(x,y):
        return board[4-y][x-1][0]

class Player:
    def __init__(self, blackorwhite, name):
        self.name = name
        self.BW = blackorwhite
        self.inv = [[],[],[]]
        for x in range(3):
            for z in range(4):
                self.inv[x].append(Piece(self.BW, 4-z))
    def usePiece(size):
        for p in self.inv:
            if p[0].size==size:
                return p.popleft()
        print "you don't have that size piece"
        return False

class Piece:
    def __int__(self, blackorwhite, s):
        self.BW = blackorwhite
        self.size = s

#-------------------------------------------------------------------


def 3inRow(x,y): #returns true if the piece is part of 3 in a row
    return vert3(x,y) or hori3(x,y) or posdia3(x,y) or negdia3(x,y)

def move1FromBoard(player,x,y):
    boardInUse = True
    pieceInUse = usePieceB(x,y)
    if pieceInUse==False:
        return 0
    updateBoard()
def move1FromInv(player, size):
    boardInUse = False
    pieceInUse = usePieceP(player, size)
    if pieceInUse==False:
        return 0
def move2OnBoard(player,x,y):
    p = pieceB(x,y)
    psize = p.size
    pcol = p.BW
    if psize==0:
        board[4-y][x-1].insert(0,pieceInUse)
        return True
    else:
        if boardInUse:
            if pieceInUse.size>psize:
                board[4-y][x-1].insert(0,pieceInUse)
                return True
            else:
                print "the piece you're trying to cover is too big"
                return False
        elif pcol==player.BW:
            print "you can't cover your own piece straight from invintory"
            return False
        elif 3inRow(x,y):
            board[4-y][x-1].insert(0,pieceInUse)
            return True
        
    


#----Individual 3 in a row checkers-------------------------------------------
def vert3(x,y):
    col=piece(x,y).BW
    c = 0
    i = 1
    while i<5:
        if piece(x,i).BW==col:
            c = c+1
        i=i+1
    return c==3
def hori3(x,y):
    col=piece(x,y).BW
    c = 0
    i = 1
    while i<5:
        if piece(i,y).BW==col:
            c = c+1
        i=i+1
    return c==3
def posdia3(x,y):
    col=piece(x,y).BW
    c = 0
    i = 1
    if x==y:
        while i<5:
            if piece(i,i).BW==col:
                c = c+1
            i=i+1
        return c==3
    if x==y+1 or x+1==y:
            if piece(x+1,y+1).BW==col and piece(x-1,y-1).BW==col:
                return True
    else:
        return False
def negdia3(x,y):
    col=piece(x,y).BW
    c = 0
    i = 1
    if x==y:
        if piece(x-1,y+1).BW==col and piece(x+1,y-1).BW==col:
            return True
    if x==y+1 or x+1==y:
        while i<5:
            if piece(i,4-i).BW==col:
                c = c+1
            i=i+1
        return c==3
    else:
        return False
#---------------------------------------------------------------------------------------------

game = Board()
