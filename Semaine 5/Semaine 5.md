# Semaine 5

# Amélioration du code

Cette semaine nous nous sommes concentrés sur des changements sur les fonctions __croissance_tun__ et __decroissance_tun__ afin de raffiner notre simulation pour qu'elle soit plus proche de la realité. Nous voulons notamment que la densité de tunnels soit plus petite et que la forme ne soit aussi circulaire que celle du résultat obtenu la semaine dernière.

## Croissance

Pour diminuer la densité de tunnels nous avons d'abord essayé l'idée evoquée precédement de faire dépendre la probabilité de creation de tunnels aussi de la distance de la reine. Pour cela nous avons changé la fonction __proba_tun__ afin de considerer 2 proportions maximales de voisins differentes, selon la distance de la reine. Si la distance d'un tunnel à la reine est plus petite que 15, la proportion reste la même (0.4), sinon elle baisse à 0.2. Comme cela nous attendions que la situation de blocage serait évité tout en diminuant la densité de tunnels. 

Voici un figure d'un résultat typique de la simulation avec ces changements:

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_visinhanca_4.png?raw=true" alt="Simulation foumilière 2">
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

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_visinhanca_3.png?raw=true" alt="Simulation foumilière 3">
</p>

La simulation est beaucoup plus proche de la realité avec de tunnels plus longs, mais elle reste plutôt circulaire avec 2 cercles bien définis. Le cercle plus petit provient de la partie avec la densité plus grande, ce qui est bien visible. Cette figure laisse l'impression que le modèle est déjà assez proche d'un générateur de fourmilière raisonnable. Pour le raffiner, nous avons fait plusieurs essais et sommes enfin abouti à la fonction suivante:

```python
        
def proba_tun (i, j, rayon):
    """
    Computes the probability of digging a new tunnel from the position (i, j) taking
    in account the proportion of neighbours that are already dig. If more than
    0.4 of neighbors are already tunnels, the function return zero (so, no more
    tunnels are made based in this position). Otherwise, the probability of digging 
    a tunnel is set to be under the form f(x) = a * (x - 1/2) ** 2, with "a" 
    chosen in order to have f(1/8) = 1/2. This way we use only half of a parabole.
    """
    
    t = voisinage_zero (i, j, voisinage_exte)
    dist = map_dist [i][j]
    if dist < 15 and t < 0.4 and dist > 0.50 * rayon:
        return (32/9) * (t - 1/2) ** 2
    if t < 0.2 and dist > 0.50 * rayon:
        # This way we increase the chance for a tunnel to be created far from the queen.
        return (32/9) * (t - 1/2) ** 2
    return 0
```

La fonction prend maintenant aussi la distance du tunnel le plus eloigné de la reine comme argument et utilisé ce nombre pour privilegier la croissance de tunnels loins de la reine. La simulation avec cette fonction a fait disparaître le cercle autour de la reine et a une allure plus naturelle, comme on peut voir sur la figure ci-après:

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_circular2.png?raw=true" alt="Simulation foumilière 3">
</p>

Par contre, on peut voir clairement le contour d'un cercle englobant la fourmilière, que nous croyons provenir de la façon déterministe
de destruction des tunnels. Nous alons donc modifier la fonction __decroissance_tun__.

## Décroissance

Nou voulons modifier la fonction __decroissance_tun__ pour qu'elle ne choisisse plus les __quant_tun__ tunnels plus éloignés mais qu'il y ait un facteur aléatoire dans la destruction. Pour cela, nous avons décidé de créer deux vecteurs, __list_zero_dist__ et __list_zero_pos__, comme dans la version précédente mais au lieu de les effacer tous, nous en choisissons un au hasard et nous détruisons le plus petit carré autour de lui contenant au moins __quant_tun__ tunnels. Voici le code de cette nouvelle version de la fonction et une image d'une simulation typique:

```python
def decroissance_tun (quant_tun) :
    """
    This function computes all the possible destruction of tunnels in 1 round and
    applies it.
    """
    map_old = copy.copy (map)
    #We use a copy of map to decide if a tunnel is destroyed so it doesnt influenciates the rest of the destruction cicle.
    list_zero_dist = np.zeros(quant_tun,dtype = "float32")
    # This is an array with the distances of a quantity "quant_tun" of zeros to the queen were in the end we will have the "quant_tun" farthest zeros.
    list_zero_pos = np.zeros((quant_tun,2),dtype = "int16")
    # This array stocks the coordinates of each zero that is in list_zero_dist.
    for i in range(size_map):
       for j in range(size_map):
           if (map_old[i][j] == 0) and map_dist[i][j] > 1.5 :
           # The 1.5 distance prevents the destruction of tunnels that are direct neighbors to the queen.
               k = 0
               while (k < quant_tun) and (list_zero_dist[k] > map_dist[i][j]):
                   k += 1
               # Test to see why it got out of the loop.
               if k < quant_tun:
                   # Displaces each element of both arrays of one position.
                   list_zero_dist[k + 1 : ] = list_zero_dist[k : quant_tun - 1]
                   list_zero_pos[k + 1 : ][ : ] =  list_zero_pos [k : quant_tun - 1][ : ]
                   # Puts the new zero, that is further to the queen, in both arrays.
                   list_zero_dist[k] = map_dist[i][j]
                   list_zero_pos[k][ : ] = [i, j] 
                   
    quant_final = quant_tun               
    destruct = np.random.choice(quant_tun)
    x, y = list_zero_pos[destruct][0], list_zero_pos[destruct][1]
    side = 1
    quant_0 = quant_zeros()
    while quant_final > 0 and quant_0 > 8 :
        for k in range(-side, side + 1):
            for l in range(-side, side + 1):
                if (k + x >= 0 and k + x < size_map and l + y >= 0 and l + y < size_map): 
                    if map[k + x][l + y] == 0 and map_dist [k + x][l + y] > 1.5:
                        quant_final -= 1 
                        map[k + x][ l + y] = 1
                        quant_0 -= 1
            side += 1
```    
<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_circular3.png?raw=true" alt="Simulation foumilière 3">
</p>

