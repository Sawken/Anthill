# -*- coding: utf-8 -*-

"""
Created on Wed Mar 01 19:57:12 2017

@author: Cécile
"""

import matplotlib.pyplot as plt
from matplotlib import mpl
import matplotlib.animation as animation
import numpy as np
import random as rd
from time import sleep


""" Le but de ce programme intermédiaire à notre projet est de simuler l'expansion d'une fourmilière, initialisée comme une matrice de 
taille dim*dim, totalement remplie de 0. La reine est placée aléatoirement dans la matrice puis, à chaque itération (correspondant aux 
jours), pond aléatoirement un nombre d'oeufs compris entre 18 et 25.
Ces oeufs, arrivés à un certain âge, se transforment en larve, puis en nymphe et enfin en ouvrière.
Dans le programme, nous ferons la différenciation de ces différents stades de vie en leur attribuant une couleur, correspondant au 
nombre de jours vécus."""

### Création de la fourmilière


# La fourmilière est initialement une matrice dim*dim. On initilise tous ses éléments à 0.
dim = 30
fourmilière = np.zeros((dim,dim),"int32")

# Position aléatoire de la reine.
x_reine = rd.randint(0, dim-1)
y_reine = rd.randint(0, dim-1)

# Positionnement de la reine à un endroit aléatoire de la matrice. On lui attribue la valeur 181.
def reine(matrice):
    print("xreine =",x_reine)
    print("yreine =",y_reine)
    matrice[x_reine, y_reine] = 181
    return matrice


### Génération automatique de nouvelles fourmis

def naissance():
    return rd.randint(18, 25)
    #la reine pond entre 18 et 25 oeufs par jour.

def oeufs(matrice):
    n = naissance()
    print(n)
    # On part de l'hypothèse que la reine veut garder aussi près d'elle que possible ses oeufs
    # Sachant qu'elle peut garder au plus proche d'elle 8 oeufs:
    matrice[x_reine-1, y_reine-1] = 1
    matrice[x_reine, y_reine-1] = 1
    matrice[x_reine+1, y_reine-1] = 1
    matrice[x_reine+1, y_reine] = 1
    matrice[x_reine+1, y_reine+1] = 1
    matrice[x_reine, y_reine+1] = 1
    matrice[x_reine-1, y_reine+1] = 1
    matrice[x_reine-1, y_reine] = 1
    # On enlève aux oeufs non-placés les 8 qui entourent la reine. La 2e couche autour de la reine peut contenir au plus 16 oeufs.
    # Si elle est remplie alors il y aura 24 oeufs placés, sachant que la reine peut pondre au plus 25 oeufs.
    n = n-8
    # dictionnaire des positions que peuvent prendre les oeufs de la 2e couche.
    dict_pos = {1 : (x_reine-2, y_reine-2), 2: (x_reine-1, y_reine-2), 3: (x_reine, y_reine-2), 4: (x_reine+1, y_reine-2),
                5: (x_reine+2, y_reine-2), 6: (x_reine+2, y_reine-1), 7: (x_reine+2, y_reine), 8: (x_reine+2, y_reine+1),
                9: (x_reine+2, y_reine+2), 10: (x_reine+1, y_reine+2), 11: (x_reine, y_reine+2), 12: (x_reine-1, y_reine+2),
                13: (x_reine-2, y_reine+2), 14: (x_reine-2, y_reine+1), 15: (x_reine-2, y_reine), 16: (x_reine-2, y_reine-1)}
    if n <= 16:
        L = []
        while len(L) < n:
            r = rd.randint(1,16)
            if r not in L:
                x, y = dict_pos[r]
                matrice[x,y] = 1
                L.append(r)
    else:
        L = []
        while len(L) < n-1:
            r = rd.randint(1,16)
            if r not in L:
                x, y = dict_pos[r]
                matrice[x,y] = 1
                L.append(r)
        matrice[x_reine + rd.randint(-3,3), y_reine + rd.randint(-3,3)] = 1
    return matrice
    
    
def evolution(matrice):
    for x in range(dim-1):
        for y in range(dim-1):
            if matrice[x,y] != 0 and matrice[x,y] < 180:
                matrice[x,y] +=1
                x1 = x
                y1 = y
                while matrice[x1,y1] != 0:
                    x1 = x + rd.randint(-1,1)
                    y1 = y +rd.randint(-1,1)
                matrice[x1,y1] = matrice[x,y]
                matrice[x,y] = 0
            if matrice[x,y] == 180:
                matrice[x,y] = 0
    return matrice

# Affichage graphique de la matrice. Cette fois-ci nous fixons nous même une échelle discrète de couleurs qui, plus tard,
# représenteront les différentes étapes de la vie d'une fourmi.

cmap = mpl.colors.ListedColormap(['white','cyan','green','yellow','orange','red'])
bounds=[0,1,15,30,45,180,181]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

def show_matrice(matrice):
    plt.ion()
    reine(matrice)
    oeufs(matrice)
    im1 = plt.matshow(matrice,interpolation='nearest', cmap = cmap,norm=norm)
    plt.colorbar(im1,cmap=cmap, norm=norm,boundaries=bounds,ticks=[0,1,15,30,45,180,181])
    plt.grid()
    plt.show()

    
## Evolution de la population de fourmi: fonctions d'itération et d'affichage graphique
    
def evolution(matrice):
    for x in range(dim-1):
        for y in range(dim-1):
            # s'il y a bien une fourmi à la position (x,y) et que
            # celle-ci n'est pas la reine, elle se déplace aléatoirement
            # vers une case qui n'est pas occupée.
            if matrice[x,y] != 0 and matrice[x,y] < 180:
                matrice[x,y] +=1
                x1 = x
                y1 = y
                while matrice[x1,y1] != 0:
                    x1 = x + rd.randint(-1,1)
                    y1 = y +rd.randint(-1,1)
                matrice[x1,y1] = matrice[x,y]
                matrice[x,y] = 0
            # si la fourmi est vieille de 180 jours, elle meurt.
            if matrice[x,y] == 180:
                matrice[x,y] = 0
    return matrice
  
  
def iterate(matrice):
    oeufs(matrice)
    evolution(matrice)
    return matrice

def update(matrice):
    iterate(matrice)
    im1.set_array(matrice)
    return im1

  
plt.ion()
nb_images = 300
fourmilière = np.zeros((dim,dim),"int32")
show_matrice(fourmilière)
im1 = plt.matshow(fourmilière,interpolation='nearest', cmap = cmap,norm=norm)
plt.colorbar(im1,cmap=cmap, norm=norm,boundaries=bounds,ticks=[0,1,15,30,45,180,181])


for k in np.arange(nb_images):
    update(fourmilière)
    plt.draw()
    sleep(0.1)
