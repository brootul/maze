import unittest
from unittest.mock import Mock, MagicMock
from maze import Maze, Cell
from geometry import Cell, Line

class Tests(unittest.TestCase):
    '''
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        mock_win = Mock()  # Create a mock window object
        
        # Create a Maze instance with the mock window
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, mock_win)
        
        self.assertEqual(len(m1._cells), num_cols, "Number of columns should match")
        self.assertEqual(len(m1._cells[0]), num_rows, "Number of rows should match")


    def test_break_entrance_and_exit(self):
        mock_win = Mock()
        m1 = Maze(0, 0, 10, 12, 10, 10, mock_win)
        
        # Assertions to check if entrance and exit are correctly broken
        self.assertFalse(m1._cells[0][0].has_top_wall, "Entrance top wall should be removed")
        self.assertFalse(m1._cells[11][9].has_bottom_wall, "Exit bottom wall should be removed")
    

    def test_reset_cells_visited(self):
        mock_win = Mock()
        num_cols = 5
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, mock_win, seed=42)
        
        # First, ensure all cells are visited by the generation process
        for col in m1._cells:
            for cell in col:
                cell.visited = True  # Simulate all cells being visited
        
        m1._reset_cells_visited()  # Reset all cells to unvisited
        
        # Check if all cells are unvisited
        for col in m1._cells:
            for cell in col:
                self.assertFalse(cell.visited, "All cells should be reset to not visited")
    '''


    def setUp(self):
        self.mock_win = MagicMock()
        self.mock_win.draw_line = MagicMock()  # Mock the draw_line method to do nothing
        self.maze = Maze(0, 0, 2, 2, 10, 10, self.mock_win, seed=42)


    def test_solve_simple_path(self):
        # Configure a simple path through the maze
        self.maze._cells[0][0].has_right_wall = False
        self.maze._cells[0][1].has_bottom_wall = False
        self.maze._cells[1][1].has_left_wall = False
        self.maze._cells[1][0].has_top_wall = False

        self.assertTrue(self.maze.solve(), "The maze should be solvable")

    def test_solve_unsolvable_maze(self):
        # All walls are up, no path is possible
        for row in self.maze._cells:
            for cell in row:
                cell.has_right_wall = True
                cell.has_left_wall = True
                cell.has_top_wall = True
                cell.has_bottom_wall = True

        self.assertFalse(self.maze.solve(), "The maze should not be solvable")

    def test_solve_with_backtracking(self):
        # Configure a path that requires backtracking
        self.maze._cells[0][0].has_right_wall = False
        self.maze._cells[0][1].has_bottom_wall = True  # Dead end, need to backtrack
        self.maze._cells[0][0].has_bottom_wall = False
        self.maze._cells[1][0].has_top_wall = False
        self.maze._cells[1][0].has_right_wall = False
        self.maze._cells[1][1].has_left_wall = False

        self.assertTrue(self.maze.solve(), "The maze should be solvable with backtracking")



if __name__ == "__main__":
    unittest.main()
