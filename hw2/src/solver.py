import time
import random
import logging
from src.maze import Maze

logging.basicConfig(level=logging.INFO)


class Solver(object):
    """Base class for solution methods.
    Every new solution method should override the solve method.

    Attributes:
        maze (list): The maze which is being solved.
        neighbor_method:
        quiet_mode: When enabled, information is not outputted to the console

    """

    def __init__(self, maze, quiet_mode, neighbor_method):
        logging.info("Class Solver ctor called")

        self.maze = maze
        self.neighbor_method = neighbor_method
        self.name = ""
        self.quiet_mode = quiet_mode

        for row in range(len(self.maze.grid)):
            for col in range(len(self.maze.grid[row])):
                self.maze.grid[row][col].g = float('inf')

    def solve(self):
        logging.info('Class: Solver solve called')
        raise NotImplementedError

    def get_name(self):
        logging.info('Class Solver get_name called')
        raise self.name

    def get_path(self):
        logging.info('Class Solver get_path called')
        return self.path


class BreadthFirst(Solver):

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.info('Class BreadthFirst ctor called')

        self.name = "Breadth First Recursive"
        super().__init__(maze, neighbor_method, quiet_mode)

    def solve(self):

        """Function that implements the breadth-first algorithm for solving the maze. This means that
                for each iteration in the outer loop, the search visits one cell in all possible branches. Then
                moves on to the next level of cells in each branch to continue the search."""

        logging.info("Class BreadthFirst solve called")
        current_level = [self.maze.entry_coor]  # Stack of cells at current level of search
        path = list()  # To track path of solution cell coordinates

        print("\nSolving the maze with breadth-first search...")
        time_start = time.clock()

        while True:  # Loop until return statement is encountered
            next_level = list()

            while current_level:  # While still cells left to search on current level
                k_curr, l_curr = current_level.pop(0)  # Search one cell on the current level
                self.maze.grid[k_curr][l_curr].visited = True  # Mark current cell as visited
                path.append(((k_curr, l_curr), False))  # Append current cell to total search path

                if (k_curr, l_curr) == self.maze.exit_coor:  # Exit if current cell is exit cell
                    if not self.quiet_mode:
                        print("Number of moves performed: {}".format(len(path)))
                        print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
                    return path


                neighbour_coors = self.maze.find_neighbours(k_curr, l_curr)  # Find neighbour indicies
                neighbour_coors = self.maze.validate_neighbours_solve(neighbour_coors, k_curr,
                                                                  l_curr, self.maze.exit_coor[0],
                                                                  self.maze.exit_coor[1], self.neighbor_method)

                if neighbour_coors is not None:
                    for coor in neighbour_coors:
                        next_level.append(coor)  # Ad   d all existing real neighbours to next search level

            for cell in next_level:
                current_level.append(cell)  # Update current_level list with cells for nex search level
        logging.info("Class BreadthFirst leaving solve")


