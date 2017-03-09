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
   
   La première fonction que nous avons crée c'est la fonction dig_tunnel qui prend comme arguments des coordonnées (i, j) d'un élément de la matrice. Elle crée une liste de tuples avec les voisins existants et ces distances relatifs à la reine. Pour calculer les differentes probabilités d'être choisi pour chacun de ces élements, nous créons un autre fonction appellé proba_direction, qui prend comme argument cette liste de tuples creé par la fonction précedent. 
   
   La foction proba_direction calcule un liste de probabilités d'être choisi par rapport a la distance des éléments à la reine de façon lineaire, avec la probabilité de choisir l'élément plus loin 100 fois plus petit que celle de choisir le plus proche. Cela correspond à prend les probabilités proportionnelles à f(d) = a*d + b, avec d la distance 
   

    This corresponds to picking the probabilities proportional to f(d) = a*d + b,
    where d is the distance to the queen and a and b are chosen in such a way that 
    f(dmin) = 1 and f(dmax) = 100. Dmin is the smallest distance present in this_neighbs
    and dmax is the biggest.
    """
   


