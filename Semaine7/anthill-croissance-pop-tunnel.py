# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 01:45:53 2017

@author: Ariana
"""

import numpy as np
import random as rd
import copy
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math

# GLOBAL PARAMETERS FOR EXPERIMENTS

size_map = 200 # Size of square matrix map.
neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]
# This array simplifies the searching for direct neighbours.
             
voisinage_exte = 4 # Size of extended neighborhood used to decide if a tunnel will be created or not.
             
max_age = 365 # 1 year is the maximal age of an ant.
max_age_phase = 15 # Number of days of each non-adult phases. 

#We suppose that an ant needs 15 to go from egg to larva, 15 days to go from larva to pupa 
#and more 15 days to became adult. An ant lives a maximum of 1 year (365 days). These values 
#were chosen based on our research on the average lifetime of an ant.

p_enfant = 5e-4
p_final = 0.1
p_adulte = np.exp(np.linspace(np.log(p_enfant),np.log(p_final),max_age - 3 * max_age_phase))

#p is the probability of death of an ant. We chose to increase this probability according to
#their age, that is, an ant will have a bigger possibility of dying the older it is.

#We use the linspace function to create a array with equally spaced entries. Since we 
#want to create a vector with entries that increase exponentially, we compute its
#componentwise exponential. For a simpler choice of initial and final entries, we use
#the logarithm of the probabilities we want.

ratio_fourmis_tunnels = 0.5 # Quantity of tunnels each ant can create and keep.

# Defining a personalized color map.
# 2 = green
# 1 = black
# 0 = white

cdict = {'red':   [(0.0, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 1.0, 1.0)],

         'green': [(0.0, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0)],

         'blue':  [(0.0, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0)]}
                   
cmap_custom = mcolors.LinearSegmentedColormap('CustomMap', cdict)

#################################################################

oeuf = np.zeros(max_age_phase,dtype = "int32")
larve = np.zeros(max_age_phase,dtype = "int32")
nymphe = np.zeros(max_age_phase,dtype = "int32")
ouvriere = np.zeros(max_age - 3 * max_age_phase,dtype = "int32")

#Each of those arrays contains the total number of ants in a development stage.
#The "i" element of an array contains the number of ants that are in the corresponding
#development stage after "i" days. For example, ouvriere[5] contains the number of
#ants that have become adults 5 days ago.  

#We created arrays and not lists to simplify the use of algebraic operations
#(componentwise sum).

map = np.ones((size_map,size_map), dtype = "int8") # This matrix represents the space were the anthill can grow.

map_dist = np.zeros ((size_map,size_map), dtype = "float16") 
# This matrix stocks each element distance relative to the queen. 

set_connexe = set()

pos_reine_i = -1 
pos_reine_j = -1

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# No idea what this one does. It works in PyCharm but not in Spider and it wasn't me who put it here =P.

###################################################################

def croissance_fourmis():
     """
     Each time this function is called, it changes the vectors "oeuf", "larve",
     "nymphe" and "ouvriere", computing the new quantity of ants in each stage of 
     developpement by aging each group by 1 day, creating new ants with 0 days 
     of age, and killing some ants in a random fashion using the functions 
     naissance and mort.
     """
    
     global oeuf, larve, nymphe, ouvriere
     
     ouvriere[1:] = ouvriere[:-1]
     ouvriere[0] = nymphe[-1]
     nymphe[1:] = nymphe[:-1]
     nymphe[0] = larve[-1]
     larve[1:] = larve[:-1]
     larve[0] = oeuf[-1]
     oeuf[1:] = oeuf[:-1]
     #aging by 1 day of the population of ants.
     
     oeuf[0] = naissance()
     #birth of new ants.
     
     oeuf = oeuf - mort(oeuf,p_enfant)
     larve = larve - mort(larve,p_enfant)
     nymphe = nymphe - mort(nymphe,p_enfant)
     ouvriere = ouvriere - mort(ouvriere,p_adulte)
     #ants death.
     
def naissance():
   """
   This function creates an aleatory number between 18 and 25 to be put at the 
   first element of the array eggs to represent new ants being created.
   """
   
   return rd.randint(18, 25)
    #The queen lays between 18 et 25 eggs a day.

def mort(liste,p):
    """
    This function computes the death of an aleatory number of ants, taking in consideration
    a probability that changes with the age of the ants (p can be an array). We do that by means 
    of the function random.binomial, that has 2 arguments (the array with the ants population
    and the probability of one ant death). Each ant has a probability "p" of dying in 1 day.
    With a quantity N of ants, the probability of K ants to die in 1 day is computed by 
    p^K(1-p)^(N-K) multiplied by the number of different ways of choosing K ants between N 
    (that is, the binomial coefficient (N,K)). That is the binomial law that computes 
    how many ants die.
    """
    
    return np.random.binomial(liste,p)

def display_map():
    """
    display the entire map replacing numbers from the array with letters in a string
    for better visualisation of the anthill.
    """
    
    global size_map
    
    string = ""
    for i in range(size_map):
        for j in range(size_map):
            if map[i][j] != 1:
                if map[i][j] == 2:
                    string += bcolors.OKGREEN + "Q " + bcolors.ENDC 
                    #Q represents the queen.
                else: string += bcolors.OKBLUE + "O " + bcolors.ENDC
                # O represents the tunnels.
            else:
                string += "X "
                #X represents any part that wasnt yet excavated.
        string += "\n"
    return string

def set_queen():
    """
    Set one queen randomly in the array map with empty spaces around her
    and computes the relative euclidean distance to her for each element
    of the array map. Those distances are stocked in the array map_dist. 
    The queen is represented by the number 2 in map.
    """

    global neighbs, pos_reine_i, pos_reine_j
    
    #queen = (rd.randint(0, size_map - 1), rd.randint(0, size_map - 1))
    queen = (rd.randint(size_map*0.25, size_map*0.75), rd.randint(size_map*0.25, size_map*0.75))
    #randomly choses a place for the queen.
    i, j = queen
    pos_reine_i = i
    pos_reine_j = j
    
    map[i][j] = 2
    for k, l in neighbs:
        if (l + i >= 0 and l + i < size_map and j + k >= 0 and k + j < size_map): 
        # Check if we're not outside boundaries of the array.
            map[l + i][k + j] = 0
            # Put empty spaces around the queen.
    # Initilize a map with distances to the queen.
    for k in range(size_map):
        for l in range(size_map):
            map_dist[k][l] = np.sqrt((i - k)**2 + (j - l)**2)
    
def rayon_fourmiliere ():
    """
    Returns the distance of the farthest tunnel from the queen. 
    We use this to determinated which tunnels should be created or destroyed first.
    """
    
    rayon = 0
    for i in range(size_map):
        for j in range(size_map):
            if map[i][j] == 0 and map_dist[i][j] > rayon:
                rayon = map_dist[i][j]
    return rayon
    
    
def quant_zeros ():
    """
    Return the quantity of zeros in map.
    We use this to determinated if tunnels should be created or destroyed.
    """
    
    return np.sum(map == 0)  
    
def voisinage_zero (i, j, exte):
    """ 
    Computes the proportion of zeros in the extended neighborhood of a element with
    coordinates (i, j) in the array map.
    """    
    
    cpt_0 = 0
    cpt_total = 0
    for k in range(-exte,exte + 1):
        for l in range(-exte, exte + 1):
           if (not (k == 0 and  l == 0) and k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
               cpt_total = cpt_total + 1
               if map[i + k, j + l] == 0:
                   cpt_0 = cpt_0 + 1
        
    return float(cpt_0/cpt_total)
             
def proba_tun (i, j, rayon):
    """
    Computes the probability of digging a new tunnel from the position (i, j) taking
    in account the proportion of neighbours that are already dig. If more than
    0.4 of neighbors are already tunnels, the function return zero (so, no more
    tunnels are made based in this position). Otherwise, the probability of digging 
    a tunnel is set to be under the form f(x) = a * (x - 1/2) ** 2, with "a" 
    chosen in order to have f(1/8) = 1/2. This way we use only half of a parabole.
    """
    
    t = voisinage_zero (i, j, voisinage_exte)
    dist = map_dist [i][j]
    if dist < 15 and t < 0.4 and dist > 0.50 * rayon:
        return (32/9) * (t - 1/2) ** 2
    if t < 0.2 and dist > 0.50 * rayon:
        # This way we increase the chance for a tunnel to be created far from the queen.
        return (32/9) * (t - 1/2) ** 2
    return 0
    
def croissance_tun ():
    """ 
    This function computes all the possible growth of the anthill in 1 round and
    applies it randomically, that is, it still has a random possibility of growth.
    """
    
    map_old = copy.copy (map)
    #We use a copy of map to decide if a tunnel generates another one so a new tunnel doesnt influenciates the rest of the creation cicle.
    rayon = rayon_fourmiliere ()
    for i in range(size_map):
        for j in range(size_map):
            if map_old[i][j] == 0:
                if rd.random() < proba_tun(i,j,rayon):
                    pos_tun = dig_tunnel(i,j)
                    if map[pos_tun] == 1: 
                        map[pos_tun] = 0
                    
def dig_tunnel (i, j):
    """
    This function chooses a random position to dig among the neighbors of a zero 
    in the position (i, j) of the array. For that, it first creates a list of tuples
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
    f(dmin) = 1 and f(dmax) = 10. Dmin is the smallest distance present in this_neighbs
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
    
