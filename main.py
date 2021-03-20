from solution import Solution
from population import Population
from subject import Subject
from point import Point
from random import random

def main():
	CROSSING_PROPABILITY = 0.6
	CROSSING_RATIO_PROPABILITY = 0.5
	MUTATION_PROPABILITY = 0.1

	iterations = 100
	iteration = 0
	population_size = 100
	sol = Solution.from_file("./data/test/zad3.txt", 5, [20, 2, 1, 20])

	prev_pop = Population.shortest(population_size, sol.points, sol.size_x, sol.size_y)
	prev_pop.evaluate(sol.weights)
	next_pop = Population()

	while iteration < iterations:
		while len(next_pop.subjects) < sol.population_size:
			subject_1 = prev_pop.subjects[prev_pop.selectRoulette()]
			if random() < CROSSING_PROPABILITY:
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
		print(prev_pop)
		next_pop = Population()
		iteration += 1
		if not prev_pop.test():
			print("TEST FAILED")
			break


if __name__ == "__main__":
    main()