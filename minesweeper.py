import random


class Board:
    def __init__(self):
        self.board_size = 5
        self.mines_count = 5
        self.grid = []

    def set_size_and_mines(self):
        mines = input("New mines count: ")
        size = input("New board size: ")
        print(" ")
        self.mines_count = int(mines)
        self.board_size = int(size)

    def create_grid(self):
        self.grid = [[[Cell] for row in range(int(self.board_size))] for column in range(int(self.board_size))]
        for row in range(int(self.board_size)):
            for column in range(int(self.board_size)):
                self.grid[column][row] = Cell(column, row)

    def show_grid(self):
        for row in range(int(self.board_size)):
            for column in range(int(self.board_size)):
                print(" #", sep=' ', end='', flush=True)
            print("")

    def refresh_grid(self):
        for row in range(int(self.board_size)):
            for column in range(int(self.board_size)):
                if not self.grid[column][row].check_if_hidden():
                    if self.grid[column][row].check_if_mine():
                        item = " #"
                    else:
                        item = " " + str(self.grid[column][row].check_adjacency())
                else:
                    item = " #"
                print(item, sep=' ', end='', flush=True)
            print("")

    def show_cell(self, x, y):
        if (self.grid[x][y].check_adjacency() == 0) and self.grid[x][y].check_if_hidden() and not self.grid[x][y].check_if_mine():
            self.show_more_cells(x, y)
        if self.grid[x][y].check_if_mine():
            return True
        no_mine = True
        self.grid[x][y].uncover_cell()
        for adj_y in range(int(self.board_size)):
            for adj_x in range(int(self.board_size)):
                if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                    if int(self.grid[adj_x][adj_y].check_if_mine()):
                        no_mine = False
        if no_mine:
            for adj_y in range(int(self.board_size)):
                for adj_x in range(int(self.board_size)):
                    if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                        if (self.grid[adj_x][adj_y].check_adjacency() == 0) and self.grid[adj_x][adj_y].check_if_hidden() and not self.grid[adj_x][adj_y].check_if_mine():
                            self.show_more_cells(adj_x, adj_y)
                        else:
                            self.grid[adj_x][adj_y].uncover_cell()
        self.refresh_grid()
        no_mine = True
        return False

    def show_more_cells(self, x, y):
        self.grid[x][y].uncover_cell()
        for adj_y in range(int(self.board_size)):
            for adj_x in range(int(self.board_size)):
                if -1 <= x - adj_x <= 1 and -1 <= y - adj_y <= 1:
                    if (self.grid[adj_x][adj_y].check_adjacency() == 0) and self.grid[adj_x][adj_y].check_if_hidden() and not self.grid[adj_x][adj_y].check_if_mine():
                        self.show_more_cells(adj_x, adj_y)
                    else:
                        self.grid[adj_x][adj_y].uncover_cell()

    def return_board_size(self):
        return self.board_size

    def return_mines_count(self):
        return self.mines_count

    def check_cell(self, x, y):
        self.grid[x][y].show(self)

    def create_minefield(self):
        for num in range(int(self.mines_count)):
            randx = random.randint(0, self.board_size-1)
            randy = random.randint(0, self.board_size-1)
            while self.grid[randx][randy].check_if_mine():
                randx = random.randint(0, self.board_size-1)
                randy = random.randint(0, self.board_size-1)
            self.grid[randx][randy].set_mine()
        for row in range(int(self.board_size)):
            for column in range(int(self.board_size)):
                self.check_adjacent(column, row)

    def check_adjacent(self, x, y):
        cur_x = int(self.grid[x][y].get_cell_x_pos())
        cur_y = int(self.grid[x][y].get_cell_y_pos())
        if not self.grid[cur_x][cur_y].check_if_mine():
            for row in range(int(self.board_size)):
                for column in range(int(self.board_size)):
                    adj_x = int(self.grid[column][row].get_cell_x_pos())
                    adj_y = int(self.grid[column][row].get_cell_y_pos())
                    if not (cur_x == adj_x and cur_y == adj_y):
                        if -1 <= cur_x - adj_x <= 1 and -1 <= cur_y - adj_y <= 1:
                            if self.grid[column][row].check_if_mine():
                                self.grid[x][y].adjacent_mines += 1


class Cell(Board):
    def __init__(self, x, y):
        Board.__init__(self)
        self.x_pos = x
        self.y_pos = y
        self.is_mine = False
        self.is_flag = False
        self.is_hidden = True
        self.adjacent_mines = 0

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