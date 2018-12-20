import math, random
from collections import defaultdict


def distance(columns, i, j):
    """
    Returns Euclidean (unit) distance between two element positions in a grid layout.
    Needed in our objective function (ST)
    """
    return math.sqrt(abs(j / columns - i / columns) ** 2 + abs(
        i % columns - j % columns) ** 2)


def linear_ST(layout, columns, o_inputs):
    """
    Our objective function: Selection time (time it takes for users to select an item).
    - A weighted sum of individual selection times weighed by their importance/probability (weight)
    - This simplifies the novice model of menu search time presented by Cockburn et al. CHI 2007
    """
    ST = 0.0
    reading_cost = 0.4  # assumed that scanning a single item takes 400 ms
    for i, element in enumerate(layout):
        try:
            # Reading cost is a function of the number of elements intervening between top of menu and target
            ST += o_inputs[0][layout[i]] * \
                  distance(columns, 0, i) * reading_cost
        except:
            pass
    return ST


def random_search(max_iters, *args):
    """Our solver: Random search method
    - Shuffles a layout (list) and asks from objective function how good it is
    - Updates incumbent (best known design) whenever an improvement is found
    - Continues like this max_iters times
    """
    columns = args[1]  # Number of columns in this layout (=1)
    obj_f = args[2]  # Handle to the objective function (=linear_ST)
    o_inputs = args[3:]  # Arguments simply passed on to the objective function
    incumbent = args[0]  # Best-known design thus far
    incumbent_ov = obj_f(incumbent, columns,
                         o_inputs)  # Set initial objective value

    for iter in range(0, max_iters):
        candidate = random.sample(incumbent, len(
            incumbent))  # Shuffle the design (note: this methos is slow)
        candidate_ov = obj_f(candidate, columns,
                             o_inputs)  # Then compute its objective value

        if candidate_ov < incumbent_ov:  # Update best known if an improvement was found
            incumbent = candidate[:]
            incumbent_ov = candidate_ov
    return incumbent, incumbent_ov


def optimize(iters, solver, *args):
    """Our generic optimization service:
    - Solver and objective function are given as arguments
    - Used throughout the exercises
    """
    return solver(iters, *args)


def ST_and_myO(layout, columns, o_inputs):
    """A new objective function that considers two objectives: selection time and YOUR function"""
    objective_weight = 0.5
    return linear_ST(layout, columns, o_inputs[0:]) + \
           objective_weight * myObjective(layout, columns, o_inputs[1:])


def myObjective(layout, columns, o_inputs):
    ov = 0.0
    for i in range(0, len(layout)):
        for j in range(i + 1, len(layout)):
            # We pick the association score, if any, from e_weights
            if o_inputs[0].get(layout[i] + layout[j]):
                association = o_inputs[0].get(layout[i] + layout[j])
            elif o_inputs[0].get(layout[j] + layout[i]):
                association = o_inputs[0].get(layout[j] + layout[i])
            else:
                association = 0

            # Added by Antti
            ov += distance(columns, i, j) * association

    return ov


def neighbor(layout, n=1):
    """
    Returns a neighbor of a layout (list);
    has a parameter 'n' to control distance in the neighborhood (optional)
    """
    # Choose a random element from layout
    i = random.randrange(0, len(layout))

    # Filter all elements that have distance over n.
    canditates = []
    for j in range(len(layout)):
        if i == j:
            continue
        if distance(columns, i, j) <= n:
            canditates.append(j)

    # Choose a random element from remaining elements
    j = random.choice(canditates)

    # Swap the elements i and j.
    new_layout = layout[:]
    new_layout[i] = layout[j]
    new_layout[j] = layout[i]
    return new_layout


def anneal(k_max, *args):
    """Solver: Simulated annealing using exponential cooling schedule"""
    s = args[0]  # solution seed
    columns = args[1]
    obj_f = args[2]
    o_inputs = args[3:]
    s_ov = obj_f(s, columns, o_inputs)
    T_min, T_initial, alpha = 0.0000001, 10000, 0.991  # Hyperparameters
    converged = False

    for k in range(0, k_max):
        # exponential cooling schedule
        T = max(T_min, T_initial * math.pow(alpha, k))
        s_new = neighbor(s[:], args[-1])
        s_new_ov = obj_f(s_new, columns, o_inputs)

        delta = s_new_ov - s_ov
        if delta < 0:
            # accept the neighbor if it is better
            s = s_new[:]
            s_ov = s_new_ov
        elif random.random() < math.exp(-delta / T):
            # if not, decide according to the Metropolis rule
            s = s_new[:]
            s_ov = s_new_ov
    return s, s_ov


# Task instance (same as above)
seed_layout = ['Tasks', 'Word', 'Excel', 'PPT', 'Admin', 'Mail', 'Cal', 'Ppl',
               'News', 'Drive', 'Sites', 'Notes']
e_weights = {'Tasks': 0.1, 'Word': 0.2, 'Excel': 0.15, 'PPT': 0.2,
             'Admin': 0.05, 'Mail': 0.5, 'Cal': 0.4, 'Ppl': 0.4, 'News': 0.4,
             'Drive': 0.2, 'Sites': 0.01, 'Notes': 0.05}
associations = {'WordExcel': 0.5, 'WordPPT': 0.5, 'MailCal': 0.3, 'PplCal': 0.3,
                'TasksCal': 0.2, 'NotesTasks': 0.3}
columns = 6

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
for n in [1, 2, 3, 4]:
    # Optimization
    r = [2000, 4000, 6000, 8000, 10000]
    trials = 10
    d_anneal = defaultdict(list)
    d_random = defaultdict(list)
    for iterations in r:
        for _ in range(trials):
            winner, winner_score = optimize(
                iterations, anneal, seed_layout, columns, ST_and_myO, e_weights,
                associations, n)
            d_anneal[iterations].append(winner_score)

            winner, winner_score = optimize(
                iterations, random_search, seed_layout, columns, ST_and_myO, e_weights,
                associations)
            d_random[iterations].append(winner_score)

    fig, ax = plt.subplots()
    for key, values in d_anneal.items():
        plt.scatter([key for _ in range(len(values))], values, color='b', alpha=0.7)
    for key, values in d_random.items():
        plt.scatter([key for _ in range(len(values))], values, color='y', alpha=0.7)

    # plt.legend()
    plt.xlabel("Iterations")
    plt.ylabel("$f(x)$")
    plt.savefig(f"figures/annealing_vs_random_search_n{n}.png")
