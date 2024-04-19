import sys
import time
import json
import csv
import random
from typing import List

from maze.util import Coordinates
from maze.maze import Maze
from maze.arrayMaze import ArrayMaze
from maze.graphMaze import GraphMaze

from generation.mazeGenerator import MazeGenerator
from generation.recurBackGenerator import RecurBackMazeGenerator

canVisualise = True
try:
    from maze.maze_viz import Visualizer
except ImportError:
    Visualizer = None
    canVisualise = False


def generate_configurations():
    configurations = []
    data_structures = ['array', 'adjlist', 'adjmat']
    row_col_combinations = [
        (5, 5), (10, 10), (50, 50), (100, 100), (200, 200),
        (1, 100), (2, 50), (100, 1), (50, 2)
    ]

    for row, col in row_col_combinations:
        for ds in data_structures:
            entrance_row = random.randint(0, row - 1)
            entrance_col = random.randint(0, col - 1)
            exit_row = random.choice([0, row - 1])
            exit_col = random.choice([0, col - 1])

            config = {
                "dataStructure": ds,
                "rowNum": row,
                "colNum": col,
                "entrances": [[entrance_row, -1], [-1, entrance_col]],
                "exits": [[exit_row, exit_col], [row - 1, col - 1]],
                "generator": "recur",
                "visualise": False
            }
            configurations.append(config)

    return configurations


def run_simulation(configurations, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['dataStructure', 'rowNum', 'colNum', 'runtime', 'avg_run_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for config in configurations:
            maze = None
            ds_approach = config['dataStructure']
            row_num = config['rowNum']
            col_num = config['colNum']
            entrances = config['entrances']
            exits = config['exits']
            gen_approach = config['generator']
            runtimes = []

            if ds_approach == 'array':
                maze = ArrayMaze(row_num, col_num)
            elif ds_approach in ['adjlist', 'adjmat']:
                maze = GraphMaze(row_num, col_num, ds_approach)
            else:
                print('Unknown data structure approach specified.')
                continue

            for [r, c] in entrances:
                maze.addEntrance(Coordinates(r, c))
            for [r, c] in exits:
                maze.addExit(Coordinates(r, c))

            generator = None
            if gen_approach == 'recur':
                generator = RecurBackMazeGenerator()
            else:
                print('Unknown generator approach specified.')
                continue

            for i in range(100):
                start_time = time.perf_counter()
                generator.generateMaze(maze)
                end_time = time.perf_counter()
                runtime = end_time - start_time
                runtimes.append(runtime)

            avg_runtime = sum(runtimes) / len(runtimes)

            writer.writerow({
                'dataStructure': ds_approach,
                'rowNum': row_num,
                'colNum': col_num,
                'runtime': runtimes[-1],  # Last runtime
                'avg_run_time': avg_runtime
            })


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 script.py <output_file.csv>')
        sys.exit(1)

    output_file = sys.argv[1]
    configurations = generate_configurations()
    run_simulation(configurations, output_file)
