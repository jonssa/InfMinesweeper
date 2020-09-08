import random
import copy


class Board:
    def __init__(self):
        self.board_x_size = 10
        self.board_y_size = 10
        self.board_size = self.board_x_size * self.board_y_size
        # Mines count in board
        self.mines_count = 3
        # grid array contain every cell in board
        self.grid = []
        # depth says how big unclickable area is
        self.depth = 5
        # reveal_depth says how many lines of board need to be added to board if you click on the board border
        self.reveal_depth = 3
        self.border = []
        self.constrains = []

    def set_size_and_mines(self):
        # set_size_and_mines() - set board start size and mines count
        # set how many column board will have
        # self.board_x_size = random.randint(5, 10)
        self.board_x_size = 10
        # set how many rows board will have
        # self.board_y_size = random.randint(5, 10)
        self.board_y_size = 10
        # count board size
        self.board_size = self.board_x_size * self.board_y_size
        # set how many mines start board will have
        # self.mines_count = random.randint(5, int(self.board_size / 4))
        self.mines_count = 30
        Cell.mine_counter = 30

    def create_grid(self):
        # create_grid() - create array containing all cells in board
        # for every row
        for row in range(int(self.board_y_size)):
            # for every column
            for column in range(int(self.board_x_size)):
                # add to grid array new cell
                self.grid.append(Cell(column, row))

    def create_minefield(self):
        # for every mine in mines_count
        for num in range(int(self.mines_count)):
            # pick random place for mine
            rand_ = random.randint(0, self.board_size - 1)
            # while chosen cell is mine
            while self.grid[rand_].check_if_mine():
                # pick another random cell
                rand_ = random.randint(0, self.board_size - 1)
            # set mine
            self.grid[rand_].set_mine()
        # for every cell in board, count adjacent mines
        for cell_pos in range(int(self.board_size)):
            # find cell neighbors
            self.find_neighbors(cell_pos)
            self.check_adjacent(cell_pos)

    def show_board(self):
        # for every row and margin
        for row in range(self.board_y_size + 2 * self.depth):
            # for every column and margin
            for column in range(self.board_x_size + 2 * self.depth):
                space = " "
                # check if current position is not on margin return, if not return next cell to show
                next_cell = next((cell for cell in self.grid if cell.x_pos + self.depth == column and cell.y_pos +
                                  self.depth == row), None)
                # if it is cell
                if next_cell:
                    # if cell is not hidden
                    if not next_cell.check_if_hidden():
                        # if flagged print 'F'
                        if next_cell.check_if_flag():
                            item = " F"
                        # if mined you lost game and print '*'
                        elif next_cell.check_if_mine():
                            item = " *"
                        # if it is safe show cell adjacent mine
                        else:
                            item = " " + str(next_cell.check_adjacency())
                    # if cell is hidden show '#
                    else:
                        item = " #"
                # if it is margin
                else:
                    item = " ."
                    # if true go to next line
                    if (column % (int(self.board_x_size) + 2 * self.depth)) == \
                            (int(self.board_x_size) + 2 * self.depth - 1):
                        space = " \n"
                    else:
                        space = " "
                # print one row
                print(item + space, sep=' ', end='', flush=True)
        print("")

    def show_cell(self, x, y):
        pos = self.grid.index(next(obj for obj in self.grid if (obj.x_pos == x and obj.y_pos == y)))
        if not self.check_if_all_neighbors(x, y):
            last = len(self.grid)
            #self.grid += self.create_cells(x, y)
            for pos in range(last, len(self.grid)):
                self.find_neighbors(pos)
                self.check_adjacent(pos)
            pos = self.grid.index(next(obj for obj in self.grid if (obj.x_pos == x and obj.y_pos == y)))
        if (self.grid[pos].check_adjacency() == 0) and self.grid[pos].check_if_hidden() \
                and not self.grid[pos].check_if_mine():
            self.show_more_cells(pos)
        if self.grid[pos].check_if_mine():
            return True
        no_mine = True
        self.grid[pos].uncover_cell()
        x = self.grid[pos].get_cell_x_pos()
        y = self.grid[pos].get_cell_y_pos()
        for adj_pos in range(Cell.counter):
            adj_x = self.grid[adj_pos].get_cell_x_pos()
            adj_y = self.grid[adj_pos].get_cell_y_pos()
            if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                if int(self.grid[adj_pos].check_if_mine()):
                    no_mine = False
                if (self.grid[adj_pos].check_adjacency() == 0) and self.grid[adj_pos].check_if_hidden() \
                        and not self.grid[adj_pos].check_if_mine():
                    self.show_more_cells(adj_pos)
        if no_mine:
            for adj_pos in range(Cell.counter):
                adj_x = self.grid[adj_pos].get_cell_x_pos()
                adj_y = self.grid[adj_pos].get_cell_y_pos()
                if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                    if (self.grid[adj_pos].check_adjacency() == 0) and self.grid[adj_pos].check_if_hidden() \
                            and not self.grid[adj_pos].check_if_mine():
                        self.show_more_cells(adj_pos)
                    else:
                        self.grid[adj_pos].uncover_cell()
        return False

    def show_more_cells(self, pos):
        self.grid[pos].uncover_cell()
        x = self.grid[pos].get_cell_x_pos()
        y = self.grid[pos].get_cell_y_pos()
        for adj_pos in range(Cell.counter):
            adj_x = self.grid[adj_pos].get_cell_x_pos()
            adj_y = self.grid[adj_pos].get_cell_y_pos()
            if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                if (self.grid[adj_pos].check_adjacency() == 0) and self.grid[adj_pos].check_if_hidden() \
                        and not self.grid[adj_pos].check_if_mine():
                    self.show_more_cells(adj_pos)
                else:
                    self.grid[adj_pos].uncover_cell()

    def create_cells(self, x, y):
        list_ = []
        if x == 0 or y == 0 or x == self.board_x_size - 1 or y == self.board_y_size - 1:
            self.update_cells_positions(x, y)
        for xx in range(0 if x == 0 else x-1, x+3 if x == 0 else x+2):  #x=0: x,x+1
            for yy in range(0 if y == 0 else y-1, y+3 if y == 0 else y+2):  #x=0: y-1, y+2
                try:
                    if next((cell for cell in self.grid if cell.x_pos == xx and cell.y_pos == yy), False):
                        continue
                    else:
                        cell_ = Cell(xx, yy)
                        rand = random.randint(0, 10)
                        if rand <= 2 and not cell_.check_if_mine():
                            cell_.set_mine()
                        else:
                            if cell_.check_if_mine():
                                cell_.unset_mine()
                        list_.append(cell_)
                        print("Cell index: %d")
                except:
                    list_.append(Cell(xx, yy))
                    print("Cell index: %d", )
        return list_

    def update_cells_positions(self, x, y):
        if x == 0 or x == self.board_x_size - 1:
            self.board_x_size += 1
            for cell in self.grid:
                if x == 0:
                    cell.x_pos += 1
        if y == 0 or y == self.board_y_size - 1:
            self.board_y_size += 1
            for cell in self.grid:
                if y == 0:
                    cell.y_pos += 1

    # check if cell has all of his neighbors
    def check_if_all_neighbors(self, x, y):
        for adj_y_pos in range(y-1, y+2):
            for adj_x_pos in range(x-1, x+2):
                if next((True for obj in self.grid if obj.x_pos == adj_x_pos and obj.y_pos == adj_y_pos), False):
                    continue
                else:
                    return False
        return True

    # find_neighbors(pos) - find all cell neighbors
    # id_ - cell id in board array
    def find_neighbors(self, id_):
        self.grid[id_].cell_neighbors.clear()
        # check current cell position in board
        cur_x_pos = int(self.grid[id_].get_cell_x_pos())
        cur_y_pos = int(self.grid[id_].get_cell_y_pos())
        # for all cell in board
        for adj_id_ in range(int(self.board_size)):
            # check cell position
            adj_x_pos = int(self.grid[adj_id_].get_cell_x_pos())
            adj_y_pos = int(self.grid[adj_id_].get_cell_y_pos())
            # if chosen cell is neighbour to checked cell
            if -1 <= cur_x_pos - adj_x_pos <= 1 and -1 <= cur_y_pos - adj_y_pos <= 1:
                # and if chosen cell is not the current checked cell
                if not (cur_x_pos == adj_x_pos and cur_y_pos == adj_y_pos):
                    # add cell to checked cell neighbors array
                    self.grid[id_].cell_neighbors.append(self.grid[adj_id_])

    # check_adjacent() - check adjacent cells and count mines in them
    # id_ - cell id in board array
    def check_adjacent(self, id_):
        # set adjacent mines counter to 0
        self.grid[id_].adjacent_mines = 0
        # if checked cell is not mine
        if not self.grid[id_].check_if_mine():
            # for all cell neighbours
            for neighbor_cell in self.grid[id_].cell_neighbors:
                # if neighbour is not mine
                if neighbor_cell.check_if_mine():
                    # add 1 to adjacent mines counter
                    self.grid[id_].adjacent_mines += 1

    # Check adjacent cells and count flags in them
    def count_adjacent_flags(self, pos):
        self.grid[pos].adjacent_flags = 0
        cur_x_pos = int(self.grid[pos].get_cell_x_pos())
        cur_y_pos = int(self.grid[pos].get_cell_y_pos())
        if not self.grid[pos].check_if_mine():
            for adj_pos in range(int(self.board_size)):
                adj_x_pos = int(self.grid[adj_pos].get_cell_x_pos())
                adj_y_pos = int(self.grid[adj_pos].get_cell_y_pos())
                if not (cur_x_pos == adj_x_pos and cur_y_pos == adj_y_pos):
                    if -1 <= cur_x_pos - adj_x_pos <= 1 and -1 <= cur_y_pos - adj_y_pos <= 1:
                        if self.grid[adj_pos].check_if_flag():
                            self.grid[pos].adjacent_flags += 1
        return self.grid[pos].adjacent_flags

    def return_board_size(self):
        return self.board_size

    def change_board_x_size(self, x):
        self.board_x_size = x
        self.board_size = self.board_x_size * self.board_y_size

    def change_board_y_size(self, y):
        self.board_y_size = y
        self.board_size = self.board_x_size * self.board_y_size

    def return_mines_count(self):
        return self.mines_count

    #   cell_index() - return cell index in board grid
    #   x - cell x position (column position)
    #   y - cell y position (row position)
    def cell_index(self, x, y):
        return self.grid.index(next((obj for obj in self.grid if obj.x_pos == x and obj.y_pos == y), None))


