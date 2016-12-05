import pickle
import cf_recommender
import similarity_functions
import movie_reviews_compiler
##      WEIGHTED AVERAGE
path = '../data/'

def run_test_data_weighted_avg():
    audience_names      = pickle.load(open(path + 'audience_names.pkl','rb'))
    audience_test_data  = pickle.load(open(path + 'audience_test_data.pkl','rb'))

    movie_critic, critic_movie, matrix, movie_keys, critic_keys = movie_reviews_compiler.import_pickle()

    toReturn = {}
    '''list of (Audience Name, masked value, masked index, difference between approx. and actual)'''
    RMSD     = []
    
    for aud_review_index in range(len(audience_test_data)):
        print('Test Vector: ' + audience_names[aud_review_index].split("'s")[0])

        toReturn[audience_names[aud_review_index].split("'s")[0]] = {}
        actualVals      = []
        predictedVals   = []
        
        relevant_indeces = [i for i in range(len(audience_test_data[aud_review_index])) if audience_test_data[aud_review_index][i] != 0]
        rsmd = 0
        for i in relevant_indeces:
            print('Masking index: ' + str(i) + ' ('+str(relevant_indeces.index(i)+1) + ' out of ' + str(len(relevant_indeces)) +')')
            masked_vector       = [val for val in audience_test_data[aud_review_index]]
            masked_vector[i]    = 0
            critic_similarity   = similarity_functions.run_cosine(masked_vector, matrix, movie_critic, movie_keys, critic_keys)
            approx_vector       = cf_recommender.weighted_average(masked_vector, critic_similarity, movie_keys, critic_keys, movie_critic)

            actualVals.append((i,audience_test_data[aud_review_index][i]))
            predictedVals.append((i,approx_vector[i]))

            print(str(abs(audience_test_data[aud_review_index][i] - approx_vector[i])))
            
            rsmd += (audience_test_data[aud_review_index][i] - approx_vector[i])**2
        RMSD.append((audience_names[aud_review_index].split("'s")[0], (rsmd/len(relevant_indeces))**1/2))
        
        toReturn[audience_names[aud_review_index].split("'s")[0]]['actual'] = actualVals
        toReturn[audience_names[aud_review_index].split("'s")[0]]['predicted'] = predictedVals
        toReturn[audience_names[aud_review_index].split("'s")[0]]['RMSE'] = audience_names[aud_review_index].split("'s")[0], (rsmd/len(relevant_indeces))**1/2


    pickle.dump(toReturn, open(path + 'weighted_avg_test_data.pkl','wb'))
    
    return RMSD
