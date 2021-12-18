#!/usr/bin/env python
#-*- coding: UTF-8 -*-


def parse(data):
    pass


def make_board(data):
    board = []
    for row in data:
        board.append(map(int, row.split()))
    return board


def mark(board, number):
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == number:
                # print '!!!!!', number, i, j
                board[i][j] = -1


def is_winning(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != -1:
                break
        else:
            return True

    for j in range(len(board[0])):
        # print j
        for i in range(len(board)):
            # print j, i, board[j][i]
            if board[i][j] != -1:
                # print "BREAK"
                break
        else:
            return True

    return False


def score(board, number):
    result = 0
    for j in range(len(board[0])):
        for i in range(len(board)):
            if board[i][j] != -1:
                result += board[i][j]
    return result * number


def solve(data, return_first=True):
    rows = data.split('\n')
    numbers = map(int, rows[0].split(','))
    boards = []
    for i in range(2, len(rows), 6):
        board = make_board(rows[i:i+5])
        boards.append(board)

    for number in numbers:
        for i, board in enumerate(boards):
            mark(board, number)
            if is_winning(board):
                if return_first:
                    return score(board, number)
                else:
                    boards = [b for b in boards if b != board]
                    if len(boards) == 0:
                        return score(board, number)


def easy(data):
    return solve(data, return_first=True)


def hard(data):
    return solve(data, return_first=False)


def test():
    data = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7'''
    assert easy(data) == 4512
    assert hard(data) == 1924


def main():
    test()
    data = open('in.txt').read()
    # print data
    print easy(data)
    print hard(data)


if __name__ == '__main__':
    main()

