import pickle

path = '../data/'

def import_pickle():
	'''Import and convert movie_reviews pickle files to following dictionaries:
		- movie_critic: dict of movies and corresponding critics that thumbs up/down them
		- critic_movie: dict of critics and corresponding movies that they thumbs up/down '''

	try:
		movie_critic = pickle.load(open(path + "movie_critic.pkl", "rb" ) )
		critic_movie = pickle.load(open(path + "critic_movie.pkl", "rb" ) )
		matrix = pickle.load(open(path + "matrix.pkl", "rb" ) )
		movie_keys = pickle.load(open(path + "movie_keys.pkl", "rb" ) )
		critic_keys = pickle.load(open(path + "critic_keys.pkl", "rb" ) )

		return movie_critic, critic_movie, matrix, movie_keys, critic_keys

	except FileNotFoundError:
		data = pickle.load(open(path + 'movie_reviews.pkl', 'rb'))

		movie_critic = {}
		critic_movie = {}

		for m in data:

			critics = {}
			for c in data[m]:

				val = data[m][c]['IsFresh']
				critics[c] = val

				try:
					critic_movie[c].update({m:val})
				except KeyError:
					critic_movie[c] = {m:val}

			movie_critic[m] = critics

		m,mk,ck = convert_matrix(movie_critic,critic_movie)
		return movie_critic, critic_movie, m,mk,ck

def convert_matrix(movie_critic,critic_movie):
	'''Uses corresponding movie_critic and critic_movie to construct numpy matrix and critic/movie key indicies (note only about 0.777625423% very sparse) '''

	movie_keys = [k for k in movie_critic]
	critic_keys = [k for k in critic_movie]

	matrix = []

	for c in critic_keys:
		row = []
		for m in movie_keys:
			try:
				if(critic_movie[c][m]):
					row.append(1)
				else:
					row.append(-1)
			except KeyError:
				row.append(0)
		matrix.append(row)

	return matrix,movie_keys,critic_keys

def export_pickle(movie_critic,critic_movie,matrix,movie_keys,critic_keys):
	'''Export everything and store as pickle files in the data folder specified in path'''

	pickle.dump(movie_critic, open(path +  "movie_critic.pkl", "wb" ) )
	pickle.dump(critic_movie, open(path +  "critic_movie.pkl", "wb" ) )
	pickle.dump(matrix, open(path +  "matrix.pkl", "wb" ) )
	pickle.dump(movie_keys, open(path +  "movie_keys.pkl", "wb" ) )
	pickle.dump(critic_keys, open(path +  "critic_keys.pkl", "wb" ) )




