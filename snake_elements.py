class Snake:
    def __init__(self, coordinate_row, coordinate_column, n):
        self.coordinate_row = int(coordinate_row)
        self.coordinate_column = int(coordinate_column)
        self.n = n

    def __str__(self):
        return f"[{self.coordinate_row},{self.coordinate_column}]"
    def get_position(self):
        return self.coordinate_row, self.coordinate_column
    
    def move_snake(self, direction):
        if direction == "w":
            column = self.coordinate_column - 1
            if column < 1:
                self.coordinate_column = self.n
            else:
                self.coordinate_column = column
        elif direction == "s":
            row = self.coordinate_row + 1
            if row > self.n:
                self.coordinate_row = row - self.n
            else:
                self.coordinate_row = row
        elif direction == "e":
            column = self.coordinate_column + 1
            if column > self.n:
                self.coordinate_column = column - self.n
            else:
                self.coordinate_column = column
        elif direction == "n":
            row = self.coordinate_row - 1
            if row < 1:
                self.coordinate_row = self.n
            else:
                self.coordinate_row = row