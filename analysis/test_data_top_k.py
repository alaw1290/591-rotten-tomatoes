import pickle
import numpy as np
import cf_recommender as cf
import similarity_functions as sf
import movie_reviews_compiler as mrc

path = '../data/'

def run_test_top_k(cosine=True,k=10):
	'''compute the predictions for masked values in the testing set (user review vectors) using the training set (critic review matrix)
		model for predictions: average of top k critics using cosine similiarity'''

	#get testing data
	audience_names              = pickle.load(open(path + 'audience_names.pkl','rb'))
	audience_review_test_set    = pickle.load(open(path + 'audience_test_data.pkl','rb'))

	#get training data
	movie_critic, critic_movie, matrix, movie_keys, critic_keys = mrc.import_pickle()

	#store results for pickle
	top_k_results = {}

	for aud_review_index in range(len(audience_review_test_set)):

		name = audience_names[aud_review_index].split("'s")[0]
		print('\nTest Vector: ' + name)
		test_vector = audience_review_test_set[aud_review_index]

		#find indicies of masks for testing
		reviewed_indicies = [i for i in range(len(test_vector)) if test_vector[i] != 0]

		#if there are more than 1 reviews for the user:
		if(len(reviewed_indicies) > 1):
			actual_vals = []
			prediced_vals = []
			av = []
			pv = []
			
			for mask in reviewed_indicies:

				#mask selected index
				vector = [i for i in test_vector]
				vector[mask] = 0

				#compute predicted value
				if(cosine):
					critics_sim = sf.run_cosine(vector,matrix,movie_critic,movie_keys,critic_keys)
				else:
					critics_sim = sf.run_pearson(vector,matrix,movie_critic,movie_keys,critic_keys)
					
				result_vector = cf.user_based_top_k(vector,critics_sim,movie_keys,critic_keys,movie_critic,k)

				print('\tPredicted for index ' + str(mask) + ': ' + str(result_vector[mask]))
				print('\tActual for index ' + str(mask) + ':    ' + str(test_vector[mask]))

				prediced_vals.append(result_vector[mask])
				actual_vals.append(test_vector[mask])

				av.append((mask,test_vector[mask]))
				pv.append((mask,result_vector[mask]))

			#calculate accuracy using the root mean square error value
			RMSE = float(((sum([(actual_vals[i]-prediced_vals[i])**2 for i in range(len(reviewed_indicies))]))/len(reviewed_indicies))**0.5)

			print('\n\tRMSE for Test Vector: 				' + str(RMSE))

			top_k_results[name] = {'actual':av,'predicted':pv,'RMSE':RMSE}
		else:
			print('\n\tOnly 1 review not predictable')
			top_k_results[name] = 'Error'

	#export weighted sums results
	if(cosine):
		pickle.dump(top_k_results, open(path +  "top_k_results_cosine.pkl", "wb" ) )
	else:
		pickle.dump(top_k_results, open(path +  "top_k_results_pearson.pkl", "wb" ) )
		
	return top_k_results
