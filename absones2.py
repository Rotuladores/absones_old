#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

import pylab as pl
import random as rd #non usare questo usa np
import scipy as sp
import numpy as np
import networkx as nx
import math
from copy import deepcopy
import argparse, sys, os
import pycxsimulator

### absones utilities
sys.path.append(os.path.abspath(os.getcwd() + '/utils'))
print(sys.path)
from user import User
from simulation import *

rd.seed()

tweets = {}
retweets = {}
dtag = {}

def init():
    global sim

    print('Generation')
    print('=' * 20)
    for n in network.nodes():
        u1 = User(n, sim.topics)
        sim.add_user(u1)
        print(sim.get_user(n))

    # add follow
    print('Follow')
    print('=' * 20)
    for e in network.edges():
        sim.new_follow(e[0],e[1])


def draw():
    global sim, positions
    colors = [sim.network.degree().get(node) for node in sim.network.nodes()]
    dims = list(map(lambda x: float(x+1)*80, [sim.network.in_degree().get(node) for node in sim.network.nodes()]))

    pl.cla()
    nx.draw(sim.network, pos = positions, node_color = colors, node_size = dims)
    pl.axis('image')
    pl.title('t = ' + str(sim.now) + ' edges = ' + str(len(sim.network.edges())))

def step():
    global sim

    sim.step_tweet()
    sim.step_retweet()
    sim.now += 1

##=====================================
## Section 4: [Optional] Create Setter/Getter Functions for Model Parameters
##=====================================



##=====================================
## Section 5: Import and Run GUI
##=====================================
def get_args():
    parser = argparse.ArgumentParser(description='ABSoNeS', add_help=True)
    #change all the defaults
    parser.add_argument('-u', '--users', action='store', type=int, default=10,
        help='specifies the number of total users.')
    parser.add_argument('-t', '--topic', action='store', type=int, default=10,
        help='specifies the number of total topics.')
    parser.add_argument('-d', '--threads', action='store', type=int, default=2,
        help='specifies the number of total threads used by the program.')
    ret = parser.parse_args()

    return ret


def main():
    # global args
    pycxsimulator.GUI(title='SocialNetwork',interval=0, parameterSetters = []).start(func=[init,draw,step])
    # 'title', 'interval' and 'parameterSetters' are optional

if __name__ == "__main__":
    args = get_args()
    network = nx.gnm_random_graph(args.users,
                                  args.users,
                                  directed=True)
    positions = nx.random_layout(network)
    sim = Simulation(args.topic, args.users, network)
    print()
    main()
