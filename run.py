# GUI.py
from sudoku_functions import solve, valid, find_empty
import pygame
import time
import random
import sys
from copy import deepcopy
pygame.font.init()

def generate():
    # Randomly generating a Sudoku grid
    while True:
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                sys.exit()
        grid = [[0]*9 for i in range(9)]
        for i in range(9):
            for j in range(9):
                if random.randint(1,10)>=5:
                    grid[i][j] = random.randint(1,9)
                    if valid(grid, (i,j), grid[i][j]):
                        continue
                    else:
                        grid[i][j]=0
        partialGrid = deepcopy(grid) # Copying a new grid object[a separate one not affecting the orginial]
        if solve(grid):
            return partialGrid

class Grid:
    '''A sudoku grid made out of Boxes'''
    def __init__(self, window):
        self.board = generate()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.boxes = [[Box(self.board[i][j], window, i*60, j*60) for j in range(9)] for i in range(9)]
        self.window = window

    def draw_board(self):
        '''Fills the board with boxes and renders their values'''
        for i in range(9):
            for j in range(9):
                if j%3 == 0 and j != 0: #vertical lines
                    pygame.draw.line(self.window, (0, 0, 0), ((j//3)*180, 0), ((j//3)*180, 540), 4)

                if i%3 == 0 and i != 0: #horizontal lines
                    pygame.draw.line(self.window, (0, 0, 0), (0, (i//3)*180), (540, (i//3)*180), 4)

                self.boxes[i][j].draw((0,0,0), 1)

                if self.boxes[i][j].value != 0: #don't draw 0s on the grid
                    self.boxes[i][j].display(self.boxes[i][j].value, (21+(j*60), (16+(i*60))), (0, 0, 0))  #20,5 are the coordinates of the first tile
        #bottom-most line
        pygame.draw.line(self.window, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)

    def deselect(self, tile):
        '''Deselects every tile except the one currently clicked'''
        for i in range(9):
            for j in range(9):
                if self.boxes[i][j] != tile:
                    self.boxes[i][j].selected = False

    def redraw(self, keys, strikes, time):
        '''Redraws board with highlighted boxes'''
        self.window.fill((255,255,255))
        self.draw_board()
        for i in range(9):
            for j in range(9):
                if self.boxes[j][i].selected:  #draws the border on selected boxes
                    self.boxes[j][i].draw((50, 205, 50), 4)

                elif self.boxes[i][j].correct:
                    self.boxes[j][i].draw((34, 139, 34), 4)

                elif self.boxes[i][j].incorrect:
                    self.boxes[j][i].draw((255, 0, 0), 4)

        if len(keys) != 0: #draws inputs that the user places on board but not their final value on that tile
            for value in keys:
                self.boxes[value[0]][value[1]].display(keys[value], (21+(value[0]*60), (16+(value[1]*60))), (128, 128, 128))

        if strikes > 0:
            font = pygame.font.SysFont('Bauhaus 93', 30) #Red X
            text = font.render('X', True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont('Bahnschrift', 40) #Number of Incorrect Inputs
            text = font.render(str(strikes), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont('Bahnschrift', 40) #Time Display
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    def visualSolve(self, strikes, time):
        '''Showcases how the board is solved via backtracking'''
        for event in pygame.event.get(): #so that touching anything doesn't freeze the screen
            if event.type == pygame.QUIT:
                sys.exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for nums in range(9):
            if valid(self.board, (empty[0],empty[1]), nums+1):
                self.board[empty[0]][empty[1]] = nums+1
                self.boxes[empty[0]][empty[1]].value = nums+1
                self.boxes[empty[0]][empty[1]].correct = True
                pygame.time.delay(1) #show boxes at a slower rate
                self.redraw({}, strikes, time)

                if self.visualSolve(strikes, time):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.boxes[empty[0]][empty[1]].value = 0
                self.boxes[empty[0]][empty[1]].incorrect = True
                self.boxes[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, strikes, time)

    def hint(self, keys):
        '''Shows a random empty tile's solved value as a hint'''
        while True: #keeps generating i,j coords until it finds a valid random spot
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.board[i][j] == 0: #hint spot has to be empty
                if (j,i) in keys:
                    del keys[(j,i)]
                self.board[i][j] = self.solvedBoard[i][j]
                self.boxes[i][j].value = self.solvedBoard[i][j]
                return True

            elif self.board == self.solvedBoard:
                return False

class Box:
    def __init__(self,value, window,row,column):
        self.value =value
        self.window = window
        self.rect = pygame.Rect((row,column),(60,60)) # Creating the dimensions for the box
        self.selected = False
        self.correct = False
        self.incorrect = False
    
    def draw(self, color,thickness):
        # Draw a tile on the board
        pygame.draw.rect(self.window, color, self.rect, thickness)
    
    def display(self,value,position,color):
        # Display a number on the tile
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(str(value), True, color)
        self.window.blit(text, position) # To enter the text in the new coordinates

    def clicked(self, mousePos):
        # Checks if a box has been selected
        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected

def main():
    win = pygame.display.set_mode((540,600))
    win.fill((255,255,255))
    pygame.display.set_caption("Sudoku")

    '''Loading Screeb when generating Grid'''
    font = pygame.font.SysFont('Bahnschrift',40)
    text = font.render('Generating',True,(0,0,0))
    win.blit(text,(230,230))
    pygame.display.flip()

    strikes = 0
    board = Grid(win)
    selected = -1,-1
    key = {}
    run = True
    start = time.time()
    while run:
        play_time = (time.time() - start)
        passedTime = time.strftime('%H:%M:%S',time.gmtime(play_time))

        if board.board == board.solvedBoard:
            for i in range(9):
                for j in range(9):
                    board.boxes[i][j].selected = False
                    run=False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()                
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.boxes[i][j].selected = False
                    key = {}  #clear keyDict out
                    board.visualSolve(strikes, passedTime)
                    for i in range(9):
                        for j in range(9):
                            board.boxes[i][j].correct = False
                            board.boxes[i][j].incorrect = False #reset boxeboard.boxes
                    run = False

                if board.board[selected[1]][selected[0]] == 0 and selected != (-1,-1):
                    if event.key == pygame.K_1:
                        key[selected] = 1
                    if event.key == pygame.K_2:
                        key[selected] = 2
                    if event.key == pygame.K_3:
                        key[selected] = 3
                    if event.key == pygame.K_4:
                        key[selected] = 4
                    if event.key == pygame.K_5:
                        key[selected] = 5
                    if event.key == pygame.K_6:
                        key[selected] = 6
                    if event.key == pygame.K_7:
                        key[selected] = 7
                    if event.key == pygame.K_8:
                        key[selected] = 8
                    if event.key == pygame.K_9:
                        key[selected] = 9
                    
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        if selected in key:
                            board.boxes[selected[1]][selected[0]].value = 0
                            del key[selected]
                        
                    if event.key == pygame.K_RETURN:
                        if selected in key:
                            if key[selected] != board.solvedBoard[selected[1]][selected[0]]:
                                strikes += 1
                                board.boxes[selected[1]][selected[0]].value = 0
                                del key[selected]
                                break
                            
                            '''Valid and Correct entry in the cell'''
                            board.boxes[selected[1]][selected[0]].value = key[selected]
                            board.board[selected[1]][selected[0]] = key[selected]
                            del key[selected]

                if event.key == pygame.K_h:
                    board.hint(key)

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range(9):
                        click = board.boxes[i][j].clicked(pos)
                        if click:
                            selected = i,j
                            board.deselect(board.boxes[i][j])
                        
        board.redraw(key, strikes, passedTime)
    while True: # Loop created so that program only closes when user closes the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

main()
pygame.quit()