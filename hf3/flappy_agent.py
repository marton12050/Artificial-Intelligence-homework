import numpy as np

epsilon = 0.001
eta = 0.6


class FlappyAgent():

    def __init__(self, observation_space_size, action_space, n_iterations):
        self.q_table = np.zeros([*observation_space_size, len(action_space)])
        self.env_action_space = action_space
        self.n_iterations = n_iterations

        self.test = False

    def step(self, state):

        if not self.test:  # and ...:
            Action_probabilities = np.ones(3, dtype=float) * epsilon / 3
            best_action = np.argmax(self.q_table[state])
            Action_probabilities[best_action] += (1.0 - epsilon)
            action = np.argmax(Action_probabilities)
        else:
            action = np.argmax(self.q_table[state])

        return action

    def epoch_end(self, epoch_reward_sum):
        pass

    def learn(self, old_state, action, new_state, reward):
        best_next = np.argmax(self.q_table[new_state])
        td_target = reward + self.q_table[new_state][best_next]
        td_delta = td_target - self.q_table[old_state][action]
        self.q_table[old_state][action] += eta * td_delta

    def train_end(self):
        self.test = True
