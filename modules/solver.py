# Solver for sokuban game using following search strategies:
# - Breadth-first search
# - Depth-first search
# - A* search
# - Uniform-cost search
# - Greedy search
# - Custom strategy
# The solver class has the following methods:
# - solve(): solve the game
# """

import time
from queue import Queue, LifoQueue, PriorityQueue


class Solver(object):
    def __init__(self, initial_state, strategy):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
        self.time = None

    def solve(self):
        start_time = time.time()
        if self.strategy == 'bfs':
            self.solution = self.bfs()
        elif self.strategy == 'dfs':
            self.solution = self.dfs()
        elif self.strategy == 'astar':
            self.solution = self.astar()
        elif self.strategy == 'ucs':
            self.solution = self.ucs()
        elif self.strategy == 'greedy':
            self.solution = self.greedy()
        elif self.strategy == 'custom':
            self.solution = self.custom()
        else:
            raise Exception('Invalid strategy')
        self.time = time.time() - start_time

    def bfs(self):
        frontier = Queue()
        visited = set()

        frontier.put((self.initial_state, []))

        while not frontier.empty():
            current_state, path = frontier.get()

            if current_state.check_solved():
                return path

            if current_state not in visited:
                visited.add(current_state)

                for direction in ['U', 'D', 'L', 'R']:
                    new_state = current_state.move(direction)
                    if new_state not in visited:
                        new_path = path + [direction]
                        frontier.put((new_state, new_path))
        
        return None
    
    def dfs(self):
        frontier = LifoQueue()
        visited = set()

        frontier.put((self.initial_state, []))

        while not frontier.empty():
            current_state, path = frontier.get()

            if current_state.check_solved():
                return path

            if current_state not in visited:
                visited.add(current_state)

                for direction in ['U', 'D', 'L', 'R']:
                    new_state = current_state.move(direction)
                    if new_state not in visited:
                        new_path = path + [direction]
                        frontier.put((new_state, new_path))
        
        return None

    def astar(self):
        frontier = PriorityQueue()
        visited = set()

        frontier.put((self.initial_state.get_total_cost(), self.initial_state, []))

        while not frontier.empty():
            _, current_state, path = frontier.get()

            if current_state.check_solved():
                return path

            if current_state not in visited:
                visited.add(current_state)

                for direction in ['U', 'D', 'L', 'R']:
                    new_state = current_state.move(direction)
                    if new_state not in visited:
                        new_path = path + [direction]
                        frontier.put((new_state.get_total_cost(), new_state, new_path))
        
        return None
    
    def ucs(self):
        frontier = PriorityQueue()
        visited = set()

        frontier.put((self.initial_state.get_current_cost(), self.initial_state, []))

        while not frontier.empty():
            _, current_state, path = frontier.get()

            if current_state.check_solved():
                return path

            if current_state not in visited:
                visited.add(current_state)

                for direction in ['U', 'D', 'L', 'R']:
                    new_state = current_state.move(direction)
                    if new_state not in visited:
                        new_path = path + [direction]
                        frontier.put((new_state.get_current_cost(), new_state, new_path))
        
        return None

    def greedy(self):
        frontier = PriorityQueue()
        visited = set()

        frontier.put((self.initial_state.get_heuristic(), self.initial_state, []))

        while not frontier.empty():
            _, current_state, path = frontier.get()

            if current_state.check_solved():
                return path

            if current_state not in visited:
                visited.add(current_state)

                for direction in ['U', 'D', 'L', 'R']:
                    new_state = current_state.move(direction)
                    if new_state not in visited:
                        new_path = path + [direction]
                        frontier.put((new_state.get_heuristic(), new_state, new_path))
        
        return None

    def custom(self):
        # uh what
        return ['U', 'U',]

    def get_solution(self):
        return self.solution
