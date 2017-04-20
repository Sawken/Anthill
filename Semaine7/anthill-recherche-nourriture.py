# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:09:32 2017

@author: 3530406
"""

# -*- coding: utf-8 -*-

"""
Created on Tue Mar 07 17:28:32 2017
@author: Cécile
"""


""" Une fourmi dite "éclaireuse", qui découvre une source de nourriture, rentre dans sa colonie en laissant sur son passage une trace 
chimique. Cette trace stimule d'autres fourmis ouvrières, les attirant à l'extérieur de la colonie afin de la suivre et de retrouver 
à leur tour la source de nourriture. Elles rentrent ensuite chez elles, laissant sur leur passage une trace chimique qui renforce la 
précédente, et le même processus se reproduit.
D'après Jean-Louis Deneubourg, on estime qu'un individu ("l'éclaireuse") attire un nombre n de congénères, qui attirent eux-mêmes n 
congénères et ainsi de suite.
On comprend ainsi que les individus ayant emprunté le chemin le plus court rentreront chez eux plus tôt et attireront ainsi le 
plus rapidement les autres fourmis ouvrières (la trace chimique sera renforcée plus rapidement). """


import numpy as np
import random as rd
import copy
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# On crée un espace représenté par une matrice de taille dim*dim. Attention cet espace n'est pas la fourmilière elle-même,
# mais bien l'environnement dans lequel elle se situe.


neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]

dim = 50

espace = np.zeros((dim,dim),"int32")

### Création de la fourmilière

def fourmilière(espace):

    """Creée une sortie du fourmilière"""    
    
    espace[dim-1,dim-1] = -1
    return espace


### Génération automatique d'une source de nourriture

# La source sera représentée dans la matrice par la valeur de la variable 'parts'. A chaque fois qu'une fourmi se sera nourrie, parts
# diminuera de 1, jusqu'à atteindre 0 (source de nourriture épuisée).
# Pour que la simulation soit intéressante, imposons pour ce premier essai que la source de nourriture se situe dans une case
# aléatoire de la zone supérieure gauche de l'espace. Bien sûr, dans des versions futures, nous pourrons générer des sources de nourriture à des endroits aléatoires de l'espace. Mais comme nous nous limitons ici à une seule source de nourriture, le comportement des fourmis sera d'autant plus visible que la source sera éloignée.

parts = 250

x_source = rd.randint(0,8)
y_source = rd.randint(0,8)

def source(espace):
    
    """Creée une source de nourriture """
    
    espace[x_source, y_source] = parts
    for x in range(x_source-3, x_source+4):
        for y in range(y_source-3, y_source+4):
            if (x < dim) and (x >= 0):
                if (y < dim) and (y >= 0):
                    if espace[x,y] != parts:
                        espace[x,y] = 3
    return espace


### Génération de la fourmi dite "éclaireuse"

# A un endroit aléatoire à l'extérieur de la fourmilière, une fourmi éclaireuse apparaît et se dirige vers la source de nourriture.

# Dictionnaire des positions possibles à la sortie de la fourmilière:

dict_pos = {1: (dim-2,dim-1), 2: (dim-2,dim-2), 3: (dim-1,dim-2)}

def eclaireuse(espace):
    
    """Creée une fourmi """    
    
    x_ecl, y_ecl = dict_pos[rd.randint(1, 3)]
    espace[x_ecl,y_ecl] += 5
    return x_ecl, y_ecl

def proba_voisins(liste_voisins):

    """ Faite le déplacement de la fourmi """    
    
    this_proba = np.zeros(len(liste_voisins))
    for i in range(len(liste_voisins)):
        x, y = liste_voisins[i]
        this_proba[i] = (espace[x][y]+1)

    this_proba = np.exp(this_proba)
   
    this_proba = this_proba/np.sum(this_proba)

    return this_proba


def compt_voisins(i,j,set_visite):
    """ Cette fonction choisit une position aléatoire voisine à la fourmi située à la position (i,j) en créant une liste de
    probabilités associées à chaque position. Elle retourne les coordonnées de de la nouvelle position."""
    liste_voisins = []
    for k, l in neighbs:
        if (l + i >= 0 and l + i < dim and j + k >= 0 and k + j < dim): 
            if ((l+i,k+j) not in set_visite) and (espace[l+i][k+j] != -1):
                # Check if we're not outside boundaries of the array.
                liste_voisins.append([l+i,k+j])
    if liste_voisins == []:

        return (-1, -1)         
    
    this_proba = proba_voisins (liste_voisins)
    indice = np.random.choice (len(liste_voisins),p = this_proba)
    
    return liste_voisins[indice]


def dynamics_premier (nb):

    """Cette fonction genere l'environement et simule le deplacement de la premiere fourmi."""    
    
    fourmilière(espace)
    source(espace)
    dynamics(nb)
    
