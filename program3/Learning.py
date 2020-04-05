from Maze import Node
from Maze import Map
from random import random
from random import randrange

class QLearning(object):
    def __init__(self, lamda, maze_map):
        self._lambda = lamda
        self.current_location = [0,0]
        self.maze = maze_map

    def run_cycle(self):
        good_node = False
        
        # find a random start location that is not a wall
        while good_node == False:
            x_start = randrange(0, 7)
            y_start = randrange(0, 6)
            self.current_location = [x_start, y_start]
            current_node = self.maze.map[self.current_location[0]][self.current_location[1]]
            if current_node.isWall == False:
                good_node = True

        found_goal = False

        while found_goal == False:
            current_node = self.maze.map[self.current_location[0]][self.current_location[1]]
            if current_node.qNorth == 100.0:
                found_goal = True
            else:
                action = self.determine_action(current_node)
                next_location = self.drift_next_location(current_node, action, self.current_location[0], self.current_location[1])
                
                next_node = Node(False, [0.0,0.0,0.0,0.0], [0,0,0,0])

                if next_location[0] < 0 or next_location[1] < 0 or next_location[0] > 6 or next_location[1] > 5:
                    next_node = Node(True, [0.0,0.0,0.0,0.0], [0,0,0,0])
                else:
                    next_node = self.maze.map[next_location[0]][next_location[1]]

                # update the n value for the current state and action
                n_updated = self.calculate_n(self.maze.map[self.current_location[0]][self.current_location[1]], action)

                if action == "n":
                    self.maze.map[self.current_location[0]][self.current_location[1]].nNorth = n_updated
                if action == "e":
                    self.maze.map[self.current_location[0]][self.current_location[1]].nEast = n_updated
                if action == "s":
                    self.maze.map[self.current_location[0]][self.current_location[1]].nSouth = n_updated
                if action == "w":
                    self.maze.map[self.current_location[0]][self.current_location[1]].nWest = n_updated

                q_updated = self.calculate_q(self.maze.map[self.current_location[0]][self.current_location[1]], action, next_node)
                if action == "n":
                    self.maze.map[self.current_location[0]][self.current_location[1]].qNorth = q_updated
                if action == "e":
                    self.maze.map[self.current_location[0]][self.current_location[1]].qEast = q_updated
                if action == "s":
                    self.maze.map[self.current_location[0]][self.current_location[1]].qSouth = q_updated
                if action == "w":
                    self.maze.map[self.current_location[0]][self.current_location[1]].qWest = q_updated

                if next_node.isWall == False:
                    self.current_location = next_location
        
        self.maze.print_optimal_path()

    def determine_action(self, node):
        action_prob = random()
        action = ""

        if action_prob <= 0.95:
            q_max = -1000000
            if node.qNorth >= q_max:
                q_max = node.qNorth
                action = "n"
            if node.qSouth >= q_max:
                q_max = node.qSouth
                action = "s"
            if node.qEast >= q_max:
                q_max = node.qEast
                action = "e"
            if node.qWest >= q_max:
                q_max = node.qWest
                action = "w"
        else:
            rand_action = randrange(1,4)
            if rand_action == 1:
                action = "n"
            elif rand_action == 2:
                action = "e"
            elif rand_action == 3:
                action = "s"
            elif rand_action == 4:
                action = "w"

        return action

    def calculate_q(self, current, action, next):
        updated_q = 0
        current_q = 0
        current_n = 0
        q_next_max = 0.0
        reward = 0

        if action == "n":
            current_q = current.qNorth
            current_n = current.nNorth
            reward = -1.0
        if action == "e":
            current_q = current.qEast
            current_n = current.nEast
            reward = -2.0
        if action == "s":
            current_q = current.qSouth
            current_n = current.nSouth
            reward = -3.0
        if action == "w":
            current_q = current.qWest
            current_n = current.nWest
            reward = -2.0

        if next.qNorth >= q_next_max:
            q_next_max = next.qNorth
        if next.qSouth >= q_next_max:
            q_next_max = next.qSouth
        if next.qEast >= q_next_max:
            q_next_max = next.qEast
        if next.qWest >= q_next_max:
            q_next_max = next.qWest

        updated_q = current_q + ((1.0/float(current_n)) * (reward + (self._lambda * q_next_max) - current_q))

        return updated_q

    def calculate_n(self, current, action):
        n = 0

        if action == "n":
            n = current.nNorth + 1
        if action == "e":
            n = current.nEast + 1
        if action == "s":
            n = current.nSouth + 1
        if action == "w":
            n = current.nWest + 1
        
        return n

    def actual_next_location(self, current, action, x, y):
        next_location = [0,0]

        if action == "n":
            next_location = [x, y+1]
        if action == "e":
            next_location = [x+1, y]
        if action == "s":
            next_location = [x, y-1]
        if action == "w":
            next_location = [x-1, y]

        return next_location

    def drift_next_location(self, current, action, x, y):
        next_location = [0,0]

        drift_prob = random()
        drift = "none"

        if drift_prob >= 0.90 and drift_prob < 0.95:
            drift = "right"
        elif drift_prob >= 0.95:
            drift = "left"

        if drift == "none":
            if action == "n":
                next_location = [x, y+1]
            if action == "e":
                next_location = [x+1, y]
            if action == "s":
                next_location = [x, y-1]
            if action == "w":
                next_location = [x-1, y]

        elif drift == "right":
            if action == "n":
                next_location = [x+1, y] # move east instead
            if action == "e":
                next_location = [x, y-1] # move south instead
            if action == "s":
                next_location = [x-1, y] # move west instead
            if action == "w":
                next_location = [x, y+1] # move north instead
        elif drift == "left":
            if action == "n":
                next_location = [x-1, y] # move west instead
            if action == "e":
                next_location = [x, y+1] # move north instead
            if action == "s":
                next_location = [x+1, y] # move east instead
            if action == "w":
                next_location = [x, y-1] # move south instead

        return next_location