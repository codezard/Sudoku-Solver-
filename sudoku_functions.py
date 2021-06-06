board = [
    [9,0,0,0,0,0,0,0,5],
    [7,1,0,0,8,0,0,6,9],
    [0,2,0,0,7,0,0,8,0],
    [0,4,0,9,0,8,0,3,0],
    [0,0,0,0,0,0,0,0,0],
    [0,8,0,2,0,5,0,9,0],
    [0,9,0,0,6,0,0,1,0],
    [4,5,0,0,9,0,0,2,7],
    [8,0,0,0,0,0,0,0,3]
]


def print_board(board):
    for i in range(len(board)):
        if i%3==0 and i!=0:
            print('-|--------|--------|-------|-')

        for j in range (len(board[0])):
            if j%3==0 :
                print(' | ', end = '')

            if j == 8:
                print(str(board[i][j]) + ' | ')
            else:
                print(str(board[i][j]) + " ", end='')
        

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j]==0:
                return i,j # row, column (y,x)


def valid(board,pos,num):
    #check row
    for i in range(len(board[0])):
        if board[pos[0]][i]== num and (pos[0],i)!=pos:
            return False

    # Check col
    for i in range(len(board)):
        if board[i][pos[1]]==num and (i,pos[1]) != pos:
            return False

    # Check box
    box_x=pos[1]//3
    box_y=pos[0]//3

    for i in range(box_y*3,box_y*3 +3):
        for j in range(box_x*3,box_x*3 +3):
            if board[i][j]== num and (i,j)!=pos:
                return False

    return True

def solve(board):
    find =find_empty(board)
    if not find:
        return True
    else:
        row, col=find
    
    for i in range(1,10): # from 0 to 8
        if valid(board,find,i):
            board[find[0]][find[1]]=i
            
            if solve(board):
                return True
            board[find[0]][find[1]]=0
    return False




print_board(board)
solve(board)
print('----------------------------------------------')
print_board(board)
