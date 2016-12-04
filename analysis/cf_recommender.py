
path = '../data/'

def weighted_average(user_vector,critics_sim,matrix,critic_keys):
	'''using the critics similarity scores set, compute new vector with weighted predictions for unrated movies
	using similarity for weight'''

	prediction_vector = [i for i in user_vector]
	count = 0

	for i in range(len(prediction_vector)):
		#compute prediction for unrated movies
		if prediction_vector[i] == 0:

			for cs in critics_sim:
				weight_total = 0
				score_total = 0
				key = critic_keys.index(cs[0])
				if matrix[key][i] != 0:
					weight_total += cs[1]
					score_total += matrix[key][i] * cs[1]

			if weight_total > 0:
				prediction_vector[i] = score_total / weight_total
				print(i)
				
	return prediction_vector





