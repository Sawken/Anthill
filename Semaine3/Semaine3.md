# Semaine 3


# Création des tunnels


   Pour créer des tunnels nous avons d'abord crée une nouvelle matrice de même taille que notre matrice map:
```python
map_dist = np.zeros ((size_map,size_map), dtype = "float16")
```
  Cette matrice est initialisé avec que des zéros et après, dans la fonction set_queen(), elle est remplie avec les distances euclidiennes de chaque élément par rapport a la reine, c'est à dire, avec les positions relatives de chaque élément de la matrice map à la reine. La matrice map_dist doit être rempli après la géneration de la reine car celle-ci est mise en place dans map de façon aléatoire. Nous voulons utiliser cette matrice pour choisir dans quel endroit creuser un tunnel.
  
  Voir ci-dessous le nouveau code de la fonction set_queen():
  
  ```python
  def set_queen():
    """
    set the queen randomly in the map
    """

    global neighbs
    
    queen = (rd.randint(0, size_map - 1), rd.randint(0, size_map - 1))
    y, x = queen
    map[y][x] = 2
    for k, l in neighbs:
        # Check if we're not outside boundaries.
        if (k + x >= 0 and k + x < size_map and y + l >= 0 and l + y < size_map): 
            map[l + y][k + x] = 0
    #initilize a map with distances to the queen.
    for i in range(size_map):
        for j in range(size_map):
            map_dist[i][j] = np.sqrt((i - y)**2 + (j - x)**2)
    
    
    print(map)
    print (display_map())
```

   Ensuite, nous avons crée la variable globale proba_tun, set à 0.1, que donne la probabilité de creuser un nouveau tunnel. Dans un deuxième temps nous alons écrire une fonction pour calculer cette probabilité de façon dynamique.

   Nous passons a l'écriture d'une fonction croissance. Dans un premier temps la fonction parcourt chaque case de la matrice map et regarde si l'élément est un zéro ou non. S'il s'agit d'un zéro, nous comparons un chiffre géneré aléatoirement avec la variable proba_tun. Le fourmilière grandira d'une case si le chiffre est plus petit.
   
   Après avoir décidé si un zéro cause la croissance du fourmilière ou non, nous alons choisir quel de ces voisins sera transformé en zéro. Pour cela, nous créons des fonctions auxiliaires pour que la fonction croissance ne devient pas très long
   et difficile à comprendre. 
   
   La première fonction que nous avons crée c'est la fonction dig_tunnel qui prend comme arguments des coordonnées (i, j) d'un élément de la matrice. Elle crée une liste de tuples avec les voisins existants et ces distances relatifs à la reine. Pour calculer les differentes probabilités d'être choisi pour chacun de ces élements, nous créons un autre fonction appellé proba_direction, qui prend comme argument cette liste de tuples creé par la fonction précedent appellée __this_neighbs__. 
   
   La foction proba_direction calcule un liste de probabilités d'être choisi par rapport a la distance des éléments à la reine de façon lineaire, avec la probabilité de choisir l'élément plus loin 100 fois plus petit que celle de choisir le plus proche. Cela correspond à prend les probabilités proportionnelles à __f(d) = a * d + b__, avec __d__ la distance par rapport à la reine et __a__ et __b__ choisi de façon à donner __f(dmin) = 1 and f(dmax) = 100__. __Dmin__ est le plus petit distance presente en __this_neighbs__ et dmax la plus grande.
   
   Voici ci-dessus le code des 3 fonctions (avec des comentaires en anglais):
   
```python   
def croissance ():
    
    map_old = copy.copy (map)
    
    for i in range(size_map):
        for j in range(size_map):
            if map_old[i][j] == 0:
                if rd.random() < proba_tun:
                    pos_tun = dig_tunnel(i,j)
                    if map[pos_tun] == 1: 
                        map[pos_tun] = 0
                    
                    
   
def dig_tunnel (i, j):
    """
    This function chooses a random position to dig among the neighbors of a zero 
    in the position (i,j) of the matrix. For that, it first creates a list of tuples
    with the existing neighbors and their distances to the queen. The probabilities 
    for each of those elements to be chosen are computed by the function proba_direction.
    The function returns the position of the cell to be dig chosen randomly according
    to those probabilities.

    """
    this_neighbs = []
    for k, l in neighbs:
        if (k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
            this_neighbs.append((map_dist[i+k][j+l], i+k, j+l))
    this_neighbs.sort (key = lambda neighb : neighb[0])
    this_proba = proba_direction (this_neighbs)
    dig_indice = np.random.choice (len(this_neighbs),p = this_proba)
    
    return (this_neighbs[dig_indice][1],this_neighbs[dig_indice][2])

    

def proba_direction (this_neighbs):
    """
    This function computes a list of probabilities of choosing one of the neighbors
    of a zero (that has already been selected to dig a tunnel), as a function of 
    the distance of each of those neighbors to the queen.
    this_neighbs is a list of tuples, each element containing the distance to 
    the queen and the absolute position in the matrix ordered in terms of distance.
    We choose to compute the probability in a linear fashion, where the probability
    of choosing the furthest element to the queen is 1 hundred times higher than choosing
    the nearest one. 
    This corresponds to picking the probabilities proportional to f(d) = a*d + b,
    where d is the distance to the queen and a and b are chosen in such a way that 
    f(dmin) = 1 and f(dmax) = 100. Dmin is the smallest distance present in this_neighbs
    and dmax is the biggest.
    """
    dmin = this_neighbs[0][0]
    dmax = this_neighbs[-1][0]
    this_proba = np.zeros(len(this_neighbs))
    a = 99 / (dmax - dmin)
    b = 1 - a * dmin
    
    for i in range(len(this_neighbs)):
        this_proba[i] = (a * this_neighbs[i][0] + b)
        
    this_proba = this_proba/np.sum(this_proba)
    
    return this_proba
```
 En iterant 50 fois la fonction __croissance__, nous obtenons la figure suivante:

<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/matrice_tunnel_fail.png?raw=true" alt="Matrice tunnel 1">
</p>

   Comme on peut le voir, les tunnels (representé par des zeros en bleu) ne sont pas de vrais tunnels et en fait la fonction a crée un cercle de zéros autour de la reine, ce qui ne pas le résultat souhaité car les fourmis font des tunnels fins et longs. Pour y remedier, nous avons crée deux autres fonctions, qui prennent en consideration les voisinage de chaque zéro.
   
```python   
   def voisinage_zero (i, j):
    """ 
    Computes the proportion of zeros in the neighborhood of a element with
    coordinates i, j in the matrix.
    """    
    
    cpt_0 = 0
    cpt_total = 0
    for k, l in neighbs:
       if (k + i >= 0 and k + i < size_map and l + j >= 0 and l + j < size_map): 
           cpt_total = cpt_total + 1
           if map[i + k, j + l] == 0:
               cpt_0 = cpt_0 + 1
    
    return float(cpt_0/cpt_total)


def proba_tun (i, j):
    """
    Computes the probability of digging a new tunnel from the position (i, j) taking in account the proportion
    of neighbors that are already dig. If more than half of the neighbors are already tunnels, the function return zero
    (so, no more tunnels are made). Otherwise, the probability of digging a tunnel is set to be under the form
    f(x) = a * (x - 1 / 2)**2, with "a" chosen in order to have f(1 / 8) = 1 / 2.
    """
    t = voisinage_zero (i, j)
    if t < 0.5:
        return (32/9)*(t - 1/2)**2
    else:
        return 0
```
