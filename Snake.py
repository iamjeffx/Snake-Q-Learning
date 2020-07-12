import tkinter as tk
import time
import keyboard
import random

CANVAS_WIDTH = CANVAS_HEIGHT = 800
CANVAS_BUFFER = 50
SNAKE_BLOCK_SIZE = 25
BOARD_SIZE = int((CANVAS_HEIGHT - 2 * CANVAS_BUFFER) / SNAKE_BLOCK_SIZE)
SNAKE_INT_SIZE = 3
BUFFER = 30
LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = 'down'


# Point class
class Point:
    def __init__(self, x_val=-1, y_val=-1):
        self.x = x_val
        self.y = y_val

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return 'X: ' + self.get_x() + ' Y: ' + self.get_y()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# Snake game class
class Snake(tk.Frame):
    '''Constructor
        Parameters: self, master

        Creates snake game object
    '''

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        # Set title and canvas
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

        # Initialize Snake
        self.snake = []
        self.snake_size = SNAKE_INT_SIZE
        for i in range(self.snake_size):
            self.snake.append(Point(int(CANVAS_WIDTH / 2 + i * SNAKE_BLOCK_SIZE), int(CANVAS_HEIGHT / 2)))

        # Snake initial direction
        self.direction = RIGHT

        self.play = True
        self.clicked = False

        # Initialize food location
        self.food = Point(CANVAS_BUFFER + random.randint(0, 14) * SNAKE_BLOCK_SIZE,
                          CANVAS_BUFFER + random.randint(0, 14) * SNAKE_BLOCK_SIZE)

        keyboard.add_hotkey('w', self.set_direction_up)
        keyboard.add_hotkey('up', self.set_direction_up)
        keyboard.add_hotkey('a', self.set_direction_left)
        keyboard.add_hotkey('left', self.set_direction_left)
        keyboard.add_hotkey('s', self.set_direction_down)
        keyboard.add_hotkey('down', self.set_direction_down)
        keyboard.add_hotkey('d', self.set_direction_right)
        keyboard.add_hotkey('right', self.set_direction_right)

    def get_food_position(self):
        return self.food

    def get_snake(self):
        return self.snake

    def get_snake_size(self):
        return self.snake_size

    def set_direction_up(self):
        self.direction = UP

    def set_direction_down(self):
        self.direction = DOWN

    def set_direction_left(self):
        self.direction = LEFT

    def set_direction_right(self):
        self.direction = RIGHT

    def generate_food(self):
        x_val = random.randint(0, 27)
        y_val = random.randint(0, 27)
        new_point = Point(x_val * SNAKE_BLOCK_SIZE + CANVAS_BUFFER,
                          y_val * SNAKE_BLOCK_SIZE + CANVAS_BUFFER)

        while new_point in self.snake:
            x_val = random.randint(0, 27)
            y_val = random.randint(0, 27)
            new_point = Point(x_val * SNAKE_BLOCK_SIZE + CANVAS_BUFFER,
                              y_val * SNAKE_BLOCK_SIZE + CANVAS_BUFFER)

        self.food.x = new_point.x
        self.food.y = new_point.y

    def reset_game(self):
        self.direction = RIGHT
        self.snake = []
        self.snake_size = SNAKE_INT_SIZE
        for i in range(self.snake_size):
            self.snake.append(Point(int(CANVAS_WIDTH / 2 + i * SNAKE_BLOCK_SIZE), int(CANVAS_HEIGHT / 2)))

    def draw_food(self):
        self.canvas.create_rectangle(self.food.x, self.food.y,
                                     self.food.x + SNAKE_BLOCK_SIZE,
                                     self.food.y + SNAKE_BLOCK_SIZE,
                                     fill="deep sky blue", outline="dodger blue")
        self.pack()

    '''Draw_Snake
        Parameters: self

        Draws snake on the canvas
    '''

    def draw_snake(self):
        self.canvas.delete("all")
        self.draw_board()
        self.draw_food()
        for i in range(len(self.snake)):
            self.canvas.create_rectangle(self.snake[i].x,
                                         self.snake[i].y,
                                         self.snake[i].x + SNAKE_BLOCK_SIZE,
                                         self.snake[i].y + SNAKE_BLOCK_SIZE,
                                         fill="black")
        self.canvas.pack()

    '''Draw_Board
        Parameters: self

        Draws the board onto the widget
    '''

    def draw_board(self):
        self.canvas.create_rectangle(CANVAS_BUFFER,
                                     CANVAS_BUFFER,
                                     CANVAS_WIDTH - CANVAS_BUFFER,
                                     CANVAS_HEIGHT - CANVAS_BUFFER)
        self.canvas.create_text(CANVAS_WIDTH / 2,
                                SNAKE_BLOCK_SIZE,
                                text="SCORE: " + str(self.snake_size))
        self.canvas.pack()

    '''Snake_Move
        Parameters: self, direction

        Given a direction, function updates the position of the snake and draws it onto the board
    '''

    def snake_move(self, direction):
        if self.snake[len(self.snake) - 1] == self.food:
            self.snake_size += 1
            self.generate_food()

        # Pop off end of snake and get values on the front of the snake
        else:
            self.snake.pop(0)

        tail_x = self.snake[len(self.snake) - 1].x
        tail_y = self.snake[len(self.snake) - 1].y

        if direction == UP:
            self.move_up(tail_x, tail_y)
        elif direction == DOWN:
            self.move_down(tail_x, tail_y)
        elif direction == LEFT:
            self.move_left(tail_x, tail_y)
        elif direction == RIGHT:
            self.move_right(tail_x, tail_y)

        self.draw_snake()

    '''Move_Left
        Parameters: self, tail_x, tail_y

        Appends a point onto the left of the tail of the snake
    '''

    def move_left(self, tail_x, tail_y):
        if tail_x == CANVAS_BUFFER:
            self.snake.append(Point(CANVAS_WIDTH - CANVAS_BUFFER - SNAKE_BLOCK_SIZE, tail_y))
        else:
            self.snake.append(Point(tail_x - SNAKE_BLOCK_SIZE, tail_y))

    '''Move_Right
        Parameters: self, tail_x, tail_y

        Appends a point onto the right of the tail of the snake
    '''

    def move_right(self, tail_x, tail_y):
        if tail_x + SNAKE_BLOCK_SIZE == CANVAS_WIDTH - CANVAS_BUFFER:
            self.snake.append(Point(CANVAS_BUFFER, tail_y))
        else:
            self.snake.append(Point(tail_x + SNAKE_BLOCK_SIZE, tail_y))

    '''Move_Up
        Parameters: self, tail_x, tail_y

        Appends a point above the tail of the snake
    '''

    def move_up(self, tail_x, tail_y):
        if tail_y == CANVAS_BUFFER:
            self.snake.append(Point(tail_x, CANVAS_HEIGHT - CANVAS_BUFFER - SNAKE_BLOCK_SIZE))
        else:
            self.snake.append(Point(tail_x, tail_y - SNAKE_BLOCK_SIZE))

    '''Move_Down
        Parameters: self, tail_x, tail_y

        Appends a point below the tail of the snake
    '''

    def move_down(self, tail_x, tail_y):
        if tail_y + SNAKE_BLOCK_SIZE == CANVAS_HEIGHT - CANVAS_BUFFER:
            self.snake.append(Point(tail_x, CANVAS_BUFFER))
        else:
            self.snake.append(Point(tail_x, tail_y + SNAKE_BLOCK_SIZE))

    def new_game_button_clicked(self, event):
        self.clicked = True
        self.play = True

    def quit_button_clicked(self, event):
        self.clicked = True
        self.play = False

    def draw_lose_buttons(self):
        x1 = CANVAS_WIDTH / 2 - CANVAS_BUFFER
        x2 = CANVAS_WIDTH / 2 + CANVAS_BUFFER

        new_game_button = self.canvas.create_rectangle(int(x1), int((CANVAS_HEIGHT - 2 * CANVAS_BUFFER) / 2),
                                                       int(x2), int(CANVAS_HEIGHT / 2),
                                                       fill="grey76", activefill="grey65")
        quit_button = self.canvas.create_rectangle(int(x1), int((CANVAS_HEIGHT + BUFFER) / 2),
                                                   int(x2), int((CANVAS_HEIGHT + BUFFER + 2 * CANVAS_BUFFER) / 2),
                                                   fill="red2", activefill="red3")
        new_game_text = self.canvas.create_text(int(CANVAS_WIDTH / 2),
                                                int((CANVAS_HEIGHT - CANVAS_BUFFER) / 2), text="New Game")
        quit_text = self.canvas.create_text(int(CANVAS_WIDTH / 2),
                                            int((CANVAS_HEIGHT + BUFFER + CANVAS_BUFFER) / 2), text="Quit")

        self.canvas.tag_bind(new_game_button, "<Button-1>", self.new_game_button_clicked)
        self.canvas.tag_bind(new_game_text, "<Button-1>", self.new_game_button_clicked)
        self.canvas.tag_bind(quit_button, "<Button-1>", self.quit_button_clicked)
        self.canvas.tag_bind(quit_text, "<Button-1>", self.quit_button_clicked)

        self.canvas.pack()

    def lose_menu(self):
        while not self.clicked:
            self.draw_lose_buttons()
            time.sleep(0.1)
            self.update()

    '''Run_Game
        Parameters: self

        Executes the object code
    '''

    def run_loop(self):
        self.draw_board()
        self.draw_snake()
        while self.snake[len(self.snake) - 1] not in self.snake[0: len(self.snake) - 2]:
            self.snake_move(self.direction)
            self.update()
            time.sleep(0.1)

    def run_game(self):
        try:
            while self.play:
                self.reset_game()
                self.run_loop()
                self.lose_menu()
                self.clicked = False
        except:
            return


def main():
    master = tk.Tk()
    snake = Snake(master)
    snake.run_game()


if __name__ == "__main__":
    main()



