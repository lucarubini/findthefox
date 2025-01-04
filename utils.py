import random
import pygame


class FindFoxBoard:
    def __init__(self, size, init_strategy, bucket):
        self.size = size
        self.board = self.build_board(self.size)
        self.init_strategy = init_strategy
        self.bucket = bucket

        self.init_board()

    def build_board(self, size):
        board = [[" " for _ in range(size)] for _ in range(size)]
        return board

    def available_cell(self, row, col):
        if self.board[row][col] == " ":
            return True
        else:
            return False

    def sample_char(self):
        # sample random char and update bucket
        tmp=[]
        for c, count in self.bucket.items():
            if count > 0:
                tmp.append(c)
        random.shuffle(tmp)
        out_c = tmp[0]
        return out_c

    def is_board_full(self):
        # check if the board is full
        for row in self.board:
            if " " in row:
                return False
        return True

    def board2print(self):
        # Return the string to print the board
        out_tmp=[]
        for row in self.board:
            out_tmp.append(" | ".join(row))
            out_tmp.append("-" * ( len(row)*3 + len(row)-2) )
        out = '\n'.join(out_tmp[:-1])+'\n'
        return out

    def init_board(self):
        # Initialize board
        if self.init_strategy == 'diag_f':
            for i in range(self.size):
                self.board[i][i] = 'f'
                self.bucket['f'] = self.bucket['f'] - 1
        if self.init_strategy == 'diag_o':
            for i in range(self.size):
                self.board[i][i] = 'o'
                self.bucket['o'] = self.bucket['o'] - 1
        if self.init_strategy == 'diag_x':
            for i in range(self.size):
                self.board[i][i] = 'x'
                self.bucket['x'] = self.bucket['x'] - 1
        if self.init_strategy == 'diag_reverse_f':
            for i in range(sizeN):
                self.board[self.size-i][self.size-i] = 'f'
                self.bucket['f'] = self.bucket['f'] - 1
        if self.init_strategy == 'diag_reverse_o':
            for i in range(self.size):
                self.board[self.size-i][self.size-i] = 'o'
                self.bucket['o'] = self.bucket['o'] - 1
        if self.init_strategy == 'diag_reverse_x':
            for i in range(sizeN):
                self.board[self.size-i][self.size-i] = 'x'
                self.bucket['x'] = self.bucket['x'] - 1

    def check_winner(self):
        # Check rows for a winner
        for i, row in enumerate(self.board):
            tmpx = [row[i]+row[i+1]+row[i+2] for i in range(len(row)-2)]
            if __debug__:
                print(f'check row {i}: {tmpx}')
            found = [x for x in tmpx if x in ['fox','xof']]
            if len(found) > 0:
              return True

        # Check columns for a winner
        for col in range(self.size):
            tmpx = [self.board[i][col]+self.board[i+1][col]+self.board[i+2][col] for i in range(self.size-2)]
            if __debug__:
                print(f'check col {col}: {tmpx}')
            found = [x for x in tmpx if x in ['fox','xof']]
            if len(found) > 0:
              return True

        # Check diagonals for a winner
        tmp=[]
        for i in range(self.size-2):
            #forward (in case of main diag they are the same)
            tmp_p1f = [self.board[j][i+j] + self.board[j+1][i+j+1] + self.board[j+2][i+j+2] for j in range(self.size-2-i)]
            tmp_m1f = [self.board[i+j][j] + self.board[i+j+1][j+1] + self.board[i+j+2][j+2] for j in range(self.size-2-i)]
            #backward (in case of main diag they are the same)
            tmp_p1b = [self.board[j][self.size-1-j-i] + self.board[j+1][self.size-1-j-i-1] + self.board[j+2][self.size-1-j-i-2] for j in range(self.size-2-i)]
            tmp_m1b = [self.board[j+i][self.size-1-j] + self.board[j+i+1][self.size-1-j-1] + self.board[j+i+2][self.size-1-j-2] for j in range(self.size-2-i)]

            tmp = tmp + tmp_p1f + tmp_m1f + tmp_p1b + tmp_m1b
        if __debug__:
            print(f'check diag forward/backward: {tmp}')
        if any([x in ['fox','xof'] for x in tmp]):
          return True
        return False


    def check_winner_index(self):
        tmp_idx=[]
        # Check rows for a winner
        for i, row in enumerate(self.board):
            tmp_rows = [((i,j),(i,j+1),(i,j+2)) for j in range(self.size-2)]
            tmp_idx = tmp_idx + tmp_rows

        # Check columns for a winner
        for col in range(self.size):
            tmp_cols = [((i,col),(i+1,col),(i+2,col)) for i in range(self.size-2)]
            tmp_idx = tmp_idx + tmp_cols

        # Check diagonals for a winner
        for i in range(self.size-2):
            #forward (in case of main diag they are the same)
            tmp_p1f_idx = [((j,i+j),(j+1,i+j+1),(j+2,i+j+2)) for j in range(self.size-2-i)]
            tmp_m1f_idx = [((i+j,j),(i+j+1,j+1),(i+j+2,j+2)) for j in range(self.size-2-i)]
            #backward (in case of main diag they are the same)
            tmp_p1b_idx = [((j,self.size-1-j-i),(j+1,self.size-1-j-i-1),(j+2,self.size-1-j-i-2)) for j in range(self.size-2-i)]
            tmp_m1b_idx = [((j+i,self.size-1-j),(j+i+1,self.size-1-j-1),(j+i+2,self.size-1-j-2)) for j in range(self.size-2-i)]

            tmp_idx = tmp_idx + tmp_p1f_idx + tmp_m1f_idx + tmp_p1b_idx + tmp_m1b_idx

        for x0,x1,x2 in tmp_idx:
            tmpx = self.board[x0[0]][x0[1]] + self.board[x1[0]][x1[1]] + self.board[x2[0]][x2[1]]
            if tmpx in ['fox','xof']:
                return True, (x0,x1,x2)
        return False, None

    def mark_cell(self, row, col, char):
        self.board[row][col] = char

    # Main function to play the game
    def play_game_cli(self, output_folder, game_id):

        if output_folder:
            fout=open(f'{output_folder}/{game_id}.log','w')

        FOX_FOUND=False

        cells = []
        for i in range(self.size):
          for j in range(self.size):
            cells.append((i,j))

        if __debug__:
            print(self.board2print())

        turn_counter = 0
        if output_folder:
            fout.write(f'Turn: {turn_counter}\n')
            fout.write(self.board2print())

        while True:
            #Filling strategy is to randomly pick a cell in the grid and a char from the remaining.
            random.shuffle(cells)
            row, col = cells.pop(0)

            if self.available_cell(row, col):
                sampled_char = self.sample_char()
                self.mark_cell(row, col, sampled_char)
                self.bucket[sampled_char] = self.bucket[sampled_char] - 1
            else:
                if __debug__:
                    print(f"Cell ({row},{col}) already taken, try again.")
                continue

            turn_counter+=1
            if output_folder:
                fout.write(f'Turn: {turn_counter}\n')
                fout.write(self.board2print())

            is_fox_found, fox_idxs = self.check_winner_index()

            if is_fox_found:
                FOX_FOUND=True
                if __debug__:
                    print(f"FOX FOUND!")
                    for xrow,ycol in fox_idxs:
                        char_x = self.board[xrow][ycol]
                        self.mark_cell(xrow, ycol, char_x.upper())

                    print(self.board2print())
                if output_folder:
                    fout.write('==>FOX FOUND!')
                break

            if self.is_board_full():
                FOX_FOUND=False
                if __debug__:
                    print("FOX NOT FOUND")
                    print(self.board2print())
                if output_folder:
                    fout.write('==>FOX NOT FOUND!')
                break
        if output_folder:
            fout.close()

        return FOX_FOUND

