import argparse
import time
import keyboard
import random
import os
import copy
from snake_elements import Snake # This module is also in git hub and it imports a file containing the Snake class - snake coordinates and movements.
import game_over # This module is also in git hub and it import a graphical game over presentation, I didn't want to include it in the game logic.

        
class Snake_game:
    def __init__(self, n = 10, speed = 0.2, end = "body"): # When running the game, you can choose size of game field, speed of snake and if you want to end the game when hitting the wall or just the snake body.
        self.n = n
        self.speed = speed
        self.game_field = self.game_field_create()
        self.snake_head = Snake(1, 1, self.n)
        self.snake_segments = [self.snake_head]
        self.position_food = self.food_create()
        self.direction = "e"
        self.score = 0
        self.end = str(end).lower()
        if self.end not in ["body", "wall"]:
            raise ValueError('The parameter can only be "body" or "wall".')
        self.wall_collision = False

    def game_field_create(self): # Creates a list of lists that represents the game filed.
        game_field = [["██" for i in range(1, self.n + 3)]] 
        for i in range(1, self.n + 1):
            game_field.append(["██"]+["  " for i in range(1, self.n + 1)]+["██"])
        game_field.append(["██" for i in range(1, self.n + 3)])
        return game_field
    
    def game_field_update(self): # Updates the field visually based on the position of each snake segment or food.
        for row in range(1, self.n + 1):
            for column in range(1, self.n + 1):
                if (row, column) == self.snake_head.get_position():
                    self.game_field[row][column] = "██"
                elif (row, column) == self.position_food.get_position():
                    self.game_field[row][column] = "\033[43m  \033[0m" # Makes the food yellow.
                elif (row, column) in [segment.get_position() for segment in self.snake_segments]:
                    self.game_field[row][column] = "██"
                else:
                    self.game_field[row][column] = "  "
        for row in self.game_field:
            for value in row:
                print(value, end='')
            print()

    def food_create(self): # Creates food on a random position and makes sure it is not created on the snake body.
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
        return Snake(coordinate_row, coordinate_column, self.n) # Food is also snake class, i. e. two coordinates.
    
    def snake_segment_create(self): # Creates new parts of the snake when food is eaten and adds them to the list of all snake elements. 
        snake = Snake(self.snake_status[-1].coordinate_row, self.snake_status[-1].coordinate_column, self.n)
        self.snake_segments.append(snake)
         
    def snake_follow(self): # Makes sure all snake elements follow the head.
            if len(self.snake_segments) > 1: 
                for index in range(len(self.snake_segments) - 1, 0, -1):
                    self.snake_segments[index].coordinate_column = self.snake_status[index-1].coordinate_column
                    self.snake_segments[index].coordinate_row = self.snake_status[index-1].coordinate_row

    def move_snake(self): # Simplifies code. And reflects which ending of the game the user is playing (if game ends when hitting the body and wall or just the body).  
        if self.end == 'body':
            self.snake_head.move_snake_body(self.direction)
            self.snake_follow()
            return True
        elif self.end == 'wall':
            if self.snake_head.move_snake_wall(self.direction) == False:
                return False
            else:
                self.snake_follow() 
                return True
          
    def pressed_keyboard(self, direction): # Checks what keyboard is pressed so that snake can change direction accordingly, plus ends the game when pressed esc.
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
    
    def check_eaten(self): # Checks if food was eaten so that the snake can grow and also keeps track of how much food was eaten as score points.    
            if self.snake_head.coordinate_row == self.position_food.coordinate_row and self.snake_head.coordinate_column == self.position_food.coordinate_column:
                self.score += 1    
                return True
            
    def snake_ending(self): # Checks the ending conditions.
        if self.end == "body":
            if self.snake_head.get_position() not in [segment.get_position() for segment in self.snake_segments[1:]]:
                return True
            else:
                return False
        elif self.end == "wall":
            if self.snake_head.get_position() not in [segment.get_position() for segment in self.snake_segments[1:]] and self.wall_collision == False:
                return True
            else:
                return False

    def snake_gameplay(self): # Puts everything together within a loop wich checks constantly what key is pressed by the user.
        self.game_field_update() 
        while self.snake_ending(): # Checks if game should end.
            time.sleep(self.speed) 
            if self.pressed_keyboard(self.direction) == False:
                break
            self.snake_status = copy.deepcopy(self.snake_segments) # Had to create a deep copy so that I could remember a previous position of the snake head so that the next snake element could move there after. The list would change constantly otherwise.
            if self.move_snake() == False:
                self.wall_collision = True
            elif self.check_eaten():
                self.position_food = self.food_create()
                self.snake_segment_create()
            os.system('cls' if os.name == 'nt' else 'clear') # Clears the screen each time so that it looks better for the user.
            self.game_field_update()
            print(f"Your score is {self.score}.")
        game_over.game_over(self)
         

def main():
    parser = argparse.ArgumentParser(description='Snake Game with three adjustable parameters.')
    parser.add_argument('--size', type=int, default=27, help='Size of the game field.')
    parser.add_argument('--speed', type=float, default=0.1, help='Speed of the snake movement.')
    parser.add_argument('--end', type=str, default="body", help='Ending when snake hits its own body (enter "body") or when it hits the wall/body (enter "wall").')
    args = parser.parse_args()

    game = Snake_game(args.size, args.speed, args.end) # When running the game, you can choose size of game field, speed of snake and if you want to end the game when hitting the wall or just the snake body.
    game.snake_gameplay()

if __name__ == "__main__":
    main()
