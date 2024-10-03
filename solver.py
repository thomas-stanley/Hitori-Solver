import numpy as np
from time import time

class Hitori():
    def __init__(self, board_size):
        self.board_size = board_size
        self.counter = 0
        self.board_setup()


    def board_setup(self):
        board_input = []
        for i in range(self.board_size):
            board_input.append([int(number) for number in input("Enter row: ").split()])
        self.board = np.array(board_input)


    def valid(self, row, column):
        surrounding = []
        for i in range(-1, 2, 2):
                try:
                    if row + i >= 0:
                        surrounding.append(self.board[row + i, column])
                except IndexError:
                    pass
                try:
                    if column + i >= 0:
                        surrounding.append(self.board[row, column + i])
                except IndexError:
                    pass
        if 0 in surrounding:
            return False
        return True


    def finished(self):
        for i in range(self.board_size):
            row_values = self.board[i, :]
            row_values = row_values[row_values != 0]
            if len(set(row_values)) != len(row_values):
                return False
            column_values = self.board[:, i]
            column_values = column_values[column_values != 0]
            if len(set(column_values)) != len(column_values):
                return False
        enclosed_valid = self.enclosed_area()
        if enclosed_valid == True:
            print(self.board)
        return enclosed_valid


    def enclosed_area(self):
        reached_board = np.ones((self.board_size, self.board_size), dtype=int)
        if self.board[0, 0] != 0:
            row = 0
            column = 0
        else:
            row = 0
            column = 1
        for board_row in range(self.board_size):
            for board_column in range(self.board_size):
                if self.board[board_row, board_column] == 0:
                    reached_board[board_row, board_column] = 0
        state = self.recur(reached_board, row, column, 0)
        return state


    def recur(self, reached_board, row, column, initial):
        surrounding = []
        for i in range(-1, 2, 2):
                try:
                    if row + i >= 0:
                        surrounding.append([row + i, column, self.board[row + i, column]])
                except IndexError:
                    pass
                try:
                    if column + i >= 0:
                        surrounding.append([row, column + i, self.board[row, column + i]])
                except IndexError:
                    pass
        for i in surrounding:
            if i[2] != 0 and reached_board[i[0], i[1]] != 0:
                reached_board[i[0], i[1]] = 0
                if not np.any(reached_board):
                    return True
                enclosed_valid = self.recur(reached_board, i[0], i[1], initial + 1)
                if enclosed_valid == True:
                    return enclosed_valid
        if initial == 0:
            return False


    def solve(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                value = self.board[row, column]
                if value != 0:
                    if self.board[row, :].tolist().count(value) > 1 or self.board[:, column].tolist().count(value) > 1:
                        self.board[row, column] = 0
                        if not self.valid(row, column):
                            self.board[row, column] = value
                        else:
                            self.counter += 1
                            result = self.solve()
                            if result:
                                return True
                            else:
                                self.board[row, column] = value
            test_row = self.board[row, :]
            test_row = test_row[test_row != 0]
            if len(set(test_row)) != len(test_row):
                return False               
        return self.finished()
    

board_size = int(input("Enter board row length: "))
board = Hitori(board_size)
start = time()
board.solve()
end = time()
print(f"{board.counter} function calls occurred.")
print(f"It took {round(end - start, 3)} seconds to solve.")  