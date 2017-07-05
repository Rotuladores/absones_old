import numpy as np
from user import User

class Simulation:
	def __init__(self, topics, total_users):
		self.topics = topics
		self.tweet = {}
		self.retweet = {}
		self.dtag = {}
		self.user_id = 1
		self.total_users = total_users
		self.users = {}
		self.now = 0

		# Iper-parameters
		self.alpha = 0.8
		self.beta = 0.6
		self.gamma = 0.4
		
	def add_user(self, user):
		self.users[user.id] = user
		
	def post(self, user, time):
		j = np.random.choice(self.topics, 1, p=user.pi)[0]
		print(j)

		if user.pi[j] >= user.pi_average:
			likability = Simulation.random_high(0.7)
			dislakability = np.random.random()
		else:
			dislakability = Simulation.random_high(0.7)
			likability = np.random.random()

		dtag = self.generate_dtag(user)
		if dtag:
			self.get_user(dtag).add_dtag(self.now, user)
		
		self.tweet[user.id, time] = [j, likability, dislakability, dtag]


	def generate_dtag(self, user):
		# TODO
		return None
		
	def repost(self, user, time):
		# TODO
		return None

	#user1 -follow-> user2
	def new_follow(self, user1, user2):
		self.get_user(user1).add_following(user2)
		self.get_user(user2).add_follower(user1)

		# change attachment to random-high
		self.get_user(user1).attachment[user2] = Simulation.random_high(0.8)

	def get_user(self, id):
		return self.users[id]

	def step_tweet(self):
		for u in self.users.keys():
			# Calculate probability of TWEET
			user = self.get_user(u)
			prob = self.alpha * \
				   user.tz[self.now % 12] * \
				   len(user.followers) / \
				   self.total_users
			#print(prob)

			# Tweet if possibile
			if np.random.random() <= prob:
				print('%d tweets' % u)
				self.post(user, self.now)
			

	def step_retweet(self):
		# TODO
		return True

	def step_evaluation(self):
		for u in self.users.keys():
			#Get FOV of U
			user = self.get_user(u)
			fov = user.generate_fov(self.now, self.tweet, self.retweet)
			print('fov:')
			print(fov)
			for twt in fov[0]:
				#Evaluate attachment
				print("EVALUATION")
				print(twt)
				

			for rtwt in fov[1]:
				#TODO EVALUATE RETWEET
				pass

			for dtag in fov[2]:
				#TODO EVALUATE DTAG
				pass
			
			
			
		return True
	
	@staticmethod
	def random_high(mean):
		return np.random.triangular(0.4, mean, 1)

	@staticmethod
	def random_low(mean):
		return np.random.triangular(0, mean, 0.6)

	

def test():
	import networkx as nx
	sim = Simulation(10,50)
	network = nx.gnm_random_graph(sim.total_users, \
								  sim.total_users, \
								  directed=True)

	# generate users
	print('Generation')
	print('='*20)
	for n in network.nodes():
		u1 = User(n, sim.topics)
		sim.add_user(u1)
		print(sim.get_user(n))

	# add follow
	print('Follow')
	print('='*20)
	for n in network.nodes():
		sim.new_follow(n, (n+1) % sim.total_users)
		sim.new_follow(n, (n+2) % sim.total_users)
		sim.new_follow(n, (n+3) % sim.total_users)
		sim.new_follow(n, (n+4) % sim.total_users)
		sim.new_follow(n, (n+5) % sim.total_users)
		sim.new_follow(n, (n+6) % sim.total_users)
		print(sim.get_user(n).get_attachment(n+1))

	print('Simulation')
	print('='*20)

	while(True):
		print('Time: %d' % sim.now)
		sim.step_tweet()
		sim.step_evaluation()
		sim.now += 1

#	sim.get_user(0).generate_fov(0, sim.tweet, sim.retweet)

	
if __name__ == '__main__':
	test()
