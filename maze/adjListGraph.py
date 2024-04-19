# ------------------------------------------------------------------------
# Please COMPLETE the IMPLEMENTATION of this class.
# Adjacent list implementation.
#
# __author__ = 'Jeffrey Chan', <Md Arafat Hossain>
# __copyright__ = 'Copyright 2024, RMIT University'
# ------------------------------------------------------------------------


from typing import List

from maze.util import Coordinates
from maze.graph import Graph


from typing import List
from maze.util import Coordinates
from maze.graph import Graph

class AdjListGraph(Graph):
    def __init__(self, rowNum, colNum):
        # Initialize the graph with dimensions rowNum x colNum
        self.rowNum = rowNum
        self.colNum = colNum
        # Initialize the adjacency list as a dictionary
        # Keys are coordinates of vertices, values are sets of tuples representing neighbouring vertices and wall status
        self.adjList = {
            (r, c): set() for r in range(-1, rowNum + 1) for c in range(-1, colNum + 1)
        }

    def addVertex(self, label: Coordinates):
        # Add a vertex to the graph if it's not already present
        if label not in self.adjList:
            self.adjList[label] = set()

    def addVertices(self, vertLabels: List[Coordinates]):
        # Add multiple vertices to the graph
        for label in vertLabels:
            self.addVertex(label)

    def addEdge(self, vert1: Coordinates, vert2: Coordinates, addWall: bool = False):
        # Add an edge between vert1 and vert2, with optional wall status
        if vert1 in self.adjList and vert2 in self.adjList:
            # Add vert2 to the neighbours of vert1, and vert1 to the neighbours of vert2
            self.adjList[vert1].add((vert2, addWall))
            self.adjList[vert2].add((vert1, addWall))
            return True
        return False

    def updateWall(self, vert1: Coordinates, vert2: Coordinates, wallStatus: bool):
        # Update the wall status between vert1 and vert2
        if vert1 in self.adjList and vert2 in self.adjList:
            # Find the tuples representing the edge between vert1 and vert2, and update the wall status
            pairs1 = {(v, w) for v, w in self.adjList[vert1] if v == vert2}
            pairs2 = {(v, w) for v, w in self.adjList[vert2] if v == vert1}
            # Remove the old tuples and add new ones with updated wall status
            self.adjList[vert1] -= pairs1
            self.adjList[vert2] -= pairs2
            self.adjList[vert1].add((vert2, wallStatus))
            self.adjList[vert2].add((vert1, wallStatus))
            return True
        return False

    def removeEdge(self, vert1: Coordinates, vert2: Coordinates):
        # Remove the edge between vert1 and vert2
        success = False
        if vert1 in self.adjList and vert2 in self.adjList:
            # Check if the edge exists and remove it
            success |= {(vert2, w) for w in [True, False]} <= self.adjList[vert1]
            success |= {(vert1, w) for w in [True, False]} <= self.adjList[vert2]
            self.adjList[vert1] = {(v, w) for v, w in self.adjList[vert1] if v != vert2}
            self.adjList[vert2] = {(v, w) for v, w in self.adjList[vert2] if v != vert1}
        return success

    def hasVertex(self, label: Coordinates):
        # Check if a vertex exists in the graph
        return label in self.adjList

    def hasEdge(self, vert1: Coordinates, vert2: Coordinates):
        # Check if an edge exists between vert1 and vert2
        return any(v == vert2 for v, _ in self.adjList.get(vert1, set()))

    def getWallStatus(self, vert1: Coordinates, vert2: Coordinates):
        # Get the wall status between vert1 and vert2
        return any(v == vert2 and w for v, w in self.adjList.get(vert1, set()))

    def neighbours(self, label: Coordinates):
        # Get the neighbours of a vertex
        return [v for v, _ in self.adjList.get(label, set())]