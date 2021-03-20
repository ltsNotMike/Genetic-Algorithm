from point import Point
import random as randomGenerator
from math import floor

def sign(x: int) -> int:
	return 0 if x >= 0 else 1

class Segment:
	def __init__(self, direction: str, size: int):
		self.direction = direction # X or Y
		self.size = size  # Signed Int

	def __repr__(self) -> str:
		return f'({self.direction}, {self.size})'
	
	@classmethod
	def copy(cls, parent):
		return cls(parent.direction, parent.size)

class Lane:
	size_x = 1;
	size_y = 1;
	def __init__(self, x1: int, y1: int, x2: int, y2: int):
		self.segments = []
		self.start = Point(x1, y1)
		self.end = Point(x2, y2)
	
	@classmethod
	def copy(cls, parent: "Lane") -> "Lane": # Type pre define 
		obj = cls(parent.start.x, parent.start.y, parent.end.x, parent.end.y)
		for segment in parent.segments:
			obj.segments.append(Segment.copy(segment))
		return obj

	def mutate_simple(self, segment_index: int) -> None:
		# FIXME: This modifies the subjects in such a way that they should not pass tests
		phrase = -1 if randomGenerator.random() < 0.5 else 1
		direction = 'X' if self.segments[segment_index].direction == 'Y' else 'Y'

		if segment_index == 0 or self.segments[segment_index - 1].direction == self.segments[segment_index].direction:
			self.segments.insert(segment_index, Segment(direction, phrase))
			segment_index += 1
		else:
			self.segments[segment_index - 1].size += phrase 

		if segment_index == len(self.segments) - 1 or self.segments[segment_index + 1].direction == self.segments[segment_index].direction:
			self.segments.insert(segment_index + 1, Segment(direction, -phrase))
		else:
			self.segments[segment_index + 1].size -= phrase
		
		# Watchout for adding new segments and len(self.segments)
		

	def mutate_complex(self) -> None:
		# TODO: This method doesnt yet have a breaking and choosing of the segment
		""" Method selects one segment, breaks it in two segments\n
			New segments have sizes [0, size of parent segment]\n
			One of those segments then gets mutated """

		segment_index = randomGenerator.randint(0, len(self.segments) - 1)
		is_previous = randomGenerator.random() < 0.5

		# Benford's law distribution
		# Its more likely that smaller number is choosen
		size_new_segment = pow(abs(self.segments[segment_index].size), randomGenerator.random())
		# Size has to be an integer
		size_new_segment = floor(size_new_segment)
		# Size has to be the same sign as parent
		size_new_segment *= -1 if sign(self.segments[segment_index].size) else 1

		if size_new_segment == self.segments[segment_index].size:
			# No division needed, the whole segment is being moved
			self.mutate_simple(segment_index)
		else:
			new_segment_direction = self.segments[segment_index].direction
			self.segments[segment_index].size -= size_new_segment
			self.segments.insert(segment_index, Segment(new_segment_direction, size_new_segment))
			if is_previous:
				# The first part of the segment will be mutated
				self.mutate_simple(segment_index)
			else:
				# The second part of the segment will be mutated
				self.mutate_simple(segment_index + 1)

		self.normalize()

	def normalize(self):
		i = 0
		while i < len(self.segments) - 1:
			# If two segments are going the same way
			if sign(self.segments[i].size) == sign(self.segments[i + 1].size) and self.segments[i].direction == self.segments[i + 1].direction:
				# Concat the two
				self.segments[i].size += self.segments[i + 1].size
				self.segments.pop(i + 1)
				i -= 1
			elif self.segments[i].size == 0:
				# Delete this one
				self.segments.pop(i)
				i -= 1
			i += 1

	def test(self) -> bool:
		""" Test if the lane connects the start and the end """
		correct_value = [self.end.x - self.start.x, self.end.y - self.start.y]
		value = [0, 0]
		for segment in self.segments:
			if segment.direction == "X":
				value[0] += segment.size
			else:
				value[1] += segment.size
		return value == correct_value

	@classmethod
	def random(cls, p1: Point, p2: Point, size_x: int, size_y: int, random_segments: int) -> "Lane":
		""" Methed creates new lane with specified number of random segments\n
			New object will have the maximum of (random_segments + 2) number of segments """
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
	 return f"{self.segments}\n"

	