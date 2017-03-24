# Semaine 5

# Amélioration du code

Cette semaine nous nous sommes concentrés sur des changements sur les fonctions __croissance_tun__ et __decroissance_tun__ afin de raffiner notre simulation pour qu'elle soit plus proche de la realité. Nous voulons notamment que la densité de tunnels soit plus petite et que la forme ne soit aussi circulaire que celle du résultat obtenu la semaine dernière.

## Croissance

Pour diminuer la densité de tunnels nous avons d'abord essayé l'idée evoquée precédement de faire dépendre la probabilité de creation de tunnels aussi de la distance de la reine. Pour cela nous avons changé la fonction __proba_tun__ afin de considerer 2 proportions maximales de voisins differentes, selon la distance de la reine. Si la distance d'un tunnel à la reine est plus petite que 15, la proportion reste la même (0.4), sinon elle baisse à 0.2. Comme cela nous attendions que la situation de blocage serait évité tout en diminuant la densité de tunnels. 

Voici un figure d'un résultat typique de la simulation avec ces changements:

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_visinhanca_4.png?raw=true" alt="Simmulation foumilière 2">
</p>

Nous pouvons voir que ce changement n'a pas été suffisant car la proportion de 0.2 rend la croissance presque impossible en dehors de la boule de rayon 15 centrée dans la reine. 

En outre, nous avons essayer quel effect aurait une augmentation de la taille du voisinage prise en compte pour décider si un nouveau tunnel sera crée ou non.  
