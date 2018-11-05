import math
import random
from functools import partial


def distance(columns, i, j):
    """
    Returns Euclidean (unit) distance between two element positions in a grid layout.
    Needed in our objective function (ST)
    """
    return math.sqrt(abs(j / columns - i / columns) ** 2 +
                     abs(i % columns - j % columns) ** 2)


def f1(layout, columns, o_inputs):
    """
    Our objective function: Selection time (time it takes for users to select an item).
    - A weighted sum of individual selection times weighed by their importance/probability (weight)
    - This simplifies the novice model of menu search time presented by Cockburn et al. CHI 2007
    """
    ST = 0.0
    # reading_cost = 0.4  # assumed that scanning a single item takes 400 ms
    for i, element in enumerate(layout):
        try:
            # Reading cost is a function of the number of elements intervening between top of menu and target
            ST += o_inputs[0][layout[i]] * \
                  distance(columns, 0, i)  # * reading_cost
        except:
            pass
    return ST


def f2(layout, columns, o_inputs):
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
            ov += distance(columns, i, j) * association
    return ov


def normalized(weights: dict):
    # w_min = min(weights.values())
    w_min = 0
    w_max = max(weights.values())
    w = dict()
    for key in weights:
        w[key] = (weights[key] - w_min) / (w_max - w_min)
    return w


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

    # Set initial objective value
    incumbent_ov = obj_f(incumbent, columns, o_inputs)
    for iter in range(0, max_iters):
        # Shuffle the design (note: this methos is slow)
        candidate = random.sample(incumbent, len(incumbent))
        # Then compute its objective value
        candidate_ov = obj_f(candidate, columns, o_inputs)
        # Update best known if an improvement was found
        if candidate_ov < incumbent_ov:
            incumbent = candidate[:]
            incumbent_ov = candidate_ov
    return incumbent, incumbent_ov


def objective(u1, u2, layout, columns, o_inputs):
    v1 = f1(layout, columns, o_inputs[0:])
    v2 = f2(layout, columns, o_inputs[1:])
    return u1 * v1 + u2 * v2


def pareto_optimal_design(u1, iterations):
    assert 0 <= u1 <= 1
    u2 = 1 - u1
    args = [seed_layout,
            columns,
            partial(objective, u1, u2),
            normalized(e_weights),
            normalized(associations)]
    winner, winner_score = random_search(iterations, *args)
    return winner, winner_score


seed_layout = ['Tasks', 'Word', 'Excel', 'PPT', 'Admin', 'Mail', 'Cal', 'Ppl',
               'News', 'Drive', 'Sites', 'Notes']
e_weights = {'Tasks': 0.1, 'Word': 0.2, 'Excel': 0.15, 'PPT': 0.2,
             'Admin': 0.05, 'Mail': 0.5, 'Cal': 0.4, 'Ppl': 0.4, 'News': 0.4,
             'Drive': 0.2, 'Sites': 0.01, 'Notes': 0.05}
associations = {'WordExcel': 0.5, 'WordPPT': 0.5, 'MailCal': 0.3, 'CalPpl': 0.3,
                'TasksCal': 0.2, 'NotesTasks': 0.3}
columns = 6

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

v1 = []
v2 = []
u1s = list(i / 20 for i in range(21))
for u1 in u1s:
    print(u1)
    winner, winner_score = pareto_optimal_design(u1, 10000)
    v1.append(f1(winner, columns, [e_weights]))
    v2.append(f2(winner, columns, [associations]))

plt.plot(v1, v2, lw=0, marker='*')
plt.xlabel("$f_1(x)$")
plt.ylabel("$f_2(x)$")
plt.savefig("figures/pareto_frontier.png")
