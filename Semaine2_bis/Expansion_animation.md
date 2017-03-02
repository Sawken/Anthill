# Animation de l'expansion d'une fourmilière


Le but de ce programme intermédiaire à notre projet est de simuler l'expansion d'une fourmilière, initialisée comme une matrice de taille ```dim*dim``` (```dim``` une variable globale) et totalement remplie de 0. La __reine__ est placée aléatoirement dans la matrice puis, à chaque itération (une itération correspondant à un jour), pond aléatoirement un nombre d'__oeufs__ compris entre 18 et 25.
Ces oeufs, arrivés à un certain âge, se transforment en __larves__, puis en __nymphes__ et enfin en __ouvrières__.
Dans ce programme, nous ferons la différenciation entre ces différents stades de vies en attribuant à chacun une couleur, qui variera en fonction du nombres de jour qu'a vécus une fourmi.
  * Entre 0 et 1 jours: espace vide (_blanc_)
  * Entre 1 et 15 jours: oeuf (_cyan_)
  * Entre 15 et 30 jours: larve (_vert_)
  * Entre 30 et 45 jours: nymphe (_jaune_)
  * Entre 45 et 180 jours: ouvrière (_orange_)
  * Plus de 180 jours: reine (_rouge_)

## Création de la fourmilière

La fourmilière est initialement une matrice de taille ```dim*dim```. Nous initialisons tous ses éléments à 0.
Nous choisissons ensuite aléatoirement les coordonnées de position de la reine grâce à la bibliothèque __random__, puis définissons une fonction __reine__, prenant en argument une matrice, qui permet de générer une reine à une position aléatoire dans la matrice. Nous lui attribuons la valeur 181 afin que lui soit attribuée la couleur rouge.

```Python
import random as rd
import numpy as np

dim = 30
fourmilière = np.zeros((dim,dim),"int32")

x_reine = rd.randint(0, dim-1)
y_reine = rd.randint(0, dim-1)

# Positionnement de la reine à un endroit aléatoire de la matrice. On lui attribue la valeur 181.

def reine(matrice):
    print("xreine =",x_reine)
    print("yreine =",y_reine)
    matrice[x_reine, y_reine] = 181
    return matrice
```

## Génération de fourmis

Nous allons maintenant écrire des fonctions qui nous serviront par la suite.

La première est celle qui permet de choisir de façon aléatoire le nombre d'oeufs pondus par la reine, compris entre 18 et 25 oeufs.

```Python
def naissance():
    return rd.randint(18, 25)
```

La deuxième fonction permet de générer ces oeufs dans la matrice de la fourmilière. On leur attribuera la valeur 1, puisqu'ils n'ont vécu qu'un jour. Nous ferons l'hypothèse que la reine voudra garder ses oeufs le plus près possible d'elle, et qu'ils se placeront en différentes couches autour d'elle.
Sachant que le nombre d'oeufs pondus varie entre 18 et 25, une première couche contiendra forcément 8 oeufs. Une deuxième couche peut contenir au plus 16 oeufs. Ainsi, les deux premières peuvent contenir ainsi au plus 24 oeufs. Dans le cas où l'on a 25 oeufs pondus, le 25e sera situé sur une troisième couche.

```Python
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
    
    # On enlève aux oeufs non-placés les 8 qui entourent la reine. La 2e couche autour de la reine peut contenir au plus 16 oeufs. Si elle est remplie alors il y aura 24 oeufs placés, sachant que la reine peut pondre au plus 25 oeufs.
    
    n = n-8
    # dictionnaire des positions que peuvent prendre les oeufs de la 2e couche.
    dict_pos = {1 : (x_reine-2, y_reine-2), 2: (x_reine-1, y_reine-2), 3: (x_reine, y_reine-2), 4: (x_reine+1, y_reine-2), 5: (x_reine+2, y_reine-2), 6: (x_reine+2, y_reine-1), 7: (x_reine+2, y_reine), 8: (x_reine+2, y_reine+1), 9: (x_reine+2, y_reine+2), 10: (x_reine+1, y_reine+2), 11: (x_reine, y_reine+2), 12: (x_reine-1, y_reine+2), 13: (x_reine-2, y_reine+2), 14: (x_reine-2, y_reine+1), 15: (x_reine-2, y_reine), 16: (x_reine-2, y_reine-1)}
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
```

Nous souhaitons obtenir une illustration de notre programme partiel. Nous faisons appel à la bibliothèque __matplotlib__ qui va nous permettre d'afficher une figure correspondant à notre matrice. A l'aide du module __colorbar__, nous fixons une échelle discrète de couleurs qui, plus tard, représenteront les différentes étapes de la vie d'une fourmi.

```Python
import matplotlib.pyplot as plt

# Affichage graphique de la matrice de la fourmilière. Nous fixons une échelle discrète de couleurs qui représenteront les différentes étapes de la vie d'une fourmi.

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
```

Voici, par exemple, une figure que nous avons obtenue avec les instructions suivantes:
```Python
dim = 25
show_matrice(fourmilière)
```
