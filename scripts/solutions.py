import random
import time

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

class Agent:
    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff = 0
        self.total_winnings = 0  # New property to track overall payoff winnings

def initialize_population(pop_size, initial_ratio):
    """Initialize population with Agent objects."""
    return [Agent('Worm' if random.random() < initial_ratio else 'Fruit') for _ in range(pop_size)]

def play_game(population):
    """Simulate one generation: agents play the game and receive payoffs."""
    indices = list(range(len(population)))
    random.shuffle(indices)

    for i in range(0, len(indices) - 1, 2):
        agent1 = population[indices[i]]
        agent2 = population[indices[i + 1]]
        payoff1, payoff2 = PAYOFF_MATRIX[(agent1.strategy, agent2.strategy)]
        agent1.payoff = payoff1
        agent2.payoff = payoff2
        # Update total winnings
        agent1.total_winnings += payoff1
        agent2.total_winnings += payoff2

def revise_strategies(population, e):
    """Revise strategies based on the revision probability e."""
    for agent in population:
        if random.random() < e:
            random_agent = random.choice(population)
            if random_agent.payoff > agent.payoff:
                agent.strategy = random_agent.strategy

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

    for run in range(1, runs + 1):
        print(f"\nSimulation Run {run}:")
        start_time = time.time()

        # Initialize population
        population = initialize_population(pop_size, initial_ratio)

        for generation in range(generations):
            play_game(population)
            worm_count = sum(agent.strategy == "Worm" for agent in population)
            fruit_count = pop_size - worm_count
            worm_proportion = worm_count / pop_size
            average_payoff = sum(agent.payoff for agent in population) / pop_size

            # Print the simulation data
            print_simulation_data(run, generation, worm_count, fruit_count, worm_proportion, average_payoff)

            # Update population
            revise_strategies(population, e)

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"  Time taken: {time_taken:.2f} seconds")

        # For single run, print final Worm ratio and total winnings
        if runs == 1:
            final_worm_proportion = worm_count / pop_size
            print(f"  Final Worm Ratio: {final_worm_proportion:.2f}")
            # Optionally, print total winnings for each agent
            for agent in population:
                print(f"Agent {agent.strategy}: Total Winnings = {agent.total_winnings}")

if __name__ == "__main__":
    main()
