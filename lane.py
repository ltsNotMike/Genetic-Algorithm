from point import Point
import random as randomGenerator

def sign(x: int):
	return 0 if x >= 0 else 1

class Segment:
	def __init__(self, direction, size):
		self.direction = direction # X or Y
		self.size = size  # Signed Int

	def __repr__(self):
		return f'({self.direction}, {self.size})'

class Lane:
	size_x = 1;
	size_y = 1;
	def __init__(self, x1: int, y1: int, x2: int, y2: int):
		self.segments = []
		self.start = Point(x1, y1)
		self.end = Point(x2, y2)
	
	@classmethod
	def copy(cls, parent): # Type pre define 
		obj = cls(parent.start.x, parent.start.y, parent.end.x, parent.end.y)
		for segment in parent.segments:
			obj.segments.append(segment)
		return obj

	def mutate_simple(self, segment_index):
		# Select which way it should be moved
		# Change length of previous segment
		# Change length of following segment
		# If previous or following segment doesnt exist it should be added

		# Direction of segment movement
		# It can be either 1 or -1
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
		# Select one segment that is going to be mutated
		# Select at what offset it will break
		# Break the selected segment into two
		# Select which part will be moved
		# Perform simple_mutation on the part 
		
		segment_index = randomGenerator.randint(0, len(self.segments) - 1)

		self.mutate_simple(segment_index)

	def test(self) -> bool:
		correct_value = [self.end.x - self.start.x, self.end.y - self.start.y]
		value = [0, 0]
		for segment in self.segments:
			if segment.direction == "X":
				value[0] += segment.size
			else:
				value[1] += segment.size
		
		return value == correct_value

	@classmethod
	def random(cls, p1: Point, p2: Point, size_x: int, size_y: int, random_segments: int):
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

	