import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import networkx as nx
from collections import deque

# task 1

class CityGrid:
    def __init__(self, rows, columns, R, obstacle_coverage=0.3):
        self.rows = rows
        self.columns = columns
        self.R = R
        self.grid = np.random.choice([1, 0], size=(rows, columns), p=[1 - obstacle_coverage, obstacle_coverage])
        self.towers = []
    
# task 2
    
    def place_tower(self, row, col):
        if not self.grid[row][col]:
            print(f"cannot put tower: ({row}, {col})")
            return

        for r in range(max(0, row - self.R), min(self.rows, row + self.R + 1)):
            for c in range(max(0, col - self.R), min(self.columns, col + self.R + 1)):
                if self.grid[r][c]==1:
                    self.grid[r][c] = 2
        self.grid[row][col] = 3
        self.towers.append((row, col))
    
# task 3

    def optimize_tower_placement(self):
        non_obstructed_blocks = [(i, j) for i in range(self.rows) for j in range(self.columns) if self.grid[i][j] == 1]
    
        final_tower_locations = []
        while non_obstructed_blocks:
            best_tower = None
            max_covered = 0
    
            for row, col in non_obstructed_blocks:
                coverage_count = 0
                for i in range(max(0, row - self.R), min(self.rows, row + self.R + 1)):
                    for j in range(max(0, col - self.R), min(self.columns, col + self.R + 1)):
                        if self.grid[i][j] == 1:
                            coverage_count += 1
    
                if coverage_count > max_covered:
                    best_tower = (row, col)
                    max_covered = coverage_count
    
            if bool(best_tower):
                row, col = best_tower
                final_tower_locations.append((row, col))
    
                for i in range(max(0, row - self.R), min(self.rows, row + self.R + 1)):
                    for j in range(max(0, col - self.R), min(self.columns, col + self.R + 1)):
                        if self.grid[i][j] == 1 and (i, j) in non_obstructed_blocks:
                            non_obstructed_blocks.remove((i, j))
    
        for row, col in final_tower_locations:
            for r in range(max(0, row - self.R), min(self.rows, row + self.R + 1)):
                for c in range(max(0, col - self.R), min(self.columns, col + self.R + 1)):
                    if self.grid[r][c]==1:
                        self.grid[r][c] = 2
            self.grid[row][col] = 3
    
        self.towers.extend(final_tower_locations)

    def is_connected(self, tower1, tower2):
        i1, j1 = tower1
        i2, j2 = tower2
        distance = abs(i1 - i2) + abs(j1 - j2)
        return distance <= 2*self.R

# task 4
    
    def find_path(self, tower1, tower2):
        graph = nx.Graph()

        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i, j] == 3:
                    graph.add_node((i, j))

        for node1 in graph.nodes():
            for node2 in graph.nodes():
                if node1 != node2 and self.is_connected(node1, node2):
                    graph.add_edge(node1, node2)

        print(graph.nodes)
        if self.is_connected(tower1, tower2):
            try:
                shortest_path = nx.shortest_path(graph, source=tower1, target=tower2, weight='weight')
                return shortest_path
            except nx.NetworkXNoPath:
                print(f"Path not found")

        indirect_path = self.find_indirect_path(tower1, tower2, graph)

        if indirect_path:
            return indirect_path
        else:
            print(f"path not found")

    def find_indirect_path(self, tower1, tower2, graph):
        visited = set()
        queue = deque([(tower1, [tower1])])

        while queue:
            current_tower, path = queue.popleft()
            if current_tower == tower2:
                return path

            if current_tower not in visited:
                visited.add(current_tower)
                for neighbor in graph.neighbors(current_tower):
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        return None


    def show_city(self):
        plt.imshow(self.grid, cmap=ListedColormap(['blue', 'white']), interpolation='none')
        plt.title("obstructed block color is blue")
        plt.colorbar()
        plt.show()
        pass
    
    def show_tower_placements(self):
        plt.imshow(self.grid, cmap="viridis", interpolation='none')
        plt.colorbar()
        plt.show()
        pass

    def visualize_paths(self, tower1, tower2, path):
        fig, ax = plt.subplots()
        ax.imshow(self.grid, cmap='viridis', interpolation='none')
        
        for tower in self.towers:
            ax.add_patch(plt.Circle(tower, 0.2, color='red'))
        
        try:
            
            for i in range(len(path) - 1):
                tower1 = path[i]
                tower2 = path[i + 1]
                plt.plot([tower1[1], tower2[1]], [tower1[0], tower2[0]], 'b-')
        
            plt.show()
        except TypeError:
            print("Не могу нарисовать график")


if __name__ == "__main__":
    city = CityGrid(rows=15, columns=15, R=3)
    city.show_city()
    city.place_tower(2, 2)
    city.show_tower_placements()
    
    city.optimize_tower_placement()
    city.show_tower_placements()
    path = city.find_path(city.towers[0],city.towers[8])
    print(city.towers)
    print(city.towers[0],city.towers[8])
    city.visualize_paths(city.towers[0], city.towers[8], path)
    