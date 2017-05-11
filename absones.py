#!/usr/bin/env python
import matplotlib
matplotlib.use('TkAgg')

##=====================================
## Section 1: Import Modules
##=====================================

import pylab as pl
import random as rd
import scipy as sp
import networkx as nx
import math

##=====================================
## Section 2: Define Model Parameters
##=====================================

rd.seed()

##=====================================
## Section 3: Define Three Functions
##=====================================

def init():
    global time, network, network_r, maxNodeID, positions, colors, dims, sharing

    time = 0

    network = nx.gnm_random_graph(250,200,directed=True)
    network_r = nx.DiGraph()
    network_r.add_nodes_from(network)

    positions = nx.random_layout(network)
    colors = [network.degree().get(node) for node in network.nodes()]
    dims = list(map(lambda x: float(x+1)*80, [network.in_degree().get(node) for node in network.nodes()]))

    sharing = []
def draw():
     pl.subplot(1,2,1)
     pl.cla()
     nx.draw(network, pos = positions, node_color = colors, node_size = dims)
     pl.axis('image')
     pl.title('t = ' + str(time))

     pl.subplot(1,2,2)
     pl.cla()
     nx.draw(network_r, pos = positions, node_color = colors, node_size = dims)
     pl.axis('image')
     pl.title('t = ' + str(time))
def step():
    global network_r, network, sharing, time
    network_r.remove_edges_from(sharing)
    a1 = rd.randint(1,200)
    a2 = a1+5
    b1 = rd.randint(1,200)
    b2 = b1+5
    network_r.add_edge(u=a1,v=a2)
    network_r.add_edge(u=b1,v=b2)
    sharing = [(a1,a2),(b1,b2)]
    time += 1

##=====================================
## Section 4: [Optional] Create Setter/Getter Functions for Model Parameters
##=====================================

#def setSomeParameter (newValue=someParameter):
#    """ The comment will appear in GUI control """
#    global someParameter
#    someParameter = newValue
#    return someParameter

##=====================================
## Section 5: Import and Run GUI
##=====================================

import pycxsimulator
pycxsimulator.GUI(title='SocialNetwork',interval=0, parameterSetters = []).start(func=[init,draw,step])
# 'title', 'interval' and 'parameterSetters' are optional
