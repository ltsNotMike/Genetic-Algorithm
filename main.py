from solution import Solution
from population import Population
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

	sol = Solution.from_file("data.txt", 1, [1, 1, 1, 1])

	pop = Population.shortest(sol.population_size, sol.points, sol.size_x, sol.size_y)

	print(pop.subjects)
	pop.estimate(sol.weights)
	pass

if __name__ == "__main__":
    main()