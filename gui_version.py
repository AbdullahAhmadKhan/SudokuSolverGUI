import pygame
import main
pygame.font.init()

screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption("Sudoku Solver")
myfont = pygame.font.SysFont('Comic Sans MS', 20)


# A box class for each cell
class Box:
    def __init__(self, board, row, column):
        self.row = row
        self.column = column
        self.orig_value = board[row][column]
        self.pencil_value = 0
        self.selected = False

    def is_pencillable(self):
        if self.orig_value != 0:
            return False
        else:
            return True

    def set_pencil_value(self, value):
        self.pencil_value = value

    def get_orig_value(self):
        return self.orig_value

    def set_orig_value(self, val):
        self.orig_value = val

    def activate(self, val):
        self.selected = val

    def return_active(self):
        return self.selected

    def get_pencil_value(self):
        return self.pencil_value


# Initializing a matrix of Box objects representing the cells
grid_array = []
for i in range(9):
    grid_array.append([])
    for j in range(9):
        grid_array[i].append(Box(main.board, i, j))

# Drawing each element of the GUI
def draw(grid_array):
    # Drawing the vertical and horizontal dark lines
    pygame.draw.line(screen, (0, 0, 0), (150, 0), (150, 450), 3)
    pygame.draw.line(screen, (0, 0, 0), (300, 0), (300, 450), 3)
    pygame.draw.line(screen, (0, 0, 0), (0, 150), (450, 150), 3)
    pygame.draw.line(screen, (0, 0, 0), (0, 300), (450, 300), 3)

    # Drawing the horizontal light lines
    for i in range(1, 10):
        if i % 3 == 0:
            continue
        else:
            pygame.draw.line(screen, (0, 0, 0), (0, 50 * i), (450, 50 * i), 1)

    # Drawing the vertical light lines
    for i in range(1, 10):
        if i % 3 == 0:
            continue
        else:
            pygame.draw.line(screen, (0, 0, 0), (50 * i, 0), (50 * i, 450), 1)

    # Displaying the value of each Box object in the grid_array
    for i in range(9):
        for j in range(9):
            if grid_array[i][j].get_orig_value() == 0:
                continue
            else:
                textsurface = myfont.render(str(grid_array[i][j].get_orig_value()), False, (0, 0, 0))
                screen.blit(textsurface, ((j * 50) + 20, (i * 50) + 10))


# Function used to check for events manually to avoid the program crashing
input_value = 0
running = True
def look_for_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos_x = pos[0] // 50
            pos_y = pos[1] // 50
            for i in range(9):
                for j in range(9):
                    if grid_array[i][j].return_active() == True:
                        grid_array[i][j].activate(False)
                        input_value = 0

            grid_array[pos_y][pos_x].activate(True)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                input_value = 1
            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                input_value = 2
            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                input_value = 3
            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                input_value = 4
            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                input_value = 5
            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                input_value = 6
            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                input_value = 7
            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                input_value = 8
            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                input_value = 9
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                for i in range(9):
                    for j in range(9):
                        if grid_array[i][j].return_active() == True:
                            if grid_array[i][j].get_pencil_value() == main.board_solved[i][j]:
                                grid_array[i][j].set_orig_value(grid_array[i][j].get_pencil_value())
                                grid_array[i][j].set_pencil_value(0)
                                grid_array[i][j].activate(False)
                                main.board[i][j] = main.board_solved[i][j]
                                input_value = 0
            if event.key == pygame.K_SPACE:
                print("Space hit")
                solver_GUI(main.board, grid_array, 0, 0)


