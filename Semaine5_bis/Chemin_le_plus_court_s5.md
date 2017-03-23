# Semaine 5 bis

# Chemin le plus court

Une fourmi dite __éclaireuse__, qui découvre une source de nourriture, rentre dans sa colonie en laissant sur son passage une trace chimique. Cette trace stimule d'autres fourmis ouvrières, les attirant à l'extérieur de la colonie afin de la suivre et de retrouver à leur tour la source de nourriture. Elles rentrent ensuite chez elles, laissant sur leur passage une trace chimique renforçant la précédente, et le même processus se reproduit.

D'après Jean-Louis Deneubourg, on estime qu'un individu (l'éclaireuse) attire un nombre _n_ de congénères, qui attirent eux-mêmes _n_ congénères et ainsi de suite. On comprend ainsi que les individus ayant emprunté le chemin le plus court rentreront chez eux le plus tôt et attireront ainsi plus rapidement les autres fourmis ouvrières (la trace chimique se renforçant plus rapidement).

<p align="center"><img src ="https://github.com/Sawken/Anthill/blob/master/Images/Fourmi_chemin_le_plus_court.png?raw=true" alt="Picture illustrating ants choosing the shortest way to food"/></p>

Le but de ce programme sera de simuler le comportement des fourmis afin de trouver le chemin le plus court pour accéder à une source de nourriture.


## Création de l'environnement de vie des fourmis

Nous créons un espace représentant l'environnement où évolueront nos fourmis. Cet espace n'est pas la fourmilière elle-même mais bien l'environnement dans lequel elle se situe. Cet espace sera représenté par une matrice de taille ```dim * dim```, pour l'instant remplie de zéros (_espace vide_).
La liste de tuplets __neighbs__ nous sera très utile par la suite: il s'agit de la liste des positions voisines possibles d'un élément de la matrice.

```Python

import numpy as np
import random as rd

neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]

dim = 15

espace = np.zeros((dim,dim),"int32")
```

Nous créons ensuite la fourmilière, fixée par une matrice de taille 5 * 5 remplie de -1. Pour plus de clarté et pour simplifier notre programme, nous choisirons de toujours placer la fourmilière en bas à droite de la matrice __espace__.

```Python

def fourmilière(espace):
    for x in range(dim - 5, dim):
        for y in range(dim-5, dim):
            espace[x,y] = -1
    return espace
```


## Génération automatique d'une source de nourriture

La source sera représentée dans la matrice par la valeur de la variable __parts__. A chaque fois qu'une fourmi se sera nourrie, parts diminuera de 1, jusqu'à atteindre 0 (source de nourriture épuisée).
Pour que la simulation soit intéressante, imposons pour ce premier essai que la source de nourriture se situe dans une case aléatoire de la zone supérieure gauche de l'espace. Bien sûr, dans des versions futures, nous pourrons générer des sources de nourriture à des endroits aléatoires de l'espace. Mais comme nous nous limitons ici à une seule source de nourriture, le comportement des fourmis sera d'autant plus visible que la source sera éloignée.

Nous avons testé plusieurs versions de cette fonction, mais nous nous trouvions à chaque fois devant le même problème: la fourmi éclaireuse se déplaçant 'aléatoirement' dans l'espace n'aura que très peu de chance de réellement croiser la source de nourriture (à moins bien sûr que nous itérions de très nombreuses fois). Pour remédier à cela, nous décidons de créer autour de la source de nourriture un espace rempli de phéromones marquées 3, qui signaleront aux fourmis la proximité d'une source de nourriture et les attireront.

```Python

parts = 17

# Tirage aléatoire des coordonnées de la source de nourriture. On imposera qu'elle suite forcément dans le coin
# supérieur gauche de la matrice espace.

x_source = rd.randint(0,8)
y_source = rd.randint(0,8)

def source(espace):
    espace[x_source, y_source] = parts
    # Création du voisinage de la source de nourriture
    for x in range(x_source-3, x_source+4):
        for y in range(y_source-3, y_source+4):
            if (x < dim) and (x >= 0):
                if (y < dim) and (y >= 0):
                    if espace[x,y] != parts:
                        espace[x,y] = 3
    return 
```