class BiDirectional(Solver):

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.info('Class BiDirectional ctor called')

        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Bi Directional"

    def solve(self):

        """Function that implements a bidirectional depth-first recursive backtracker algorithm for
        solving the maze, i.e. starting at the entry point and exit points where each search searches
        for the other search path. NOTE: THE FUNCTION ENDS IN AN INFINITE LOOP FOR SOME RARE CASES OF
        THE INPUT MAZE. WILL BE FIXED IN FUTURE."""
        logging.info("Class BiDirectional solve called")

        grid = self.maze.grid
        k_curr, l_curr = self.maze.entry_coor            # Where to start the first search
        p_curr, q_curr = self.maze.exit_coor             # Where to start the second search
        grid[k_curr][l_curr].visited = True    # Set initial cell to visited
        grid[p_curr][q_curr].visited = True    # Set final cell to visited
        backtrack_kl = list()                  # Stack of visited cells for backtracking
        backtrack_pq = list()                  # Stack of visited cells for backtracking
        path_kl = list()                       # To track path of solution and backtracking cells
        path_pq = list()                       # To track path of solution and backtracking cells

        if not self.quiet_mode:
            print("\nSolving the maze with bidirectional depth-first search...")
        time_start = time.clock()

        while True:   # Loop until return statement is encountered
            neighbours_kl = self.maze.find_neighbours(k_curr, l_curr)    # Find neighbours for first search
            real_neighbours_kl = [neigh for neigh in neighbours_kl if not grid[k_curr][l_curr].is_walls_between(grid[neigh[0]][neigh[1]])]
            neighbours_kl = [neigh for neigh in real_neighbours_kl if not grid[neigh[0]][neigh[1]].visited]

            neighbours_pq = self.maze.find_neighbours(p_curr, q_curr)    # Find neighbours for second search
            real_neighbours_pq = [neigh for neigh in neighbours_pq if not grid[p_curr][q_curr].is_walls_between(grid[neigh[0]][neigh[1]])]
            neighbours_pq = [neigh for neigh in real_neighbours_pq if not grid[neigh[0]][neigh[1]].visited]

            if len(neighbours_kl) > 0:   # If there are unvisited neighbour cells
                backtrack_kl.append((k_curr, l_curr))              # Add current cell to stack
                path_kl.append(((k_curr, l_curr), False))          # Add coordinates to part of search path
                k_next, l_next = random.choice(neighbours_kl)      # Choose random neighbour
                grid[k_next][l_next].visited = True                # Move to that neighbour
                k_curr = k_next
                l_curr = l_next

            elif len(backtrack_kl) > 0:                  # If there are no unvisited neighbour cells
                path_kl.append(((k_curr, l_curr), True))   # Add coordinates to part of search path
                k_curr, l_curr = backtrack_kl.pop()        # Pop previous visited cell (backtracking)

            if len(neighbours_pq) > 0:                        # If there are unvisited neighbour cells
                backtrack_pq.append((p_curr, q_curr))           # Add current cell to stack
                path_pq.append(((p_curr, q_curr), False))       # Add coordinates to part of search path
                p_next, q_next = random.choice(neighbours_pq)   # Choose random neighbour
                grid[p_next][q_next].visited = True             # Move to that neighbour
                p_curr = p_next
                q_curr = q_next

            elif len(backtrack_pq) > 0:                  # If there are no unvisited neighbour cells
                path_pq.append(((p_curr, q_curr), True))   # Add coordinates to part of search path
                p_curr, q_curr = backtrack_pq.pop()        # Pop previous visited cell (backtracking)

            # Exit loop and return path if any opf the kl neighbours are in path_pq.
            if any((True for n_kl in real_neighbours_kl if (n_kl, False) in path_pq)):
                path_kl.append(((k_curr, l_curr), False))
                path = [p_el for p_tuple in zip(path_kl, path_pq) for p_el in p_tuple]  # Zip paths
                if not self.quiet_mode:
                    print("Number of moves performed: {}".format(len(path)))
                    print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
                logging.info("Class BiDirectional leaving solve")
                return path

            # Exit loop and return path if any opf the pq neighbours are in path_kl.
            elif any((True for n_pq in real_neighbours_pq if (n_pq, False) in path_kl)):
                path_pq.append(((p_curr, q_curr), False))
                path = [p_el for p_tuple in zip(path_kl, path_pq) for p_el in p_tuple]  # Zip paths
                if not self.quiet_mode:
                    print("Number of moves performed: {}".format(len(path)))
                    print("Execution time for algorithm: {:.4f}".format(time.clock() - time_start))
                logging.info("Class BiDirectional leaving solve")
                return path

