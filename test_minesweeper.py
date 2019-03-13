import unittest
from Minesweeper import Model
from tkinter import *
import os.path


class Minesweeper_test(unittest.TestCase):

    root = Tk()
    m = Model(root, 'Test', 5, 5, 5)
    n = Model(root, 'Test', 5, 5, 5)

    def test(self):
        self.assertIsInstance(self.m.master, Tk)

        self.assertIsInstance(self.m.game, Toplevel)

        self.assertEqual(self.m.name, 'Test')

        self.assertEqual(self.m.flag_counter_number, 5)

        self.assertEqual(self.m.mines, 5)

        self.assertEqual(len(self.m.cellStatus), len(self.m.gameGrid))

        self.assertEqual(self.m.mines, 5)

        self.assertEqual(self.m.rows, 5)

        self.assertEqual(self.m.columns, 5)

        self.assertEqual(self.m.bug_fix, 0)

        mine_counter = 0
        for i in range(5):
            for j in range(5):
                self.assertEqual(self.m.cellStatus[(i, j)], 'Closed')
                if self.m.gameGrid[(i, j)] == 'Mine':
                    mine_counter += 1
        self.assertEqual(mine_counter, self.m.mines)

        counter_buttons = 0
        for i in range(5):
            for j in range(5):
                self.m.open(i, j)
                counter_buttons += 1
        self.assertEqual(counter_buttons, 25)

        self.assertNotEqual(self.m.gameGrid, self.n.gameGrid)

        self.assertNotEqual(self.m.cellStatus, self.n.cellStatus)

        self.assertFalse(self.m.victory_flags())

        self.assertFalse(self.m.victory_open())

        self.assertTrue(os.path.isfile('highscore.txt'))


if __name__ == '__main__':

    unittest.main()