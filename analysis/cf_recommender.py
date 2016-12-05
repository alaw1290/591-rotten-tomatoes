
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


def weighted_sums(user_vector,critics_sim,movie_keys,critic_keys,movie_critic,critic_movie):

        prediction_vector = [i for i in user_vector]
        avg_user_ratiing = sum(user_vector)/len([0 for i in user_vector if i != 0])

        for i in range(len(prediction_vector)):
                if prediction_vector[i] == 0:
                        weight_total = 0
                        value_total = 0

                        movie = movie_keys[i]

                        for c in set(movie_critic[movie].keys()).intersection(critics_sim.keys()):
                                suM = 0
                                print(c)
                                for movie in critic_movie[c]:
                                        suM += int(critic_movie[c][movie])
                                average_rating = suM/len(critic_movie[c])
                                if(movie_critic[movie][c]):
                                        val = 1
                                else:
                                        val = -1
                                weight_total += abs(critics_sim[c])
                                value_total += (val - average_rating)*critics_sim[c]
                        if weight_total > 0:
                                prediction_vector[i] = value_total/weight_total

        return prediction_vector


def user_based_top_k(user_vector, critics_sim, movie_keys, critic_keys, movie_critic, k, movie):

        if k > len(critics_sim):
                k = len(critics_sim)
                print('Reduced to %k' %(k))
        print(len(critics_sim))
        criticSim = sorted([(k,critics_sim[k]) for k in critics_sim], key = lambda tup: tup[1])
        prediction_vector = [i for i in user_vector]

        rec_items = [0]*len(prediction_vector)
        
        for i in range(k):
                print(critic_keys.index(criticSim[i][0]))
                rec_items = [rec_items[l] + movie[critic_keys.index(criticSim[i][0])][l]/k for l in range(len(prediction_vector))]
        for i in range(len(prediction_vector)):
                if prediction_vector[i] == 0:
                        prediction_vector[i] = rec_items[i]
                        
        return prediction_vector