def decroissance_tun (quant_tun) :
    """
    This function computes all the possible destruction of tunnels in 1 round and
    applies it.
    """
    
    global set_connexe    
    
    map_old = copy.copy (map)
    #We use a copy of map to decide if a tunnel is destroyed so it doesnt influenciates the rest of the destruction cicle.
    list_zero_dist = np.zeros(quant_tun,dtype = "float32")
    # This is an array with the distances of a quantity "quant_tun" of zeros to the queen were in the end we will have the "quant_tun" farthest zeros.
    list_zero_pos = np.zeros((quant_tun,2),dtype = "int16")
    # This array stocks the coordinates of each zero that is in list_zero_dist.
    for i in range(size_map):
       for j in range(size_map):
           if (map_old[i][j] == 0) and map_dist[i][j] > 1.5 :
           # The 1.5 distance prevents the destruction of tunnels that are direct neighbors to the queen.
               k = 0
               while (k < quant_tun) and (list_zero_dist[k] > map_dist[i][j]):
                   k += 1
               # Test to see why it got out of the loop.
               if k < quant_tun:
                   # Displaces each element of both arrays of one position.
                   list_zero_dist[k + 1 : ] = list_zero_dist[k : quant_tun - 1]
                   list_zero_pos[k + 1 : ][ : ] =  list_zero_pos [k : quant_tun - 1][ : ]
                   # Puts the new zero, that is further to the queen, in both arrays.
                   list_zero_dist[k] = map_dist[i][j]
                   list_zero_pos[k][ : ] = [i, j] 
                   
    quant_final = quant_tun               
    destruct = np.random.choice(quant_tun)
    x, y = list_zero_pos[destruct][0], list_zero_pos[destruct][1]
    side = 1
    quant_0 = quant_zeros()
    while quant_final > 0 and quant_0 > 8 :
        for k in range(-side, side + 1):
            for l in range(-side, side + 1):
                if (k + x >= 0 and k + x < size_map and l + y >= 0 and l + y < size_map): 
                    if map[k + x][l + y] == 0 and map_dist [k + x][l + y] > 1.5:
                        quant_final -= 1 
                        map[k + x][ l + y] = 1
                        quant_0 -= 1
            side += 1
    set_connexe = set ()
    connexe (pos_reine_i, pos_reine_j)
    for i in range(size_map):
       for j in range(size_map):
           if (map[i][j] == 0) and (i,j) not in set_connexe:
               map[i][j] = 1
        
    
