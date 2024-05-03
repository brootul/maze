class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.start_point.x, self.start_point.y,
            self.end_point.x, self.end_point.y,
            fill=fill_color, width=2
        )


class Cell:
    def __init__(self, win, x1, y1, x2, y2):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = False

    def draw(self):
        background_color = "#d9d9d9"  # GUI's background color

        # Left wall
        color = background_color if not self.has_left_wall else "black"
        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), color)

        # Right wall
        color = background_color if not self.has_right_wall else "black"
        self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), color)

        # Top wall
        color = background_color if not self.has_top_wall else "black"
        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), color)

        # Bottom wall
        color = background_color if not self.has_bottom_wall else "black"
        self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), color)


    def center(self):
        return Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)

    def draw_move(self, to_cell, undo=False):
        from_center = self.center()
        to_center = to_cell.center()
        color = "gray" if undo else "red"
        self._win.draw_line(Line(from_center, to_center), fill_color=color)

         