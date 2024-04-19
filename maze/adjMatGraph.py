# ------------------------------------------------------------------------
# Please COMPLETE the IMPLEMENTATION of this class.
# Adjacent matrix implementation.
#
# __author__ = 'Jeffrey Chan', <Md Arafat Hossain>
# __copyright__ = 'Copyright 2024, RMIT University'
# ------------------------------------------------------------------------


from typing import List

from maze.util import Coordinates
from maze.graph import Graph

class AdjMatGraph(Graph):
    def __init__(self, rowNum, colNum):
        # Initialize a matrix representation of the graph with rows and columns
        # The matrix includes sentinel nodes (-1, -1) to simplify boundary conditions
        self.rowNum = rowNum
        self.colNum = colNum
        self.matrix = {(r, c): {} for r in range(-1, rowNum + 1) for c in range(-1, colNum + 1)}

    def addVertex(self, label: Coordinates):
        # Add a vertex to the graph if it doesn't already exist
        if label not in self.matrix:
            self.matrix[label] = {}

    def addVertices(self, vertLabels: List[Coordinates]):
        # Add multiple vertices to the graph
        for label in vertLabels:
            self.addVertex(label)

    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False):
        # Add an edge between two vertices
        # If addWall is True, mark the edge as a wall
        if vert1 in self.matrix and vert2 in self.matrix:
            self.matrix[vert1][vert2] = addWall
            self.matrix[vert2][vert1] = addWall
            return True
        return False

    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool):
        # Update the wall status of an edge between two vertices
        if vert1 in self.matrix and vert2 in self.matrix:
            self.matrix[vert1][vert2] = wallStatus
            self.matrix[vert2][vert1] = wallStatus
            return True
        return False

    def removeEdge(self, vert1: Coordinates, vert2: Coordinates):
        # Remove an edge between two vertices
        if vert1 in self.matrix and vert2 in self.matrix and vert2 in self.matrix[vert1]:
            del self.matrix[vert1][vert2]
            del self.matrix[vert2][vert1]
            return True
        return False

    def hasVertex(self, label: Coordinates):
        # Check if a vertex exists in the graph
        return label in self.matrix

    def hasEdge(self, vert1: Coordinates, vert2: Coordinates):
        # Check if an edge exists between two vertices
        return vert2 in self.matrix.get(vert1, {})

    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates):
        # Get the wall status of an edge between two vertices
        return self.matrix.get(vert1, {}).get(vert2, False)

    def neighbours(self, label: Coordinates):
        # Get the list of neighbors for a vertex
        return list(self.matrix.get(label, {}).keys())