class FindFoxBoardGUI(FindFoxBoard):
    def __init__(self, size, init_strategy, bucket):
        super().__init__(size, init_strategy, bucket)
        self.WIDTH=400
        self.HEIGHT=400
        self.LINE_WIDTH=15
        self.LINE_COLOR= (23, 145, 135)
        self.SQUARE_SIZE=self.WIDTH//size
        self.CIRCLE_RADIUS=self.SQUARE_SIZE//3
        self.CIRCLE_WIDTH=5
        self.CROSS_WIDTH=5
        self.CHAR_COLOR=(239, 231, 200)
        self.SPACE = self.SQUARE_SIZE//4

    def draw_o(self, screen, row, col):
        pygame.draw.circle(screen, self.CHAR_COLOR, (int(col*self.SQUARE_SIZE+self.SQUARE_SIZE//2), int(row*self.SQUARE_SIZE + self.SQUARE_SIZE // 2)), self.CIRCLE_RADIUS, self.CIRCLE_WIDTH)

    def draw_x(self, screen, row, col):
        pygame.draw.line(screen, self.CHAR_COLOR, (col*self.SQUARE_SIZE+self.SPACE, row*self.SQUARE_SIZE+self.SPACE), (col*self.SQUARE_SIZE+self.SQUARE_SIZE-self.SPACE, row*self.SQUARE_SIZE+self.SQUARE_SIZE-self.SPACE), self.CROSS_WIDTH)
        pygame.draw.line(screen, self.CHAR_COLOR, (col*self.SQUARE_SIZE+self.SPACE, row*self.SQUARE_SIZE+self.SQUARE_SIZE-self.SPACE), (col*self.SQUARE_SIZE+self.SQUARE_SIZE-self.SPACE, row*self.SQUARE_SIZE+self.SPACE), self.CROSS_WIDTH)

    def draw_f(self, screen, row, col):
        x0=col*self.SQUARE_SIZE+self.SPACE
        y0=row*self.SQUARE_SIZE+self.SPACE
        x1=col*self.SQUARE_SIZE+self.SPACE
        y1=row*self.SQUARE_SIZE+3*self.SPACE
        x2=col*self.SQUARE_SIZE+3*self.SPACE
        y3=row*self.SQUARE_SIZE+2*self.SPACE
        x3=col*self.SQUARE_SIZE+2*self.SPACE
        pygame.draw.line(screen, self.CHAR_COLOR, (x0, y0), (x1, y1) , self.CROSS_WIDTH)
        pygame.draw.line(screen, self.CHAR_COLOR, (x0, y0), (x2, y0) , self.CROSS_WIDTH)
        pygame.draw.line(screen, self.CHAR_COLOR, (x0, y3), (x3, y3) , self.CROSS_WIDTH)

    # Drawing functions
    def draw_lines(self, screen):

        for i in range(self.size-1):
            # Horizontal lines
            pygame.draw.line(screen, self.LINE_COLOR, (0, (i+1)*self.SQUARE_SIZE), (self.WIDTH, (i+1)*self.SQUARE_SIZE), self.LINE_WIDTH)
            # Vertical lines
            pygame.draw.line(screen, self.LINE_COLOR, ((i+1)*self.SQUARE_SIZE, 0), ((i+1)*self.SQUARE_SIZE, self.HEIGHT), self.LINE_WIDTH)

    def draw_chars(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 'f':
                    self.draw_f(screen, row, col)
                elif self.board[row][col] == 'o':
                    self.draw_o(screen, row, col)
                elif self.board[row][col] == 'x':
                    self.draw_x(screen, row, col)


