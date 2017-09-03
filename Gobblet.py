#Gobblet
board = [[[0],[0],[0],[0]],
         [[0],[0],[0],[0]],
         [[0],[0],[0],[0]],
         [[0],[0],[0],[0]]] #4x4 grid with array of pieces on each spot and standard coordinates
currentPlayer=_
player1 = 
boardInUse = False
pieceInUse = _

def updateBoard():
    print 

class Player:
    BW = _
    inv = [[4,3,2,1],[4,3,2,1],[4,3,2,1]] #pieces invintory

class Piece:
    BW = _
    size = _

#Attempt to use piece from Board B or Player P-------------------------
def usePieceP(player,size):
    for p in player.inv:
        if p[0].size==size:
            return p.popleft()
    print "you don't have that size piece"
    return False
def usePieceB(x,y):
    if piece(x,y).size==0:
        print "there is no piece at that spot"
        return False
    return board[4-y][x-1].popleft()

#get top piece at spoton the board
def pieceB(x,y):
    return board[4-y][x-1][0]

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
