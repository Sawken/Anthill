import numpy as np
import random as rd
import copy


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# GLOBAL PARAMETERS FOR EXPERIMENTS

size_map = 20
neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]
           
#probability of making a new tunnel (we intend to make a function so this probability can change)           
#proba_tun = 0.1
           
#################################################################

map = np.ones((size_map,size_map), dtype = "int8")

map_dist = np.zeros ((size_map,size_map), dtype = "float16")        

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
                    string += bcolors.OKGREEN + "Q " + bcolors.ENDC
                else: string += bcolors.OKBLUE + "O " + bcolors.ENDC
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
    y, x = queen
    map[y][x] = 2
    for k, l in neighbs:
        # Check if we're not outside boundaries.
        if (k + x >= 0 and k + x < size_map and y + l >= 0 and l + y < size_map): 
            map[l + y][k + x] = 0
    #initilize a map with distances to the queen.
    for i in range(size_map):
        for j in range(size_map):
            map_dist[i][j] = np.sqrt((i - y)**2 + (j - x)**2)
    
    
    print(map)
    print (display_map())


def voisinage_zero (i, j):
    """ 
    Computes the proportion of zeros in the neighborhood of a element with
    coordinates i, j in the matrix.
    """    
    
    cpt_0 = 0
    cpt_total = 0
    for k, l in neighbs:
       if (k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
           cpt_total = cpt_total + 1
           if map[i + k, j + l] == 0:
               cpt_0 = cpt_0 + 1
    
    return float(cpt_0/cpt_total)


def proba_tun (i, j):
    """
    Computes the probability of digging a new tunnel from the position (i, j) taking in account the proportion
    of neighbors that are already dig. If more than half of the neighbors are already tunnels, the function return zero
    (so, no more tunnels are made). Otherwise, the probability of digging a tunnel is set to be under the form
    f(x) = a * (x - 1 / 2) ** 2, with "a" chosen in order to have f(1 / 8) = 1 / 2.
    """


    t = voisinage_zero (i, j)
    if t < 0.5:
        return (32/9)*(t - 1/2)**2
    else:
        return 0



def croissance ():
    
    map_old = copy.copy (map)
    
    for i in range(size_map):
        for j in range(size_map):
            if map_old[i][j] == 0:
                if rd.random() < proba_tun(i, j):
                    pos_tun = dig_tunnel(i,j)
                    if map[pos_tun] == 1: 
                        map[pos_tun] = 0
                    
                    
   
def dig_tunnel (i, j):
    """
    This function chooses a random position to dig among the neighbors of a zero 
    in the position (i,j) of the matrix. For that, it first creates a list of tuples
    with the existing neighbors and their distances to the queen. The probabilities 
    for each of those elements to be chosen are computed by the function proba_direction.
    The function returns the position of the cell to be dig chosen randomly according
    to those probabilities.

    """
    this_neighbs = []
    for k, l in neighbs:
        if (k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
            this_neighbs.append((map_dist[i+k][j+l], i+k, j+l))
    this_neighbs.sort (key = lambda neighb : neighb[0])
    this_proba = proba_direction (this_neighbs)
    dig_indice = np.random.choice (len(this_neighbs),p = this_proba)
    
    return (this_neighbs[dig_indice][1],this_neighbs[dig_indice][2])

    

def proba_direction (this_neighbs):
    """
    This function computes a list of probabilities of choosing one of the neighbors
    of a zero (that has already been selected to dig a tunnel), as a function of 
    the distance of each of those neighbors to the queen.
    this_neighbs is a list of tuples, each element containing the distance to 
    the queen and the absolute position in the matrix ordered in terms of distance.
    We choose to compute the probability in a linear fashion, where the probability
    of choosing the furthest element to the queen is 1 hundred times higher than choosing
    the nearest one. 
    This corresponds to picking the probabilities proportional to f(d) = a*d + b,
    where d is the distance to the queen and a and b are chosen in such a way that 
    f(dmin) = 1 and f(dmax) = 100. Dmin is the smallest distance present in this_neighbs
    and dmax is the biggest.
    """
    dmin = this_neighbs[0][0]
    dmax = this_neighbs[-1][0]
    this_proba = np.zeros(len(this_neighbs))
    a = 99 / (dmax - dmin)
    b = 1 - a * dmin
    
    for i in range(len(this_neighbs)):
        this_proba[i] = (a * this_neighbs[i][0] + b)
        
    this_proba = this_proba/np.sum(this_proba)
    
    return this_proba

def plot ():
    
    set_queen()
    
    for i in range(200):
        croissance ()
        print(display_map())
        input()

plot()