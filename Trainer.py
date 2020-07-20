import Snake
import random
import numpy as np
import pandas as pd
import tkinter as tk
import time

EAT_FOOD = 3
NOTHING = 0.01
LOSE = -3
TRAIN_SIZE = 2500

CANVAS_WIDTH = CANVAS_HEIGHT = 500
CANVAS_BUFFER = 50
SNAKE_BLOCK_SIZE = 25
BOARD_SIZE = int((CANVAS_HEIGHT - 2 * CANVAS_BUFFER) / SNAKE_BLOCK_SIZE)
SNAKE_INT_SIZE = 3
BUFFER = 30
LEFT = "Left"
RIGHT = "Right"
UP = "Up"
DOWN = 'Down'
BOARD_DIM = int((CANVAS_WIDTH - 2 * CANVAS_BUFFER) / SNAKE_BLOCK_SIZE)

LR = 0.95
DR = 0.85
RANDOMIZE = 0.05
MAX_ITER = 100


def construct_q_table(q_table, x_length, y_length):
    for i in range(1, x_length + 1):
        for j in range(1, y_length + 1):
            food = [i, j]
            for k in range(1, x_length + 1):
                for l in range(1, y_length + 1):
                    tail = [k, l]
                    state = {'Food': food,
                             'Tail': tail,
                             'Up': random.uniform(-1, 1),
                             'Down': random.uniform(-1, 1),
                             'Left': random.uniform(-1, 1),
                             'Right': random.uniform(-1, 1)}
                    q_table.append(state)


# Doesn't work for Pandas DataFrame type
def print_q_table(q_table):
    for state in q_table:
        print(state)


def run():
    master = tk.Tk()
    snake = Snake.Snake(master)
    q_table = []
    construct_q_table(q_table, BOARD_DIM, BOARD_DIM)
    train(snake, q_table)
    for state in q_table:
        print(state)
    play(q_table)


def translate_point(point):
    translated_x = (point.get_x() - CANVAS_BUFFER) / SNAKE_BLOCK_SIZE + 1
    translated_y = (point.get_y() - CANVAS_BUFFER) / SNAKE_BLOCK_SIZE + 1
    return [int(translated_x), int(translated_y)]


def get_state(snake):
    food_point = snake.get_food_position()
    snake_point = snake.get_snake()[len(snake.snake) - 1]
    return {'Food': translate_point(food_point),
            'Tail': translate_point(snake_point)}


def get_index(food, tail):
    food_x = -1
    food_y = -1
    tail_x = -1
    tail_y = -1

    if food[0] > BOARD_DIM:
        food_x = 1
    elif food[0] <= 0:
        food_x = BOARD_DIM
    else:
        food_x = food[0]

    if food[1] > BOARD_DIM:
        food_y = 1
    elif food[1] <= 0:
        food_y = BOARD_DIM
    else:
        food_y = food[1]

    if tail[0] > BOARD_DIM:
        tail_x = 1
    elif tail[0] <= 0:
        tail_x = BOARD_DIM
    else:
        tail_x = tail[0]

    if tail[1] > BOARD_DIM:
        tail_y = 1
    elif tail[1] <= 0:
        tail_y = BOARD_DIM
    else:
        tail_y = tail[1]

    if food_y < 0 or food_x < 0 or tail_x < 0 or tail_y < 0:
        return -1

    return (food_x - 1) * BOARD_SIZE ** 3 + (food_y - 1) * BOARD_SIZE ** 2 + (tail_x - 1) * BOARD_SIZE + (tail_y - 1)


def get_reward(state, direction, lose, snake):
    if direction == 'Up':
        if lose:
            return LOSE
        elif snake.snake[len(snake.snake) - 1].get_x() == state['Food'][0] and snake.snake[len(snake.snake) - 1].get_y() - 1 == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING
    elif direction == 'Down':
        if lose:
            return LOSE
        elif snake.snake[len(snake.snake) - 1].get_x() == state['Food'][0] and snake.snake[len(snake.snake) - 1].get_y() + 1 == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING
    elif direction == 'Left':
        if lose:
            return LOSE
        elif snake.snake[len(snake.snake) - 1].get_x() - 1 == state['Food'][0] and snake.snake[len(snake.snake) - 1].get_y() == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING
    elif direction == 'Right':
        if lose:
            return LOSE
        elif snake.snake[len(snake.snake) - 1].get_x() + 1 == state['Food'][0] and snake.snake[len(snake.snake) - 1].get_y() == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING


def play(q_table):
    master = tk.Tk()
    snake = Snake.Snake(master)
    snake.draw_board()
    snake.draw_snake()
    time.sleep(2)
    while snake.snake[len(snake.snake) - 1] not in snake.snake[0: len(snake.snake) - 2]:
        snake.snake_move(snake.direction)
        snake.update()

        state = get_state(snake)
        food = state['Food']
        tail = state['Tail']

        index = get_index(food, tail)
        current = q_table[index]
        index_max = np.argmax([current['Up'], current['Down'], current['Left'], current['Right']])
        if (index_max == 0 or state['Food'][1] == state['Tail'][1] - 1) and snake.direction != 'Down':
            snake.direction = 'Up'
        elif (index_max == 1 or state['Food'][1] == state['Tail'][1] + 1) and snake.direction != 'Up':
            snake.direction = 'Down'
        elif (index_max == 2 or state['Food'][0] == state['Tail'][0] - 1) and snake.direction != 'Right':
            snake.direction = 'Left'
        elif (index_max == 3 or state['Food'][0] == state['Tail'][0] + 1) and snake.direction != 'Left':
            snake.direction = 'Right'

        time.sleep(0.5)


