# Anthill
Anthill ARE (Dynamics) - UPMC

# Introduction

Nous avons choisi d'étudier __l'évolution temporelle d'une fourmilière en fonction de plusieurs paramètres__, en particulier l'environnement, ainsi que des paramètres internes à la population de fourmis (taux de natalité et de mortalité, durée des différentes phases de vie, etc...).

![Ant eating honey](https://github.com/Sawken/Anthill/blob/master/Images/fourmi.jpeg?raw=true)

# Début de code

Dans un premier temps nous avons élaboré un programme capable de simuler l'evolution temporelle de la population d'une fourmiliere et de nous renvoyer un __graphe montrant la quantité de fourmis vivantes appartenant à une certaine phase de vie (oeuf, larve, nymphe, ouvriere) en fonction de leur âge__. Pour cela, nous avons mis en place des fonctions simulant separement la naissance et la mortalité d'une fourmi; de cette façon nous serons capables dans le futur de les modifier afin qu'elles se rapprochent de plus en plus de la réalité.

A noter que tous nos chiffres sont basés sur la realite, nous pouvons ainsi nous rapprocher au mieux du système dynamique que nous voulons modéliser.

# Code

```Python

import numpy as np
import random as rd
import matplotlib.pyplot as plt

oeuf = np.zeros(15,dtype = "int32")
larve = np.zeros(15,dtype = "int32")
nymphe = np.zeros(15,dtype = "int32")
ouvriere = np.zeros(135,dtype = "int32")

```
Chaque vecteur contient le nombre total de fourmis dans chaque étape de developpement.
L'élément i d'un vecteur contient le nombre de fourmis qui sont dans l'étape correspondante 
depuis i jours. Par exemple, adulte[5] contient le nombre de fourmis qui sont adultes depuis 5 jours.

Nous avons supposé qu'une fourmi prend 15 jours pour passer de oeuf à larve, 15 jours pour passer
de larve à nymphe et plus 15 jours pour devenir adulte. Elle vit au maximum 6 mois (180 jours). 
On a choisi ces valeurs là d'après nos recherches sur le temps moyen de vie d'une fourmi.

Nous avons créé des vecteurs et pas de listes pour simplifier les opérations algebriques (somme élement
par élément).


```Python
p_enfant = 5e-4
p_final = 0.1
p_adulte = np.exp(np.linspace(np.log(p_enfant),np.log(p_final),135))
```

p est la probabilité de mort d'une fourmi. Nous avons choisi une probabilité qui augmente selon 
le vieillissement de la population de fourmis, c'est-à-dire que plus une fourmi sera âgée, plus elle aura de chances de mourir.

Nous utilisons la fonction linspace qui crée un vecteur à valeurs également espacées. Pour créer un
vecteur à valeurs qui croissent exponentiellement, nous prenons son exponentielle. Pour que ce soit
plus facile de choisir les valeurs initiale et finale, nous utilisons le logarithme des probabilités
que nous voulons. 

``` Python

def dynamics():
     global oeuf, larve, nymphe, ouvriere
     ouvriere[1:] = ouvriere[:-1]
     ouvriere[0] = nymphe[-1]
     nymphe[1:] = nymphe[:-1]
     nymphe[0] = larve[-1]
     larve[1:] = larve[:-1]
     larve[0] = oeuf[-1]
     oeuf[1:] = oeuf[:-1]
     #viellissent d'un jour de la population de fourmis.
     
     oeuf[0] = naissance()
     #naissance des fourmis.
     
     oeuf = oeuf - mort(oeuf,p_enfant)
     larve = larve - mort(larve,p_enfant)
     nymphe = nymphe - mort(nymphe,p_enfant)
     ouvriere = ouvriere - mort(ouvriere,p_adulte)
     #mort des fourmis.
     
def naissance():
    return rd.randint(18, 25)
    #la reine pond entre 18 et 25 oeufs par jour.

def mort(liste,p):
    return np.random.binomial(liste,p)
 
 ```
 Nous utilisons la fonction random.binomial, qui prend 2 arguments (le vecteur avec la population
de fourmis et la probabilité d'une fourmi de mourir).
Chaque fourmi a une probabilité p de mourir à un jour donné. Sur une quantité N de fourmis,
la probabilité que k fourmis meurent un jour donné vaut p^k(1-p)^(N-k) fois le 
nombre de façons differentes de choisir k fourmis parmi N, soit le coefficient binomial (N,k). 
Ceci est la loi binomiale qui calcule combien de fourmis sont mortes.

``` Python

def sim_plot(steps):
    plt.figure(0)
    plt.ion()
    end_oeuf = len(oeuf)
    end_larve = end_oeuf + len(larve)
    end_nymphe = end_larve + len(nymphe)
    end_ouvriere = end_nymphe + len(ouvriere)
    for i in range(steps):
        dynamics()
        plt.cla()
        plt.plot(np.arange(0,end_oeuf),oeuf)
        plt.plot(np.arange(end_oeuf,end_larve),larve)
        plt.plot(np.arange(end_larve,end_nymphe),nymphe)
        plt.plot(np.arange(end_nymphe,end_ouvriere),ouvriere)
        plt.show()
        plt.pause(0.05)
 ```
 ![Graphe](https://github.com/Sawken/Anthill/blob/master/Images/figure_0.png?raw=true)


Cette image est un exemple du graphe créé par notre fonction. L'axe des ordonnées montre la quantité de fourmis vivantes et l'axe des abscisses leur âge en jours. Nous pouvons voir que la quantité de fourmis suit une loi exponentielle décroissante à partir d'un temps t.
Le graphe ne sera pas toujours le même car nous utilisons dans notre code des variables aléatoires (loi binomiale, etc...).
