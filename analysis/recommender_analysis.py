import pickle
import numpy as np
import matplotlib.pyplot as plt

path = '../data/'

def construct_dict(file):

	results = pickle.load(open(path + file,'rb'))

	#filter results to non-error ones
	results = [results[i] for i in results if results[i] != 'Error']

	movie_dict = {}

	for user in results:
		indicies = [i[0] for i in user['actual']]
		
		for i in range(len(indicies)):
			val = 0
			if user['actual'][i][1] > 0 and user['predicted'][i][1] > 0:
				val = 1
			if user['actual'][i][1] < 0 and user['predicted'][i][1] < 0:
				val = 1
			try:
				movie_dict[str(indicies[i])].append([user['actual'][i][1],user['predicted'][i][1],val])
			except KeyError:
				movie_dict[str(indicies[i])] = [[user['actual'][i][1],user['predicted'][i][1],val]]

	#actual,predicted,accuracy
	return movie_dict

def find_table_values(movie_dict):

	#for baseline & method, return (RMSE , % accuracy , least accurate , most accurate)
	movie_keys = pickle.load(open(path + 'movie_keys.pkl','rb'))

	#baseline

	# times wrong, times right
	movie_accuracy = {}

	count = 0
	rmse_total = 0
	total_correct = 0

	#baseline
	for m in movie_dict:
		for i in range(len(movie_dict[m])):

			if(movie_dict[m][i][0] != 1):	
				rmse_total += 4
				try:
					movie_accuracy[m][0] -= 1
				except KeyError:
					movie_accuracy[m] = [-1,0]

			else:
				total_correct += 1
				try:
					movie_accuracy[m][1] += 1
				except KeyError:
					movie_accuracy[m] = [0,1]

			count += 1

	least_accurate = sorted([(movie_accuracy[m][0], movie_keys[int(m)] , abs(movie_accuracy[m][0]) + movie_accuracy[m][1] ) for m in movie_accuracy], key=lambda x: x[0])[0]
	most_accurate = sorted([(movie_accuracy[m][1] , movie_keys[int(m)] , abs(movie_accuracy[m][0]) + movie_accuracy[m][1] ) for m in movie_accuracy], key=lambda x: x[0])[-1]

	baseline = ((rmse_total/count)**0.5,total_correct/count, least_accurate, most_accurate)

	#method

	# times wrong, times right
	movie_accuracy = {}

	count = 0
	rmse_total = 0
	total_correct = 0

	#baseline
	for m in movie_dict:
		for i in range(len(movie_dict[m])):

			rmse_total += (movie_dict[m][i][1] - movie_dict[m][i][0])**2

			if(movie_dict[m][i][2] != 1):	
				try:
					movie_accuracy[m][0] -= 1
				except KeyError:
					movie_accuracy[m] = [-1,0]

			else:
				total_correct += 1
				try:
					movie_accuracy[m][1] += 1
				except KeyError:
					movie_accuracy[m] = [0,1]

			count += 1

	least_accurate = sorted([(movie_accuracy[m][0], movie_keys[int(m)] , abs(movie_accuracy[m][0]) + movie_accuracy[m][1] ) for m in movie_accuracy], key=lambda x: x[0])[0]
	most_accurate = sorted([(movie_accuracy[m][1] , movie_keys[int(m)] , abs(movie_accuracy[m][0]) + movie_accuracy[m][1] ) for m in movie_accuracy], key=lambda x: x[0])[-1]

	method = ((rmse_total/count)**0.5,total_correct/count, least_accurate, most_accurate)

	return baseline,method	

def plot_data_barh(movie_dict):

	# number of bins for y axis
	n = 20
	positive_hits = [0]*n
	positive_misses = [0]*n
	negative_hits = [0]*n
	negative_misses = [0]*n

	positive_y = list(range(n))
	negative_y = list(range(-1,-(n+1),-1))


	#actual,predicted,accuracy
	for m in movie_dict:
		for i in range(len(movie_dict[m])):
			val = min(19,int(movie_dict[m][i][1]*n))
			#positive
			if movie_dict[m][i][0] == 1:
				#hit
				if movie_dict[m][i][2] > 0:
					positive_hits[val] += 1
				#miss
				else:
					positive_misses[val] -= 1
			#negative
			else:
				#hit
				if movie_dict[m][i][2] > 0:
					negative_hits[val] -= 1
				#miss
				else:
					negative_misses[val] += 1

	plt.rcdefaults()

	plt.barh(positive_y, positive_hits, align='edge',color='blue')
	plt.barh(positive_y, positive_misses, align='edge',color='orange')
	plt.barh(negative_y, negative_hits, align='edge',color='blue')
	plt.barh(negative_y, negative_misses, align='edge',color='orange')

	plt.yticks(negative_y + positive_y,[str(i) for i in list(np.arange(-0.05,-1.05,-0.05))] + [str(i) for i in list(np.arange(0,1,0.05))])

	plt.show()







