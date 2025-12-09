import random
import time

# --- Global Constants ---
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
    [0, 4, 8], [2, 4, 6]             # Diagonals
]

HUMAN_PLAYER = 'X'
AI_PLAYER = 'O'
# --- Board and Display Functions ---

def display_board(board):
    """
    Prints the Tic-Tac-Toe board to the console.
    The numbers (1-9) correspond to the board indices for easy input.
    """
    print("\n   --- Current Board ---")
    print(f" {board[0] or 1} | {board[1] or 2} | {board[2] or 3} ")
    print("---|---|---")
    print(f" {board[3] or 4} | {board[4] or 5} | {board[5] or 6} ")
    print("---|---|---")
    print(f" {board[6] or 7} | {board[7] or 8} | {board[8] or 9} ")
    print("-----------------------\n")


# --- Game Logic Functions ---

def check_win(board, player):
    """
    Checks if the given player has won the game.
    :param board: The current state of the board.
    :param player: The player to check ('X' or 'O').
    :return: True if the player has won, False otherwise.
    """
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == player and board[b] == player and board[c] == player:
            return True
    return False

def check_draw(board):
    """
    Checks if the game is a draw (no empty cells left).
    :param board: The current state of the board.
    :return: True if it's a draw, False otherwise.
    """
    return '' not in board

# --- AI Strategy Functions ---

def find_strategic_move(board, player):
    """
    Finds a winning move or a blocking move for the given player.
    :param board: The current state of the board.
    :param player: The player symbol to look for.
    :return: The index of the strategic move (0-8) or None.
    """
    for a, b, c in WINNING_COMBINATIONS:
        line = [board[a], board[b], board[c]]
        
        # Check if the line has exactly two of the 'player' and one empty spot
        if line.count(player) == 2 and line.count('') == 1:
            # Find the index of the empty spot within the combination
            if board[a] == '':
                return a
            elif board[b] == '':
                return b
            elif board[c] == '':
                return c
    return None

def get_ai_move(board):
    """
    Determines the best move for the AI using a simple strategy.
    Strategy: 1. Win, 2. Block, 3. Center, 4. Random Corner/Side.
    :param board: The current state of the board.
    :return: The index of the AI's chosen move (0-8).
    """
    # 1. Check for a winning move (Offense)
    move = find_strategic_move(board, AI_PLAYER)
    if move is not None:
        return move

    # 2. Check for a blocking move (Defense)
    move = find_strategic_move(board, HUMAN_PLAYER)
    if move is not None:
        return move

    # 3. Take the center (index 4) if it's open
    if board[4] == '':
        return 4

    # 4. Take a random corner (indices 0, 2, 6, 8) if open
    corners = [i for i in [0, 2, 6, 8] if board[i] == '']
    if corners:
        return random.choice(corners)

    # 5. Take a random side (indices 1, 3, 5, 7) if open
    sides = [i for i in [1, 3, 5, 7] if board[i] == '']
    if sides:
        return random.choice(sides)

    # Should only happen if the board is full (a draw)
    return -1


# --- Main Game Loop ---

def play_game():
    """
    Main function to run the command-line Tic-Tac-Toe game.
    """
    print("Welcome to Tic-Tac-Toe!")
    print(f"You are {HUMAN_PLAYER}, and the AI is {AI_PLAYER}.")

    # Initialize the board with empty strings
    board = [''] * 9 
    current_turn = HUMAN_PLAYER
    game_active = True

    while game_active:
        display_board(board)
        
        if current_turn == HUMAN_PLAYER:
            while True:
                try:
                    # Input is 1-9, so we subtract 1 for the 0-8 index
                    move_input = input(f"Player {HUMAN_PLAYER}, enter your move (1-9): ")
                    move_index = int(move_input) - 1
                    
                    if 0 <= move_index <= 8 and board[move_index] == '':
                        board[move_index] = HUMAN_PLAYER
                        break
                    else:
                        print("Invalid move. Please choose an empty square (1-9).")
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 9.")
            
            # Check after Human move
            if check_win(board, HUMAN_PLAYER):
                display_board(board)
                print(f"*** Congratulations! Player {HUMAN_PLAYER} Wins! ***")
                game_active = False
            elif check_draw(board):
                display_board(board)
                print("--- It's a Draw! ---")
                game_active = False
            else:
                current_turn = AI_PLAYER

        # AI's Turn
        elif current_turn == AI_PLAYER and game_active:
            print(f"AI ({AI_PLAYER}) is thinking...")
            time.sleep(1) # Pause for a second to simulate thinking
            
            ai_move = get_ai_move(board)
            
            if ai_move != -1:
                board[ai_move] = AI_PLAYER
                print(f"AI chooses position {ai_move + 1}.")

                # Check after AI move
                if check_win(board, AI_PLAYER):
                    display_board(board)
                    print(f"*** Game Over! AI ({AI_PLAYER}) Wins! ***")
                    game_active = False
                elif check_draw(board):
                    display_board(board)
                    print("--- It's a Draw! ---")
                    game_active = False
                else:
                    current_turn = HUMAN_PLAYER
            else:
                # Should not happen if check_draw is working correctly, but as a safeguard
                game_active = False
                
    # Ask to play again
    while True:
        restart = input("\nDo you want to play again? (y/n): ").lower()
        if restart in ['y', 'yes']:
            play_game() # Recursively start a new game
            return # Exit current game loop
        elif restart in ['n', 'no']:
            print("Thanks for playing! Goodbye.")
            return # Exit the function
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


# Start the game automatically when the script is run
if __name__ == "__main__":
    play_game()