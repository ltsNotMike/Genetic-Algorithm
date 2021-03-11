class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	@classmethod
	def copy(cls, other):
		return cls(other.x, other.y)
	
	def __eq__(self, value):
	 	return self.x == value.x and self.y == value.y
	
	def __ne__(self, value):
	 	return self.x != value.x or self.y != value.y
	def __repr__(self):
	 	return f'({self.x}, {self.y})'
	def add(self, segment):
		if segment.direction == "Y":
			self.y += segment.size
		elif segment.direction == "X":
			self.x += segment.size			