def train(snake, q_table):
    # try:
        for i in range(TRAIN_SIZE):
            iterations = 0
            snake.draw_board()
            snake.draw_snake()
            while snake.snake[len(snake.snake) - 1] not in snake.snake[0: len(snake.snake) - 2] & iterations < MAX_ITER:
                # Perform next move
                snake.snake_move(snake.direction)
                snake.update()

                # Get current state
                state = get_state(snake)
                food = state['Food']
                tail = state['Tail']

                # Index for current state in Q-table
                index = get_index(food, tail)
                current = q_table[index]

                # Index in Q-table if snake moved up
                index_up = get_index([food[0], food[1]], [tail[0], tail[1] - 1])
                if index_up < 0:
                    print("INVALID INDEX UP: " + str(food[0]) + ", " + str(food[1]) + ", " + str(tail[0]) + ", " + str(tail[1] - 1))
                    return
                next_up = q_table[index_up]

                # Index in Q-table if snake moved down
                index_down = get_index([food[0], food[1]], [tail[0], tail[1] + 1])
                if index_down < 0:
                    print("INVALID INDEX DOWN: " + str(food[0]) + ", " + str(food[1]) + ", " + str(tail[0]) + ", " + str(tail[1] + 1))
                    return
                next_down = q_table[index_down]

                # Index in Q-table if snake moved left
                index_left = get_index([food[0], food[1]], [tail[0] - 1, tail[1]])
                if index_left < 0:
                    print("INVALID INDEX LEFT: " + str(food[0]) + ", " + str(food[1]) + ", " + str(tail[0] - 1) + ", " + str(tail[1]))
                    return
                next_left = q_table[index_left]

                # Index in Q-table if snake moved right
                index_right = get_index([food[0], food[1]], [tail[0] + 1, tail[1]])
                if index_right < 0:
                    print("INVALID INDEX RIGHT: " + str(food[0]) + ", " + str(food[1]) + ", " + str(tail[0] + 1) + ", " + str(tail[1]))
                    return
                next_right = q_table[index_right]

                # Get boolean if game lost and the reward for going in a certain direction
                lose = snake.snake[len(snake.snake) - 1] in snake.snake[0: len(snake.snake) - 2]
                reward_up = get_reward(state, 'Up', lose, snake)
                reward_down = get_reward(state, 'Down', lose, snake)
                reward_left = get_reward(state, 'Left', lose, snake)
                reward_right = get_reward(state, 'Right', lose, snake)

                # Q-values for current state
                up = current['Up']
                down = current['Down']
                left = current['Left']
                right = current['Right']

                # Update Q-values
                new_q_up = up + LR * (reward_up + DR * max(next_up['Up'],
                                                           next_up['Down'],
                                                           next_up['Left'],
                                                           next_up['Right']) - up)
                new_q_down = down + LR * (reward_down + DR * max(next_down['Up'],
                                                                 next_down['Down'],
                                                                 next_down['Left'],
                                                                 next_down['Right']) - down)
                new_q_left = left + LR * (reward_left + DR * max(next_left['Up'],
                                                                 next_left['Down'],
                                                                 next_left['Left'],
                                                                 next_left['Right']) - left)
                new_q_right = right + LR * (reward_right + DR * max(next_right['Up'],
                                                                    next_right['Down'],
                                                                    next_right['Left'],
                                                                    next_right['Right']) - right)
                # Update Q-table
                q_table[index]['Up'] = new_q_up
                q_table[index]['Down'] = new_q_down
                q_table[index]['Left'] = new_q_left
                q_table[index]['Right'] = new_q_right

                # Update next direction
                directions = [q_table[index]['Up'], q_table[index]['Down'],
                              q_table[index]['Left'], q_table[index]['Right']]

                index_max = -1

                if q_table[index]['Up'] == 0 and q_table[index]['Down'] == 0 and q_table[index]['Left'] == 0 and q_table[index]['Right'] == 0 or random.random() < RANDOMIZE:
                    index_max = random.randint(0, 3)

                else:
                    index_max = np.argmax(directions)

                if (index_max == 0 or state['Food'][1] == state['Tail'][1] - 1) and snake.direction != 'Down':
                    snake.direction = 'Up'
                elif (index_max == 1 or state['Food'][1] == state['Tail'][1] + 1) and snake.direction != 'Up':
                    snake.direction = 'Down'
                elif (index_max == 2 or state['Food'][0] == state['Tail'][0] - 1) and snake.direction != 'Right':
                    snake.direction = 'Left'
                elif (index_max == 3 or state['Food'][0] == state['Tail'][0] + 1) and snake.direction != 'Left':
                    snake.direction = 'Right'
            snake.reset_game()

    # except:
    #     return


def main():
    run()


if __name__ == '__main__':
    main()
