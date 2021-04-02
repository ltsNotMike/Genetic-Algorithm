from solution import Solution
from population import Population
from subject import Subject
from point import Point
from random import random
import tkinter as tk
import threading
from sys import argv
from datetime import datetime

def printHelp():
	print("Help: Genetyczne Maciej Witkowski")
	print("\"--segments x\": x liczba segmentów losowych w generowanej ścieżce")
	print("\"--population x\" : x liczba osobników w populacji")
	print("\"--muatation x\" : x liczba [0,1] oznaczająca prawdopodobienstwo mutacji")
	print("\"--crossing x\" : x liczba [0,1] oznaczająca prawdopodobienstwo krzyżowania")
	print("\"--parerentRatio x\" : liczba [0,1] oznaczająca procent genów odziedziczonych po jednym z rodziców")
	print("\"--tournament x\" : ustawienie selekcji na turniej i podanie liczby x (0,1] oznaczającej procent populacji w turnieju")
	print("\"--random x\" : x liczba losowych populacji")
	print("\"--visual\" : włączenie trybu wizualizacji")


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

def saveToFile(pop: Population, file: "File") -> float:
	line = f"{pop.getAverageFitness()}; {pop.getBestFitness()}; {pop.getWorstFitness()}\n"
	file.write(line)

def main():
	POPULATION_SIZE = 250
	ITERATIONS = 50
	CROSSING_PROPABILITY = 0.8
	MUTATION_PROPABILITY = 0.3
	IS_SELECTION_TOURNAMENT = True
	TOURNAMENT_SIZE = 0.4
	CROSSING_RATIO_PROPABILITY = 0.3
	RANDOM_SEGMENTS = 3
	IS_RANDOM=False
	VISUAL = False
	dt = datetime.now()
	FILE_NAME = f"./data/out/file_name_{dt.strftime('%Y%m%d_%H%M%S')}.txt"
	

	if "--visual" in argv:
		VISUAL = True
	if "--mutation" in argv:
		index = argv.index("--mutation")
		MUTATION_PROPABILITY = argv[index + 1]
	if "--crossing" in argv:
		index = argv.index("--crossing")
		CROSSING_PROPABILITY = argv[index + 1]
	if "--segments" in argv:
		index = argv.index("--segments")
		RANDOM_SEGMENTS = argv[index + 1]
	if "--population" in argv:
		index = argv.index("--population")
		POPULATION_SIZE = argv[index + 1]
	if "--parerentRatio" in argv:
		index = argv.index("--parerentRatio")
		CROSSING_RATIO_PROPABILITY = argv[index + 1]
	if "--tournamet" in argv:
		index = argv.index("--tournamet")
		TOURNAMENT_SIZE = argv[index + 1]
	if "--random" in argv:
		index = argv.index("--random")
		IS_RANDOM = True
		ITERATIONS = int(argv[index + 1])
	if "--help" in argv:
		printHelp()
		return
	
	try:
		FILE = open(FILE_NAME, 'a')
	except IOError as e:
		print(e)
		return
		
	iteration = 0
	sol = Solution.from_file("./data/test/zad3.txt", [150, 30, 10, 100])

	if IS_RANDOM:
		while iteration < ITERATIONS:
			pop = Population.random(POPULATION_SIZE, sol.points, sol.size_x, sol.size_y, RANDOM_SEGMENTS)
			pop.evaluate(sol.weights)
			iteration += 1
			saveToFile(pop, FILE)

		FILE.close()
		return

	if VISUAL:

		app = MainWindow()
		while not app.running:
			pass

		multiplier = 800/(sol.size_x + 2)
		canvas = tk.Canvas(app.root, bg="grey", height=800, width=800)
		canvas.pack()

	prev_pop = Population.random(POPULATION_SIZE, sol.points, sol.size_x, sol.size_y, RANDOM_SEGMENTS)
	prev_pop.evaluate(sol.weights)
	next_pop = Population()

	if VISUAL:
		best_index = prev_pop.best()
		best_sub = prev_pop.subjects[best_index]
		drawBest(canvas, best_sub, multiplier)

	while iteration < ITERATIONS and (not VISUAL or app.running):
		while len(next_pop.subjects) < POPULATION_SIZE:
			if IS_SELECTION_TOURNAMENT:
				subject_1 = prev_pop.subjects[prev_pop.selectTournament(TOURNAMENT_SIZE)]
			else:
				subject_1 = prev_pop.subjects[prev_pop.selectRoulette()]
			if random() < CROSSING_PROPABILITY:
				if IS_SELECTION_TOURNAMENT:
					subject_2 = prev_pop.subjects[prev_pop.selectTournament(TOURNAMENT_SIZE)]
				else:
					subject_2 = prev_pop.subjects[prev_pop.selectRoulette()]
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

		saveToFile(prev_pop, FILE)

		best_index = prev_pop.best()
		best_sub = prev_pop.subjects[best_index]
		if VISUAL:
			drawBest(canvas, best_sub, multiplier)
		else:
			print(f"Score: {prev_pop.scores[best_index]}")
			print(best_sub)
	print("Simulation Ended")
	FILE.close()
if __name__ == "__main__":
    main()