import Snake
import numpy as np
import pandas as pd


def run():
    master = Snake.tk.Tk()
    snake = Snake.Snake(master)
    trainer_run(snake)


def translate_point(point):
    translated_x = (point.get_x() - Snake.CANVAS_BUFFER) / Snake.SNAKE_BLOCK_SIZE + 1
    translated_y = (point.get_y() - Snake.CANVAS_BUFFER) / Snake.SNAKE_BLOCK_SIZE + 1
    return [translated_x, translated_y]


def get_state(snake):
    food_point = snake.get_food_position()
    snake_point = snake.get_snake()[snake.get_snake_size() - 1]
    return [translate_point(food_point), translate_point(snake_point)]


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
    run()


if __name__ == '__main__':
    main()