class Cell:
    mine_counter = 0
    flag_counter = 0
    counter = 0

    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.is_mine = False
        self.is_flag = False
        self.is_hidden = True
        self.adjacent_mines = 0
        self.adjacent_flags = 0
        self.cell_neighbors = []
        Cell.counter += 1

    def check_if_mine(self):
        if self.is_mine:
            return True
        return False

    def check_if_hidden(self):
        if self.is_hidden:
            return True
        return False

    def check_if_flag(self):
        if self.is_flag:
            return True
        return False

    def toggle_flag(self):
        if self.check_if_flag():
            self.is_flag = False
            self.cover_cell()
        else:
            self.is_flag = True
            self.uncover_cell()

    def set_flag(self):
        if not self.check_if_flag():
            self.is_flag = True
            self.uncover_cell()

    def unset_flag(self):
        if self.check_if_flag():
            self.is_flag = False
            self.cover_cell()

    def set_mine(self):
        self.is_mine = True
        self.is_hidden = True
        #Cell.mine_counter += 1

    def unset_mine(self):
        self.is_mine = False
        self.is_hidden = True
        #Cell.mine_counter -= 1

    def get_cell_x_pos(self):
        return self.x_pos

    def get_cell_y_pos(self):
        return self.y_pos

    def cover_cell(self):
        self.is_hidden = True

    def uncover_cell(self):
        self.is_hidden = False

    # Return count of mines in adjacent cells
    def check_adjacency(self):
        return self.adjacent_mines

    # Return count of flags in adjacent cells
    def check_flags(self):
        return self.adjacent_flags

    def check_if_has_neighbour(self, board):
        x = self.get_cell_x_pos()
        y = self.get_cell_y_pos()
        for adj_y_pos in range(y-1, y+2):
            for adj_x_pos in range(x-1, x+2):
                cell = next((obj for obj in board.grid if obj.x_pos == adj_x_pos and obj.y_pos == adj_y_pos), None)
                if cell:
                    if not cell.check_if_hidden() and ((cell.check_adjacency() != 0) or cell.check_if_flag()):
                        return True
        return False

    def check_if_constraint(self, board):
        x = self.get_cell_x_pos()
        y = self.get_cell_y_pos()
        for adj_y_pos in range(y - 1, y + 2):
            for adj_x_pos in range(x - 1, x + 2):
                cell = next((obj for obj in board.grid if obj.x_pos == adj_x_pos and obj.y_pos == adj_y_pos), None)
                if cell:
                    if cell.check_if_hidden():
                        return True
        return False


