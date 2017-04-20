# Semaine 6

## Chemin le plus court

  La semaine dernière, nous avons commencer à coder un programme permettant de simuler __le choix du chemin le plus court vers une source de nourriture__. Nous avions réussi à faire en sorte que l'éclaireuse trouve la source de nourriture en créant une liste des positions qu'elle a déjà emprunté, positions qu'elle ne pourra plus prendre par la suite. Si la source de nourriture est trouvée, elle laisse une trace chimique sur son passage, modélisée par l'incrémentation des cases de passage de +1. Il nous restait à coder le retour de l'éclaireuse vers la fourmilière.

## Cheminement de l'éclaireuse - Suite

  Pour plus de lisibilité, nous nous sommes mis d'accord pour modifier notre code de la semaine dermière afin de réduire la fourmilière à un seul point, à la position (dim-1,dim-1). Une fois que l'éclaireuse trouve la source de nourriture, elle 'disparaît': en réalité on veut dire qu'elle n'est plus représentée sur notre matrice **espace**, seule sa trace chimique persiste.

## Cheminement des autres fourmis ouvrières

  Maintenant que l'éclaireuse a trouvé sa source de nourriture, nous allons générer d'autres fourmis qui chercherons elles aussi de quoi se nourrir. Mais en quoi sont-elles différentes de la fourmi éclaireuse ? Eh bien cette fois-ci, les ouvrières prendront en compte la trace chimique laissée par cette dernières. En effet, à chaque itération, elle prendra en compte la présence (ou l'absence) d'une trace chimique attractive ainsin que sa force, pour se déplacer. Ainsi, si l'on considère deux cases a et b voisines d'une fourmi, si la case a a pour valeur 5 et la case b pour valeur 0, la probabilité que la fourmi se déplace vers a sera plus grande. Pour ce faire, utilisons une liste de probabilités associées à chaque position voisine à notre fourmi.
  
  Voici la fonction permettant ceci:
  
 ```Python
 
 
 ```
 
Or l'on remarque que dans les faits, les fourmis continuent à se déplacer plus ou moins sur 'les traces' de l'éclaireuse, sans pour autant suivre un chemin de plus en plus précis. Au contraire, plus on avance dans nos itérations, plus une zone (très large) alentour à la première trace se dessine, et cette zone ne cesse de s'élargir ! Cela ne nous donne pas du tout ce que l'on veut.

Noous décidons alors d'incrémenter une trace chimique de +5 à chaque fois afin de voir une plus grande différence dans les probabilités, mais cela ne fonctionne pas non plus. En effet, si l'écart entre les valeurs des cases est élevée, en proportion les probabilités ne sont pas significativement différentes.

```Python


```

Nous décidons dons de réutiliser une idée qu'Ariana avait déjà eu pendant la programmation de l'expansion des tunnels: il s'agirait de traduire en probabilités exponentielles les valeurs associées à chaque case du voisinage d'une fourmi. Cela se fait aisément grâce à la fonction np.exp(). Voici le code de la fonction traduisant la probabilité associée à chaque case, modifiée avec la fonction np.exp().

```Python


```

Le code étant maintenant fonctionnel, nous nous occupons de la mise en graphique avec __Matplotlib__, comme nous l'avions déjà fait dans les programmes pour l'expansion des tunnels (*Semaine 5*) et la croissance de population (*Semaine 3 bis*).

```Python


```


Voici des figures que nous pouvons obtenir:

