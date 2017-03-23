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
    return espace
```


## Génération et déplacement de la fourmi dite "éclaireuse"

A un endroit aléatoire alentour de la fourmilière, une fourmi éclaireuse apparaît et se déplace dans l'espace jusqu'à atteindre la source de nourriture.

```Python

# Dictionnaire des positions possibles à la sortie de la fourmilière:

dict_pos = {1: (dim - 6, dim - 1), 2: (dim -6, dim -2), 3: (dim -6,dim -3), 4: (dim -6, dim -4),
5: (dim -6, dim -5), 6: (dim -6, dim -6), 7: (dim -5, dim -6), 8: (dim -4,dim  -6),
9: (dim -3, dim -6), 10: (dim -2,dim -6), 11: (dim -1,dim -6)}

def eclaireuse(espace):
    x_ecl, y_ecl = dict_pos[rd.randint(1, 11)]
    espace[x_ecl,y_ecl] += 1
    return x_ecl, y_ecl
```

Pour repérer la fourmi, nous ferons en sorte que chaque case par laquelle elle passe soit incrémentée de 1: il s'agit de la trace chimique, qui permettra à d'autres fourmi de suivre son chemin dans le futur. Plus la valeur de la case sera élevée, plus la probabilité que le chemin soit choisi sera grande.

Nous devons maintenant simuler le déplacement de l'éclaireuse. Nous dirons que la fourmi choisira de se placer à une certaine case de son voisinage, en fonction de la probabilité qui lui est associée. Afin de simuler l'attractivité de la trace chimique (qui sera renforcée au fil des itérations), nous décidons que plus la valeur associée à une case de voisinage est élevée, plus grande sera la probabilité que la fourmi choisisse de s'y placer. Cependant, pour éviter que la fourmi ne repasse toujour par le même chemin et soit attirée par sa propre trace chimique, nous créerons dans le même temps une liste de positions par lesquelles elle est déjà passée, et donc par lesquelles elle __ne pourra plus__ passer.

Pour cela, nous codons la fonction __proba_voisins__ qui prend en argument la liste __liste_voisins__ des positions déjà visitées par la fourmi. Elle retournera une liste __this_proba__des probabilités respectives associées à chacun des voisins de la fourmi.

```Python

def proba_voisins(liste_voisins):

    this_proba = np.zeros(len(liste_voisins))
    for i in range(len(liste_voisins)):
        x, y = liste_voisins[i]
        print (espace[x][y])
        this_proba[i] = (espace[x][y]+1)
    this_proba = this_proba/np.sum(this_proba)
    
    return this_proba
```

La fonction __compt_voisins__ paramètres les coordonnées de position d'une fourmi et choisit une position aléatoire voisine à la fourmi, en associant à chaque case voisine par laquelle elle peut passer (ie différente de -1) la probabilité qui lui correspond dans l liste __this_proba__, grâce à la méthode ```np.random.choice(liste1, liste2)```. La fonction retourne les coordonnées de la nouvelle position de la fourmi.

```Python

def compt_voisins(i,j,set_visite):
    
    liste_voisins = []
    for k, l in neighbs:
        if (l + i >= 0 and l + i < dim and j + k >= 0 and k + j < dim): 
        # Vérifie qu'on ne soit pas en-dehors de la matrice
            if ((l+i,k+j) not in set_visite) and (espace[l+i][k+j] != -1):
                # Assure que la position n'a pas encore été visitée, et que ce ne soit
                # pas la fourmilière
                liste_voisins.append([l+i,k+j])
                
    this_proba = proba_voisins (liste_voisins)
    indice = np.random.choice (len(liste_voisins),p = this_proba)
    
    return liste_voisins[indice]
```

Ecrivons maintenant une première fonction __dynamics(nb_d'itérations)__ qui simulera la création et le déplacement de l'éclaireuse.

```Python

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
```

Voici ce que l'on peut obtenir:

__Première itération__: Création de l'espace, la fourmilière (-1), la source de nourriture (17) et son entourage (3). L'éclaireuse est aussi générée (1)

<p align="center"><img src ="https://github.com/Sawken/Anthill/blob/master/Images/premiere_iteration.jpg?raw=true" alt="Première itération"/></p>

__Plus tard__:

<p align="center"><img src ="https://github.com/Sawken/Anthill/blob/master/Images/milieu.jpg?raw=true" alt="Plus tard"/></p>

__Encore plus tard__:

<p align="center"><img src ="https://github.com/Sawken/Anthill/blob/master/Images/fin.jpg?raw=true" alt="Encore plus tard"/></p>

## Bilan partiel

Notre début de code est fonctionnel, mais nous remarquons qu'arrivée à la source de nourriture, la fourmi continue de se déplacer. Il faudra donc que l'on fasse en sorte qu'une fois la source trouvée, la fourmi revienne d'elle-même vers la fourmilière.
