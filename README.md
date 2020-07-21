# Snake-Q-Learning
Q-learning algorithm that trains a model to play snake. Uses a pre-made snake game file in a repository linked here. 

## Installation
Clone the git repository to your local machine.
```bash
git clone <https link>
```
## Execution
To run the game, simply execute the driver.
```bash
python Snake.py
```
For the Q-learning driver, run the training model.
```bash
python Trainer.py
```
Hyperparameters are adjustable at the top of the training model driver. Learning rate, discount rate and max iterations per game during training are labelled at the top. Rewards for each policy is at the very top of the training model. Snake block size and the size of the board can also be adjusted; Board dimension(supports square boards) is equal to canvas width/height minus double the canvas buffer all divided by the snake block size. Default values for the buffer and block size are 50 and 25 respectively. 
