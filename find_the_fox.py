import os
import random
import argparse
from datetime import datetime

# Function to print the Fox board
def print_board(board):
    out_tmp=[]
    for row in board:
        out_tmp.append(" | ".join(row))
        out_tmp.append("-" * 14)
    out = '\n'.join(out_tmp[:-1])+'\n'
    return out

# Function to check for a winner
def check_winner(board):
    # Check rows for a winner
    for row in board:
        tmp0 = row[0]+row[1]+row[2]
        tmp1 = row[1]+row[2]+row[3]
        if tmp0 in ['fox','xof'] or tmp1 in ['fox','xof']:
          return True

    # Check columns for a winner
    for col in range(4):
        tmp0=board[0][col] + board[1][col] + board[2][col]
        tmp1=board[1][col] + board[2][col] + board[3][col]
        if tmp0 in ['fox','xof'] or tmp1 in ['fox','xof']:
          return True

    # Check diagonals for a winner
    tmp=[]
    tmp.append(board[0][0] + board[1][1] + board[2][2])
    tmp.append(board[1][1] + board[2][2] + board[3][3])
    tmp.append(board[0][3] + board[1][2] + board[2][1])
    tmp.append(board[0][2] + board[1][1] + board[2][0])
    tmp.append(board[0][1] + board[1][2] + board[2][3])
    tmp.append(board[1][0] + board[2][1] + board[3][2])
    tmp.append(board[0][2] + board[1][1] + board[2][0])
    tmp.append(board[1][3] + board[2][2] + board[3][1])

    if any([x in ['fox','xof'] for x in tmp]):
      return True

    return None

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

    if strategy == 'empty':
        return board, CHARS
    if strategy == 'diag_f':
        for i in range(4):
            board[i][i] = 'f'
            CHARS['f'] = CHARS['f'] - 1
    if strategy == 'diag_o':
        for i in range(4):
            board[i][i] = 'o'
            CHARS['o'] = CHARS['o'] - 1
    if strategy == 'diag_x':
        for i in range(4):
            board[i][i] = 'x'
            CHARS['x'] = CHARS['x'] - 1
    if strategy == 'diag_reverse_f':
        for i in range(4):
            board[3-i][3-i] = 'f'
            CHARS['f'] = CHARS['f'] - 1
    if strategy == 'diag_reverse_o':
        for i in range(4):
            board[3-i][3-i] = 'o'
            CHARS['o'] = CHARS['o'] - 1
    if strategy == 'diag_reverse_x':
        for i in range(4):
            board[3-i][3-i] = 'x'
            CHARS['x'] = CHARS['x'] - 1
    return board, CHARS


# Main function to play the game
def play_game(strategy, log_match, output_folder, game_id):

    if log_match:
        fout=open(f'{output_folder}/{game_id}.log','w')

    FLAG_FOUND_FOX=None
    #TODO: init number of chars
    CHARS_BUCKET={'f':5, 'o':5, 'x':6}

    board = [[" " for _ in range(4)] for _ in range(4)]
    cells = []
    for i in range(4):
      for j in range(4):
        cells.append((i,j))

    board, CHARS_BUCKET = init_board(board, CHARS_BUCKET, strategy)
    turn_counter = 0
    if args.log_match:
        board2print = print_board(board)
        fout.write(f'Turn: {turn_counter}\n')
        fout.write(board2print)

    while True:
        #Filling strategy is to randomly pick a cell in the grid and a char from the remaining.
        random.shuffle(cells)
        row, col = cells.pop(0)
        char_fox = sample_char(CHARS_BUCKET)

        if board[row][col] == " ":
            board[row][col] = char_fox
            CHARS_BUCKET[char_fox] = CHARS_BUCKET[char_fox] - 1
        else:
            if __debug__:
                print(f"Cell ({row},{col}) already taken, try again.")
            continue

        turn_counter+=1
        if log_match:
            board2print = print_board(board)
            fout.write(f'Turn: {turn_counter}\n')
            fout.write(board2print)

        winner = check_winner(board)
        if winner:
            FLAG_FOUND_FOX=True
            if __debug__:
                print(f"FOX FOUND!")
                print_board(board)
            if log_match:
                fout.write('==>FOX FOUND!')
            break

        if is_board_full(board):
            FLAG_FOUND_FOX=False
            if __debug__:
                print("Fox not found")
                print_board(board)
            if log_match:
                fout.write('==>FOX NOT FOUND!')
            break
    if log_match:
        fout.close()

    return FLAG_FOUND_FOX


def create_output_folder():
    # Get current date and time
    now = datetime.now()
    # Format date and time as year-month-day-hour-minute-second
    folder_name = 'log_game/'+now.strftime("%Y-%m-%d-%H-%M-%S")
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
        game = play_game(args.init_strategy, args.log_match, output_folder=output_folder, game_id=i)
        if game:
            n_win += 1
        else:
            n_lost += 1
    print(f'After {i+1} runs --> {n_win} fox_found, {n_lost} fox_not_found')




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a sample argparse program')

    # Add arguments
    parser.add_argument('--n-runs', type=int, default=1, help='Number of runs')
    parser.add_argument('--init-strategy', type=str, default='empty', help='Age of the person')
    parser.add_argument('--log-match', type=str, default='empty', help='Age of the person')

    # Parse arguments
    args = parser.parse_args()

    print(args)

    main(args)

