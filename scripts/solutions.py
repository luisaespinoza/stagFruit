import random
import time

# Constants
POPULATION_SIZE = 100
REVISION_PROBABILITY = 0.1
GENERATIONS = 100
SIMULATION_RUNS = 1

# Parameterizable Payoff Matrix Constants
CC_PAYOFF = (4, 4)
CC_REPUTATION = (1, 1)
CD_PAYOFF = (0, 3)
CD_REPUTATION = (-0.5, 0.5)
DC_PAYOFF = (3, 0)
DC_REPUTATION = (0.5, -0.5)
DD_PAYOFF = (2, 2)
DD_REPUTATION = (0, 0)

COMPROMISE_WINS_PAYOFF_MATRIX = {
    ("Cooperate", "Cooperate"): (CC_PAYOFF, CC_REPUTATION),
    ("Cooperate", "Defect"): (CD_PAYOFF, CD_REPUTATION),
    ("Defect", "Cooperate"): (DC_PAYOFF, DC_REPUTATION),
    ("Defect", "Defect"): (DD_PAYOFF, DD_REPUTATION)
}

PAYOFF_MATRIX = COMPROMISE_WINS_PAYOFF_MATRIX


class Agent:
    def __init__(self, strategy):
        self.strategy = strategy
        self.payoff = 0
        self.reputation = 0
        self.total_winnings = 0
        self.total_reputation = 0


def initialize_population(pop_size, initial_ratio):
    """Initialize population with Agent objects."""
    return [Agent('Cooperate' if random.random() < initial_ratio else 'Defect') for _ in range(pop_size)]


def play_game(population):
    """Simulate one generation: agents play the game and receive payoffs."""
    indices = list(range(len(population)))
    random.shuffle(indices)

    for i in range(0, len(indices) - 1, 2):
        agent1 = population[indices[i]]
        agent2 = population[indices[i + 1]]
        (payoff1, payoff2), (reputation1, reputation2) = PAYOFF_MATRIX[(agent1.strategy, agent2.strategy)]

        # Update payoffs and reputation separately
        agent1.payoff = payoff1
        agent1.reputation = reputation1
        agent2.payoff = payoff2
        agent2.reputation = reputation2

        # Update total winnings and reputation
        agent1.total_winnings += payoff1
        agent1.total_reputation += reputation1
        agent2.total_winnings += payoff2
        agent2.total_reputation += reputation2


def calculate_reputation_score(agent):
    """Calculate the reputation score of an agent."""
    return agent.total_reputation  # You can customize this formula if needed


def revise_strategies(population, e, reputation_mode=False):
    """Revise strategies based on the revision probability e and, if enabled, reputation."""
    for agent in population:
        if random.random() < e:
            random_agent = random.choice(population)
            if reputation_mode:
                # Consider both payoff and reputation score
                if (random_agent.payoff > agent.payoff) and (calculate_reputation_score(random_agent) > 0):
                    agent.strategy = random_agent.strategy
            else:
                if random_agent.payoff > agent.payoff:
                    agent.strategy = random_agent.strategy


def print_simulation_data(run, generation, cooperate_count, defect_count, cooperate_proportion, average_payoff):
    """Print the simulation data for the current generation."""
    print(f"Run {run}, Generation {generation}:")
    print(f"  Cooperate Count: {cooperate_count}")
    print(f"  Defect Count: {defect_count}")
    print(f"  Cooperate Proportion: {cooperate_proportion:.2f}")
    print(f"  Average Payoff: {average_payoff:.2f}")
    print()


def print_final_results(population, generations, reputation_mode):
    """Print the agent with the most reputation, the agent with the most total payoff, and the best average payoff."""
    max_payoff_agent = max(population, key=lambda agent: agent.total_winnings)
    best_average_payoff_agent = max(population, key=lambda agent: agent.total_winnings / generations)

    if reputation_mode:
        max_reputation_agent = max(population, key=lambda agent: agent.total_reputation)
        print(f"Agent with the most reputation: Strategy = {max_reputation_agent.strategy}, "
              f"Total Payoff = {max_reputation_agent.total_winnings}, "
              f"Total Reputation = {max_reputation_agent.total_reputation}, "
              f"Average Payoff = {max_reputation_agent.total_winnings / generations:.2f}")

    print(f"Agent with the most total payoff: Strategy = {max_payoff_agent.strategy}, "
          f"Total Payoff = {max_payoff_agent.total_winnings}, "
          f"{'Reputation = '+str(max_payoff_agent.total_reputation)+', ' if reputation_mode else ''}"
          f"Average Payoff = {max_payoff_agent.total_winnings / generations:.2f}")

    print(f"Agent with the best average payoff: Strategy = {best_average_payoff_agent.strategy}, "
          f"Total Payoff = {best_average_payoff_agent.total_winnings}, "
          f"{'Reputation = '+str(best_average_payoff_agent.total_reputation)+', ' if reputation_mode else ''}"
          f"Average Payoff = {best_average_payoff_agent.total_winnings / generations:.2f}")

    # if reputation_mode:
    #     print("\nReputation for each agent:")
    #     for agent in population:
    #         print(f"Strategy = {agent.strategy}, "
    #               f"Total Reputation = {agent.total_reputation}, "
    #               f"Total Payoff = {agent.total_winnings}, "
    #               f"Average Payoff = {agent.total_winnings / generations:.2f}")

def main():
    print("Stag Hunt Evolutionary Simulation")
    print("---------------------------------")

    # Get user inputs with defaults
    pop_size = int(input(f"Population size (default {POPULATION_SIZE}): ") or POPULATION_SIZE)
    initial_ratio = float(input(f"Initial Cooperate ratio (0-1, default 0.5): ") or 0.5)
    e = float(input(f"Revision probability e (0-1, default {REVISION_PROBABILITY}): ") or REVISION_PROBABILITY)
    generations = int(input(f"Number of generations (default {GENERATIONS}): ") or GENERATIONS)
    runs = int(input(f"Number of simulation runs (default {SIMULATION_RUNS}): ") or SIMULATION_RUNS)

    # Choose mode: classic or reputation
    reputation_mode = input("Use reputation mode? (y/n, default n): ").lower() == "y"

    for run in range(1, runs + 1):
        print(f"\nSimulation Run {run}:")
        start_time = time.time()

        # Initialize population
        population = initialize_population(pop_size, initial_ratio)

        for generation in range(generations):
            play_game(population)
            cooperate_count = sum(agent.strategy == "Cooperate" for agent in population)
            defect_count = pop_size - cooperate_count
            cooperate_proportion = cooperate_count / pop_size
            average_payoff = sum(agent.payoff for agent in population) / pop_size

            # Print the simulation data
            print_simulation_data(run, generation, cooperate_count, defect_count, cooperate_proportion, average_payoff)

            # Update population based on selected mode
            revise_strategies(population, e, reputation_mode)

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"  Time taken: {time_taken:.2f} seconds")

        # Print final results for each run
        print_final_results(population, generations,reputation_mode)


if __name__ == "__main__":
    main()