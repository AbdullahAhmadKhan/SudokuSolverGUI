board = [[1,  0,  6,  0,  0,  2,  3,  0,  0],
         [0,  5,  0,  0,  0,  6,  0,  9,  1],
         [0,  0,  9,  5,  0,  1,  4,  6,  2],
         [0,  3,  7,  9,  0,  5,  0,  0,  0],
         [5,  8,  1,  0,  2,  7,  9,  0,  0],
         [0,  0,  0,  4,  0,  8,  1,  5,  7],
         [0,  0,  0,  2,  6,  0,  5,  4,  0],
         [0,  0,  4,  1,  5,  0,  6,  0,  9],
         [9,  0,  0,  8,  7,  4,  2,  1,  0]]

# Create a copy of the original board
board_solved = []
for i in range(9):
    board_solved.append([])
    for j in range(9):
        board_solved[i].append(board[i][j])


# Printing the board
def print_board(board):
    for i in range(9):  # rows
        for j in range(9):  # columns
            if (j + 1) % 3 == 0 and j != 8:
                print(board[i][j], end="|")
            elif j == 8:
                print(board[i][j])
            else:
                print(board[i][j], end="")
        if (i + 1) % 3 == 0 and i != 8:
            print('-----------')


# Creating an array containing the non valid choices for a cell
def non_valid_choices(board, row, column):
    arr = []
    # Checking the rows
    for j in range(9):
        if board[row][j] != 0:
            arr.append(board[row][j])

    # Checking the columns
    for i in range(9):
        if board[i][column] != 0:
            arr.append(board[i][column])

    # Checking the grid
    box_x = column // 3
    box_y = row // 3

    for i in range(3):
        for j in range(3):
            if board[(3 * box_y) + i][(3 * box_x) + j] != 0:
                arr.append(board[(box_y * 3) + i][(box_x * 3) + j])
    return arr


# Creating an array containing the valid choices for a cell
def valid_choices(board, row, column):
    arr = non_valid_choices(board, row, column)
    valid_choices = []
    for i in range(1, 10):
        if i in arr:
            continue
        else:
            valid_choices.append(i)
    return valid_choices


# Flag for algorithm to stop
solved = False


# Main solver function
def solver(board, row, column):

    # Base condition
    if row == 9:
        global solved
        solved = True
        return

    # If the cell value has already been given
    elif board[row][column] != 0:
        if column == 8:
            solver(board, row + 1, 0)
            if solved:
                return
        else:
            solver(board, row, column + 1)
            if solved:
                return

    # If the cell doesn't have a value
    else:
        choice_array = valid_choices(board, row, column)

        # If the cell has no valid choice of value with the given set
        if not choice_array:
            return

        # Looping through all the possible values for a cell with the given set
        for i in range(len(choice_array)):
            board[row][column] = choice_array[i]
            if column == 8:
                solver(board, row + 1, 0)
                if solved:
                    return
            else:
                solver(board, row, column + 1)
                if solved:
                    return


print_board(board)
print('\n', '\n')
solver(board_solved, 0, 0)
print_board(board_solved)