import numpy as np


class Simulation:
	def __init__(self, topic):
		self.topic = topic
		self.tweet = {}
		self.retweet = {}
		self.dtag = {}
		self.id = 1

	def generate_new_user(self):
		attr = {}
		attr['id'] = self.id
		self.id += 1

		##### personal interest
		attr['pi'] = np.random.random_sample((1,self.topic)).tolist()[0]

		##### timezone (refer to documentation)
		tz = np.zeros(12)
		i = np.random.randint(13) + 4
		i = i % 12

		## low activity - CHANGE
		for k in range(4):
		    tz[(k + i) % 12] = np.random.random_sample((1,1)).tolist()[0][0]
		i = (i + 4) % 12
		## high activity - CHANGE
		for k in range(4):
		    tz[(k + i) % 12] = np.random.random_sample((1,1)).tolist()[0][0] - 5

		attr['tz'] = tz.tolist()
		attr['followers'] = []
		attr['following'] = []

		interest = []
		for j in range(len(attr['pi'])):
		    if attr['pi'][j] > 0.5:
		        interest.append(j)
		attr['interest'] = interest
		return attr

	def post(self, user, time):

		return True

	def repost(self, user, time):

		return True

	def generate_fov(self, user, time):
		return True
