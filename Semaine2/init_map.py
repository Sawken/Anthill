import numpy as np
import random as rd


# GLOBAL PARAMETERS FOR EXPERIMENTS

size_map = 200
yx_map = (size_map, size_map)
neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]
#################################################################

map = np.ones(yx_map)           

def display_map():
    """
    display the entire map
    """
    global size_map
    
    string = ""
    for i in range(size_map):
        for j in range(size_map):
            if map[i][j] != 1:
                if map[i][j] == 2:
                    string += "Q "
                else: string += "O "
            else:
                string += "X "
        string += "\n"
    return string

def set_queen():
    """
    set the queen randomly in the map
    """

    global neighbs
    
    queen = (rd.randint(0, size_map - 1), rd.randint(0, size_map - 1))
    x, y = queen
    map[y][x] = 2
    for k, l in neighbs:
        # Check if we're not outside boundaries.
        if (k + x >= 0 and k + x < size_map and y + l >= 0 and l  + y < size_map): 
            map[l + y][k + x] = 0
    print(map)
    print (display_map())
