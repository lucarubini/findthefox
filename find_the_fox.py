import os
import random
import argparse
from datetime import datetime

# Function to print the Fox board
def print_board(board):
    out_tmp=[]
    for row in board:
        out_tmp.append(" | ".join(row))
        out_tmp.append("-" * ( len(row)*3 + len(row)-2) )
    out = '\n'.join(out_tmp[:-1])+'\n'
    return out

# Function to check for a winner
def check_winner(board):
    if __debug__:
        print('check_winner')
    sizeN=len(board)
    # Check rows for a winner
    for row in board:
        tmpx = [row[i]+row[i+1]+row[i+2] for i in range(len(row)-2)]
        if __debug__:
            print(f'check row: {tmpx}')
        found = [x for x in tmpx if x in ['fox','xof']]
        if len(found) > 0:
          return True

    # Check columns for a winner
    for col in range(sizeN):
        tmpx = [board[i][col]+board[i+1][col]+board[i+2][col] for i in range(sizeN-2)]
        if __debug__:
            print(f'check col {col}: {tmpx}')
        found = [x for x in tmpx if x in ['fox','xof']]
        if len(found) > 0:
          return True

    # Check diagonals for a winner
    tmp=[]
    for i in range(len(board)-2):
        #forward (in case of main diag they are the same)
        tmp_p1f = [board[j][i+j] + board[j+1][i+j+1] + board[j+2][i+j+2] for j in range(len(board)-2-i)]
        tmp_m1f = [board[i+j][j] + board[i+j+1][j+1] + board[i+j+2][j+2] for j in range(len(board)-2-i)]
        #backward (in case of main diag they are the same)
        tmp_p1b = [board[j][sizeN-1-j-i] + board[j+1][sizeN-1-j-i-1] + board[j+2][sizeN-1-j-i-2] for j in range(len(board)-2-i)]
        tmp_m1b = [board[j+i][sizeN-1-j] + board[j+i+1][sizeN-1-j-1] + board[j+i+2][sizeN-1-j-2] for j in range(len(board)-2-i)]

        tmp = tmp + tmp_p1f + tmp_m1f + tmp_p1b + tmp_m1b
    if __debug__:
        print(f'check diag forward/backward: {tmp}')
    if any([x in ['fox','xof'] for x in tmp]):
      return True
    return False

# Function to check if the board is full
def is_board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def sample_char(bucket):
    tmp=[]
    for c, count in bucket.items():
        if count > 0:
            tmp.append(c)
    random.shuffle(tmp)
    out_c = tmp[0]
    return out_c

def init_board(board, CHARS, strategy):

    sizeN = len(board)
    print(sizeN)

    if strategy == 'empty':
        return board, CHARS
    if strategy == 'diag_f':
        for i in range(sizeN):
            board[i][i] = 'f'
            CHARS['f'] = CHARS['f'] - 1
    if strategy == 'diag_o':
        for i in range(sizeN):
            board[i][i] = 'o'
            CHARS['o'] = CHARS['o'] - 1
    if strategy == 'diag_x':
        for i in range(sizeN):
            board[i][i] = 'x'
            CHARS['x'] = CHARS['x'] - 1
    if strategy == 'diag_reverse_f':
        for i in range(sizeN):
            board[sizeN-i][sizeN-i] = 'f'
            CHARS['f'] = CHARS['f'] - 1
    if strategy == 'diag_reverse_o':
        for i in range(sizeN):
            board[sizeN-i][sizeN-i] = 'o'
            CHARS['o'] = CHARS['o'] - 1
    if strategy == 'diag_reverse_x':
        for i in range(sizeN):
            board[sizeN-i][sizeN-i] = 'x'
            CHARS['x'] = CHARS['x'] - 1
    return board, CHARS


# Main function to play the game
def play_game(args, output_folder, game_id):

    if args.log_match:
        fout=open(f'{output_folder}/{game_id}.log','w')

    FLAG_FOUND_FOX=None

    board = [[" " for _ in range(args.size)] for _ in range(args.size)]
    cells = []
    for i in range(args.size):
      for j in range(args.size):
        cells.append((i,j))

    chars_bucket = {'f': args.f_chr, 'o': args.o_chr, 'x': args.x_chr}
    board, chars_bucket = init_board(board, chars_bucket, args.init_strategy)

    if __debug__:
        board2print = print_board(board)
        print(board2print)

    turn_counter = 0
    if args.log_match:
        board2print = print_board(board)
        fout.write(f'Turn: {turn_counter}\n')
        fout.write(board2print)

    while True:
        #Filling strategy is to randomly pick a cell in the grid and a char from the remaining.
        random.shuffle(cells)
        row, col = cells.pop(0)
        char_fox = sample_char(chars_bucket)

        if board[row][col] == " ":
            board[row][col] = char_fox
            chars_bucket[char_fox] = chars_bucket[char_fox] - 1
        else:
            if __debug__:
                print(f"Cell ({row},{col}) already taken, try again.")
            continue

        turn_counter+=1
        if args.log_match:
            board2print = print_board(board)
            fout.write(f'Turn: {turn_counter}\n')
            fout.write(board2print)

        winner = check_winner(board)
        if winner:
            FLAG_FOUND_FOX=True
            if __debug__:
                print(f"FOX FOUND!")
                print(print_board(board))
            if args.log_match:
                fout.write('==>FOX FOUND!')
            break

        if is_board_full(board):
            FLAG_FOUND_FOX=False
            if __debug__:
                print("FOX NOT FOUND")
                print(print_board(board))
            if args.log_match:
                fout.write('==>FOX NOT FOUND!')
            break
    if args.log_match:
        fout.close()

    return FLAG_FOUND_FOX


def create_output_folder():
    # Get current date and time
    now = datetime.now()
    # Format date and time as year-month-day-hour-minute-second
    folder_name = 'log_games/'+now.strftime("%Y-%m-%d-%H-%M-%S")
    # Create the folder
    os.makedirs(folder_name)
    print(f"Folder '{folder_name}' created successfully!")
    return folder_name

def main(args):

    output_folder=None
    if args.log_match:
        output_folder = create_output_folder()

    #count the number of wins/loss
    n_win = 0
    n_lost = 0
    for i in range(args.n_runs):
        game = play_game(args, output_folder=output_folder, game_id=i)
        if game:
            n_win += 1
        else:
            n_lost += 1
    print(f'After {i+1} runs --> {n_win} fox_found, {n_lost} fox_not_found')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the fox game!')

    # Add arguments
    parser.add_argument('--size', type=int, default=4, help='Size of the NxN grid.')
    parser.add_argument('--n-runs', type=int, default=1, help='Number of runs of the game')
    parser.add_argument('--init-strategy', type=str, default='empty', help='What is the initial setting of the grid')
    parser.add_argument('--log-match', action='store_true', help='Enable the flag to store in the ouptu folder (log_games) the games')
    parser.add_argument('--f-chr', type=int, default=50, help='Number of `f` char to sample')
    parser.add_argument('--o-chr', type=int, default=60, help='Number of `o` char to sample')
    parser.add_argument('--x-chr', type=int, default=50, help='Number of `x` char to sample')

    # Parse arguments
    args = parser.parse_args()

    print(args)

    main(args)
