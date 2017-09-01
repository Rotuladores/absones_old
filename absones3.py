import random as rd #non usare questo usa np
import scipy as sp
import numpy as np
import networkx as nx
import math
from copy import deepcopy
import argparse, sys, os
from user import User
from simulation import *

tweets = {}
retweets = {}
dtag = {}

network = nx.gnm_random_graph(1000, round((float(1000)*((float(1000)-1)/1))/2), directed=True)
positions = nx.random_layout(network)
sim = Simulation(10, 1000, network)

print('Generation')
print('=' * 20)
for n in network.nodes():
    u1 = User(n, sim.topics)
    sim.add_user(u1)
    for y in range(0,int(math.floor(20.0*network.in_degree().get(n)/max(network.in_degree().values())))):
        sim.post(sim.get_user(n),-y-1)

# add follow
print('Follow')
print('=' * 20)
for e in network.edges():
    sim.new_follow(e[0],e[1])

evo = []

for n in network.nodes():
    for y in range(0,int(math.floor(20.0*network.in_degree().get(n)/max(network.in_degree().values())))):
        sim.repost(sim.get_user(n),-y-1)

print(sim.retweet)

for step in range(1,1080):
    print('')
    print("#" * 40)
    print('# Step ' + str(step))
    print('# Numero di archi ' + str(len(network.edges())))
    print('# Grado di completamento ' + str(len(network.edges())*100/(1000**2 - 1000)))
    print('# Tweets = ' + str(len(sim.tweet)))
    print('# Retweets = ' + str(len(sim.retweet)))
    print("#" * 40)
    sim.step_tweet()
    sim.step_retweet()
    #sim.attachment_eval()
    sim.now = step
    evo.append(len(sim.network.edges()))