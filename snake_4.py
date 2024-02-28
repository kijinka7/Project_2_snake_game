import time
import keyboard
import random
import os
import copy
import snake_elements
import game_over

        
class Snake_game:
    def __init__(self, n = 10, speed = 0.1):
        self.n = n
        self.speed = speed
        self.game_field = self.game_field_create()
        self.snake_head = snake_elements.Snake(1, 1, self.n)
        self.snake_segments = [self.snake_head]
        self.position_food = self.food_create()
        self.direction = "e"
        self.score = 0

    def game_field_create(self):
        game_field = [["██" for i in range(1, self.n + 3)]]
        for i in range(1, self.n + 1):
            game_field.append(["██"]+["  " for i in range(1, self.n + 1)]+["██"])
        game_field.append(["██" for i in range(1, self.n + 3)])
        return game_field
    
    def game_field_update(self):
        for row in range(1, self.n + 1):
            for column in range(1, self.n + 1):
                if (row, column) == self.snake_head.get_position():
                    self.game_field[row][column] = "██"
                elif (row, column) == self.position_food.get_position():
                    self.game_field[row][column] = "\033[43m  \033[0m"
                elif (row, column) in [segment.get_position() for segment in self.snake_segments]:
                    self.game_field[row][column] = "██"
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
        return snake_elements.Snake(coordinate_row, coordinate_column, self.n)
    
    def snake_segment_create(self):
        snake = snake_elements.Snake(self.snake_status[-1].coordinate_row, self.snake_status[-1].coordinate_column, self.n)
        self.snake_segments.append(snake)
         
    def snake_follow(self):
            if len(self.snake_segments) > 1: 
                for index in range(len(self.snake_segments) - 1, 0, -1):
                    self.snake_segments[index].coordinate_column = self.snake_status[index-1].coordinate_column
                    self.snake_segments[index].coordinate_row = self.snake_status[index-1].coordinate_row

    def move_snake(self):
        self.snake_head.move_snake(self.direction)
        self.snake_follow()
          
    def pressed_keyboard(self, direction):
        if keyboard.is_pressed('up') and direction != "s":
            self.direction = "n"
        elif keyboard.is_pressed('down') and direction != "n":
            self.direction = 's'
        elif keyboard.is_pressed('left') and direction != "e":
            self.direction = 'w'
        elif keyboard.is_pressed('right') and direction != "w":
            self.direction = 'e'
        elif keyboard.is_pressed('esc'):
            return False
    
    def check_eaten(self):        
            if self.snake_head.coordinate_row == self.position_food.coordinate_row and self.snake_head.coordinate_column == self.position_food.coordinate_column:
                self.score += 1    
                return True
            
    def snake_gameplay(self):
        self.game_field_update() 
        while self.snake_head.get_position() not in [segment.get_position() for segment in self.snake_segments[1:]]:
            time.sleep(self.speed)
            if self.pressed_keyboard(self.direction) == False:
                break
            self.snake_status = copy.deepcopy(self.snake_segments)
            self.move_snake()
            if self.check_eaten():
                self.position_food = self.food_create()
                self.snake_segment_create()
            os.system('cls' if os.name == 'nt' else 'clear')
            self.game_field_update()
            print(f"Your score is {self.score}.")
        game_over.game_over(self)
         
game = Snake_game(27,0.1)
game.snake_gameplay()
