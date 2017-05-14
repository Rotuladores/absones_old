#!/usr/bin/env python

import matplotlib
matplotlib.use('TkAgg')

import pylab as pl
import random as rd #non usare questo usa np
import scipy as sp
import numpy as np
import networkx as nx
import math
import argparse, sys, os
import pycxsimulator

### absones utilities 
sys.path.append(os.path.abspath(os.getcwd() + '/utils'))
from simulation import *

rd.seed()

tweets = {}
retweets = {}
dtag = {}

def init():
    global time, network, network_r, maxNodeID, positions, colors, dims, sharing
    global sim

    time = 0

    network = nx.gnm_random_graph(sim.total_users,sim.total_users*2,directed=True)
    network_r = nx.DiGraph()
    network_r.add_nodes_from(network)

    positions = nx.random_layout(network)
    colors = [network.degree().get(node) for node in network.nodes()]
    dims = list(map(lambda x: float(x+1)*80, [network.in_degree().get(node) for node in network.nodes()]))

    sharing = []

    for n in network.nodes():
        sim.generate_new_user(network.node[n])
        print(network.node[n])

def draw():
     colors = [network.degree().get(node) for node in network.nodes()]
     dims = list(map(lambda x: float(x+1)*80, [network.in_degree().get(node) for node in network.nodes()]))

     pl.subplot(1,2,1)
     pl.cla()
     nx.draw(network, pos = positions, node_color = colors, node_size = dims)
     pl.axis('image')
     pl.title('t = ' + str(time) + ' edges = ' + str(len(network.edges())))

     pl.subplot(1,2,2)
     pl.cla()
     nx.draw(network_r, pos = positions, node_color = 'w', node_size = dims, with_labels=True)
     pl.axis('image')
     pl.title('t = ' + str(time))

def step():
    global network_r, network, sharing, time
    network_r.remove_edges_from(sharing)
    l = network.nodes()
    a1 = rd.choice(l)
    l.remove(a1)
    a2 = rd.choice(l)
    l.remove(a2)
    b1 = rd.choice(l)
    l.remove(b1)
    b2 = rd.choice(l)
    network_r.add_edge(u=a1,v=a2)
    network_r.add_edge(u=b1,v=b2)
    sharing = [(a1,a2),(b1,b2)]
    time += 1

    for e in sharing:
        skl = skl_d(network.node[e[0]]['interest'],network.node[e[1]]['interest'])
        print("%d,%d skl= %f" % (e[0],e[1],skl))
        if skl > 0.5:
            network.add_edge(u=e[0],v=e[1])
    print(network.edges())

##=====================================
## Section 4: [Optional] Create Setter/Getter Functions for Model Parameters
##=====================================

def skl_d(p,q):
	kl1 = 0
	for i in range(0, len(p)):
		kl1 = kl1 + p[i]*np.log2(p[i]/q[i])
	kl2 = 0
	for j in range(0, len(q)):
		kl2 = kl2 + q[j]*np.log2(q[j]/p[j])
	return np.mean([kl1,kl2])





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
    sim = Simulation(args.topic, args.users)
    print()
    main()

