# Snake-Q-Learning
Q-learning algorithm that trains a model to play snake. Uses a pre-made snake game file in a repository linked here. 

Q-learning is an algorithm based on the ideas of a Markovian-Decision-Process which derives from a simple Markov chain. Basically, the client has many states and each state has multiple actions that the client can take to get to another state. This model can be represented by a finite automata, where the nodes represent states and the directed-weighted edges represent actions. 

The Q-Score is way of numerically representing how well the client is doing in the game and the idea is to take actions that have an optimized Q-Score. This application uses the Bellman equation of learning:

![Bellman Equation](https://miro.medium.com/max/3276/1*jmcVWHHbzCxDc-irBy9JTw.png)

## Installation
Clone the git repository to your local machine.
```bash
git clone https://github.com/iamjeffx/Snake-Q-Learning.git
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
