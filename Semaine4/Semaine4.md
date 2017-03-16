# Semaine 4

# Idées de continuation pour le code

Le problème avec le code de la semaine 3 est qu'il ne prend pas en compte les fourmis contenues dans la fourmilière: en effet, jusque-là, la seule condition pour créer des tunnels était l'existence d'une fourmilière et de sa reine. L'idée est maintenant de créer de nouvelles fonctions qui prennent cette fois-ci en compte l'existence ou non de fourmis autres que la reine.

Deux possibilités s'offrent à nous, chacune avec ses avantages ou inconvénients.

## 1ère possibilité

La première possibilité serait de créer une fonction qui va prendre en compte la quantité de fourmis déjà existantes initialement, ainsi que la quantité de zéros de notre matrice fourmilière (chaque zéro représentant un tunnel). Nous utiliserons ensuite une variable ```ratio_fourmis_tunnels``` qui serait soit globale, soit donnée par l'utilisateur en paramètre de la fonction, qui indiquerait la quantité maximale de tunnels qui peuvent être créées par fourmi. Par exemple, si nous prenons ```ratio_fourmis_tunnels = 1``` et une quantité ```n = 100``` de fourmis, nous pourrons avoir au maximum 1 * 100 tunnels dans notre matrice.

Il faudrait aussi créer une fonction qui compte la quantité de zéros dans notre matrice-fourmilière. Ce chiffre sera utilisée pendant l'appel de la fonction précédente.

