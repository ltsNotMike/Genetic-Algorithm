from point import Point
import random as randomGenerator

class Segment:
	def __init__(self, direction, size):
		self.direction = direction # X or Y
		self.size = size  # Signed Int

	def __repr__(self):
		return f'({self.direction}, {self.size})'

class Lane:
	size_x = 1;
	size_y = 1;
	def __init__(self, x1, y1, x2, y2):
		self.segments = []
		self.start = Point(x1, y1)
		self.end = Point(x2, y2)
	
	@classmethod
	def copy(cls, parent):
		obj = cls(parent.start.x, parent.start.y, parent.end.x, parent.end.y)
		for segment in parent.segements:
			obj.segments.append(segment)
		return obj

	def mutate(self):
		# Go through the entire path and determine if they should be mutated
		# Mutation can go in two different ways
		# 	First is addition of segment
		# 	If segment is added then new opposite segment has to be added somewhere
		#
		#	Second is deletion of segment
		#	If a segment was deleted then a similar segment must be added somewhere
		pass
	
	@classmethod
	def random(cls, p1, p2, size_x, size_y, random_segments: int):
		obj = cls(p1.x, p1.y, p2.x, p2.y)
		point = Point.copy(p1)
		i = 0
		s = None
		while i < random_segments or point == p2:
			direction = "X" if randomGenerator.random() > 0.5 else "Y"
			if direction == "X":
				s = int(randomGenerator.random() * (size_x * 2)) - size_x
			elif direction == "Y":
				s = int(randomGenerator.random() * (size_y * 2)) - size_y
			
			segment = Segment(direction, s)
			obj.segments.append(segment)
			point.add(segment)
			i += 1
		
		if point != p2:
			s1 = Segment('X', p2.x - point.x)
			if s1.size != 0:
				obj.segments.append(s1)

			s2 = Segment('Y', p2.y - point.y)
			if s2.size != 0:
				obj.segments.append(s2)

		return obj

	@classmethod
	def shortest(cls, p1, p2):
		obj = cls(p1.x, p1.y, p2.x, p2.y)
		s1 = Segment('X', p2.x - p1.x)
		if s1.size != 0:
			obj.segments.append(s1)

		s2 = Segment('Y', p2.y - p1.y)
		if s2.size != 0:
			obj.segments.append(s2)

		return obj
	
	def __repr__(self):
	 return "\n" + str(self.segments)
