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

 La première fonction qui nous avons écrit cette semaine est  __quant_zeros__, qui compte la quantité totale de tunnels existentes dans notre matrice __map__ à un moment donné. Au lieu d'utiliser une boucle imbriquée double pour parcourir la matrice nous avons preferé utiliser la fonction ```sum``` de la bibliothèque numpy et exploiter le fait que ```True``` en Python est consideré comme 1 et ```False``` comme 0.

```python
def quant_zeros ():
    """
    Return the quantity of zeros in map.
    We use this to determinated if tunnels should be created or destroyed.
    """
    
    return np.sum(map == 0)  
 ```
 
 La deuxième fonction implementée est __rayon_fourmiliere__ , qui retourne la distance maximale des tunnels à la reine:
 
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
 
 
Nous avons decidé de ne pas changer la fonction __croissance__, maintenant appelé __croissance_tun__ (pour eviter la confusion avec la fonction __croissance_fourmis__ de la semaine 1), et à la place de créer une nouvelle fonction __dynamics__. Elle s'occuppe d'initialiser la fourmilière et ensuite faire la boucle où, a chaque tour, la fonction __croissance_fourmis__ est appellée et on decide si l'on appelera soit la fonction __croissance_tun__, soit la fonction __decroissance_tun__ en termes de la différence entre la quantité de tunnels dans __map__ et le nombre maximal de tunnels qui peuvent être construits, calculé par ```ratio_fourmis_tunnels * np.sum(ouvriere)``` 
 
```python
def dynamics (nb):
    """
    This function creates an anthill and simulates its growth, relating the creation
    of tunnels to the quantity of adults ants alive each turn. If the quantity of 
    ants isnt big enough, the function destroys tunnels, else it creates new ones. 
    """
    
    init_fourmis ()
    set_queen()
    ax1, fig1 = init_plot_fourmiliere ()
    ax2, fig2 = init_plot_fourmis ()
    plt.ion()
    
    for i in range(nb):
        croissance_fourmis()
        quant_tun = quant_zeros () - ratio_fourmis_tunnels * np.sum(ouvriere)
        if quant_tun < 0:
            croissance_tun ()
            
        elif quant_tun > 0:
            decroissance_tun (math.ceil (quant_tun))
            #we need it to be an integer bigger than zero.

        display_plot_fourmiliere (ax1, fig1)
        display_plot_fourmis (ax2, fig2)

        plt.show()
        plt.pause(0.01)

        #plt.waitforbuttonpress() #If we want to control manually when it changes.
```   
Pour l'initialisation, outre la fonction __set_queen__ que nous avons écrite dans la semaine 2, nous avons aussi appelé la fonction __init_fourmis__ dont le code est donné ci-dessous.

```python
def init_fourmis ():
    """
    It fills the first 20 spaces of the array ouvriere with a random quantity of ants,
    so that when the queen is created the anthill can grow immediately (It simulates
    the ants that go out of an anthill with a new queen to form a new colony).
    """
    
    nb_fourmis = rd.randint(50, 100)
    for i in range (nb_fourmis):
        age = rd.randint(0,20)
        ouvriere[age] += 1
```

Elle choisit un nombre aléatoire entre 50 et 99 fourmis ouvrières, d'âge entre 46 et 65 jours, pour accompagner la reine à la création de la fourmilière. De cette façon il ne faut pas attendre la maturité des oeufs pondus par la reine pour avoir de changements de taille de la fourmilière.  

Comme vous pouvez voir, __dynamics__ implemente aussi des fonctions de visualisation des simulations. Les fonctions __init_plot_fourmis__ et __display_plot_fourmis__ font essentielement le même graphique que celui de la semaine 1 qui donné la quantité de fourmis par rapport à leur âge en jours. Leurs codes sont donnés ci-dessous:

