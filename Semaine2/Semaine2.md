# Anthill

# Création de la fourmilière

Nous avons cette semaine travaillé sur la mise en place de la fourmilière. Tout d'abord, nous avons créé une matrice remplie de 1 dont la taille est fixée par la variable globale ```python size_map```. Cette matrice représente un espace arbitraire faisant office d'environnement de vie pour les fourmis.

```python
import numpy as np

size_map = 10
yx_map = (10, 10)
map = np.ones(yx_map)
neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]
```

Dans un second temps, nous avons créé une fonction générant une reine placée aléatoirement sur la matrice. Cette reine est représentée par l'entier '2'. Nous avons automatiquement créé un espace autour d'elle rempli de 0, qui représentent des espaces vides dans lesquelles les fourmis pourront se déplacer.

``` python
import random as rd

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
```

Voici ci-dessous le résultat obtenu en exécutant la fonction set_queen avec la valeur de 
```python
size_map = 10
```

<p align="center"><img src ="https://github.com/Sawken/Anthill/blob/master/Images/matrice_1.png?raw=true" alt="matrice with the queen"/></p>

Nous avons fait face à une contrainte au moment où la reine se retrouvait au bord de la map car python gère les arrays de manière circulaire (comme un donut lol), nous avons donc géré ça en vérifiant la position relative autour de celle-ci à l'aide de la variable global
```python
neighbs = [(-1, -1), (-1, 0), (-1, 1),
           ( 0, -1),          ( 0, 1),
           ( 1, -1), ( 1, 0), ( 1, 1)]
           ```
Ci-dessous un exemple où la reine est dans un angle

<p align="center"><img src ="https://github.com/Sawken/Anthill/blob/master/Images/matrice_2.png?raw=true" alt="matrice with the queen in angle"/></p>
