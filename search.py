
# Iterative Deepening Depth First Search on 15 Puzzle
#Spring 2024

import queue
import random
import math
import time
import psutil
import os
from collections import deque
import sys


CUTOFF = 0 
FAILURE = 1 
depth_expand = 0 


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        if len(tiles) != 16:
            raise ValueError("Not a 4x4 grid.")
        self.tiles = tiles


    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        newTiles = self.tiles[:]
        emptySpot = newTiles.index('0')
        
        if action == 'U' and emptySpot - 4 >= 0:
            origSpot = newTiles[emptySpot - 4]
            newTiles[emptySpot - 4] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        elif action == 'D' and emptySpot + 4 < 16:
            origSpot = newTiles[emptySpot + 4]
            newTiles[emptySpot + 4] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        elif action == 'L' and emptySpot % 4 > 0: 
            origSpot = newTiles[emptySpot - 1]
            newTiles[emptySpot - 1] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        elif action == 'R' and emptySpot % 4 < 3 :
            origSpot = newTiles[emptySpot + 1]
            newTiles[emptySpot + 1] = newTiles[emptySpot]
            newTiles[emptySpot] = origSpot 
        
        return Board(newTiles)


            



# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action 

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))



class Search:




    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        actions = ['U', 'D', 'L', 'R']
        children = []
        for action in actions:
            children.append(Node(parent_node.state.execute_action(action), parent_node, action) )
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while node.parent:
            path.insert(0, node.action)
            node = node.parent 
        return path 


   
 # This function runs depth limited search from the given root node and returns path
    def run_dfs(self, curr_node, lim):
        global depth_expand  
        if self.goal_test(curr_node.state.tiles):
            return curr_node, depth_expand
    
        elif lim == 0: 
            return CUTOFF, depth_expand
    
        depth_expand += 1 
        cutoff_check = False 
    
        for child in self.get_children(curr_node):
            result, expanded_nodes = self.run_dfs(child, lim - 1)
        
            if not isinstance(result, Node):
                if result != FAILURE:
                    return FAILURE, expanded_nodes
                elif result == CUTOFF:
                    cutoff_check = True
            else: 
                return result, expanded_nodes
    
        if cutoff_check:
            return CUTOFF, depth_expand
        else: 
            return FAILURE, depth_expand

           
          

    def goal_test(self, cur_tiles):
        return cur_tiles == [str(i) for i in range(1,16)] + ['0']

    def solve(self, input):
        
        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        process =  psutil.Process(os.getpid())
        initMem = process.memory_info().rss / 1024.0
        expanded_nodes_total = 0
        time_taken_total = 0
        memory_consumed_total = 0

        notFoundYet = True 
        i = 0 
        path = None
        startTime = time.time()
        # interative deepening search
        while(notFoundYet):
            depth_expand = 0
            result, expanded_nodes_total = self.run_dfs(root, i)
            if isinstance(result, Node):
                path = self.find_path(result)
                notFoundYet = False
            i += 1
        finalMem = process.memory_info().rss / 1024.0
        endTime = time.time()
        totalTime = endTime - startTime
        memoryUsed = finalMem - initMem
        #path, expanded_nodes, time_taken, memory_consumed = self.run_bfs(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes_total))
        print("Time Taken: " + str(totalTime))
        print("Max Memory (Bytes): " + str(memoryUsed))
        return "".join(path)

# Testing the algorithm locally
if __name__ == '__main__':
    agent = Search()
    #agent.solve("1 2 3 4 5 6 7 8 9 10 11 0 13 14 15 12")
    agent.solve("2 8 1 0 4 6 3 7 5 9 10 12 13 14 11 15")

