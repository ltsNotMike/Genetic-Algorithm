from subject import Subject
from random import randint, choices
from math import floor
import numpy as np

class Population:
	def __init__(self):
		self.subjects = []
		self.scores = []
		pass

	@classmethod
	def random(cls, population_size, points, size_x, size_y, random_segments):
		obj = cls()
		for i in range(population_size):
			obj.subjects.append(Subject.random(points, size_x, size_y, random_segments))
			obj.scores.append(0)
		return obj
	
	@classmethod
	def shortest(cls, population_size, points, size_x, size_y):
		obj = cls()
		for i in range(population_size):
			obj.subjects.append(Subject.shortest(points, size_x, size_y))
			obj.scores.append(0)
		return obj

	def evaluate(self, weights):
		for i in range(len(self.subjects)):
			self.scores[i] = self.subjects[i].fitness(weights)

	def getAverageFitness(self) -> float:
		return np.average(self.scores)

	def getBestFitness(self) -> float:
		return np.min(self.scores)

	def getWorstFitness(self) -> float:
		return np.max(self.scores)

	def selectTournament(self, tournament_size: float) -> int:
		""" Returns index of the selected subject\n
			Tournament is number (0,1] it reprezents percentage of population """

		number_subjects = floor(len(self.subjects) * tournament_size)
		tournament = []
		for i in range(number_subjects):
			new = randint(0, len(self.subjects) - 1)
			while new in tournament:
				new = randint(0, len(self.subjects) - 1)
			tournament.append(new)

		winner_score = self.scores[tournament[0]]
		winner = tournament[0] 

		i = 1
		while i < len(tournament):
			t = tournament[i]
			if self.scores[t] < winner_score:
				winner_score = self.scores[t]
				winner = t
			i += 1

		return winner

	def selectRoulette(self) -> int:
		""" Returns index of the selected subject """
		weights = []
		for score in self.scores:
			weights.append(1 / score)
		
		return choices([i for i in range(len(self.subjects))], weights)[0]

	def test(self):
		for subject in self.subjects:
			if not subject.test():
				print(subject)
				return False
		return True

	def __repr__(self):
		res = ""
		for i in range(len(self.subjects)):
			res += f"{i} {self.subjects[i]}"
		return res
	
	def best(self):
		return self.scores.index(min(self.scores))
		