```python
def init_plot_fourmis () :
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_ylabel("Quantité de fourmis")
    ax2.set_xlabel("Âge des fourmis en jours")  
    ax2.grid()
    
    return ax2, fig2    

def display_plot_fourmis (ax2, fig2) :
    end_oeuf = len(oeuf)
    end_larve = end_oeuf + len(larve)
    end_nymphe = end_larve + len(nymphe)
    end_ouvriere = end_nymphe + len(ouvriere)
    
    ax2.cla()
    ax2.plot(np.arange(0,end_oeuf),oeuf)
    ax2.plot(np.arange(end_oeuf,end_larve),larve)
    ax2.plot(np.arange(end_larve,end_nymphe),nymphe)
    ax2.plot(np.arange(end_nymphe,end_ouvriere),ouvriere)
    ax2.set_ylabel("Quantité de fourmis")
    ax2.set_xlabel("Âge des fourmis en jours")  
    ax2.grid()
    fig2.canvas.draw()    
   ```
   
Les deux autres fonctions, __init_plot_fourmiliere__ et __display_plot_fourmiliere__, s'occupent de l'affichage de la fourmilière. La première initialise la fenêtre graphique et la deuxième fait l'affichage en boucle de la fourmilière. Pour les couleurs, nous avons crée un _color map_ personalisé (la reine apparaît en rouge, les tunnels en blanc): 

```python
# Defining a personalized color map.
# 2 = red
# 1 = black
# 0 = white

cdict = {'red':   [(0.0, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 1.0, 1.0)],

         'green': [(0.0, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0)],

         'blue':  [(0.0, 1.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (1.0, 0.0, 0.0)]}
                   
cmap_custom = mcolors.LinearSegmentedColormap('CustomMap', cdict)

def init_plot_fourmiliere ():                

    dpi = 20.0 #We find 72 dpi to be too small.
    figsize = (size_map/float(dpi),size_map/float(dpi))
    fig1 = plt.figure(figsize=figsize,facecolor = "white")
    ax1 = fig1.add_axes([0.0, 0.0, 1.0, 1.0], frameon = False)
    ax1.imshow(map, interpolation = 'nearest', cmap = cmap_custom)
    ax1.set_xticks([]), ax1.set_yticks([])
    
    return ax1, fig1
    
def display_plot_fourmiliere (ax1, fig1):

    ax1.cla()
    ax1.imshow(map, interpolation = 'nearest', cmap = cmap_custom)
    ax1.set_xticks([]), ax1.set_yticks([])
    fig1.canvas.draw()   
```

## Simulations 

Nous avons tourne le code presenté plusieurs fois, voici une figure correspondante du résultat typique obtenu avec  ```ratio_fourmis_tunnels = 0.5``` après 1 an (c'est-à-dire 365 tours de boucle):
<p align="center"><img src="https://github.com/Sawken/Anthill/blob/master/Images/formigas_circular1.png?raw=true" alt="Simmulation foumilière 1">
</p>

Nous pouvons voir dans l'image que la fourmilière ansi crée est encore un peu loin de la realité car son format est circulaire et la densité de tunnels est très grande. Nous croyons que le format circulaire provient du choix deterministe de tunnels à détruire dans la fonction __decroissance_tun__, qui sont ceux qui sont le plus eloignés de la reine (dans la distance euclidienne, d'où le cercle). Pour résoudre cela nous comptons modifier la fonction pour que le choix de tunnels à détruire soit plus aléatoire. 

Dans un premier momment, nous avons cru que pour résoudre le problème de la densité de tunnels il suffirait de changer la proportion maximale de voisins d'un tunnel à partir de laquelle on empecherait la création de nouveaux tunnels autour de celui-ci. Néanmoins, cette première solution n'est pas satisfaisante car si nous diminuons trop ce paramètre, nous arrivons à des situations où la croissance de la fourmilière est completement empechée. Il faut donc une solution plus élaboré a ce problème (probablement en créant des differents cas selon la distance de la reine).

Pour la semaine prochaine nous comptons résoudre ces problèmes afin de avoir une simmulation complètement fonctionnelle. Nous alons aussi travailler sur la deuxième partie de ce projet, portant sur la simulation de la recherche de la nourriture par une fourmi. 
