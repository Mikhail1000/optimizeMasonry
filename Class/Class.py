class Block:
    def __init__(self, x: int, y: int, width: int, height: int, original_width: int = None,
                 original_height: int = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x2 = x + width
        self.y2 = y + height
        self.original_width = original_width if original_width else width
        self.original_height = original_height if original_height else height
        self.is_cut = (width != original_width or height != original_height)

    def __str__(self):
        return f"Block({self.x}, {self.y}, {self.x2}, {self.y2}, {self.width}x{self.height})"


class Hole:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x2 = x + width
        self.y2 = y + height

    def __str__(self):
        return f"Hole({self.x}, {self.y}, {self.x2}, {self.y2}, {self.width}x{self.height})"


class Wall:
    def __init__(self, width, height):
        self.width = width
        self.height = height

#c.create_line(10, 10, 190, 50)

#c.create_line(100, 180, 100, 60, width=5, dash=(10, 2),
#              fill='green', activefill='lightgreen',
#              arrow=LAST, arrowshape=(10, 20, 10))
