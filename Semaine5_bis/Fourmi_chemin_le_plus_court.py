
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


# On crée un espace représenté par une matrice de taille dim*dim. Attention cet espace n'est pas la fourmilière elle-même,
# mais bien l'environnement dans lequel elle se situe.


neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]

dim = 15

espace = np.zeros((dim,dim),"int32")

### Création de la fourmilière

# C'est facile, on fixera la fourmilière à une matrice de taille 5*5 remplie de -1, toujours située en bas à droite de l'environnement 
# créé.


def fourmilière(espace):
    for x in range(dim - 5, dim):
        for y in range(dim-5, dim):
            espace[x,y] = -1
    return espace


### Génération automatique d'une source de nourriture

# La source sera représentée dans la matrice par la valeur de la variable 'parts'. A chaque fois qu'une fourmi se sera nourrie, parts
# diminuera de 1, jusqu'à atteindre 0 (source de nourriture épuisée).
# Pour que la simulation soit intéressante, imposons pour ce premier essai que la source de nourriture se situe dans une case
# aléatoire de la zone supérieure gauche de l'espace. Bien sûr, dans des versions futures, nous pourrons générer des sources de nourriture à des endroits aléatoires de l'espace. Mais comme nous nous limitons ici à une seule source de nourriture, le comportement des fourmis sera d'autant plus visible que la source sera éloignée.

parts = 17

x_source = rd.randint(0,8)
y_source = rd.randint(0,8)

def source(espace):
    espace[x_source, y_source] = parts
    for x in range(x_source-3, x_source+4):
        for y in range(y_source-3, y_source+4):
            if (x < dim) and (x >= 0):
                if (y < dim) and (y >= 0):
                    if espace[x,y] != parts:
                        espace[x,y] = 3
    return espace



### Génération de la fourmi dite "éclaireuse"

# A un endroit aléatoire à l'extérieur de la fourmilière, une fourmi éclaireuse (-2) apparaît et se dirige vers la source de nourriture.

# Dictionnaire des positions possibles à la sortie de la fourmilière:

dict_pos = {1: (dim - 6, dim - 1), 2: (dim -6, dim -2), 3: (dim -6,dim -3), 4: (dim -6, dim -4), 5: (dim -6, dim -5), 
            6: (dim -6, dim -6), 7: (dim -5, dim -6), 8: (dim -4,dim  -6), 9: (dim -3, dim -6), 10: (dim -2,dim -6), 
            11: (dim -1,dim -6)}



def eclaireuse(espace):
    x_ecl, y_ecl = dict_pos[rd.randint(1, 11)]
    espace[x_ecl,y_ecl] += 1
    return x_ecl, y_ecl

""" Déplacement de la fourmi """

def proba_voisins(liste_voisins):
    this_proba = np.zeros(len(liste_voisins))
    print (this_proba)
    for i in range(len(liste_voisins)):
        x, y = liste_voisins[i]
        print (espace[x][y])
        this_proba[i] = (espace[x][y]+1)
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
                
    this_proba = proba_voisins (liste_voisins)
    indice = np.random.choice (len(liste_voisins),p = this_proba)
    
    return liste_voisins[indice]

     
def dynamics(nb):
    fourmilière(espace)
    source(espace)
    x, y = eclaireuse(espace)
    set_visite = set()
    set_visite.add((x,y))
    print(espace)
    for i in range(nb):
        x, y = compt_voisins(x,y, set_visite)
        espace[x][y] += 1
        set_visite.add((x,y))
        print(espace)
        if x == x_source and y == y_source :
            print("trouve")
