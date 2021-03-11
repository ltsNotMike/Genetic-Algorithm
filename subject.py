from lane import Lane, Segment
from point import Point
import numpy as np

class Subject:
	def __init__(self, size_x, size_y):
		# Decide what collection this should be
		self.lanes = []
		self.size_x = size_x
		self.size_y = size_y

	@classmethod
	def crossover(cls, parent1, parent2):
		# Return new subject that is a crossover of two other subjects
		pass

	@classmethod
	def copy(cls, parent):
		# Return new subject that is a copy of another subject
		pass
	

	@classmethod
	def shortest(cls, points, size_x, size_y):
		obj = cls(size_x, size_y)
		i = 0
		while i < len(points):
			obj.lanes.append(Lane.shortest(points[i], points[i + 1]))
			i += 2
		return obj
		

	def mutate(self, probability):
		# Mutate each gen with some probability
		pass
	
	def fitness(self, weights):
		# Scores
		# 0. Number of crosses
		# 1. Size of lanes
		# 2. Number of lanes
		# 3. Number of lanes outside  
		scores = [0, 0, 0, 0]
		visited_points = []

		# Every lane on this solution of the board
		for lane in self.lanes:
			p = Point(lane.start.x, lane.start.y)
			if p in visited_points:
				scores[0] += 1
			else:
				visited_points.append(Point.copy(p))

			# Analaze every segement of the lane
			for segement in lane.segments:
				scores[1] += abs(segement.size)
				scores[2] += 1
				
				# Get every point on the way of this segment
				for i in range(abs(segement.size)):
					# Change point 
					if segement.size < 0:
						p.add(Segment(segement.direction, -1))
					else: 
						p.add(Segment(segement.direction, 1))

					# Update score of crosses if the point was visited
					if p in visited_points:
						scores[0] += 1
					else:
						visited_points.append(Point.copy(p))

				# Update score of outside segmets if point is outside 
				if p.x < 0 or p.x > self.size_x or p.y < 0 or p.y > self.size_y:
					scores[3] += 1
					
		scores = np.multiply(scores, weights)
		return np.sum(scores)
	
	def __repr__(self):
	 	return str(self.lanes)
	
	# FIXME: This is old version
	# @classmethod
	# def random(cls, points, size_x, size_y):
	# 	# Create subject with random lanes
	# 	obj = cls()
	# 	i = 0
	# 	while i < len(points):
	# 		obj.lanes.append(Lane.random(points[i], points[i + 1], size_x, size_y))
	# 		i += 2
	# 	return obj