import time
import random
from geometry import Cell, Line

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None):
        if seed is not None:
            random.seed(seed)
        self._win = win
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)  # Start the maze generation from the top-left corner
        self._reset_cells_visited()


    def _create_cells(self):
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                x1 = self.x1 + i * self.cell_size_x
                y1 = self.y1 + j * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(self._win, x1, y1, x2, y2)
                column.append(cell)
            self._cells.append(column)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)  # Ensure this matches the definition

        self._break_entrance_and_exit()


    def _break_entrance_and_exit(self):
        # Entrance: Top wall of the top-left cell
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        # Exit: Bottom wall of the bottom-right cell
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)


    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()
        self._animate()



    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)  # Adjust timing as needed for visualization


    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        directions = []

        # Add potential moves (checking boundaries and visited status)
        if i > 0 and not self._cells[i - 1][j].visited:
            directions.append((i - 1, j))
        if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
            directions.append((i + 1, j))
        if j > 0 and not self._cells[i][j - 1].visited:
            directions.append((i, j - 1))
        if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
            directions.append((i, j + 1))

        while directions:
            next_i, next_j = random.choice(directions)  # Randomly select the next cell to visit
            self._remove_wall(i, j, next_i, next_j)  # Remove the wall between the current and next cell
            self._break_walls_r(next_i, next_j)  # Recursively visit the next cell
            directions = [d for d in directions if not self._cells[d[0]][d[1]].visited]  # Refresh possible directions
            self._animate()

            
    def _remove_wall(self, ci, cj, ni, nj):
        if ci == ni:  # Same column, different rows
            if cj < nj:  # Moving downward
                self._cells[ci][cj].has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False
            else:  # Moving upward
                self._cells[ci][cj].has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False
        elif cj == nj:  # Same row, different columns
            if ci < ni:  # Moving right
                self._cells[ci][cj].has_right_wall = False
                self._cells[ni][nj].has_left_wall = False
            else:  # Moving left
                self._cells[ci][cj].has_left_wall = False
                self._cells[ni][nj].has_right_wall = False

        # Ensure to redraw the affected cells to update GUI
        self._cells[ci][cj].draw()
        self._cells[ni][nj].draw()


           
    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False


    def solve(self):
        return self._solve_r(0, 0)
    

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        # Check if it's the end cell
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        directions = [
            (i + 1, j),  # Right
            (i - 1, j),  # Left
            (i, j + 1),  # Down
            (i, j - 1)   # Up
        ]

        for ni, nj in directions:
            if self._is_valid_move(i, j, ni, nj):
                self._draw_move(self._cells[i][j], self._cells[ni][nj], undo=False)
                if self._solve_r(ni, nj):
                    return True
                self._draw_move(self._cells[i][j], self._cells[ni][nj], undo=True)

        return False


    def _is_valid_move(self, ci, cj, ni, nj):
        if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
            if ci == ni and cj < nj:  # Moving down
                return not self._cells[ci][cj].has_bottom_wall
            if ci == ni and cj > nj:  # Moving up
                return not self._cells[ci][cj].has_top_wall
            if cj == nj and ci < ni:  # Moving right
                return not self._cells[ci][cj].has_right_wall
            if cj == nj and ci > ni:  # Moving left
                return not self._cells[ci][cj].has_left_wall
        return False

    def _draw_move(self, from_cell, to_cell, undo=False):
        fill_color = "gray" if undo else "red"
        from_center = from_cell.center()
        to_center = to_cell.center()
        self._win.draw_line(Line(from_center, to_center), fill_color)