L'image est beaucoup plus satisfaisante mais présente encore un problème: Les tunnels continuent à croître même lorsqu'ils ne sont plus connectés à la reine! Pour le remedier nous avons fait le choix de, à la fin de la fonction __decroissance_tun__, détruire aussi les tunnels qui ne sont pas connectés à la reine.

Pour ce faire nous devrons donc être capables d'identifier les tunnels connectés à la reine. Nous avons cherché sur internet pour des idées et nous avons trouvé que cela est un problème classique en théorie de graphes, celui de chercher la composant connexe contenant un point specifique. Nous avons donc implementé une fonction appelée __connexe__ qui nous permet de calculer l'ensemble de tunnels reliés à la reine.

Cette fonction prend deux arguments (les coordonnées d'un point) et utilise une variable globale __set_connexe__, une ensemble qui doit être vide avant l'appel de la fonction et qui contiendra à la fin l'ensemble de points connectés au point donné en argument. Son implementation est faite par recurrence: étant donné un point, on vérifie parmi tous ses voisins lequels sont de tunnels et qui ne sont pas encore dans __set_connexe__. Dans ce cas, nous l'ajoutons à __set_connexe__ et nous appelons la fonction __connexe__ encore une fois avec les coordonnées de ce voisin. Le code est donné ci-dessous:

```python
def connexe (i,j):
    """
    """    
    
    for k, l in neighbs:
         if (k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
             if map [k + i][l + j] == 0 and (k + i, j + l) not in set_connexe:
                 set_connexe.add((k + i, j + l))
                 connexe (k + i, j + l)
                 
```
 Malgré le fait que l'appel recurrent à la fonction n'est pas très efficace, nous n'observons pas dans notre simulation d'augmentation significative du temps de calcul.
 
 Nous appelerons cette fonction dans __decroissance_tun__ après la destruction des tunnels. Une fois cet ensemble rempli, la fonction __decroissance_tun__ parcourt la matrice __map__ en effaçant tout les tunnels qui n'apparaissent pas dans cet ensemble. Le code final de la fonction __decroissance_tun__ est le suivant:
 
 ```python
 def decroissance_tun (quant_tun) :
    """
    This function computes all the possible destruction of tunnels in 1 round and
    applies it.
    """
    
    global set_connexe    
    
    map_old = copy.copy (map)
    #We use a copy of map to decide if a tunnel is destroyed so it doesnt influenciates the rest of the destruction cicle.
    list_zero_dist = np.zeros(quant_tun,dtype = "float32")
    # This is an array with the distances of a quantity "quant_tun" of zeros to the queen were in the end we will have the "quant_tun" farthest zeros.
    list_zero_pos = np.zeros((quant_tun,2),dtype = "int16")
    # This array stocks the coordinates of each zero that is in list_zero_dist.
    for i in range(size_map):
       for j in range(size_map):
           if (map_old[i][j] == 0) and map_dist[i][j] > 1.5 :
           # The 1.5 distance prevents the destruction of tunnels that are direct neighbors to the queen.
               k = 0
               while (k < quant_tun) and (list_zero_dist[k] > map_dist[i][j]):
                   k += 1
               # Test to see why it got out of the loop.
               if k < quant_tun:
                   # Displaces each element of both arrays of one position.
                   list_zero_dist[k + 1 : ] = list_zero_dist[k : quant_tun - 1]
                   list_zero_pos[k + 1 : ][ : ] =  list_zero_pos [k : quant_tun - 1][ : ]
                   # Puts the new zero, that is further to the queen, in both arrays.
                   list_zero_dist[k] = map_dist[i][j]
                   list_zero_pos[k][ : ] = [i, j] 
                   
    quant_final = quant_tun               
    destruct = np.random.choice(quant_tun)
    x, y = list_zero_pos[destruct][0], list_zero_pos[destruct][1]
    side = 1
    quant_0 = quant_zeros()
    while quant_final > 0 and quant_0 > 8 :
        for k in range(-side, side + 1):
            for l in range(-side, side + 1):
                if (k + x >= 0 and k + x < size_map and l + y >= 0 and l + y < size_map): 
                    if map[k + x][l + y] == 0 and map_dist [k + x][l + y] > 1.5:
                        quant_final -= 1 
                        map[k + x][ l + y] = 1
                        quant_0 -= 1
            side += 1
    set_connexe = set ()
    connexe (pos_reine_i, pos_reine_j)
    for i in range(size_map):
       for j in range(size_map):
           if (map[i][j] == 0) and (i,j) not in set_connexe:
               map[i][j] = 1    
```
Le résultat de tout ces changements est bien vu dans les figures suivantes:

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas4.png?raw=true" alt="Simulation foumilière 3">
</p>

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas3.png?raw=true" alt="Simulation foumilière 3">
</p>

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas7.png?raw=true" alt="Simulation foumilière 3">
</p>


