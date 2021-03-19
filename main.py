from solution import Solution
from population import Population
from subject import Subject
from point import Point

def main():

	# Main loop
	# iteration_index = 0
	# pop = init_population()
	# evalute_score(pop)
	# while not condition:
	# 	new_pop = empty_collection
	# 	while size(new_pop) < MAX_POP_SIZE:
	# 		subject_1 = select_one(pop)
	# 		if(random() < CROSSING_PROBABILITY):
	#			subject_2 = select_one(pop)
	#			new_subject = crossover(subject_1, subject_2)
	#		else:
	#			new_subject = copy(subject_1)
	# 		mutate(new_subject, MUTATION_PROBABILITY)
	# 	iteration_index++

	sol = Solution.from_file("./data/test/zad2.txt", 2, [1, 1, 1, 1])

	pop = Population.shortest(sol.population_size, sol.points, sol.size_x, sol.size_y)
	pop.subjects[0].mutate()
	pop.subjects[0].mutate()
	pop.subjects[0].mutate()
	pop.subjects[0].mutate()
	pop.subjects[1].mutate()
	pop.subjects[1].mutate()
	pop.subjects[1].mutate()
	pop.subjects[1].mutate()

	print(pop)
	print(Subject.crossover(pop.subjects[0], pop.subjects[1], 0.5))
	

if __name__ == "__main__":
    main()