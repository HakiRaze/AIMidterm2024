"""
Sokuban game state class
The state of the game consists the map which is a 2D array of characters. There are 6 types of characters:
- ' ': empty space
- '#': wall
- '$': box
- '.': target
- '@': player
- '+': player on target
- '*': box on target
The game state class keeps track of the map.
The game state also keeps track of the player and box positions, and whether the game is solved or not.
The game state class has the following methods:
- find_player(): find the player in the map and return its position
- find_boxes(): find all the boxes in the map and return their positions
- find_targets(): find all the targets in the map and return their positions  
- generate_next_state(direction): generate the next game state by moving the player to the given direction
- check_solved(): check if the game is solved
"""

import math

class GameState:
    def __init__(self, map, current_cost=0):
        self.map = map
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.is_solved = self.check_solved()
        self.current_cost = current_cost
        self.height = len(self.map)
        self.width = len(self.map[0])

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to find the player, boxes, and targets in the map
    # The positions are tuples (row, column)
    # ------------------------------------------------------------------------------------------------------------------

    def find_player(self):
        """Find the player in the map and return its position"""
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == '@' or self.map[i][j] == '+':
                    return (i, j)
        return None

    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        boxes = []
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == '$' or self.map[i][j] == '*':
                    boxes.append((i, j))
        return boxes


    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        targets = []
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == '.' or self.map[i][j] == '*':
                    targets.append((i, j))
        return targets

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to check if a position is a wall, box, target, or empty space
    # The position is a tuple (row, column)
    # ------------------------------------------------------------------------------------------------------------------

    def is_wall(self, position):
        """Check if the given position is a wall"""
        i, j = position
        return self.map[i][j] == '#'

    def is_box(self, position):
        """Check if the given position is a box
            Note: the box can be on "$" or "*" (box on target)
        """
        i, j = position
        return self.map[i][j] == '$' or self.map[i][j] == '*'


    def is_target(self, position):
        """Check if the given position is a target
            Note: the target can be "." or "*" (box on target)
        """
        i, j = position
        return self.map[i][j] == '.' or self.map[i][j] == '*'



    def is_empty(self, position):
        """Check if the given position is empty"""
        i, j = position
        return self.map[i][j] == ' '


    # ------------------------------------------------------------------------------------------------------------------
    # The following methods get heuristics for the game state (for informed search strategies)
    # ------------------------------------------------------------------------------------------------------------------

    def manhattan_distance(self, box_position, target_positions):
        # Calculate the Manhattan distance from the box to its nearest target
        min_distance = math.inf
        for target_position in target_positions:
            distance = abs(box_position[0] - target_position[0]) + abs(box_position[1] - target_position[1])
            min_distance = min(min_distance, distance)
        return min_distance

    def get_heuristic(self):
        """Get the heuristic for the game state
            Note: the heuristic is the sum of the distances from all the boxes to their nearest targets
        """
        heuristic = 0
        for box_position in self.boxes:
            heuristic += self.manhattan_distance(box_position, self.targets)
        return heuristic


    def get_total_cost(self):
        """Get the cost for the game state
            Note: the cost is the number of moves from the initial state to the current state + the heuristic
        """
        return self.get_current_cost() + self.get_heuristic()

    def get_current_cost(self):
        """Get the current cost for the game state
            Note: the current cost is the number of moves from the initial state to the current state
        """
        return self.current_cost

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to generate the next game state and check if the game is solved
    # ------------------------------------------------------------------------------------------------------------------

    def move(self, direction):
        """Generate the next game state by moving the player to the given direction. 
            The rules are as follows:
            - The player can move to an empty space
            - The player can move to a target
            - The player can push a box to an empty space (the box moves to the empty space, the player moves to the box's previous position)
            - The player can push a box to a target (the box moves to the target, the player moves to the box's previous position)
            - The player cannot move to a wall
            - The player cannot push a box to a wall
            - The player cannot push two boxes at the same time
        """
        i, j = self.player
        if direction == 'U':
            new_position = (i - 1, j)
        elif direction == 'D':
            new_position = (i + 1, j)
        elif direction == 'L':
            new_position = (i, j - 1)
        elif direction == 'R':
            new_position = (i, j + 1)
        else:
            raise ValueError('Invalid direction')

        if not self.is_wall(new_position):
            if self.is_box(new_position):
                # If there's a box, check if we can push it
                new_box_position = (new_position[0] + (new_position[0] - i), new_position[1] + (new_position[1] - j))
                if not self.is_wall(new_box_position) and not self.is_box(new_box_position):
                    new_map = [list(row) for row in self.map]
                    new_map[i][j] = ' '  # Player leaves current position
                    if self.map[i][j] == '+':
                        new_map[i][j] = '.'  # Player leaves target position
                    new_map[new_position[0]][new_position[1]] = '@'  # Player moves to new position
                    if self.map[new_position[0]][new_position[1]] == '.':
                        new_map[new_position[0]][new_position[1]] = '+'  # Player moves to target position
                    new_map[new_box_position[0]][new_box_position[1]] = '$'  # Move the box
                    if self.map[new_box_position[0]][new_box_position[1]] == '.':
                        new_map[new_box_position[0]][new_box_position[1]] = '*'  # Box moves to target position
                    return GameState(new_map, self.current_cost + 1)
                else:
                    return self  # Can't push the box, stay in the same state
            else:
                # Move the player
                new_map = [list(row) for row in self.map]
                new_map[i][j] = ' '  # Player leaves current position
                if self.map[i][j] == '+':
                    new_map[i][j] = '.'  # Player leaves target position
                new_map[new_position[0]][new_position[1]] = '@'  # Player moves to new position
                if self.map[new_position[0]][new_position[1]] == '.':
                    new_map[new_position[0]][new_position[1]] = '+'  # Player moves to target position
                return GameState(new_map, self.current_cost + 1)
        else:
            return self

    def check_solved(self):
        """Check if the game is solved"""
        return all(box in self.targets for box in self.boxes)
