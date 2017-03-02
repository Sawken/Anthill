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
