# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:46:25 2017

@author: Guilherme
"""
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

p_enfant = 5e-4
p_final = 0.1
p_adulte = np.exp(np.linspace(np.log(p_enfant),np.log(p_final),135))

"""p est la probabilité de mort d'une fourmi. On a choisi une probabilité qu'agumente selon 
le viellissement de la population de fourmis, c'est-à-dire, une fourmi aura plus de chance de
mourrir le plus elle est agée.

On utilise la fonction linspace que crée un vecteur à valeurs également espacées. Pour crée un
vecteur à valeurs que croissent exponentiellement, on prend son exponentielle. Pour que ce soit
plus facile de choisir les valeurs initiale et finale, on utilise le logarithme des probabilités
qu'on veut. """


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
    
"""On utilise la fonction random.binomial, qui prend 2 arguments (le vecteur avec la population
de fourmis et lá probabilité d'une fourmi mourrir).
Chaque fourmi a une probabilité p de mourrir à un jour donné. Sur une quantité N de fourmis,
la probabilité que k fourmis soient mortes un jour donné vaut p^k(1-p)^(N-k) fois le 
nombre de façons differents de choisir k fourmis parmi N, soit le coefficient binomial (N,k). 
Ceci est la loi binomial qui calcule combien de fourmis sont mortes. """

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
        