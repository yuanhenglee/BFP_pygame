import utils
import pygame
import copy
import numpy as np
from color import *
import globals

cost = 1
class PotentialField:
    def __init__(self, goal ):
        self.bitmap = np.full( (128,128), 0) 
        self.mark_NF1( goal )
        # self.mark_NF2( goal)


    def show_bitmap(self, gameDisplay):
        for i in range(128):
            for j in range(128):
                color = 255 - self.bitmap[i][j]
                color = 0 if color<0 else color
                color = (color, color, color)
                x, y = utils.world2Canvas((i, j))
                pygame.draw.rect(gameDisplay, color, [x, y, utils.multiplier, utils.multiplier])

    def mark_NF1(self, goal ):
        bitmap = copy.deepcopy(globals.obstacles_bitmap)
        bitmap[goal[0]][goal[1]] = 0

        # BFS from goal
        l_configs = {0:[goal]}
        # for i, Li in l_configs.items():
        i = 0
        while True:
            if i not in l_configs:
                break

            Li = l_configs[i]
            for q in Li:
                for neighbor in utils.findNeighbors(q):
                    if bitmap[neighbor[0]][neighbor[1]] == 254:
                        bitmap[neighbor[0]][neighbor[1]] = i+cost
                        if i+cost in l_configs:
                            l_configs[i+cost].append(neighbor)
                        else:
                            l_configs[i+cost] = [neighbor]
            i+=cost
        self.bitmap += bitmap

    def mark_NF2(self, goal):
        # edge init
        distance = np.full((128, 128), 254)
        origin = {}
        l_configs = {0:[]}
        S = set()
        for i in range(128):
            for j in range(128):
                if globals.obstacles_bitmap[i][j] == 255:
                    for neighbor in utils.findNeighbors((i,j)):
                        if globals.obstacles_bitmap[neighbor[0]][neighbor[1]] == 254:
                            distance[i][j] = 0
                            origin[(i,j)] = (i,j)
                            l_configs[0].append((i,j))
                            break

        i = 0
        while True:
            if i not in l_configs:
                break

            Li = l_configs[i]
            for q in Li:
                for neighbor in utils.findNeighbors(q):
                    if globals.obstacles_bitmap[neighbor[0]][neighbor[1]] == 254:
                        if distance[neighbor[0]][neighbor[1]] == 254:
                            distance[neighbor[0]][neighbor[1]] = i+cost
                            origin[neighbor] = origin[q]
                            if i+cost in l_configs:
                                l_configs[i+cost].append(neighbor)
                            else:
                                l_configs[i+cost] = [neighbor]
                        elif utils.distance(origin[neighbor], origin[q] ) > 5 and q not in S:
                            S.add(neighbor)
            i+=cost
        
        bitmap = np.full((128, 128), 254)
        Sigma = set([goal])
        l_configs = {0:[]}
        q = goal
        while q not in S:
            q_prime = utils.findBestNeighbor( q, distance )
            Sigma.add(q_prime)
            q = q_prime
        S = S.union(Sigma)

        # for p in S:
        #     bitmap[p[0]][p[1]] = 0


        bitmap[goal[0]][goal[1]] = 0
        Q = [goal]
        while len(Q) > 0 :
            q = Q.pop(0)
            l_configs[0].append(q)
            for neighbor in utils.findNeighbors(q):
                if neighbor in S and bitmap[neighbor[0]][neighbor[1]] == 254:
                    bitmap[neighbor[0]][neighbor[1]] = 0 
                    # bitmap[neighbor[0]][neighbor[1]] = bitmap[q[0]][q[1]] + 1
                    Q.append(neighbor)

        i = 0
        while True:
            if i not in l_configs:
                break

            Li = l_configs[i]
            for q in Li:
                for neighbor in utils.findNeighbors(q):
                    if globals.obstacles_bitmap[neighbor[0]][neighbor[1]] == 254 and bitmap[neighbor[0]][neighbor[1]] == 254:
                        bitmap[neighbor[0]][neighbor[1]] = bitmap[q[0]][q[1]] + 1
                        if i+cost in l_configs:
                            l_configs[i+cost].append(neighbor)
                        else:
                            l_configs[i+cost] = [neighbor]
            i+=cost
        

        self.bitmap = bitmap 


    