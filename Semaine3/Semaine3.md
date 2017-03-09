# Semaine 3


# Création des tunnels


   Pour créer des tunnels nous avons d'abord crée une nouvelle matrice de même taille que notre matrice map:
```python
map_dist = np.zeros ((size_map,size_map), dtype = "float16")
```
  Cette matrice est initialisé avec que des zéros et après, dans la fonction set_queen(), elle est remplie avec les distances euclidiennes de chaque élément par rapport a la reine, c'est à dire, avec les positions relatives de chaque élément de la matrice map à la reine. La matrice map_dist doit être rempli après la géneration de la reine car celle-ci est mise en place dans map de façon aléatoire.
  
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
