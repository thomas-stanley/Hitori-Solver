import numpy as np
from time import time

class Hitori:
    def __init__(self):
        self.counter = 0
        self.board_setup()


    def board_setup(self):
        board_input = []
        with open("input.txt", "r") as file:
            self.board_size = int(file.readline())
            for line in range(self.board_size):
                board_input.append([int(number) for number in file.readline().split()])
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


    def finished(self):  # No need for row check as this is already done in the solve function
        for i in range(self.board_size):
            column_values = self.board[:, i]
            column_values = column_values[column_values != 0]
            if len(set(column_values)) != len(column_values):
                print(column_values)
                print("-----")
                return False  # This is where the function keeps on coming to when there is an infinite loop
        enclosed_valid = self.enclosed_area()
        if enclosed_valid:
            print(self.board)
        return enclosed_valid


    def enclosed_area(self):
        reached_board = self.board.copy()
        row = 0
        if reached_board[0, 0] != 0:
            column = 0
        else:
            column = 1
        state = self.recur(reached_board, row, column, 0)
        return state


    def recur(self, reached_board, row, column, initial):
        print("here")
        surrounding = []
        for i in range(-1, 2, 2):
                if 0 <= row + i < self.board_size:
                    surrounding.append([row + i, column])
                if 0 <= column + i < self.board_size:
                    surrounding.append([row, column + i])
        for r, c in surrounding:
            if self.board[r, c] != 0 and reached_board[r, c] != 0:
                reached_board[r, c] = 0
                if not np.any(reached_board):  # What does this do? It clearly does something useful
                    return True
                enclosed_valid = self.recur(reached_board, r, c, initial + 1)
                if enclosed_valid:
                    return True
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
    

def main():
    board = Hitori()
    start = time()
    board.solve()
    end = time()
    print(f"{board.counter} function calls occurred.")
    print(f"It took {round(end - start, 3)} seconds to solve.")  


if __name__ == "__main__":
    main()
