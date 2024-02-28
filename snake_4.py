import time
import keyboard
import random
import os
import copy

class Snake:
    def __init__(self, coordinate_row, coordinate_column, n = 10):
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
        
class Snake_game:
    def __init__(self, n = 10):
        self.n = n
        self.game_field = self.game_field_create()
        self.snake_head = Snake(1, 1)
        self.snake_segments = [self.snake_head]
        self.position_food = self.food_create()
        self.direction = "e"

    def game_field_create(self):
        game_field = [["__" for i in range(1, self.n + 3)]]
        for i in range(1, self.n + 1):
            game_field.append(["| "]+["  " for i in range(1, self.n + 1)]+[" |"])
        game_field.append(["__" for i in range(1, self.n + 3)])
        return game_field
    
    def game_field_update(self):
        for row in range(1, self.n + 1):
            for column in range(1, self.n + 1):
                if (row, column) == self.snake_head.get_position():
                    self.game_field[row][column] = "XX"
                elif (row, column) == self.position_food.get_position():
                    self.game_field[row][column] = "()"
                elif (row, column) in [segment.get_position() for segment in self.snake_segments]:
                    self.game_field[row][column] = "XX"
                else:
                    self.game_field[row][column] = "  "
        for row in self.game_field:
            for value in row:
                print(value, end='')
            print()

    def food_create(self):
        while True:
            coordinate_row = random.randrange(1, self.n + 1)
            coordinate_column = random.randrange(1, self.n + 1)
            collision = False
            if (coordinate_row, coordinate_column) == (self.snake_head.coordinate_row, self.snake_head.coordinate_column):
                collision = True
            else:
                for segment in self.snake_segments:
                    if (coordinate_row, coordinate_column) == (segment.coordinate_row, segment.coordinate_column):
                        collision = True
                        break
            if not collision:
                break
        return Snake(coordinate_row, coordinate_column)
    
    def snake_segment_create(self):
        # snake = Snake(self.snake_segments[0].coordinate_row, self.snake_segments[0].coordinate_column)
        snake = Snake(self.snake_status[-1].coordinate_row, self.snake_status[-1].coordinate_column)
        self.snake_segments.append(snake)
         
    def snake_follow(self):
            if len(self.snake_segments) > 1: 
                for index in range(len(self.snake_segments) - 1, 0, -1):
                    self.snake_segments[index].coordinate_column = self.snake_status[index-1].coordinate_column
                    self.snake_segments[index].coordinate_row = self.snake_status[index-1].coordinate_row

    def move_snake(self):
        self.snake_head.move_snake(self.direction)
        self.snake_follow()
          
    def pressed_keyboard(self):
        if keyboard.is_pressed('up'):
            self.direction = "n"
        elif keyboard.is_pressed('down'):
            self.direction = 's'
        elif keyboard.is_pressed('left'):
            self.direction = 'w'
        elif keyboard.is_pressed('right'):
            self.direction = 'e'

    
    def check_eaten(self):        
            if self.snake_head.coordinate_row == self.position_food.coordinate_row and self.snake_head.coordinate_column == self.position_food.coordinate_column:
                #self.snake_food_eaten += 1    
                return True
            
    def snake_gameplay(self):
        self.game_field_update() 
        while self.snake_head.get_position() not in [segment.get_position() for segment in self.snake_segments[1:]]:
            time.sleep(0.5)
            self.pressed_keyboard()
            self.snake_status = copy.deepcopy(self.snake_segments)
            self.move_snake()
            if self.check_eaten():
                self.position_food = self.food_create()
                self.snake_segment_create()
            os.system('cls' if os.name == 'nt' else 'clear')
            self.game_field_update()
            print(self.snake_head.get_position() not in [segment.get_position() for segment in self.snake_segments[1:]])
            for i in self.snake_segments: 
                print(i)
        print("Game Over")
         
            


game = Snake_game(10)
game.snake_gameplay()
