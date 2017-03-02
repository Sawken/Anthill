# Animation de l'expansion d'une fourmilière


Le but de ce programme intermédiaire à notre projet est de simuler l'expansion d'une fourmilière, initialisée comme une matrice de taille ```dim*dim``` (```dim``` une variable globale) et totalement remplie de 0. La reine est placée aléatoirement dans la matrice puis, à chaque itération (une itération correspondant à un jour), pond aléatoirement un nombre d'oeufs compris entre 18 et 25.
Ces oeufs, arrivés à un certain âge, se transforment en larves, puis en nymphes et enfin en ouvrières.
Dans ce programme, nous ferons la différenciation entre ces différents stades de vies en attribuant à chacun une couleur, qui variera en fonction du nombres de jour qu'a vécus une fourmi.


## Création de la fourmilière

La fourmilière est initialement une matrice de taille ```dim*dim```. On initialise tous ses éléments à 0.
On choisi ensuite aléatoirement les coordonnées de position de la reine grâce à la bibliothèque __random__
