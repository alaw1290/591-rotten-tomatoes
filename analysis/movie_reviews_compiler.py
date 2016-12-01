import pickle
import json
import numpy as np

path = '../data/'

def import_pickle():
	'''Import and convert movie_reviews pickle files to following dictionaries:
		- movie_critic: dict of movies and corresponding critics that thumbs up/down them
		- critic_movie: dict of critics and corresponding movies that they thumbs up/down '''

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

	return movie_critic, critic_movie

def export_matrix(movie_critic,critic_movie):
	'''Uses corresponding movie_critic and critic_movie to construct numpy matrix and critic/movie key indicies (note only about 0.481196028% full) '''

	movie_keys = [k for k in movie_critic]
	critic_keys = [k for k in critic_movie]

	matrix = []

	for c in critic_keys:
		row = []
		for m in movie_keys:
			try:
				row.append(int(critic_movie[c][m]))
			except KeyError:
				row.append(0)
		matrix.append(row)

	return np.toarray(matrix),movie_keys,critic_keys
