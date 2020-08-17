import random


class Board:
    def __init__(self):
        self.board_size = 5
        self.mines_count = 3
        self.grid = []
        self.depth = 5

    def set_size_and_mines(self):
        size = input("New start board size: ")
        mines = input("New start mines count: ")
        print(" ")
        self.mines_count = int(mines)
        self.board_size = int(size)

    def create_grid(self):
        #self.grid = [[[Cell] for row in range(int(self.board_size))] for column in range(int(self.board_size))]
        for row in range(int(self.board_size)):
            for column in range(int(self.board_size)):
                self.grid.append(Cell(column, row))

    def show_grid(self):
        for row in range(int(self.board_size) + 2 * self.depth):
            for column in range(int(self.board_size) + 2 * self.depth):
                if next((obj for obj in self.grid if obj.x_pos + self.depth == row and obj.y_pos + self.depth == column), False):
                    item = " #"
                else:
                    item = " U"
                print(item, sep=' ', end='', flush=True)
            print("")

    def refresh_grid(self):
        for row in range(self.board_size + 2 * self.depth):
            for column in range(self.board_size + 2 * self.depth):
                space = " "
                if next((obj for obj in self.grid if obj.x_pos + self.depth == column and obj.y_pos + self.depth == row), False):
                    if not self.grid[self.board_size * (row - self.depth) + column - self.depth].check_if_hidden():
                        if self.grid[self.board_size * (row - self.depth) + column - self.depth].check_if_mine():
                            item = " #"
                        else:
                            item = " " + str(self.grid[self.board_size * (row - self.depth) + column - self.depth].check_adjacency())
                    else:
                        item = " #"
                else:
                    item = " U"
                    if (column % (int(self.board_size) + 2 * self.depth)) == (int(self.board_size) + 2 * self.depth - 1):
                        space = " \n"
                    else:
                        space = " "
                print(item + space, sep=' ', end='', flush=True)
        print("")

    def show_cell(self, x, y):
        pos = self.grid.index(next(obj for obj in self.grid if (obj.x_pos == x and obj.y_pos == y)))
        if (self.grid[pos].check_adjacency() == 0) and self.grid[pos].check_if_hidden() and not self.grid[pos].check_if_mine():
            self.show_more_cells(pos)
        if self.grid[pos].check_if_mine():
            return True
        no_mine = True
        self.grid[pos].uncover_cell()
        x = self.grid[pos].get_cell_x_pos()
        y = self.grid[pos].get_cell_y_pos()
        for adj_pos in range(int(self.board_size) ** 2):
            adj_x = self.grid[adj_pos].get_cell_x_pos()
            adj_y = self.grid[adj_pos].get_cell_y_pos()
            if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                if int(self.grid[adj_pos].check_if_mine()):
                    no_mine = False
        if no_mine:
            for adj_pos in range(int(self.board_size) ** 2):
                adj_x = self.grid[adj_pos].get_cell_x_pos()
                adj_y = self.grid[adj_pos].get_cell_y_pos()
                if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                    if (self.grid[adj_pos].check_adjacency() == 0) and self.grid[adj_pos].check_if_hidden() and not self.grid[adj_pos].check_if_mine():
                        self.show_more_cells(adj_pos)
                    else:
                        self.grid[adj_pos].uncover_cell()
        self.refresh_grid()
        no_mine = True
        return False

    def show_more_cells(self, pos):
        self.grid[pos].uncover_cell()
        x = self.grid[pos].get_cell_x_pos()
        y = self.grid[pos].get_cell_y_pos()
        for adj_pos in range(int(self.board_size) ** 2):
            adj_x = self.grid[adj_pos].get_cell_x_pos()
            adj_y = self.grid[adj_pos].get_cell_y_pos()
            if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                if (self.grid[adj_pos].check_adjacency() == 0) and self.grid[adj_pos].check_if_hidden() and not self.grid[adj_pos].check_if_mine():
                    self.show_more_cells(adj_pos)
                else:
                    self.grid[adj_pos].uncover_cell()

    def return_board_size(self):
        return self.board_size

    def return_mines_count(self):
        return self.mines_count

    def check_cell(self, x, y):
        self.grid[x][y].show(self)

    def create_minefield(self):
        for num in range(int(self.mines_count)):
            rand_ = random.randint(0, self.board_size ** 2 - 1)
            while self.grid[rand_].check_if_mine():
                rand_ = random.randint(0, self.board_size ** 2 - 1)
            self.grid[rand_].set_mine()
        for pos in range(int(self.board_size) ** 2):
            self.check_adjacent(pos)

    def check_adjacent(self, pos):
        cur_xpos = int(self.grid[pos].get_cell_x_pos())
        cur_ypos = int(self.grid[pos].get_cell_y_pos())
        if not self.grid[pos].check_if_mine():
            for adj_pos in range(int(self.board_size) ** 2):
                adj_xpos = int(self.grid[adj_pos].get_cell_x_pos())
                adj_ypos = int(self.grid[adj_pos].get_cell_y_pos())
                if not (cur_xpos == adj_xpos and cur_ypos == adj_ypos):
                    if -1 <= cur_xpos - adj_xpos <= 1 and -1 <= cur_ypos - adj_ypos <= 1:
                        if self.grid[adj_pos].check_if_mine():
                            self.grid[pos].adjacent_mines += 1


