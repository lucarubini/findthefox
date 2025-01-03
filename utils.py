import random

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
        # check for a winner
        if __debug__:
            print('check_winner')
        # Check rows for a winner
        for row in self.board:
            tmpx = [row[i]+row[i+1]+row[i+2] for i in range(len(row)-2)]
            if __debug__:
                print(f'check row: {tmpx}')
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
            char_fox = self.sample_char()

            if self.board[row][col] == " ":
                self.board[row][col] = char_fox
                self.bucket[char_fox] = self.bucket[char_fox] - 1
            else:
                if __debug__:
                    print(f"Cell ({row},{col}) already taken, try again.")
                continue

            turn_counter+=1
            if output_folder:
                fout.write(f'Turn: {turn_counter}\n')
                fout.write(self.board2print())

            if self.check_winner():
                FOX_FOUND=True
                if __debug__:
                    print(f"FOX FOUND!")
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


