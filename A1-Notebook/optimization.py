import math, random
import render  # For presenting layouts for rendering in Jupyter
from IPython.display import SVG  # SVG capabilities for showing layouts


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


# Task instance

# Initial (seed) layout
seed_layout = ['Home', 'World', 'Zones', 'Cal', 'Weather', 'Sun', 'Timers',
               'Calc', 'Apps', 'Free']

# Element weights
e_weights = {'Home': 0.5, 'World': 0.2, 'Zones': 0.1, 'Cal': 0.1,
             'Weather': 0.3, 'Sun': 0.2, 'Timers': 0.2, 'Calc': 0.6,
             'Apps': 0.2, 'Free Fun': 0.1}

# Call the optimizer
winner, winner_score = optimize(1000, random_search, seed_layout, 1, linear_ST,
                                e_weights)

# Show result
print("Objective value (expected selection time):", winner_score)
SVGlayout = render.SVGlayout(winner, 1)
SVG(SVGlayout.inSVG)


def ST_and_myO(layout, columns, o_inputs):
    """A new objective function that considers two objectives: selection time and YOUR function"""
    # TODO: 1. How does changing objective_weight effect the outcome?
    # TODO: 2. Implement normalization such that objective weight is not
    #       sensitive to change in e_weight or associations.
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

            # TASK: ADD YOUR OBJECTIVE FUNCTION HERE.
            # TODO: 3. Pareto frontier

            # Added by Antti
            ov += distance(columns, i, j) * association

    return ov


def normalize(weights: dict):
    w_min = min(weights.values())
    w_max = max(weights.values())
    w = dict()
    for key in weights:
        w[key] = (weights[key] - w_min) / (w_max - w_min)
    return w


def ST_and_myO_normalized(layout, columns, o_inputs):
    """A new objective function that considers two objectives: selection time and YOUR function"""
    # TODO: 1. How does changing objective_weight effect the outcome?
    # TODO: 2. Implement normalization such that objective weight is not
    #       sensitive to change in e_weight or associations.
    u1 = 0.5
    u2 = 1 - u1
    reading_cost = 0.4
    return u1 * linear_ST(layout, columns, o_inputs[0:]) / reading_cost + \
           u2 * myObjective(layout, columns, o_inputs[1:])


# Task instance

seed_layout = ['Tasks', 'Word', 'Excel', 'PPT', 'Admin', 'Mail', 'Cal', 'Ppl',
               'News', 'Drive', 'Sites', 'Notes']
e_weights = {'Tasks': 0.1, 'Word': 0.2, 'Excel': 0.15, 'PPT': 0.2,
             'Admin': 0.05, 'Mail': 0.5, 'Cal': 0.4, 'Ppl': 0.4, 'News': 0.4,
             'Drive': 0.2, 'Sites': 0.01, 'Notes': 0.05}
associations = {'WordExcel': 0.5, 'WordPPT': 0.5, 'MailCal': 0.3, 'CalPpl': 0.3,
                'TasksCal': 0.2, 'NotesTasks': 0.3}
columns = 6

# Optimization
winner, winner_score = optimize(3000, random_search, seed_layout, columns,
                                ST_and_myO, e_weights, associations)

# Results
print("Objective value:", winner_score)
SVGlayout = render.SVGlayout(winner, columns, 10, associations)
SVG(SVGlayout.inSVG)


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

# Optimization
winner, winner_score = optimize(10000, anneal, seed_layout, columns, ST_and_myO,
                                e_weights, associations, 1)

# Present results
print("Objective value:", winner_score)
SVGlayout = render.SVGlayout(winner, columns, 10, associations)
SVG(SVGlayout.inSVG)