def connexe (i,j):
    """
    Test to see if the each case of the anthill is still connected to the queen. 
    """    
    
    for k, l in neighbs:
         if (k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
             if map [k + i][l + j] == 0 and (k + i, j + l) not in set_connexe:
                 set_connexe.add((k + i, j + l))
                 connexe (k + i, j + l)
    
def init_fourmis ():
    """
    It fills the first 20 spaces of the array ouvriere with a random quantity of ants,
    so that when the queen is created the anthill can grow immediately (It simulates
    the ants that go out of an anthill with a new queen to form a new colony).
    """
    
    nb_fourmis = rd.randint(50, 100)
    for i in range (nb_fourmis):
        age = rd.randint(0,20)
        ouvriere[age] += 1

def dynamics (nb):
    """
    This function creates an anthill and simulates its growth, relating the creation
    of tunnels to the quantity of adults ants alive each turn. If the quantity of 
    ants isnt big enough, the function destroys tunnels, else it creates new ones. 
    """
    
    init_fourmis ()
    set_queen()
    ax1, fig1 = init_plot_fourmiliere ()
    ax2, fig2 = init_plot_fourmis ()
    plt.ion()
    
    for i in range(nb):
        croissance_fourmis()
        quant_tun = quant_zeros () - ratio_fourmis_tunnels * np.sum(ouvriere)
        if quant_tun < 0:
            croissance_tun ()
            
        elif quant_tun > 0:
            decroissance_tun (math.ceil (quant_tun))
            #we need it to be an integer bigger than zero.

        display_plot_fourmiliere (ax1, fig1)
        display_plot_fourmis (ax2, fig2)

        plt.show()
        plt.pause(0.01)

        #plt.waitforbuttonpress() #If we want to control manually when it changes.


#To create a new simulation, call the fonction dynamics with nb the number of iteractions wanted.
#It will plot automatically the growth of the anthill and also a graph with the quantity of ants x their age in days. 

#########################################################################
   
# FUNCTIONS TO PLOT OUR SIMULATIONS
   
# To create any simulation, just call the fonction with nb number of iteractions wanted.
# Be careful, some fonctions do not work with an elevated number of iteractions (not enough memory).


def sim_pop_fourmis (nb):
    
     init_fourmis ()
     
     sum_fourmis_total = np.zeros (nb+1)
     
     sum_fourmis_total[0] = np.sum(oeuf)+ np.sum(larve) + np.sum(nymphe) + np.sum(ouvriere) + 1
  
     for i in range (nb):
          croissance_fourmis()
          sum_fourmis_total[i + 1] = np.sum(oeuf)+ np.sum(larve) + np.sum(nymphe) + np.sum(ouvriere) + 1
  
     plt.plot(sum_fourmis_total)
     plt.ylabel("Quantité totale de fourmis")
     plt.xlabel("Temps (jours)")  
     plt.grid()
     plt.show()
  
def sim_old_fourmi (nb, initial = 0.1,final = 1.0,jump = 0.05):
    
    global p_final, p_adulte
    
    #saving global variables.
    global_p_final = p_final
    global_p_adulte = p_adulte
    
    p = np.arange(initial, final + jump/2, jump)
    p[-1] = 1
    print (p)
    
    age_fourmi = np.zeros_like(p)
    
    for j in range(p.shape[0]):
        oeuf[:] = 0
        larve[:] = 0
        nymphe[:] = 0
        ouvriere[:] = 0
        p_final = p[j]
        p_adulte = np.exp(np.linspace(np.log(p_enfant),np.log(p_final),max_age - 3 * max_age_phase))
        init_fourmis ()
        
        for i in range (nb):
            croissance_fourmis()
        
        i = -1
        
        while ouvriere[i] == 0:
            i -= 1
            
        age_fourmi[j] = max_age + i
            
    #restoring global variables.
    p_final = global_p_final
    p_adulte = global_p_adulte
    
    plt.plot(p,age_fourmi)
    plt.xlabel("Probabilité de mort d'une fourmi de 365 jours")
    plt.ylabel("Âge de la fourmi la plus âgée")  
    plt.grid()
    plt.show()
  
def sim_rayon_moyen (nb, fois = 10):    
   
    rayon_moyen = np.zeros(nb + 1)   
   
    for j in range(fois):
        oeuf[:] = 0
        larve[:] = 0
        nymphe[:] = 0
        ouvriere[:] = 0        
        map[:] = 1
        
        init_fourmis ()
        set_queen()
        rayon_moyen[0] += rayon_fourmiliere ()
        
        for i in range(nb):
            croissance_fourmis()
            quant_tun = quant_zeros () - ratio_fourmis_tunnels * np.sum(ouvriere)
            if quant_tun < 0:
                croissance_tun ()
                
            elif quant_tun > 0:
                decroissance_tun (math.ceil (quant_tun))
            rayon_moyen[i + 1] += rayon_fourmiliere ()    
            print (j,i)
        
    rayon_moyen = rayon_moyen / fois
    
    plt.plot(rayon_moyen)
    plt.ylabel("Rayon moyen de la fourmilière")
    plt.xlabel("Temps (jours)")  
    plt.grid()
    plt.show()
      
def sim_rayon_voisinage(nb, fois = 10, initial = 1,final = 10,jump = 1):

    global voisinage_exte
    
    #saving global variables.
    global_voisinage_exte = voisinage_exte
    
    voisi = np.arange(initial, final + jump, jump, dtype = "int32")
    print(voisi)
    
    rayon_moyen = np.zeros_like(voisi)   
   
    for i in range (voisi.shape[0]):
        voisinage_exte = voisi[i]
        
        for j in range(fois):
            oeuf[:] = 0
            larve[:] = 0
            nymphe[:] = 0
            ouvriere[:] = 0        
            map[:] = 1
            
            init_fourmis ()
            set_queen()
        
            for k in range(nb):
                print(i, j, k)
                croissance_fourmis()
                quant_tun = quant_zeros () - ratio_fourmis_tunnels * np.sum(ouvriere)
                if quant_tun < 0:
                    croissance_tun ()
                    
                elif quant_tun > 0:
                    decroissance_tun (math.ceil (quant_tun))
                    
            rayon_moyen[i] += rayon_fourmiliere ()
        
    rayon_moyen = rayon_moyen / fois
   
    plt.plot(voisi,rayon_moyen)
    plt.xlabel("Taille du voisinage")
    plt.ylabel("Rayon moyen de la fourmilière")  
    plt.grid()
    plt.show()
    
    #restoring global variables.
    voisinage_exte = global_voisinage_exte
    
# The fonctions below do not need to be called, they will be called automatically if you call dynamics. 
# They plot the simulation of growth and the graph of number of ants x their age.

def init_plot_fourmiliere ():                

    dpi = 20.0 #We find 72 dpi to be too small.
    figsize = (size_map/float(dpi),size_map/float(dpi))
    fig1 = plt.figure(figsize=figsize,facecolor = "white")
    ax1 = fig1.add_axes([0.0, 0.0, 1.0, 1.0], frameon = False)
    ax1.imshow(map, interpolation = 'nearest', cmap = cmap_custom)
    ax1.set_xticks([]), ax1.set_yticks([])
    
    return ax1, fig1
    
def display_plot_fourmiliere (ax1, fig1):

    ax1.cla()
    ax1.imshow(map, interpolation = 'nearest', cmap = cmap_custom)
    ax1.set_xticks([]), ax1.set_yticks([])
    fig1.canvas.draw()    
 
def init_plot_fourmis () :
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_ylabel("Quantité de fourmis")
    ax2.set_xlabel("Âge des fourmis en jours")  
    ax2.grid()
    
    return ax2, fig2    

def display_plot_fourmis (ax2, fig2) :
    end_oeuf = len(oeuf)
    end_larve = end_oeuf + len(larve)
    end_nymphe = end_larve + len(nymphe)
    end_ouvriere = end_nymphe + len(ouvriere)
    
    ax2.cla()
    ax2.plot(np.arange(0,end_oeuf),oeuf)
    ax2.plot(np.arange(end_oeuf,end_larve),larve)
    ax2.plot(np.arange(end_larve,end_nymphe),nymphe)
    ax2.plot(np.arange(end_nymphe,end_ouvriere),ouvriere)
    ax2.set_ylabel("Quantité de fourmis")
    ax2.set_xlabel("Âge des fourmis en jours")  
    ax2.grid()
    fig2.canvas.draw()   
    
