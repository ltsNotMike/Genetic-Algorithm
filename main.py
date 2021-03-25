from solution import Solution
from population import Population
from subject import Subject
from point import Point
from random import random
import tkinter as tk
import threading
class MainWindow(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()
		self.root = None
		self.running = False

	def callback(self):
		self.root.quit()
		self.running = False

	def run(self):
		self.root = tk.Tk()
		self.root.title("Best Subject")
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.running = True
		self.root.mainloop()

def drawBest(canvas, best_sub, multiplier):
	canvas.delete("all")
	for lane in best_sub.lanes:
		canvas.create_oval((lane.start.x * multiplier) -3, (lane.start.y * multiplier) - 3, (lane.start.x * multiplier) + 3, (lane.start.y * multiplier) + 3)
		canvas.create_oval((lane.end.x * multiplier) - 3, (lane.end.y * multiplier) - 3, (lane.end.x * multiplier) + 3, (lane.end.y * multiplier) + 3)
		
		p1 = Point.copy(lane.start)
		for segment in lane.segments:
			p2 = Point.copy(p1)
			p2.add(segment)
			canvas.create_line(p1.x * multiplier, p1.y * multiplier, p2.x * multiplier, p2.y * multiplier)
			p1.add(segment)

def main():
	CROSSING_PROPABILITY = 0.6
	CROSSING_RATIO_PROPABILITY = 0.5
	MUTATION_PROPABILITY = 0.1
	ITERATIONS = 1500
	POPULATION_SIZE = 50
	RANDOM_SEGMENTS = 5

	iteration = 0
	sol = Solution.from_file("./data/test/zad3.txt", POPULATION_SIZE, [50, 2, 1, 40], RANDOM_SEGMENTS)

	app = MainWindow()
	while not app.running:
		pass

	multiplier = 800/(sol.size_x + 2)
	canvas = tk.Canvas(app.root, bg="grey", height=800, width=800)
	canvas.pack()
	prev_pop = Population.random(sol.population_size, sol.points, sol.size_x, sol.size_y, sol.random_segments)
	prev_pop.evaluate(sol.weights)
	next_pop = Population()

	best_index = prev_pop.best()
	best_sub = prev_pop.subjects[best_index]
	drawBest(canvas, best_sub, multiplier)

	while iteration < ITERATIONS and app.running:
		while len(next_pop.subjects) < sol.population_size:
			subject_1 = prev_pop.subjects[prev_pop.selectTournament(0.3)]
			if random() < CROSSING_PROPABILITY:
				subject_2 = prev_pop.subjects[prev_pop.selectTournament(0.3)]
				new_subject = Subject.crossover(subject_1, subject_2, CROSSING_RATIO_PROPABILITY)
			else:
				new_subject = Subject.copy(subject_1)
			if random() < MUTATION_PROPABILITY:
				new_subject.mutate()
			next_pop.subjects.append(new_subject)
			next_pop.scores.append(0)
		
		prev_pop = next_pop
		prev_pop.evaluate(sol.weights)
		next_pop = Population()
		iteration += 1

		best_index = prev_pop.best()
		best_sub = prev_pop.subjects[best_index]
		drawBest(canvas, best_sub, multiplier)
		if not prev_pop.test():
			print("TEST FAILED")
			break
		print(".")
		
	print("Simulation Ended")
	
if __name__ == "__main__":
    main()