
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





