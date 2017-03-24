# Semaine 5

# Amélioration du code

Cette semaine nous nous sommes concentrés sur des changements sur les fonctions __croissance_tun__ et __decroissance_tun__ afin de raffiner notre simulation pour qu'elle soit plus proche de la realité. Nous voulons notamment que la densité de tunnels soit plus petite et que la forme ne soit aussi circulaire que celle du résultat obtenu la semaine dernière.

## Croissance

Pour diminuer la densité de tunnels nous avons d'abord essayé l'idée evoquée precédement de faire dépendre la probabilité de creation de tunnels aussi de la distance de la reine. Pour cela nous avons changé la fonction __proba_tun__ afin de considerer 2 proportions maximales de voisins differentes, selon la distance de la reine. Si la distance d'un tunnel à la reine est plus petite que 15, la proportion reste la même (0.4), sinon elle baisse à 0.2. Comme cela nous attendions que la situation de blocage serait évité tout en diminuant la densité de tunnels. 

Voici un figure d'un résultat typique de la simulation avec ces changements:

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_visinhanca_4.png?raw=true" alt="Simmulation foumilière 2">
</p>

Nous pouvons voir que ce changement n'a pas été suffisant car la proportion de 0.2 rend la croissance presque impossible en dehors de la boule de rayon 15 centrée dans la reine. Pour corriger cela nous avons décidé de changer un autre paramètre du système, la taille du voisinage autour duquel on regarde pour calculer la proportion de tunnels voisins. En effet, à proximité des extremités de la fourmilière il y a beaucoup d'espaces vides ce qui nous fait penser que ce changement favoriserait une croissance vers l'exterieur, tout en gardant moins de densité. Nous avons crée une variable globale appelée __voisinage_exte__, fixée dans un premier momment à 4, et changé le code de la fonction __voisinage_zero__ pour qu'elle prenne cette variable comme argument. 

```python
def voisinage_zero (i, j, exte):
    """ 
    Computes the proportion of zeros in the extended neighborhood of a element with
    coordinates (i, j) in the array map.
    """    
    
    cpt_0 = 0
    cpt_total = 0
    for k in range(-exte,exte + 1):
        for l in range(-exte, exte + 1):
           if (not (k == 0 and  l == 0) and k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
               cpt_total = cpt_total + 1
               if map[i + k, j + l] == 0:
                   cpt_0 = cpt_0 + 1
        
    return float(cpt_0/cpt_total)
 ```
Voici une simulation avec ce changement:

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_visinhanca_3.png?raw=true" alt="Simmulation foumilière 3">
</p>
En outre, nous avons essayer quel effect aurait une augmentation de la taille du voisinage prise en compte pour décider si un nouveau tunnel sera crée ou non.  
