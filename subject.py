from lane import Lane, Segment
from point import Point
from random import randint, random as randfloat
import numpy as np

class Subject:
	def __init__(self, size_x, size_y):
		# Decide what collection this should be
		self.lanes = []
		self.size_x = size_x
		self.size_y = size_y

	@classmethod
	def copy(cls, parent: object) -> object:
		obj = cls(parent.size_x, parent.size_y)
		for lane in parent.lanes:
			obj.lanes.append(Lane.copy(lane))
		return obj	

	@classmethod
	def shortest(cls, points: [object], size_x: int, size_y: int) -> object:
		obj = cls(size_x, size_y)
		i = 0
		while i < len(points):
			obj.lanes.append(Lane.shortest(points[i], points[i + 1]))
			i += 2
		return obj
		

	def mutate(self) -> None:
		lane_index = randint(0, len(self.lanes) - 1)
		self.lanes[lane_index].mutate_complex()
	
	def fitness(self, weights: list) -> int:

		# Scores
		# 0. Number of crosses
		# 1. Size of lanes
		# 2. Number of segments
		# 3. Number of lanes outside  
		number_of_crossings = 0
		length_of_lanes = 0
		number_of_segments = 0
		number_of_lanes_outside = 0
		
		visited_points = []

		# Every lane on this solution of the board
		for lane in self.lanes:
			p = Point(lane.start.x, lane.start.y)
			if p in visited_points:
				number_of_crossings += 1
			else:
				visited_points.append(Point.copy(p))

			# Analaze every segment of the lane
			for segment in lane.segments:
				length_of_lanes += abs(segment.size)
				number_of_segments += 1
				
				# Get every point on the way of this segment
				for i in range(abs(segment.size)):
					# Change point 
					if segment.size < 0:
						p.add(Segment(segment.direction, -1))
					else: 
						p.add(Segment(segment.direction, 1))

					# Update score of crosses if the point was visited
					if p in visited_points:
						number_of_crossings += 1
					else:
						visited_points.append(Point.copy(p))

				# Update score of outside segmets if point is outside 
				if p.x < 0 or p.x > self.size_x or p.y < 0 or p.y > self.size_y:
					number_of_lanes_outside += 1
					
		scores = np.multiply([
			number_of_crossings,
			length_of_lanes,
			number_of_segments,
			number_of_lanes_outside
		], weights)
		return np.sum(scores)
	
	@classmethod
	def crossover(cls, mother: "Subject", father: "Subject", gen_ratio: float) -> "Subject":
		""" Return new subject that is a crossover of mother and father genes\n
			gen_ratio is a number [0,1] it defines the propability of inheriting gen from father\n"""

		obj = Subject(mother.size_x, mother.size_y)
		for gen_index in range(len(mother.lanes)):
			gen = Lane.copy(mother.lanes[gen_index] if randfloat() >= gen_ratio else father.lanes[gen_index])
			obj.lanes.append(gen)
		return obj

	def test(self):
		for lane in self.lanes:
			if not lane.test():
				return False
		return True

	def __repr__(self):
		res = "Subject:\n"
		for lane in self.lanes:
			res += str(lane)
		return res
	
	@classmethod
	def random(cls, points, size_x, size_y, ):
		obj = cls()
		i = 0
		while i < len(points):
			obj.lanes.append(Lane.random(points[i], points[i + 1], size_x, size_y))
			i += 2
		return obj