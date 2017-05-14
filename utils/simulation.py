import numpy as np


class Simulation:
	def __init__(self, topic, total_users):
		self.topic = topic
		self.tweet = {}
		self.retweet = {}
		self.dtag = {}
		self.id = 1
		self.total_users = total_users

	def generate_new_user(self, node):
		
		node['id'] = self.id
		self.id += 1

		##### personal interest
		pi = np.random.random_integers(100, size=(1,self.topic))[0].tolist()
		sumpi = sum(pi)
		fpi = map(lambda x: float(x)/sumpi, pi)
		node['pi'] = fpi
		node['pi_average'] = np.average(fpi)

		##### timezone (refer to documentation)
		tz = np.zeros(12)
		i = np.random.randint(13) + 4
		i = i % 12

		## low activity
		for k in range(4):
		    tz[(k + i) % 12] = np.random.triangular(0, 0.25, 0.6)
		i = (i + 4) % 12
		## high activity
		for k in range(4):
		    tz[(k + i) % 12] = np.random.triangular(0.4, 0.75, 1)

		node['tz'] = tz.tolist()
		node['followers'] = []
		node['following'] = []

		interest = []
		for j in range(self.topic):
		    if node['pi'][j] > 0.5:
		        interest.append(j)
		node['interest'] = interest
		# return attr

	def post(self, user, time):

		return True

	def repost(self, user, time):

		return True

	def generate_fov(self, user, time):
		return True
