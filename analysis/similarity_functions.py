import operator
import scipy.stats

path = '../data/'

def find_critics(user_vector,movie_critic,movie_keys, critic_keys):
	'''with the user input row and corresponding adjacency lists, return the set of critics that share at least one common movie rating'''

	result_set = set()

	#for each movie the user rated
	for i in range(len(user_vector)):
		
		if(user_vector[i] != 0):
			#find corresponding movie title
			movie_title = movie_keys[i]
			
			#find critics that rated movie in the same way:
			if(user_vector[i] > 0):
				rating = True
			else:
				rating = False				
			for c in movie_critic[movie_title]:
				if movie_critic[movie_title][c] == rating:
					#store critics to result set
					result_set.add(c)

	return result_set

def cosine_similarity(user_vector,critic_vector):
	'''calculates the cosine similarity of two vectors'''
	return sum([user_vector[i] * critic_vector[i] for i in range(len(user_vector))]) / ( len([i for i in user_vector if i != 0])**0.5 * len([i for i in critic_vector if i != 0])**0.5 )

def pearsonr_correlation(user_vector,critic_vector):
	'''calculates the correlation coefficent of two vectors'''
	return scipy.stats.pearsonr(user_vector,critic_vector)

def run_cosine(user_vector,matrix,movie_critic,movie_keys, critic_keys):
	'''given user input vector, compute list of cosine similarities with critics
		drop critics that have 5 or less reviews (do not contribute enough to make any meaningful predictions'''

	#find list of critics that share at least one review
	critic_set = find_critics(user_vector,movie_critic,movie_keys, critic_keys)
	
	critic_sim = {}

	for c in critic_set:
		key = critic_keys.index(c)
		row = matrix[key]

		#ignore critics with less than 5 reviews
		if(len([i for i in row if i != 0]) >= 5):
			#add critic to similiarity set with similarity score
			val = cosine_similarity([i for i in user_vector if i != 0],[row[i] for i in range(len(row)) if user_vector[i] != 0])
			if val != 0:
				critic_sim[c] = val
		# row = [i if i > 0 else 0 for i in matrix[key]]
		# negarow = [-1*i if i < 0 else 0 for i in matrix[key]]

		# if(len([i for i in row if i != 0]) >= 5):
		# 	#ignore critics with less than 5 reviews
			
		# 	#add critic to similiarity set with similarity score
		# 	critic_sim[c] = cosine_similarity(user_vector,row)

		# if(len([i for i in negarow if i != 0]) >= 5):
		# 	#ignore critics with less than 5 reviews
			
		# 	#add critic to similiarity set with similarity score
		# 	critic_sim['nega-' + c] = cosine_similarity(user_vector,negarow)


	return critic_sim

def run_pearson(user_vector,matrix,movie_critic,movie_keys, critic_keys):
	'''given user input vector, compute list of cosine similarities with critics
		drop critics that have 5 or less reviews (do not contribute enough to make any meaningful predictions'''

	#find list of critics that share at least one review
	critic_set = find_critics(user_vector,movie_critic,movie_keys, critic_keys)
	
	critic_sim = {}

	for c in critic_set:
		key = critic_keys.index(c)
		row = matrix[key]

		#ignore critics with less than 5 reviews
		if(len([i for i in row if i != 0]) >= 5):
			#add critic to similiarity set with similarity score
			 val, pval = pearsonr_correlation([i for i in user_vector if i != 0],[row[i] for i in range(len(row)) if user_vector[i] != 0])
			 if val != 0:
			 	critic_sim[c] = (val, pval)
		# row = [i if i > 0 else 0 for i in matrix[key]]
		# negarow = [-1*i if i < 0 else 0 for i in matrix[key]]

		# if(len([i for i in row if i != 0]) >= 5):
		# 	#ignore critics with less than 5 reviews
			
		# 	#add critic to similiarity set with similarity score
		# 	critic_sim[c] = cosine_similarity(user_vector,row)

		# if(len([i for i in negarow if i != 0]) >= 5):
		# 	#ignore critics with less than 5 reviews
			
		# 	#add critic to similiarity set with similarity score
		# 	critic_sim['nega-' + c] = cosine_similarity(user_vector,negarow)


	return critic_sim
