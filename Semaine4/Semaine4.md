# Semaine 4

# Idées de continuation pour le code

Le problème avec le code de la semaine 3 est qu'il ne prend pas en compte les fourmis contenues dans la fourmilière: en effet, jusque-là, la seule condition pour créer des tunnels était l'existence d'une fourmilière et de sa reine. L'idée est maintenant de créer de nouvelles fonctions qui prennent cette fois-ci en compte l'existence ou non de fourmis autres que la reine.

## Explication

L'idée serait de créer une fonction qui va prendre en compte la quantité de fourmis déjà existante initialement, ainsi que la quantité de zéros de notre matrice fourmilière (chaque zéro représentant un tunnel). Nous utiliserons ensuite une variable ```ratio_fourmis_tunnels``` qui serait soit globale, soit donnée par l'utilisateur en paramètre de la fonction, et qui indiquerait la quantité maximale de tunnels qui peuvent être créées par fourmi. Par exemple, si nous prenons ```ratio_fourmis_tunnels = 1``` et une quantité ```n = 100``` de fourmis, nous pourrons avoir au maximum ```max = n * ratio_fourmis_tunnels``` soit 1 * 100 tunnels dans notre matrice.


Il faudrait aussi créer une fonction qui compte la quantité de zéros dans notre matrice-fourmilière. Ce chiffre sera utilisée pendant l'appel de la fonction précédente.

## Premier cas

Si le nombre de tunnels existants est supérieur à __max__, alors la fourmilière sera trop grande par rapport à la quantité de fourmis; on choisira donc de supprimer des tunnels. Ainsi, on espère obtenir une croissance/décroissance de la fourmilière qui sera représentative de la réalité.

Pour faire cette suppression, on prendra également en considération la distance de chaque tunnel par rapport à la reine. On créera ensuite une fonction pseudo-aléatoire, mais qui prendra en considération cette distance, qui choisira de détruire en priorité les tunnels les plus éloignés de la reine.

## Deuxième cas

Dans le cas où le nombre de tunnels déjà existants est égal à __max__, on est dans un état d'équilibre momentané. On n'effectue pas de changement sur les tunnels.

## Troisième cas

Si le nombre de tunnels existants est inférieur à __max__, alors la possibilté de croissance existe.
Deux possibilités s'offrent à nous:

 * Soit on laisse le programme créer des tunnels jusqu'à ce que la quantité de tunnels soit égale à __max__. Pour cela, nous serions probablement obligés de modifier la fonction croissance afin qu'elle prenne ce cas en considération.
 
 * Une autre possibilité est de laisser le programme créer une quantité illimitée de tunnels avec la fonction __croissance__. Il peut alors arriver que la fonction crée un nombre __x__ de tunnels tel que x + nombre de tunnels existants soit supérieur à max.






