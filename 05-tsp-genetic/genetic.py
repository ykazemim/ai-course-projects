import random
from typing import List, Callable, Tuple


class GeneticAlgorithm:
    def __init__(
        self,
        population: List[List[int]],
        fitness_func: Callable[[List[int]], float],
        num_generations: int = 200,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.9,
        selection_strategy: str = 'tournament',  # 'tournament', 'roulette', 'rank'
        crossover_strategy: str = 'CX',  # 'PMX', 'CX'
        mutation_strategy: str = 'inversion',        # 'swap', 'inversion', 'scramble'
        tournament_size: int = 3,
    ) -> None:
        """
        Initialize the genetic algorithm with population and configuration parameters.

        Args:
            population (List[List[int]]): Initial population of individuals.
            fitness_func (Callable[[List[int]], float]): Function to evaluate the fitness of an individual.
            num_generations (int): Number of generations to run the algorithm.
            mutation_rate (float): Probability of mutation for each individual.
            crossover_rate (float): Probability of crossover between pairs.
            selection_strategy (str): Selection method ('tournament', 'roulette', or 'rank').
            crossover_strategy (str): Crossover method ('PMX', 'CX').
            mutation_strategy (str): Mutation method ('swap', 'inversion', or 'scramble').
            tournament_size (int): Size of the tournament in tournament selection.
        """
        self.population: List[List[int]] = population
        self.fitness_func: Callable[[List[int]], float] = fitness_func
        self.num_generations: int = num_generations
        self.mutation_rate: float = mutation_rate
        self.crossover_rate: float = crossover_rate
        self.selection_strategy: str = selection_strategy
        self.crossover_strategy: str = crossover_strategy
        self.mutation_strategy: str = mutation_strategy
        self.tournament_size: int = tournament_size

        # History tracking
        self.best_fitness_history: List[float] = []
        self.best_distance_history: List[float] = []

    def evaluate_population(self) -> List[float]:
        """
        Evaluate the fitness of the current population.

        Returns:
            List[float]: A list containing the fitness value of each individual.
        """

        return [self.fitness_func(ind) for ind in self.population]

    def selection(self, fitnesses: List[float]) -> int:
        """
        Select an individual index based on the configured selection strategy.

        Args:
            fitnesses (List[float]): List of fitness values for the population.

        Returns:
            int: Index of the selected individual.
        """

        if self.selection_strategy == 'tournament':
            participants = random.sample(
                # Randomly select participants for the tournament
                range(len(fitnesses)), self.tournament_size)
            return max(participants, key=lambda i: fitnesses[i])

        elif self.selection_strategy == 'roulette':
            total = sum(fitnesses)
            pick = random.uniform(0, total)
            current = 0
            for i, f in enumerate(fitnesses):  # Iterate over fitnesses
                current += f
                if current > pick:
                    return i

        elif self.selection_strategy == 'rank':
            ranked = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])
            probs = [(i + 1) / sum(range(1, len(fitnesses) + 1))
                     # Calculate probabilities based on rank
                     for i in range(len(fitnesses))]
            pick = random.uniform(0, 1)
            current = 0
            # Iterate over ranked indices and their probabilities
            for i, p in zip(ranked, probs):
                current += p
                if current >= pick:
                    return i

        # Fallback to random selection
        return random.randint(0, len(fitnesses) - 1)

    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """
        Perform permutation-preserving crossover between two parents.

        Args:
            parent1 (List[int]): First parent individual.
            parent2 (List[int]): Second parent individual.

        Returns:
            List[int]: Offspring individual produced by crossover.
        """

        if self.crossover_strategy == 'PMX':
            return self.pmx_crossover(parent1, parent2)
        elif self.crossover_strategy == 'CX':
            return self.cx_crossover(parent1, parent2)
        else:
            # Default: return a copy of one parent
            return parent1.copy()

    def pmx_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        size = len(parent1)
        child = [None] * size

        # Choose crossover points
        start, end = sorted(random.sample(range(size), 2))

        # Copy slice from parent1 to child
        child[start:end + 1] = parent1[start:end + 1]

        # Mapping from parent2 to parent1 segment
        for i in range(start, end + 1):
            gene = parent2[i]
            if gene not in child:
                pos = i
                while True:
                    gene_in_parent1 = parent1[pos]

                    pos = parent2.index(gene_in_parent1)
                    if child[pos] is None:
                        child[pos] = gene
                        break

        # Fill remaining None positions with genes from parent2
        for i in range(size):
            if child[i] is None:
                child[i] = parent2[i]

        return child

    def cx_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        size = len(parent1)
        child = [None] * size

        # Start cycle from position 0
        start = 0
        idx = start

        while True:
            child[idx] = parent1[idx]
            idx = parent1.index(parent2[idx])
            if idx == start:
                break

        # Fill rest from parent2
        for i in range(size):
            if child[i] is None:
                child[i] = parent2[i]

        return child

    def mutation(self, individual: List[int]) -> List[int]:
        """
        Apply mutation to an individual using the configured mutation strategy.

        Args:
            individual (List[int]): Individual to mutate.

        Returns:
            List[int]: Mutated individual.
        """

        if self.mutation_strategy == 'swap':
            return self.swap_mutation(individual)
        elif self.mutation_strategy == 'inversion':
            return self.inversion_mutation(individual)
        elif self.mutation_strategy == 'scramble':
            return self.scramble_mutation(individual)
        else:
            return individual

    def swap_mutation(self, individual: List[int]) -> List[int]:
        ind = individual.copy()
        size = len(ind)
        idx1, idx2 = random.sample(range(size), 2)
        ind[idx1], ind[idx2] = ind[idx2], ind[idx1]
        return ind

    def inversion_mutation(self, individual: List[int]) -> List[int]:
        ind = individual.copy()
        size = len(ind)
        start, end = sorted(random.sample(range(size), 2))
        ind[start:end + 1] = reversed(ind[start:end + 1])
        return ind

    def scramble_mutation(self, individual: List[int]) -> List[int]:
        ind = individual.copy()
        size = len(ind)
        start, end = sorted(random.sample(range(size), 2))
        subset = ind[start:end + 1]
        random.shuffle(subset)
        ind[start:end + 1] = subset
        return ind

    def run(self) -> Tuple[List[int], float, List[float], List[float]]:
        """
        Run the genetic algorithm for the configured number of generations.

        Returns:
            Tuple containing:
                - List[int]: The best solution found.
                - float: Fitness of the best solution.
                - List[float]: History of best fitness values.
                - List[float]: History of best distance values.
        """
        for generation in range(self.num_generations):
            fitnesses = self.evaluate_population()

            # Track best individual
            best_idx = max(range(len(fitnesses)),
                           key=lambda i: fitnesses[i])
            best_fit = fitnesses[best_idx]
            best_individual = self.population[best_idx]

            # Track best fitness and distance (distance = 1/fitness)
            self.best_fitness_history.append(best_fit)
            self.best_distance_history.append(
                1.0 / best_fit if best_fit != 0 else float('inf'))

            new_population = []

            while len(new_population) < len(self.population):
                # Selection
                parent1_idx = self.selection(fitnesses)
                parent2_idx = self.selection(fitnesses)
                parent1 = self.population[parent1_idx]
                parent2 = self.population[parent2_idx]

                # Crossover
                if random.random() < self.crossover_rate:
                    child = self.crossover(parent1, parent2)
                else:
                    child = parent1.copy()

                # Mutation
                if random.random() < self.mutation_rate:
                    child = self.mutation(child)

                new_population.append(child)

            self.population = new_population

        # Final evaluation to get best individual overall
        final_fitnesses = self.evaluate_population()
        best_idx = max(range(len(final_fitnesses)),
                       key=lambda i: final_fitnesses[i])
        best_fit = final_fitnesses[best_idx]
        best_individual = self.population[best_idx]

        return best_individual, best_fit, self.best_fitness_history, self.best_distance_history