class Cell(Board):
    counter = 0
    def __init__(self, x, y):
        Board.__init__(self)
        self.x_pos = x
        self.y_pos = y
        self.is_mine = False
        self.is_flag = False
        self.is_hidden = True
        self.adjacent_mines = 0
        Cell.counter += 1

    def new_pos(self):
        x = input("New x pos: ")
        y = input("New y pos: ")
        print(" ")
        self.x_pos = x
        self.y_pos = y

    def show(self, board):
        print("Your current position is x = {} and y = {}".format(self.x_pos, self.y_pos))
        print("Size of board is {} with {} mines!".format(board.board_size, board.mines_count))
        print(" ")
        
    def check_if_mine(self):
        if self.is_mine:
            return True
        return False

    def check_if_hidden(self):
        if self.is_hidden:
            return True
        return False
    
    def set_mine(self):
        self.is_mine = True
        self.adjacent_mines = -1

    def get_cell_x_pos(self):
        return self.x_pos

    def get_cell_y_pos(self):
        return self.y_pos

    def uncover_cell(self):
        self.is_hidden = False

    def check_adjacency(self):
        return self.adjacent_mines


def game():
    print("Hello World!")
    board = Board()
    board.set_size_and_mines()
    print("Creating new Board ...")
    board.create_grid()
    board.create_minefield()
    print("Number of cells: ", Cell.counter)
    board.show_grid()
    while(1):
        print("Which cell You want to uncover?")
        x = int(input("Type X: "))
        y = int(input("Type Y: "))
        board.show_cell(x - 1, y - 1)

if __name__ == "__main__":
    try:
        game()
    except KeyboardInterrupt:
        print('\nEnd of Game. Bye Bye!')

        """self.grid[9][0].set_mine()
        self.grid[3][1].set_mine()
        self.grid[6][1].set_mine()
        self.grid[8][1].set_mine()
        self.grid[9][1].set_mine()
        self.grid[6][2].set_mine()
        self.grid[8][2].set_mine()
        self.grid[9][2].set_mine()
        self.grid[8][3].set_mine()
        self.grid[0][4].set_mine()
        self.grid[6][4].set_mine()
        self.grid[1][5].set_mine()
        self.grid[0][6].set_mine()
        self.grid[1][7].set_mine()
        self.grid[3][7].set_mine()
        self.grid[6][7].set_mine()
        self.grid[0][8].set_mine()
        self.grid[3][8].set_mine()
        self.grid[1][9].set_mine()"""