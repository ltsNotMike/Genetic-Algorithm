from point import Point
class Solution:

	@property
	def size_x(self):
		return self.__size_x

	@property
	def size_y(self):
		return self.__size_y
	
	@property
	def population_size(self):
		return self.__size_pop

	def __init__(self, x, y, points, population_size, weights):
		self.__size_x = x
		self.__size_y = y
		self.__size_pop = population_size
		self.points = points
		self.weights = weights

	@classmethod
	def from_file(cls, file_name, population_size, weights):
		obj = None
		with open(file_name, "r", encoding="utf-8") as file:
			values = file.readline().split(';')
			size_x = int(values[0])
			size_y = int(values[1])
			points = []
			for line in file:
				values = line.split(';')
				points.append(Point(int(values[0]), int(values[1])))
				points.append(Point(int(values[2]), int(values[3])))
			obj = cls(size_x, size_y, points, population_size, weights)
			file.close()

		return obj