class Solver:

    resolved = []
    flag_counter = 0

    def __init__(self, board):
        self.temp_board = copy.deepcopy(board)
        self.solved_board = []
        self.solved_border = []
        self.grid = []
        self.border = [Cell]
        self.constrains = []
        resolved = []

    def solve(self, board):
        print("Solver this is my board: ")
        board.show_board()
        print("Can you solve it?")
        while not self.try_to_solve(board, 0):
            self.generate_adjacent(board)
            print("Is it ok?")
            board.show_board()
        # self.find_border(board)
        # self.find_constrains(board)
        # board.border = copy.deepcopy(self.border)
        # board.constrains = copy.deepcopy(self.constrains)
        # self.swap_border(board)
        board = copy.deepcopy(self.solved_board)
        for cell in board.grid:
            cell.cover_cell()
            cell.unset_flag()
        Solver.flag_counter = 0
        return board

    def try_to_solve(self, board, depth):
        temp_board = copy.deepcopy(board)
        solvable = self.check_if_solvable(temp_board, depth)
        while not solvable:
            print("Mines: ", Cell.mine_counter)
            print("Flags: ", Solver.flag_counter)
            if Cell.mine_counter == Solver.flag_counter:
                print("NP, I can solve it!")
                temp_board.show_board()
                self.solved_board = temp_board
                return True
            if depth != 0:
                self.generate_adjacent(temp_board)
            elif depth == 0 and not self.check_if_solvable(temp_board, depth):
                print("Sorry can't solve it, try another adjustment")
                return False
            if self.check_if_solvable(temp_board, depth):
                solvable = True
        self.try_to_solve(temp_board, depth+1)
        return True

    def check_if_solvable(self, board, depth):
        self.find_constrains(board)
        self.find_border(board)
        #board.show_board()
        for cell in self.constrains:
            x = cell.get_cell_x_pos()
            y = cell.get_cell_y_pos()
            if self.check_if_safe(board, x, y):
                self.show_resolved(board)
                return True
        return False

    def check_if_safe(self, brd, x, y):
        hidden_neighbors = 0
        for adj_y_pos in range(y-1, y+2):
            for adj_x_pos in range(x-1, x+2):
                cell = next((obj for obj in self.border if obj.x_pos == adj_x_pos and obj.y_pos == adj_y_pos), None)
                if cell:
                    if cell.check_if_hidden():
                        hidden_neighbors += 1
        cell = next((obj for obj in self.constrains if obj.x_pos == x and obj.y_pos == y), None)
        idx = brd.cell_index(x, y)
        if hidden_neighbors == (cell.check_adjacency() - brd.count_adjacent_flags(idx)) != 0:
            self.resolved.append(["M", cell.x_pos, cell.y_pos])
        elif (cell.check_adjacency() == brd.count_adjacent_flags(idx) != 0) and hidden_neighbors != 0:
            self.resolved.append(["E", cell.x_pos, cell.y_pos])
        else:
            return False
        return True

    def find_border(self, board):
        # if cell has at last one visible neighbour
        self.border.clear()
        for cell in board.grid:
            if cell.check_if_hidden() and cell.check_if_has_neighbour(board):
                self.border.append(cell)

    def find_constrains(self, board):
        self.constrains.clear()
        for cell in board.grid:
            if not cell.check_if_hidden() and cell.check_if_constraint(board):
                self.constrains.append(cell)

    def check_adjacent_neighbors(self, x, y):
        mines, neighbors = 0, 0
        for adj_y_pos in range(y-1, y+2):
            for adj_x_pos in range(x-1, x+2):
                cell = next((obj for obj in self.grid if obj.x_pos == adj_x_pos and obj.y_pos == adj_y_pos), None)
                if cell:
                    neighbors += 1
                    if cell.check_if_mine():
                        mines += 1
        return mines, neighbors

    def show_resolved(self, board):
        self.grid = self.temp_board.grid
        for cell_ in self.resolved:
            x, y = cell_[1], cell_[2]
            for adj_y_pos in range(y-1, y+2):
                for adj_x_pos in range(x-1, x+2):
                    cell = next((obj for obj in self.grid if obj.x_pos == adj_x_pos and obj.y_pos == adj_y_pos), None)
                    if cell:
                        if cell_[0] == "E":
                            board.grid[board.cell_index(adj_x_pos, adj_y_pos)].uncover_cell()
                        else:
                            if board.grid[board.cell_index(adj_x_pos, adj_y_pos)].check_if_hidden():
                                if not board.grid[board.cell_index(adj_x_pos, adj_y_pos)].check_if_flag():
                                    board.grid[board.cell_index(adj_x_pos, adj_y_pos)].set_flag()
                                    Solver.flag_counter += 1
                                else:
                                    board.grid[board.cell_index(adj_x_pos, adj_y_pos)].unset_flag()
                                    Solver.flag_counter -= 1
                        board.show_cell(x, y)
            self.resolved.remove(cell_)

    # generate_adjacent() - generate new properties for adjacent cells
    def generate_adjacent(self, board):
        # find border in board
        self.find_border(board)
        # for border generate new set of mine
        Cell.mine_counter = 0
        for cell in board.grid:
            if cell.check_if_mine():
                Cell.mine_counter += 1
        for cell in self.border:
            rand = random.randint(0, 10)
            if rand <= 4 and not cell.check_if_mine():
                cell.set_mine()
            else:
                if cell.check_if_mine():
                    cell.unset_mine()
        # count new adjacent mines for board
        for pos in range(Cell.counter):
            board.find_neighbors(pos)
            board.check_adjacent(pos)
        # find constrains in border
        self.find_constrains(board)
        # for every cell in constrain check if their adjacent mines count is equal to zero
        for cell in self.constrains:
            if cell.check_adjacency() == 0 and not cell.check_if_mine() and not cell.check_if_hidden():
                # if it is show cells around that cell
                board.show_more_cells(board.cell_index(cell.x_pos, cell.y_pos))
        # find border in board
        self.find_border(board)
        # find constrains in border
        self.find_constrains(board)

    # def swap_border(self, board):
    #     for cell in board.constrains:
    #         board.grid[board.cell_index(cell.x_pos, cell.y_pos)] = self.solved_board.grid[
    #             self.solved_board.cell_index(cell.x_pos, cell.y_pos)]
    #         if board.grid[board.cell_index(cell.x_pos, cell.y_pos)].adjacent_mines == 0:
    #             board.show_cell(cell.x_pos - 1, cell.y_pos - 1)
    #     for cell in board.border:
    #         board.grid[board.cell_index(cell.x_pos, cell.y_pos)] = self.solved_board.grid[
    #             self.solved_board.cell_index(cell.x_pos, cell.y_pos)]
    #         board.grid[board.cell_index(cell.x_pos, cell.y_pos)].cover_cell()


class Generator(Board):

    def generate_map(self, board):
        pass


def game():
    print("Hello World!")
    board = Board()
    board.set_size_and_mines()
    print("Creating new Board ...")
    board.create_grid()
    board.create_minefield()
    print("Number of cells: ", Cell.counter)
    board.show_board()
    solver = Solver(board)
    print("Which cell You want to uncover?")
    x = int(input("X = "))
    y = int(input("Y = "))
    if board.grid[board.cell_index(x-1, y-1)].check_if_mine():
        board.grid[board.cell_index(x - 1, y - 1)].unset_mine()
    board.show_cell(x - 1, y - 1)
    board.show_board()
    while(1):
        choice = "1"
        try:
            solver.find_border(board)
            solver.find_constrains(board)
            board = solver.solve(copy.deepcopy(board))
            print("Original board")
            board.show_cell(x - 1, y - 1)
            board.show_board()
            print("Which cell You want to uncover?")
            x = int(input("X = "))
            y = int(input("Y = "))
            if input("F to flag?") == "f":
                board.grid[board.cell_index(x-1, y-1)].toggle_flag()
        except:
            print("Error")


if __name__ == "__main__":
    try:
        game()
    except KeyboardInterrupt:
        print('\nEnd of Game. Bye Bye!')
