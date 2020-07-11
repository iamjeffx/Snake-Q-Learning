import Snake


def run():
    master = Snake.tk.Tk()
    snake = Snake.Snake(master)
    snake.run_game()


def main():
    run()


if __name__ == '__main__':
    main()