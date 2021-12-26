#!/usr/bin/env python3
import unittest
code = __import__('23')

#
#    0   1    2    3    4    5    6    7    8    9   10
# 0 [ ]-[ ]-[   ]-[ ]-[   ]-[ ]-[   ]-[ ]-[   ]-[ ]-[ ]
# 1         [   ]     [   ]     [   ]     [   ]
# 2         [   ]     [   ]     [   ]     [   ]
# 3         [   ]     [   ]     [   ]     [   ]
# 4         [   ]     [   ]     [   ]     [   ]
#

class Test23Methods(unittest.TestCase):

    #############
    #...........#
    ###D#A#C#D###
      #B#C#B#A#
      #########
    def test_start_moves(self):
        board = (
            tuple(' '),
            tuple(' '),
            (' ', 'D', 'B', None, None),
            tuple(' '),
            (' ', 'A', 'C', None, None),
            tuple(' '),
            (' ', 'C', 'B', None, None),
            tuple(' '),
            (' ', 'D', 'A', None, None),
            tuple(' '),
            tuple(' ')
        )
        expected = []
        for i in [2, 4, 6, 8]:
            for j in [0, 1, 3, 5, 7, 9, 10]:
                expected.append(((i, 1), (j, 0)))
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    #############
    #.D.........#
    ###.#A#C#D###
      #B#C#B#A#
      #########
    def test_2nd_move(self):
        board = (
            tuple(' '),
            tuple('D'),
            (' ', ' ', 'B', None, None),
            tuple(' '),
            (' ', 'A', 'C', None, None),
            tuple(' '),
            (' ', 'C', 'B', None, None),
            tuple(' '),
            (' ', 'D', 'A', None, None),
            tuple(' '),
            tuple(' '),
        )
        expected = []
        for i in [2, 4, 6, 8]:
            for j in [3, 5, 7, 9, 10]:
                expected.append(((i, 1 if i != 2 else 2), (j, 0)))
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    #############
    #.D.A.......#
    ###.#.#C#D###
      #B#C#B#A#
      #########
    def test_3rd_move(self):
        board = (
            tuple(' '),
            tuple('D'),
            (' ', ' ', 'B', None, None),
            tuple('A'),
            (' ', ' ', 'C', None, None),
            tuple(' '),
            (' ', 'C', 'B', None, None),
            tuple(' '),
            (' ', 'D', 'A', None, None),
            tuple(' '),
            tuple(' ')
        )
        expected = []
        for i in [4, 6, 8]:
            for j in [5, 7, 9, 10]:
                expected.append(((i, 1 if i != 4 else 2), (j, 0)))
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    #############
    #.A.B.D.C.A.#
    ###.#.#.#.###
      #D#C#B#.#
      #########
    def test_no_move(self):
        board = (
            tuple(' '),
            tuple('A'),
            (' ', ' ', 'D', None, None),
            tuple('B'),
            (' ', ' ', 'C', None, None),
            tuple('D'),
            (' ', ' ', 'B', None, None),
            tuple('C'),
            (' ', ' ', ' ', None, None),
            tuple('A'),
            tuple(' ')
        )
        expected = []
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    #############
    #BA.B.C.D.CD#
    ###.#.#.#.###
      #A#.#.#.#
      #########
    def test_bottom_move(self):
        board = (
            tuple('B'),
            tuple('A'),
            (' ', ' ', 'A', None, None),
            tuple('B'),
            (' ', ' ', ' ', None, None),
            tuple('C'),
            (' ', ' ', ' ', None, None),
            tuple('D'),
            (' ', ' ', ' ', None, None),
            tuple('C'),
            tuple('D')
        )
        expected = []
        for i in [1, 3, 5, 7]:
            expected.append(((i, 0), (i + 1, 1 if i == 1 else 2)))
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    #############
    #.A.B.....B.#
    ###.#.#C#D###
      #A#.#C#D#
      #########
    def test_end_game(self):
        board = (
            tuple(' '),
            tuple('A'),
            (' ', ' ', 'A', None, None),
            tuple('B'),
            (' ', ' ', ' ', None, None),
            tuple(' '),
            (' ', 'C', 'C', None, None),
            tuple(' '),
            (' ', 'D', 'D', None, None),
            tuple('B'),
            tuple(' ')
        )
        expected = []
        expected.append(((1, 0), (2, 1)))
        expected.append(((3, 0), (4, 2)))
        expected.append(((9, 0), (4, 2)))
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    #############
    #..........D#
    ###A#B#C#.###
      #A#B#C#D#
      #########
    def test_end_game2(self):
        board = (
            tuple(' '),
            tuple(' '),
            (' ', 'A', 'A', None, None),
            tuple(' '),
            (' ', 'B', 'B', None, None),
            tuple(' '),
            (' ', 'C', 'C', None, None),
            tuple(' '),
            (' ', ' ', 'D', None, None),
            tuple(' '),
            tuple('D')
        )
        expected = []
        expected.append(((10, 0), (8, 1)))
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    #############
    #...........#
    ###A#B#C#D###
      #A#B#C#D#
      #########
    def test_done_moves(self):
        board = (
            tuple(' '),
            tuple(' '),
            (' ', 'A', 'A', None, None),
            tuple(' '),
            (' ', 'B', 'B', None, None),
            tuple(' '),
            (' ', 'C', 'C', None, None),
            tuple(' '),
            (' ', 'D', 'D', None, None),
            tuple(' '),
            tuple(' ')
        )
        expected = []
        moves = code.getMoves(board)
        self.assertTrue(sorted(expected) == sorted(moves))

    def test_cost_bb_to_c(self):
        move = ((4, 2), (1, 0))
        expected = 500
        cost = code.getCost('C', move)
        self.assertTrue(expected == cost)

    def test_cost_c_to_bb(self):
        move = ((10, 0), (2, 2))
        expected = 100
        cost = code.getCost('B', move)
        self.assertTrue(expected == cost)

    def test_cost_c_to_tb(self):
        move = ((10, 0), (6, 1))
        expected = 5000
        cost = code.getCost('D', move)
        self.assertTrue(expected == cost)

    def test_cost_c_to_bb2(self):
        move = ((0, 0), (2, 2))
        expected = 4
        cost = code.getCost('A', move)
        self.assertTrue(expected == cost)

    def test_done_2d(self):
        board = (
            tuple(' '),
            tuple(' '),
            (' ', 'A', 'A', None, None),
            tuple(' '),
            (' ', 'B', 'B', None, None),
            tuple(' '),
            (' ', 'C', 'C', None, None),
            tuple(' '),
            (' ', 'D', 'D', None, None),
            tuple(' '),
            tuple(' ')
        )
        self.assertTrue(code.done(board))

    def test_not_done_2d(self):
        board = (
            tuple(' '),
            tuple(' '),
            (' ', ' ', 'A', None, None),
            tuple(' '),
            (' ', 'B', 'B', None, None),
            tuple('A'),
            (' ', 'C', 'C', None, None),
            tuple(' '),
            (' ', 'D', 'D', None, None),
            tuple(' '),
            tuple(' ')
        )
        self.assertFalse(code.done(board))

    def test_sort_moves1(self):
        board = (
            tuple(' '),
            tuple(' '),
            (' ', 'D', 'B', None, None),
            tuple(' '),
            (' ', 'A', 'C', None, None),
            tuple(' '),
            (' ', 'C', 'B', None, None),
            tuple(' '),
            (' ', 'D', 'A', None, None),
            tuple(' '),
            tuple(' ')
        )
        moves = [((2, 1), (9, 0)), ((2, 1), (0, 0)), ((4, 1), (10, 0)), ((2, 1), (1, 0)), ((4, 1), (1, 0)), ((2, 1), (10, 0)), ((4, 1), (0, 0)), ((4, 1), (9, 0))]
        expected = [((4, 1), (1, 0)), ((4, 1), (0, 0)), ((4, 1), (9, 0)), ((4, 1), (10, 0)), ((2, 1), (1, 0)), ((2, 1), (0, 0)), ((2, 1), (9, 0)), ((2, 1), (10, 0))]
        moves = code.sortByCost(board, moves)
        self.assertTrue(expected == moves)

if __name__ == '__main__':
    unittest.main()
