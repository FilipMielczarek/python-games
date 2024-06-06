def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    for row in board:
        print("|".join(row))
        print("-" * 5)


def check_winner(board, player):
    """Checks if the given player has won."""
    # Check rows, columns, and diagonals
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    return [player, player, player] in win_states


def check_draw(board):
    """Checks if the game is a draw."""
    for row in board:
        if " " in row:
            return False
    return True


def tic_tac_toe():
    """Main function to play Tic-Tac-Toe."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)

        # Get player input
        try:
            row, col = map(
                int,
                input(
                    f"Player {current_player}, enter row and column (0, 1, or 2): "
                ).split(),
            )
            if board[row][col] != " ":
                print("Cell is already taken. Try again.")
                continue
        except (ValueError, IndexError):
            print("Invalid input. Enter row and column numbers between 0 and 2.")
            continue

        # Place the mark and check for a win or draw
        board[row][col] = current_player
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch players
        current_player = "O" if current_player == "X" else "X"


# Run the game
tic_tac_toe()
