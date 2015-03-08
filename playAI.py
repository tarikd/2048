# -*- coding: utf-8 -*-

import solver

b = solver.SimpleAI(.25)

b.goal = 2048
#b.prob = 1




# Je fais tourner mon AI naïve sur X board à la suite, jusqu'à ce que j'atteigne le GOAL fixé
b.simPlay(100)


# Je fais tourner mon AI naïve sur un seul board, jusqu'à ce qu'il y ai un Game Over.
#b.loop(printBoard=True)