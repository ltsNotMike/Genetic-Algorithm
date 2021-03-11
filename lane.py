from point import Point
import random

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
	
	def normalize(self):
		# Method is removing all Xx xX Yy yY from path
		# This type of neibouring gens are canceling each other out
		pass

	def is_outside(self, size_x, size_y):
		# Method analizes the genes if they are outside of the given size
		return False
	
	def mutate(self):
		# Go through the entire path and determine if they should be mutated
		# Mutation can go in two different ways
		# 	First is addition of segment
		# 	If segment is added then new opposite segment has to be added somewhere
		#
		#	Second is deletion of segment
		#	If a segment was deleted then a similar segment must be added somewhere
		pass
	
	# FIXME: This method is created with segments of size 1
	# @classmethod
	# def random(cls, p1, p2, size_x, size_y):
	# 	# Create a lane with random segments
	# 	# Add random segments until reaching a destination or achiving maximum size
	# 	cls.size_x = size_x
	# 	cls.size_y = size_y
	# 	cls.max_size = cls.size_x * cls.size_y * 0.5
	# 	obj = cls(p1.x, p1.y, p2.x, p2.y)
	# 	p = Point.copy(obj.start)

	# 	while p != obj.end:	
	# 		# Create new object 
	# 		p = Point.copy(obj.start)
	# 		obj.segments = []

	# 		# First gen can be one of 4
	# 		# Every other gen 
	# 		last_gen = Lane.random_gen()
	# 		p.add(last_gen)
	# 		obj.segments.append(last_gen)
	# 		while len(obj.segments) <= cls.max_size and p != obj.end:
				
	# 			last_gen = Lane.random_gen(last_gen)
	# 			p.add(last_gen)
	# 			obj.segments.append(last_gen)
	# 	return obj

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
		
	@staticmethod
	def random_gen(last_gen=""):
		# Returns random gen that is not opposite to the last gen
		# Example: If last_gen=="x" the method will return only "y" or "Y" or "x"
		pop = []
		if last_gen != "x":
			pop.append("X")
		if last_gen != "X":
			pop.append("x")
		if last_gen != "y":
			pop.append("Y")
		if last_gen != "Y":
			pop.append("y")
		return random.choice(pop)

	max_size = 0

	def __repr__(self):
	 return "\n" + str(self.segments)
