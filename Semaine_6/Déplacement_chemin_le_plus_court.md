# Semaine 6


## Chemin le plus court

  La semaine dernière, nous avons commencer à coder un programme permettant de simuler __le choix du chemin le plus court vers une source de nourriture__. Nous avions réussi à faire en sorte que l'éclaireuse trouve la source de nourriture en créant une liste des positions qu'elle a déjà emprunté, positions qu'elle ne pourra plus prendre par la suite. Si la source de nourriture est trouvée, elle laisse une trace chimique sur son passage, modélisée par l'incrémentation des cases de passage de +1. Il nous restait à coder le retour de l'éclaireuse vers la fourmilière.


## Cheminement de l'éclaireuse - Suite

  Pour plus de lisibilité, nous nous sommes mis d'accord pour modifier notre code de la semaine dermière afin de réduire la fourmilière à un seul point, à la position (dim-1,dim-1). Une fois que l'éclaireuse trouve la source de nourriture, elle 'disparaît': en réalité on veut dire qu'elle n'est plus représentée sur notre matrice **espace**, seule sa trace chimique persiste.


## Cheminement des autres fourmis ouvrières

  Maintenant que l'éclaireuse a trouvé sa source de nourriture, nous allons générer d'autres fourmis qui chercherons elles aussi de quoi se nourrir. Mais en quoi sont-elles différentes de la fourmi éclaireuse ? Eh bien cette fois-ci, les ouvrières prendront en compte la trace chimique laissée par cette dernières. En effet, à chaque itération, elle prendra en compte la présence (ou l'absence) d'une trace chimique attractive ainsin que sa force, pour se déplacer. Ainsi, si l'on considère deux cases a et b voisines d'une fourmi, si la case a a pour valeur 5 et la case b pour valeur 0, la probabilité que la fourmi se déplace vers a sera plus grande. Pour ce faire, utilisons une liste de probabilités associées à chaque position voisine à notre fourmi.
  
  
  Voici la fonction permettant ceci:
  
 ```Python
def compt_voisins(i,j,set_visite):
    """ Cette fonction choisit une position aléatoire voisine à la fourmi située à la position (i,j) en créant une liste 
    de probabilités associées à chaque position. Elle retourne les coordonnées de de la nouvelle position."""
    liste_voisins = []
    for k, l in neighbs:
        if (l + i >= 0 and l + i < dim and j + k >= 0 and k + j < dim): 
            if ((l+i,k+j) not in set_visite) and (espace[l+i][k+j] != -1):
                # Check if we're not outside boundaries of the array.
                liste_voisins.append([l+i,k+j])
    if liste_voisins == []:

        return (-1, -1)         
    
    this_proba = proba_voisins (liste_voisins)
    indice = np.random.choice (len(liste_voisins),p = this_proba)
    
    return liste_voisins[indice] 
 
 ```
 
 
Or l'on remarque que dans les faits, les fourmis continuent à se déplacer plus ou moins sur 'les traces' de l'éclaireuse, sans pour autant suivre un chemin de plus en plus précis. Au contraire, plus on avance dans nos itérations, plus une zone (très large) alentour à la première trace se dessine, et cette zone ne cesse de s'élargir ! Cela ne nous donne pas du tout ce que l'on veut.

Noous décidons alors d'incrémenter une trace chimique de +5 à chaque fois afin de voir une plus grande différence dans les probabilités, mais cela ne fonctionne pas non plus. En effet, si l'écart entre les valeurs des cases est élevée, en proportion les probabilités ne sont pas significativement différentes.


```Python

def dynamics(nb):
    """"Cette fonction simule le deplacement d'une fourmi. """    
    
    global espace
    espace_old = copy.copy(espace)
    
    x, y = eclaireuse(espace)
    set_visite = set()
    set_visite.add((x,y))
    
    for i in range(nb):
        x, y = compt_voisins(x,y, set_visite)
        if (x == -1 and y == -1) or (x == x_source and y == y_source) :
            if (x == x_source) and (y == y_source):
                espace[x][y] += 5
                return True

            else:

                espace = copy.copy (espace_old)
                return False
        else:
            espace[x][y] += 5
            set_visite.add((x,y))

```


Nous décidons dons de réutiliser une idée qu'Ariana avait déjà eu pendant la programmation de l'expansion des tunnels: il s'agirait de traduire en probabilités exponentielles les valeurs associées à chaque case du voisinage d'une fourmi. Cela se fait aisément grâce à la fonction np.exp(). Voici le code de la fonction traduisant la probabilité associée à chaque case, modifiée avec la fonction np.exp().


```Python

def proba_voisins(liste_voisins):

    """ Fait le déplacement de la fourmi """    
    
    this_proba = np.zeros(len(liste_voisins))
    for i in range(len(liste_voisins)):
        x, y = liste_voisins[i]
        this_proba[i] = (espace[x][y]+1)

    this_proba = np.exp(this_proba)
   
    this_proba = this_proba/np.sum(this_proba)

    return this_proba

```


Le code étant maintenant fonctionnel, nous nous occupons de la mise en graphique avec __Matplotlib__, comme nous l'avions déjà fait dans les programmes pour l'expansion des tunnels (*Semaine 5*) et la croissance de population (*Semaine 3 bis*).


```Python
def plot_espace ():
    
    """Cette fonction dessine le graphe du chemin, il faut l'appeler à
    chaque fois qu'on veut voir le graphe. """    
    
    M = np.max(espace)
    norm = mcolors.Normalize(-1,M)
         
    # Defining a personalized color map.
    # M = blue
    # 0 = white
    # -1 = red
    
    cdict = {'red':   [(norm(-1), 1.0, 1.0),
                       (norm(0), 1.0, 1.0),
                       (norm(M), 0.0, 0.0)],
    
             'green': [(norm(-1), 0.0, 0.0),
                       (norm(0), 1.0, 1.0),
                       (norm(M), 0.0, 0.0)],
    
             'blue':  [(norm(-1), 0.0, 0.0),
                       (norm(0), 1.0, 1.0),
                       (norm(M), 1.0, 1.0)]}
                       
    cmap_custom = mcolors.LinearSegmentedColormap('CustomMap', cdict, N = M + 2)

    
    dpi = 20.0 
    figsize = (dim/float(dpi),dim/float(dpi))
    fig1 = plt.figure(figsize=figsize,facecolor = "white")
    ax1 = fig1.add_axes([0.0, 0.0, 1.0, 1.0], frameon = False)
    ax1.imshow(espace, interpolation = 'nearest', cmap = cmap_custom, norm = norm)
    ax1.set_xticks([]), ax1.set_yticks([])
    fig1.canvas.draw()    


def sim_1 (nb):
    
    """Cette fonction tourne jusqu'à ce que la première fourmi trouve la source de nourriture"""
    
    dynamics_premier (nb)    
    
    while not dynamics(nb):
        print("a",end = "")
        
def sim_renforce (nb):
    
    """ Elle génère à chaque itération (nb en tout) une fourmi qui va effectuer nb pas, en laissant une trace
    chimique que si elle trouve la source de nourriture""""
    
    for i in range(200):
        dynamics(nb)
     
#Il faut appeler d'abbord la fonction sim_1 avec nb le nombre d'iterations maximale pour 
#     qu'une fourmi trouve la nourriture, après appeler sim_renforce pour generer 200 fourmis
#     suplementaires et à la fin appeler plot_espace pour creer le graphe.

```

Voici des figures que nous pouvons obtenir:

