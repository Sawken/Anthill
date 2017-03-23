# Semaine 4

# Idées de continuation pour le code

 Le problème avec le code de la semaine 3 est qu'il ne prend pas en compte les fourmis contenues dans la fourmilière: en effet, jusque-là, la seule condition pour créer des tunnels était l'existence d'une fourmilière et de sa reine. L'idée est maintenant de créer de nouvelles fonctions qui prennent cette fois-ci en compte l'existence ou non de fourmis autres que la reine.

## Explication

 L'idée première serait de modifier la fonction __croissance__ pour créer une fonction qui prend en compte la quantité de fourmis déjà existante initialement, ainsi que la quantité de zéros de notre matrice fourmilière (chaque zéro représentant un tunnel). Nous alons ensuite créer une fonction __decroissance_tun__ qui détruit des tunnels si leur nombre est trop grand par rapport à la quantité de fourmis. 
 
 Pour cela, il faudrait créer une fonction qui compte la quantité de zéros dans notre matrice-fourmilière et aussi une fonction qui calcule le rayon de la fourmilière, c'est-à-dire, la distance entre la reine et le tunnel le plus eloigné d'elle . Ce nombres seront utilisés pendant l'appel des fonction. Nous utiliserons une variable ```ratio_fourmis_tunnels``` qui serait soit globale, soit donnée par l'utilisateur en paramètre de la fonction, et qui indiquerait la quantité maximale de tunnels qui peuvent être créés par fourmi. Par exemple, si nous prenons ```ratio_fourmis_tunnels = 1``` et une quantité ```n = 100``` de fourmis, nous pourrons avoir au maximum ```max = n * ratio_fourmis_tunnels``` soit __1 * 100__ tunnels dans notre matrice.

## Premier cas

 Si le nombre de tunnels existants est supérieur à __max__, alors la fourmilière sera trop grande par rapport à la quantité de fourmis; on choisira donc de supprimer des tunnels. Ainsi, nous espèrons obtenir une croissance/décroissance de la fourmilière qui sera représentative de la réalité.

 Pour faire cette suppression, nous voulons prendre également en considération la distance de chaque tunnel par rapport à la reine. Dans un premier temps, nous essaierons de créer une fonction qui prendra en considération cette distance et choisira de détruire en priorité les tunnels les plus éloignés de la reine. 

## Deuxième cas

 Dans le cas où le nombre de tunnels déjà existants est égal à __max__, nous sommes dans un état d'équilibre momentané et nous n'effectuerons pas de changement sur les tunnels.

## Troisième cas

 Si le nombre de tunnels existants est inférieur à __max__, alors la possibilté de croissance existe.
Deux possibilités s'offrent à nous:

 * Soit on laisse le programme créer des tunnels jusqu'à ce que la quantité de tunnels soit égale à __max__. Pour cela, nous serions probablement obligés de modifier la fonction croissance afin qu'elle prenne ce cas en considération.
 
 * Une autre possibilité est de laisser le programme créer une quantité illimitée de tunnels avec la fonction __croissance__. Il peut alors arriver que la fonction crée un nombre __x__ de tunnels tel que __x + nombre de tunnels existants__ soit supérieur à __max__.

Nous avons choisi la deuxième possibilité car elle nous semble plus interessante. De cette façon, la dinamique de croissance/décroissance du fourmillière difficilement attendra un équilibre statique.

## Fonctions

 La première fonction qui nous avons écrit cette semaine est  ```quant_zeros ()```, qui compte la quantité totale de tunnels existentes dans notre matrice __map__ à un moment donné. Au lieu d'utiliser une boucle imbriquée double pour parcourir la matrice nous avons preferé utiliser la fonction ```sum``` de la bibliothèque numpy et exploiter le fait que ```True``` en Python est consideré comme 1 et ```False``` comme 0.

```python
def quant_zeros ():
    """
    Return the quantity of zeros in map.
    We use this to determinated if tunnels should be created or destroyed.
    """
    
    return np.sum(map == 0)  
 ```
 
 La deuxième fonction implementée est ```rayon_fourmiliere ()``` , qui retourne la distance maximale des tunnels à la reine:
 
 ```python
 def rayon_fourmiliere ():
    """
    Returns the distance of the farthest tunnel from the queen. 
    We use this to determinated which tunnels should be created or destroyed first.
    """
    
    rayon = 0
    for i in range(size_map):
        for j in range(size_map):
            if map[i][j] == 0 and map_dist[i][j] > rayon:
                rayon = map_dist[i][j]
    return rayon
```
 
 Avec ces deux fonctions prêtes, nous avons ensuite travaillé sur la fonction __decroissance_tun__. Nous avons decidé que cette fonction prendra en argument le nombre de tunnels (__quant_tun__) que l'on veut détruire, que nous calculerons dans la fonction __dynamics__ dont la description sera donnée dans la suite. 

Pour détruire les  __quant_tun__ tunnels le plus eloignés de la reine, Nous commençons par crée deux vecteurs, __list_zero_dist__ et __list_zero_pos__, de taille __quant_tun__, qui contiendront respectivement la distance et les coordonnées des tunnels marqués pour être détruits, ordonnés par distance décroissante. La fonction parcourt tous les éléments de la matrice et à chaque fois qu'il y a un zéro, elle compare sa distance de la reine à celles du vecteur __list_zero_dist__ et, le cas écheant, la met dans la bonne position des vecteurs pour qu'ils restent ordonnés. À noter que les 8 tunnels au tour de la reine ne seront jamais marqués pour la destruction (à cause de la condition  ```map_dist[i][j] > 1.5```).
 ```python
def decroissance_tun_old (quant_tun) :
    """
    This function computes all the possible destruction of tunnels in 1 round and
    applies it.
    """
    
    map_old = copy.copy (map)
    list_zero_dist = np.zeros(quant_tun,dtype = "float32")
    list_zero_pos = np.zeros((quant_tun,2),dtype = "int16")
    for i in range(size_map):
       for j in range(size_map):
           if (map_old[i][j] == 0) and map_dist[i][j] > 1.5 :
               k = 0
               while (k < quant_tun) and (list_zero_dist[k] > map_dist[i][j]):
                   k += 1
               if k < quant_tun:
                   list_zero_dist[k + 1 : ] = list_zero_dist[k : quant_tun - 1]
                   list_zero_pos[k + 1 : ][ : ] =  list_zero_pos [k : quant_tun - 1][ : ]
                   list_zero_dist[k] = map_dist[i][j]
                   list_zero_pos[k][ : ] = [i, j]              
    for i in range(quant_tun):
        map[list_zero_pos[i][0], list_zero_pos[i][1]] = 1
  ```
 
 
 decidé de ne pas changer la fonction __croissance__, maintenant appelé __croissance_tun__ (pour eviter la confusion avec la fonction __croissance_fourmis__), et la place de créer une nouvelle fonction __dynamics__ qui englob




