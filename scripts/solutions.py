import random
import time
# import csv  # Uncomment this when using CSV functionality

# Constants
POPULATION_SIZE = 100
REVISION_PROBABILITY = 0.1
GENERATIONS = 100
SIMULATION_RUNS = 1

# Payoff matrix for the Stag Hunt game
PAYOFF_MATRIX = {
    ("Worm", "Worm"): (4, 4),
    ("Worm", "Fruit"): (0, 2),
    ("Fruit", "Worm"): (2, 0),
    ("Fruit", "Fruit"): (2, 2)
}

def initialize_population(pop_size, initial_ratio):
    """Initialize the population with the given initial Worm ratio."""
    return ['Worm' if random.random() < initial_ratio else 'Fruit' for _ in range(pop_size)]

def play_game(population):
    """Simulate one generation: agents play the game and receive payoffs."""
    payoffs = [0] * len(population)
    indices = list(range(len(population)))
    random.shuffle(indices)

    for i in range(0, len(indices) - 1, 2):
        agent1 = population[indices[i]]
        agent2 = population[indices[i + 1]]
        payoff1, payoff2 = PAYOFF_MATRIX[(agent1, agent2)]
        payoffs[indices[i]] = payoff1
        payoffs[indices[i + 1]] = payoff2

    return payoffs

def revise_strategies(population, payoffs, e):
    """Revise strategies based on the revision probability e."""
    new_population = population.copy()
    for i in range(len(population)):
        if random.random() < e:
            j = random.randint(0, len(population) - 1)
            if payoffs[j] > payoffs[i]:
                new_population[i] = population[j]
    return new_population

def print_simulation_data(run, generation, worm_count, fruit_count, worm_proportion, average_payoff):
    """Print the simulation data for the current generation."""
    print(f"Run {run}, Generation {generation}:")
    print(f"  Worm Count: {worm_count}")
    print(f"  Fruit Count: {fruit_count}")
    print(f"  Worm Proportion: {worm_proportion:.2f}")
    print(f"  Average Payoff: {average_payoff:.2f}")
    print()

def main():
    print("Stag Hunt Evolutionary Simulation")
    print("---------------------------------")

    # Get user inputs with defaults
    pop_size = int(input(f"Population size (default {POPULATION_SIZE}): ") or POPULATION_SIZE)
    initial_ratio = float(input(f"Initial Worm ratio (0-1, default 0.5): ") or 0.5)
    e = float(input(f"Revision probability e (0-1, default {REVISION_PROBABILITY}): ") or REVISION_PROBABILITY)
    generations = int(input(f"Number of generations (default {GENERATIONS}): ") or GENERATIONS)
    runs = int(input(f"Number of simulation runs (default {SIMULATION_RUNS}): ") or SIMULATION_RUNS)

    # CSV file setup (uncomment the block below to initialize the CSV file)
    # with open('simulation_results.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['run', 'generation', 'worm_count', 'fruit_count', 'worm_proportion', 'average_payoff'])

    for run in range(1, runs + 1):
        print(f"\nSimulation Run {run}:")
        start_time = time.time()

        # Initialize population
        population = initialize_population(pop_size, initial_ratio)

        for generation in range(generations):
            payoffs = play_game(population)
            worm_count = population.count("Worm")
            fruit_count = pop_size - worm_count
            worm_proportion = worm_count / pop_size
            average_payoff = sum(payoffs) / pop_size if payoffs else 0

            # Print the simulation data
            print_simulation_data(run, generation, worm_count, fruit_count, worm_proportion, average_payoff)

            # CSV writing (uncomment the block below to write to CSV for each generation)
            # with open('simulation_results.csv', 'a', newline='') as csvfile:
            #     writer = csv.writer(csvfile)
            #     writer.writerow([run, generation, worm_count, fruit_count, worm_proportion, average_payoff])

            # Update population
            population = revise_strategies(population, payoffs, e)

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"  Time taken: {time_taken:.2f} seconds")

        # For single run, print final Worm ratio
        if runs == 1:
            final_worm_count = population.count("Worm")
            final_worm_proportion = final_worm_count / pop_size
            print(f"  Final Worm Ratio: {final_worm_proportion:.2f}")

if __name__ == "__main__":
    random.seed()  # Seed with system time
    main()

