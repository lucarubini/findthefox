import os
import argparse
from datetime import datetime
from utils import FindFoxBoard


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
    n_win, n_lost = 0, 0
    for i in range(args.n_runs):
        bucket = {'f': args.f_chr, 'o': args.o_chr, 'x': args.x_chr}
        board = FindFoxBoard(args.size, args.init_strategy, bucket)
        game_outcome = board.play_game_cli(output_folder, i)
        if game_outcome:
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
