#!/usr/bin/env python3
import random as rd #non usare questo usa np
import scipy as sp
import pandas as pd
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

num_nodes = 1000

#network = nx.gnm_random_graph(num_nodes, round((float(num_nodes)*((float(num_nodes)-1)/5))/2), directed=True)
network = nx.scale_free_graph(num_nodes)
network = nx.DiGraph(network)
positions = nx.random_layout(network)
sim = Simulation(10, num_nodes, network)

attributes = {}

print('Generation')
print('=' * 20)
for n in network.nodes():
	u1 = User(n, sim.topics)
	attributes[n] = np.argmax(u1.pi)
	sim.add_user(u1)
	for y in range(0,int(math.floor(20.0*network.in_degree().get(n)/max(network.in_degree().values())))):
		sim.post(sim.get_user(n),-y-1)

nx.set_node_attributes(sim.network,'toptopic',attributes)

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

graph = open('graph_init.csv','w')
graph.write('id,weight\n')
for n in sim.network.nodes():
	graph.write(str(n) + ',' + str(network.in_degree().get(n)) + '\n')
graph.close()

edg = open('edges_init.csv','w')
edg.write('Source,Target\n')
for e in sim.network.edges():
	edg.write(str(e[0]) + ',' + str(e[1]) + '\n')
edg.close()

df = pd.DataFrame(columns=list(range(1000)))

for step in range(1, 400):

	classification = open('classification.csv','a')
	dd = sim.network.in_degree()
	dds = sorted(dd, key=dd.get, reverse=True)
	classification.write(str(step) + ',' + ','.join(str(v) for v in dds[0:50]) + '\n')
	classification.close()

	dft = pd.DataFrame([list(sim.network.in_degree().values())], columns=list(range(1000)))
	df = df.append(dft, ignore_index=True)

	evo = open('evolution.csv','a')
	clust = open('clustering.csv','a')
	assor = open('deg_assortativity.csv','a')
	homo = open('homophily.csv','a')
	spath = open('spath.csv','a')
	print('')
	print("#" * 40)
	print('# Step ' + str(step))
	print('# Numero di archi ' + str(len(sim.network.edges())))
	print('# Grado di completamento ' + str(len(sim.network.edges())*100/(num_nodes**2 - num_nodes)))
	print('# Tweets = ' + str(len(sim.tweet)))
	print('# Retweets = ' + str(len(sim.retweet)))
	print("#" * 40)
	sim.personal_follow()
	sim.step_tweet()
	sim.step_retweet()
	sim.attachment_eval()
	sim.now = step
	evo.write(str(len(sim.network.edges()))+'\n')
	evo.close()
	clust.write(str(nx.transitivity(sim.network))+'\n')
	clust.close()
	assor.write(str(nx.degree_assortativity_coefficient(sim.network))+'\n')
	assor.close()
	homo.write(str(nx.attribute_assortativity_coefficient(sim.network,'toptopic'))+'\n')
	homo.close()
	if not 0 in list(sim.network.in_degree().values()):
		spath.write(str(nx.average_shortest_path_length(sim.network))+'\n')
	else:
		spath.write('nullo\n')	
	spath.close()

	if step == 200:
		top = dds[0]
		bottom = dds[-1]
		user = sim.get_user(top)
		j = np.random.choice(sim.topics, 1, p=user.pi)[0]
		sim.tweet[bottom, step] = [bottom, step, j, 1, 0, top]
		sim.retweet[top, step] = [bottom, step, j, 1, 0, top]

		with open("prescelto.txt", "w") as f: 
			f.write(str(bottom) + "\n" + str(top)) 

df.to_csv(path_or_buf='class_complete.csv',sep=",",header=True, index=True)

graph = open('graph_end.csv','w')
graph.write('id,weight\n')
for n in sim.network.nodes():
	graph.write(str(n) + ',' + str(network.in_degree().get(n)) + '\n')
graph.close()

edg = open('edges_end.csv','w')
edg.write('Source,Target\n')
for e in sim.network.edges():
	edg.write(str(e[0]) + ',' + str(e[1]) + '\n')
edg.close()
