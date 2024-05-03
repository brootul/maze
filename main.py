from window import MazeWindow
from geometry import Point, Line, Cell
from maze import Maze


def main():
    maze_window = MazeWindow(width=800, height=600)  # Specify desired dimensions

    maze = Maze(x1=50, y1=50, num_rows=10, num_cols=10, cell_size_x=50, cell_size_y=50, win=maze_window, seed=None)
    if maze.solve():
        print("Maze solved!")
    else:
        print("No solution found.")    

    maze_window.wait_for_close()

if __name__ == "__main__":
    main()
