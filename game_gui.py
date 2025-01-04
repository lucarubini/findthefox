import argparse
import pygame
import sys
from utils import FindFoxBoardGUI

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
#CHAR_COLOR = (239, 231, 200)




def main(args):

    # Constants
    WIDTH, HEIGHT = 400, 400
    LINE_WIDTH = 15
    BOARD_ROWS, BOARD_COLS = args.size, args.size
    SQUARE_SIZE = WIDTH // BOARD_COLS
    #CIRCLE_RADIUS = SQUARE_SIZE // 3
    #CIRCLE_WIDTH = 5
    #CROSS_WIDTH = 5
    #SPACE = SQUARE_SIZE // 4

    bucket = {'f': args.f_chr, 'o': args.o_chr, 'x': args.x_chr}
    board = FindFoxBoardGUI(args.size, args.init_strategy, bucket)
    #import code
    #code.interact(local=locals())

    # Initialize pygame
    pygame.init()

    # Screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Do Not Find the Fox')
    screen.fill(BG_COLOR)

    # Game loop
    game_over = False
    board.draw_lines(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if board.available_cell(clicked_row, clicked_col):

                    sampled_char = board.sample_char()
                    board.mark_cell(clicked_row, clicked_col, sampled_char)
                    board.bucket[sampled_char] = board.bucket[sampled_char] - 1
                    if board.check_winner():
                        game_over = True

                    board.draw_chars(screen)

        pygame.display.update()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the fox game!')

    # Add arguments
    parser.add_argument('--size', type=int, default=4, help='Size of the NxN grid.')
    parser.add_argument('--init-strategy', type=str, default='empty', help='What is the initial setting of the grid', \
        choices=['diag_f', 'diag_o', 'diag_x', 'diag_reverse_f', 'diag_reverse_o', 'diag_reverse_x', 'empty'])
    parser.add_argument('--f-chr', type=int, default=50, help='Number of `f` char to sample')
    parser.add_argument('--o-chr', type=int, default=60, help='Number of `o` char to sample')
    parser.add_argument('--x-chr', type=int, default=50, help='Number of `x` char to sample')

    # Parse arguments
    args = parser.parse_args()

    print(args)

    main(args)
