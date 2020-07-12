import Snake
import math
import numpy as np
import pandas as pd

EAT_FOOD = 15
NOTHING = 1
LOSE = -30
BOARD_SIZE = 28


def construct_q_table(q_table, x_length, y_length):
    for i in range(1, x_length + 1):
        for j in range(1, y_length + 1):
            food = [i, j]
            for k in range(1, x_length + 1):
                for l in range(1, y_length + 1):
                    tail = [k, l]
                    state = {'Food': food,
                             'Tail': tail}
                    q_table.append(state)


# Doesn't work for Pandas DataFrame type
def print_q_table(q_table):
    for state in q_table:
        print(state)


def run():
    master = Snake.tk.Tk()
    snake = Snake.Snake(master)
    trainer_run(snake)


def translate_point(point):
    translated_x = (point.get_x() - Snake.CANVAS_BUFFER) / Snake.SNAKE_BLOCK_SIZE + 1
    translated_y = (point.get_y() - Snake.CANVAS_BUFFER) / Snake.SNAKE_BLOCK_SIZE + 1
    return [int(translated_x), int(translated_y)]


def get_state(snake):
    food_point = snake.get_food_position()
    snake_point = snake.get_snake()[snake.get_snake_size() - 1]
    return {'Food': translate_point(food_point),
            'Tail': translate_point(snake_point)}


def trainer_run(snake):
    try:
        snake.draw_board()
        snake.draw_snake()
        while snake.snake[len(snake.snake) - 1] not in snake.snake[0: len(snake.snake) - 2]:
            snake.snake_move(snake.direction)
            snake.update()
            Snake.time.sleep(0.1)
            print(get_state(snake))

    except:
        return


def main():
    q_table = []
    construct_q_table(q_table, BOARD_SIZE, BOARD_SIZE)
    q_table = pd.DataFrame(data=q_table)

    print(q_table)
    # run()


if __name__ == '__main__':
    main()
