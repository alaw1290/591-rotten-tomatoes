path = '../data/'

def weighted_average(user_vector,critics_sim,movie_keys,critic_keys,movie_critic):
	'''using the critics similarity scores set, compute new vector with weighted predictions for unrated movies
	using similarity for weight'''

	prediction_vector = [i for i in user_vector]

	for i in range(len(prediction_vector)):

		#compute prediction for unrated movies
		if prediction_vector[i] == 0:

			weight_total = 0
			score_total = 0

			#check which critics also rated that movie
			movie = movie_keys[i]

			for c in set(movie_critic[movie].keys()).intersection(critics_sim.keys()): 
				if(movie_critic[movie][c]):
					val = 1
				else:
					val = -1

				weight_total += abs(critics_sim[c])
				score_total += val * critics_sim[c]

			if weight_total > 0:
				prediction_vector[i] = score_total / weight_total

	return prediction_vector


def weighted_sums(user_vector,critics_sim,movie_keys,critic_keys,movie_critic,avg_ratings):

	prediction_vector = [i for i in user_vector]
	avg_user_ratiing = sum(user_vector)/len([0 for i in user_vector if i != 0])

	for i in range(len(prediction_vector)):
		if prediction_vector[i] == 0:
			weight_total = 0
			value_total = 0
			movie = movie_keys[i]

			for c in set(movie_critic[movie].keys()).intersection(critics_sim.keys()):
				
				average_rating = avg_ratings[c]
				if(movie_critic[movie][c]):
					val = 1
				else:
					val = -1
				weight_total += abs(critics_sim[c])
				value_total += (val - average_rating)*critics_sim[c]

			if weight_total > 0:
				prediction_vector[i] = value_total/weight_total

	return prediction_vector


def user_based_top_k(user_vector, critics_sim, movie_keys, critic_keys, movie_critic, k):
	'''return predictions based on the % of critics that rated movie i to what degree'''

	#if not enough k critics then reduce to size of the critic set
	if k > len(critics_sim):
		k = len(critics_sim)

	#only use top k most signficant similar results, grab top 10
	top_k_critics = sorted([(key,critics_sim[key]) for key in critics_sim], key = lambda tup: abs(tup[1]))[-k:]
	prediction_vector = [i for i in user_vector]

	#make predictions for empty values
	for i in range(len(prediction_vector)):
		if prediction_vector[i] == 0:
			
			# weight_total = 0
			value_total = 0
			movie = movie_keys[i]

			for critic in top_k_critics:
				name = critic[0]
				if(name in movie_critic[movie]):
					# weight_total += 1
					if movie_critic[movie][name]:
						value_total += 1
					else:
						value_total -= 1

			if True: #weight_total > 0:
				prediction_vector[i] = value_total / k
			
	return prediction_vector
