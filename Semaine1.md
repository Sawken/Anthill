# Anthill
Anthill ARE (Dynamics) - UPMC

# Introduction

Nous avons choisi d'étudier l'évolution temporelle d'une fourmilière en fonction de plusieurs paramètres, en particulier l'environnement, ainsi que des paramètres internes à la population de fourmis (taux de natalité et de mortalité, durée des différentes phases de vie, etc...).

![Ant eating honey](http://orig15.deviantart.net/6ad2/f/2008/151/3/f/3f3b98c589d2917a80716c8ffb76982f.jpg)

# Début de code

Dans un premier temps nous avons élaboré un programme capable de simuler l'evolution temporelle de la population d'une fourmiliere et de nous renvoyer un graphe montrant la quantité de fourmis vivantes appartenant à une certaine phase de vie (oeuf, larve, nymphe, ouvriere) en fonction de leur âge. Pour cela, nous avons mis en place des fonctions simulant separement la naissance et la mortalité d'une fourmi; de cette façon nous serons capables dans le futur de les modifier afin qu'elles se rapprochent de plus en plus de la réalité.

A noter que tous nos chiffres sont basés sur la realite, nous pouvons ainsi nous rapprocher au mieux du système dynamique que nous voulons modéliser.

# Code
```
import numpy as np
import random as rd
import matplotlib.pyplot as plt

oeuf = np.zeros(15,dtype = "int32")
larve = np.zeros(15,dtype = "int32")
nymphe = np.zeros(15,dtype = "int32")
ouvriere = np.zeros(135,dtype = "int32")

"""chaque vecteur contient le nombre total de fourmis dans chaque étape de developement.
L'élément i d'une vecteur contient le nombre de fourmis qui sont dans l'étape correspondante 
depuis i jours. Par exemple, adulte[5] contient le nombre de fourmis qui sont adultes depuis 5 jours."""

"""On a supposé qu'une fourmi prend 15 jours pour passer de oeuf à larve, 15 jours pour passer
de larve à nymphe et plus 15 jours pour devenir adulte. Elle vit au maximum 6 mois (180 jours). 
On a choisi ces valeurs là d'après nos recherches sur le temps moyen de vie d'une fourmi."""

"""On crée des vecteurs et pas de listes pour simplifier les opérations algebriques (somme élement
par élément)."""

```
