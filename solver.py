import numpy as np
from time import time

def board_setup():
    global board_size
    for row in range(board_size):
        to_add = np.array([int(number) for number in input("Enter row: ").split()])
        if row == 0:
            board = to_add
        else:
            board = np.vstack((board, to_add))
    return board


def valid(board, row, column):
    surrounding = []
    for i in range(-1, 2, 2):
            try:
                if row + i >= 0:
                    surrounding.append(board[row + i, column])
            except IndexError:
                pass
            try:
                if column + i >= 0:
                    surrounding.append(board[row, column + i])
            except IndexError:
                pass
    if 0 in surrounding:
        return False
    return True


def finished(board):
    global board_size
    for i in range(board_size):
        row_values = board[i, :]
        row_values = row_values[row_values != 0]
        if len(set(row_values)) != len(row_values):
            return False
        column_values = board[:, i]
        column_values = column_values[column_values != 0]
        if len(set(column_values)) != len(column_values):
            return False
    enclosed_valid = enclosed_area(board)
    if enclosed_valid == True:
        print(board)
    return enclosed_valid


def enclosed_area(board):
    global board_size
    reached_board = np.ones((board_size, board_size), dtype=int)
    if board[0, 0] != 0:
        row = 0
        column = 0
    else:
        row = 0
        column = 1
    for board_row in range(board_size):
        for board_column in range(board_size):
            if board[board_row, board_column] == 0:
                reached_board[board_row, board_column] = 0
    state = recur(board, reached_board, row, column, 0)
    return state


def recur(board, reached_board, row, column, initial):
    surrounding = []
    for i in range(-1, 2, 2):
            try:
                if row + i >= 0:
                    surrounding.append([row + i, column, board[row + i, column]])
            except IndexError:
                pass
            try:
                if column + i >= 0:
                    surrounding.append([row, column + i, board[row, column + i]])
            except IndexError:
                pass
    for i in surrounding:
        if i[2] != 0 and reached_board[i[0], i[1]] != 0:
            reached_board[i[0], i[1]] = 0
            if not np.any(reached_board):
                return True
            enclosed_valid = recur(board, reached_board, i[0], i[1], initial + 1)
            if enclosed_valid == True:
                return enclosed_valid
    if initial == 0:
        return False




counter = 0

def solve(board):
    global counter, board_size
    for row in range(board_size):
        for column in range(board_size):
            value = board[row, column]
            if value != 0:
                if board[row, :].tolist().count(value) > 1 or board[:, column].tolist().count(value) > 1:
                    board[row, column] = 0
                    if not valid(board, row, column):
                        board[row, column] = value
                    else:
                        counter += 1
                        result = solve(board)
                        if result:
                            return True
                        else:
                            board[row, column] = value
        test_row = board[row, :]
        test_row = test_row[test_row != 0]
        if len(set(test_row)) != len(test_row):
            return False

                        
    return finished(board)
    

board_size = int(input("Enter board row length: "))
board = board_setup()
start = time()
solve(board)
print(f"{counter} function calls occurred.")
end = time()
print(f"It took {round(end - start, 3)} seconds to solve.")  