def dynamics(nb):
    """"Cette fonction simule le deplacement d'une fourmi. """    
    
    global espace
    espace_old = copy.copy(espace)
    
    x, y = eclaireuse(espace)
    set_visite = set()
    set_visite.add((x,y))
    
    for i in range(nb):
        x, y = compt_voisins(x,y, set_visite)
        if (x == -1 and y == -1) or (x == x_source and y == y_source) :
            if (x == x_source) and (y == y_source):
                espace[x][y] += 5
                return True

            else:

                espace = copy.copy (espace_old)
                return False
        else:
            espace[x][y] += 5
            set_visite.add((x,y))

    espace = copy.copy (espace_old)      
    return False
          
def plot_espace ():
    
    """Cette fonction dessine le graphe du chemin, il faut l'appeler à
    chaque fois qu'on veut voir le graphe. """    
    
    M = np.max(espace)
    norm = mcolors.Normalize(-1,M)
         
    # Defining a personalized color map.
    # M = blue
    # 0 = white
    # -1 = red
    
    cdict = {'red':   [(norm(-1), 1.0, 1.0),
                       (norm(0), 1.0, 1.0),
                       (norm(M), 0.0, 0.0)],
    
             'green': [(norm(-1), 0.0, 0.0),
                       (norm(0), 1.0, 1.0),
                       (norm(M), 0.0, 0.0)],
    
             'blue':  [(norm(-1), 0.0, 0.0),
                       (norm(0), 1.0, 1.0),
                       (norm(M), 1.0, 1.0)]}
                       
    cmap_custom = mcolors.LinearSegmentedColormap('CustomMap', cdict, N = M + 2)

    
    dpi = 20.0 
    figsize = (dim/float(dpi),dim/float(dpi))
    fig1 = plt.figure(figsize=figsize,facecolor = "white")
    ax1 = fig1.add_axes([0.0, 0.0, 1.0, 1.0], frameon = False)
    ax1.imshow(espace, interpolation = 'nearest', cmap = cmap_custom, norm = norm)
    ax1.set_xticks([]), ax1.set_yticks([])
    fig1.canvas.draw()    


def sim_1 (nb):
    
    """Cette fonction tourne jusqu'à ce que la première fourmi trouve la source de nourriture"""
    
    dynamics_premier (nb)    
    
    while not dynamics(nb):
        print("a",end = "")
        
def sim_renforce (nb):
    
    """ Elle génère à chaque itération (nb en tout) une fourmi qui va effectuer nb pas, en laissant une trace chimique
    que si elle trouve la source de nourriture""""
    
    for i in range(200):
        dynamics(nb)
     
#Il faut appeler d'abbord la fonction sim_1 avec nb le nombre d'iterations maximale pour 
#     qu'une fourmi trouve la nourriture, après appeler sim_renforce pour generer 200 fourmis
#     suplementaires et à la fin appeler plot_espace pour creer le graphe.