# A modified version of the original solver function to display how the algorithm works
solved = False
def solver_GUI(board, grid_array, row, column):
    if row == 9:    # end of board
        global solved
        solved = True
        return
    elif board[row][column] != 0:   # it is a number other than 0
        if column == 8:
            solver_GUI(board, grid_array, row + 1, 0)
            if solved:
                return
            else:
                pygame.draw.rect(screen, (0, 0, 255), (50 * column, 50 * row, 50, 50), 2)
                pygame.display.update()
                pygame.time.wait(250)
                look_for_events()
        else:
            solver_GUI(board, grid_array, row, column + 1)
            if solved:
                return
            else:
                pygame.draw.rect(screen, (0, 0, 255), (50 * column, 50 * row, 50, 50), 2)
                pygame.display.update()
                pygame.time.wait(250)
                look_for_events()
    else:
        pygame.draw.rect(screen, (0, 255, 0), (50 * column, 50 * row, 50, 50), 2)
        pygame.display.update()
        pygame.time.wait(250)
        look_for_events()
        choice_array = main.valid_choices(board, row, column)
        if choice_array == []:     # no valid choices
            pygame.draw.rect(screen, (0, 0, 255), (50 * column, 50 * row, 50, 50), 2)
            pygame.display.update()
            pygame.time.wait(250)
            look_for_events()
            return

        for i in range(len(choice_array)):
            pygame.draw.rect(screen, (0, 255, 0), (50 * column, 50 * row, 50, 50), 2) 
            board[row][column] = choice_array[i]
            grid_array[row][column].set_orig_value(choice_array[i])
            screen.fill((255, 255, 255))
            draw(grid_array)
            pygame.display.update()
            pygame.time.wait(250)
            look_for_events()
            if column == 8:
                solver_GUI(board, grid_array, row + 1, 0)
                if solved:
                    return
                else:
                    pygame.draw.rect(screen, (0, 0, 255), (50 * column, 50 * row, 50, 50), 2)
                    pygame.display.update()
                    pygame.time.wait(250)
                    look_for_events()

            else:
                solver_GUI(board, grid_array, row, column + 1)
                if solved:
                    return
                else:
                    pygame.draw.rect(screen, (0, 0, 255), (50 * column, 50 * row, 50, 50), 2)
                    pygame.display.update()
                    pygame.time.wait(250)
                    look_for_events()


while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos_x = pos[0] // 50
            pos_y = pos[1] // 50
            for i in range(9):
                for j in range(9):
                    if grid_array[i][j].return_active() == True:
                        grid_array[i][j].activate(False)
                        input_value = 0

            grid_array[pos_y][pos_x].activate(True)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                input_value = 1
            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                input_value = 2
            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                input_value = 3
            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                input_value = 4
            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                input_value = 5
            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                input_value = 6
            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                input_value = 7
            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                input_value = 8
            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                input_value = 9
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                for i in range(9):
                    for j in range(9):
                        if grid_array[i][j].return_active() == True:
                            if grid_array[i][j].get_pencil_value() == main.board_solved[i][j]:
                                grid_array[i][j].set_orig_value(grid_array[i][j].get_pencil_value())
                                grid_array[i][j].set_pencil_value(0)
                                grid_array[i][j].activate(False)
                                main.board[i][j] = main.board_solved[i][j]
                                input_value = 0
            if event.key == pygame.K_SPACE:
                print("Space hit")
                solver_GUI(main.board, grid_array, 0, 0)

    draw(grid_array)

    for i in range(9):
        for j in range(9):
            if grid_array[i][j].return_active() == True:

                # Coloring the selected box
                pygame.draw.rect(screen, (255, 0, 0), (50 * j, 50 * i, 50, 50), 2)
                if input_value != 0 and grid_array[i][j].is_pencillable() == True:

                    # Setting the pencil value to the input value
                    grid_array[i][j].set_pencil_value(input_value)

            if grid_array[i][j].get_pencil_value() != 0:

                # Displaying the pencil value
                textsurface = myfont.render(str(grid_array[i][j].get_pencil_value()), False, (169, 169, 169))
                screen.blit(textsurface, ((j * 50) + 20, (i * 50) + 10))

    pygame.display.update()