class DepthFirstBacktracker(Solver):
    """A solver that implements the depth-first recursive backtracker algorithm.
    """

    def __init__(self, maze, quiet_mode=False,  neighbor_method="fancy"):
        logging.info('Class DepthFirstBacktracker ctor called')

        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Depth First Backtracker"

    def solve(self):
        logging.info("Class DepthFirstBacktracker solve called")
        k_curr, l_curr = self.maze.entry_coor      # Where to start searching
        self.maze.grid[k_curr][l_curr].visited = True     # Set initial cell to visited
        visited_cells = list()                  # Stack of visited cells for backtracking
        path = list()                           # To track path of solution and backtracking cells
        if not self.quiet_mode:
            print("\nSolving the maze with depth-first search...")

        time_start = time.time()

        while (k_curr, l_curr) != self.maze.exit_coor:     # While the exit cell has not been encountered
            neighbour_indices = self.maze.find_neighbours(k_curr, l_curr)    # Find neighbour indices
            neighbour_indices = self.maze.validate_neighbours_solve(neighbour_indices, k_curr,
                l_curr, self.maze.exit_coor[0], self.maze.exit_coor[1], self.neighbor_method)

            if neighbour_indices is not None:   # If there are unvisited neighbour cells
                visited_cells.append((k_curr, l_curr))              # Add current cell to stack
                path.append(((k_curr, l_curr), False))  # Add coordinates to part of search path
                k_next, l_next = random.choice(neighbour_indices)   # Choose random neighbour
                self.maze.grid[k_next][l_next].visited = True                 # Move to that neighbour
                k_curr = k_next
                l_curr = l_next

            elif len(visited_cells) > 0:              # If there are no unvisited neighbour cells
                path.append(((k_curr, l_curr), True))   # Add coordinates to part of search path
                k_curr, l_curr = visited_cells.pop()    # Pop previous visited cell (backtracking)

        path.append(((k_curr, l_curr), False))  # Append final location to path
        if not self.quiet_mode:
            print("Number of moves performed: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))

        logging.info('Class DepthFirstBacktracker leaving solve')
        return path



class UniformCostSearch(Solver):
    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.info('Class UniformCostSearch ctor called')
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "UniformCostSearch"

    def solve(self):
        logging.info("Class UniformCostSearch solve called")
        k_curr, l_curr = self.maze.entry_coor
        visited = list()
        path = list()
        if not self.quiet_mode:
            print("\nSolving the maze with UniformCostSearch...")

        time_start = time.time()

        while (k_curr, l_curr) != self.maze.exit_coor:
            neighbour_indices = self.maze.find_neighbours(k_curr, l_curr)
            neighbour_indices = self.maze.validate_neighbours_solve(neighbour_indices, k_curr,
                                                                    l_curr, self.maze.exit_coor[0],
                                                                    self.maze.exit_coor[1], self.neighbor_method)
            if neighbour_indices is not None:
                visited.append((k_curr, l_curr))
                path.append(((k_curr, l_curr), False))

                min_cost = float('inf')
                min_neighbour = None
                for (k_next, l_next) in neighbour_indices:
                    if (k_next != k_curr):
                        cost = 1.1
                    else:
                        cost = 0.9

                    if cost < min_cost:
                        min_cost = cost
                        min_neighbour = (k_next, l_next)

                k_next, l_next = min_neighbour
                self.maze.grid[k_next][l_next].visited = True
                k_curr = k_next
                l_curr = l_next


            elif len(visited) > 0:
                path.append(((k_curr, l_curr), True))
                k_curr, l_curr = visited.pop()

        path.append(((k_curr, l_curr), False))

        if not self.quiet_mode:
            print("Number of moves performed: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))

        logging.info('Class UniformCostSearch leaving solve')
        return path


import heapq

class AStarSearch(Solver):
    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.info('Class A*Search ctor called')
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "A*Search"

    def heuristic_function(self, start, goal):
        return abs(start[0] - goal[0])*0.9 + abs(start[1] - goal[1])*1.1

    def solve(self):
        logging.info("Class A*Search solve called")
        k_curr, l_curr = self.maze.entry_coor
        visited = dict()
        path = list()
        frontier = [(0, (k_curr, l_curr))]
        heapq.heapify(frontier)

        if not self.quiet_mode:
            print("\nSolving the maze with A*Search...")

        time_start = time.time()

        while frontier:
            min_cost, current = heapq.heappop(frontier)

            if current == self.maze.exit_coor:
                while current != self.maze.entry_coor:
                    path.append((current, False))
                    current = visited[current]
                path.append((self.maze.entry_coor, False))
                path.reverse()
                break

            for neighbor in self.maze.find_neighbours(*current):
                if neighbor not in visited and not self.maze.grid[current[0]][current[1]].is_walls_between(self.maze.grid[neighbor[0]][neighbor[1]]):
                    if current[0] != neighbor[0]:
                        g = min_cost + 1.1
                    else:
                        g = min_cost + 0.9
                    h = self.heuristic_function(neighbor, self.maze.exit_coor)
                    f = g + h
                    heapq.heappush(frontier, (f, neighbor))
                    visited[neighbor] = current

        if not self.quiet_mode:
            print("Number of moves performed: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))

        logging.info('Class A*Search leaving solve')
        return path







import random
import numpy as np

class QLearning(Solver):

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.info('QLearning ctor called')
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "QLearning"
        self.q_table = np.zeros((maze.num_rows, maze.num_cols, 4))
        self.current_state = None

    def q_learning(self, episodes, learning_rate, discount_factor, exploration_rate):
        for episode in range(episodes):
            self.current_state = self.maze.entry_coor  # 에피소드 시작시 현재 상태를 초기화합니다.
            total_reward = 0
            path = [(self.current_state, False)]

            while not self.check_if_solved(self.current_state):
                if np.random.rand() < exploration_rate:
                    action = np.random.choice(4)  # Explore: 무작위 행동 선택
                else:
                    action = np.argmax(self.q_table[self.current_state])

                next_state = self.get_next_state(self.current_state, action)

                neighbour = self.maze.grid[self.current_state[0]][self.current_state[1]]
                if neighbour.is_walls_between(self.maze.grid[next_state[0]][next_state[1]]):
                    continue

                reward = self.get_reward(next_state)

                max_next_q = np.max(self.q_table[next_state])
                self.q_table[self.current_state][action] += learning_rate * (
                        reward + discount_factor * max_next_q - self.q_table[self.current_state][action])

                self.current_state = next_state
                total_reward += reward
                path.append((self.current_state, False))

            print("Total Reward:", total_reward)
            return path

    def get_next_state(self, current_state, action):
        next_state = current_state

        if action == 0 and current_state[0] > 0:  # 상
            next_state = (current_state[0] - 1, current_state[1])
        elif action == 1 and current_state[0] < self.maze.num_rows - 1:  # 하
            next_state = (current_state[0] + 1, current_state[1])
        elif action == 2 and current_state[1] > 0:  # 좌
            next_state = (current_state[0], current_state[1] - 1)
        elif action == 3 and current_state[1] < self.maze.num_cols - 1:  # 우
            next_state = (current_state[0], current_state[1] + 1)

        # Ensure next_state is within Q table index range
        next_state = (max(0, min(next_state[0], self.maze.num_rows - 1)),
                      max(0, min(next_state[1], self.maze.num_cols - 1)))

        return next_state

    def get_reward(self, next_state):
        current_state = self.current_state  # 현재 상태를 가져옵니다.
        current_cell = self.maze.grid[current_state[0]][current_state[1]]
        next_cell = self.maze.grid[next_state[0]][next_state[1]]

        if next_state == self.maze.exit_coor:
            reward = 100
        elif current_cell.is_walls_between(next_cell):
            reward = -1
        else:
            reward = -0.1

        return reward

    def check_if_solved(self, state):
        return state == self.maze.exit_coor

    def solve(self):

        path = self.q_learning(episodes=10000, learning_rate=0.4, discount_factor=0.4, exploration_rate=0.1)
        return path
