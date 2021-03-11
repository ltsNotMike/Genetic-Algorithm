from subject import Subject
class Population:
	def __init__(self):
		self.subjects = []
		pass

	@classmethod
	def random(cls, population_size, points, size_x, size_y):
		obj = cls()
		for i in range(population_size):
			obj.subjects.append(Subject.random(points, size_x, size_y))
		return obj
	
	@classmethod
	def shortest(cls, population_size, points, size_x, size_y):
		obj = cls()
		for i in range(population_size):
			obj.subjects.append(Subject.shortest(points, size_x, size_y))
		return obj

	@classmethod
	def copy(cls, parent):
		# IDK if this is needed but still could be usefull
		pass

	def estimate(self, weights):
		for subject in self.subjects:
			print(subject.fitness(weights))
