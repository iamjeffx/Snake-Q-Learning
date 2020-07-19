import Snake
import math
import random
import numpy as np
import pandas as pd
import tkinter as tk

EAT_FOOD = 2
NOTHING = 0.1
LOSE = -2
BOARD_SIZE = 28
TRAIN_SIZE = 100000

LR = 0.9
DR = 0.9


def construct_q_table(q_table, x_length, y_length):
    for i in range(1, x_length + 1):
        for j in range(1, y_length + 1):
            food = [i, j]
            for k in range(1, x_length + 1):
                for l in range(1, y_length + 1):
                    tail = [k, l]
                    state = {'Food': food,
                             'Tail': tail,
                             'Up': 0,
                             'Down': 0,
                             'Left': 0,
                             'Right': 0}
                    q_table.append(state)


# Doesn't work for Pandas DataFrame type
def print_q_table(q_table):
    for state in q_table:
        print(state)


def run():
    master = tk.Tk()
    snake = Snake.Snake(master)
    q_table = []
    construct_q_table(q_table, BOARD_SIZE, BOARD_SIZE)
    q_table = pd.DataFrame(data=q_table)
    train(snake, q_table)


def translate_point(point):
    translated_x = (point.get_x() - Snake.CANVAS_BUFFER) / Snake.SNAKE_BLOCK_SIZE + 1
    translated_y = (point.get_y() - Snake.CANVAS_BUFFER) / Snake.SNAKE_BLOCK_SIZE + 1
    return [int(translated_x), int(translated_y)]


def get_state(snake):
    food_point = snake.get_food_position()
    snake_point = snake.get_snake()[0]
    return {'Food': translate_point(food_point),
            'Tail': translate_point(snake_point)}


def get_index(food, tail):
    food_x = -1
    food_y = -1
    tail_x = -1
    tail_y = -1

    if food[0] >= 29:
        food_x = 1
    elif food[0] <= 0:
        food_x = 28
    else:
        food_x = food[0]

    if food[1] >= 29:
        food_y = 1
    elif food[1] <= 0:
        food_y = 28
    else:
        food_y = food[1]

    if tail[0] >= 29:
        tail_x = 1
    elif tail[1] <= 0:
        tail_x = 28
    else:
        tail_x = tail[0]

    if tail[1] >= 29:
        tail_y = 1
    elif tail[1] <= 0:
        tail_y = 28
    else:
        tail_y = tail[1]

    return (food_x - 1) * BOARD_SIZE ** 3 + (food_y - 1) * BOARD_SIZE ** 2 + (tail_x - 1) * BOARD_SIZE + (tail_y - 1)


def get_reward(state, direction, lose):
    if direction == 'Up':
        if lose:
            return LOSE
        elif state['Tail'][0] == state['Food'][0] and state['Tail'][1] - 1 == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING
    elif direction == 'Down':
        if lose:
            return LOSE
        elif state['Tail'][0] == state['Food'][0] and state['Tail'][1] + 1 == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING
    elif direction == 'Left':
        if lose:
            return LOSE
        elif state['Tail'][0] - 1 == state['Food'][0] and state['Tail'][1] == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING
    elif direction == 'Right':
        if lose:
            return LOSE
        elif state['Tail'][0] + 1 == state['Food'][0] and state['Tail'][1] == state['Food'][1]:
            return EAT_FOOD
        else:
            return NOTHING


def train(snake, q_table):
    # try:
        for i in range(TRAIN_SIZE):
            snake.draw_board()
            snake.draw_snake()
            while snake.snake[len(snake.snake) - 1] not in snake.snake[0: len(snake.snake) - 2]:
                # Perform next move
                snake.snake_move(snake.direction)
                snake.update()

                # Get current state
                state = get_state(snake)
                food = state['Food']
                tail = state['Tail']

                # Index for current state in Q-table
                index = get_index(food, tail)
                current = q_table.loc[index]

                # Index in Q-table if snake moved up
                index_up = get_index([food[0], food[1]], [tail[0], tail[1] - 1])
                next_up = q_table.loc[index_up]

                # Index in Q-table if snake moved down
                index_down = get_index([food[0], food[1]], [tail[0], tail[1] + 1])
                next_down = q_table.loc[index_down]

                # Index in Q-table if snake moved left
                index_left = get_index([food[0], food[1]], [tail[0] - 1, tail[1]])
                next_left = q_table.loc[index_left]

                # Index in Q-table if snake moved right
                index_right = get_index([food[0], food[1]], [tail[0] + 1, tail[1]])
                next_right = q_table.loc[index_right]

                # Get boolean if game lost and the reward for going in a certain direction
                lose = snake.snake[len(snake.snake) - 1] in snake.snake[0: len(snake.snake) - 2]
                reward_up = get_reward(state, 'Up', lose)
                reward_down = get_reward(state, 'Down', lose)
                reward_left = get_reward(state, 'Left', lose)
                reward_right = get_reward(state, 'Right', lose)

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
                                                                 next_down['Right']) - up)
                new_q_left = left + LR * (reward_left + DR * max(next_left['Up'],
                                                                 next_left['Down'],
                                                                 next_left['Left'],
                                                                 next_left['Right']) - up)
                new_q_right = right + LR * (reward_right + DR * max(next_right['Up'],
                                                                    next_right['Down'],
                                                                    next_right['Left'],
                                                                    next_right['Right']) - up)
                # Update Q-table
                q_table.at[index, 'Up'] = new_q_up
                q_table.at[index, 'Down'] = new_q_down
                q_table.at[index, 'Left'] = new_q_left
                q_table.at[index, 'Right'] = new_q_right

                # Update next direction
                directions = [q_table.loc[index]['Up'], q_table.loc[index]['Down'],
                              q_table.loc[index]['Left'], q_table.loc[index]['Right']]

                index_max = -1

                if q_table.loc[index]['Up'] < 0.1 and q_table.loc[index]['Down'] < 0.1 and q_table.loc[index]['Left'] < 0.1 and q_table.loc[index]['Right'] < 0.1:
                    index_max = random.randint(0, 3)

                else:
                    index_max = np.argmax(directions)

                if index_max == 0:
                    snake.direction = 'Up'
                elif index_max == 1:
                    snake.direction = 'Down'
                elif index_max == 2:
                    snake.direction = 'Left'
                elif index_max == 3:
                    snake.direction = 'Right'

                print(q_table)
                # Snake.time.sleep(0.1)
            snake.reset_game()

    # except:
    #     return


def main():
    run()


if __name__ == '__main__':
    main()
