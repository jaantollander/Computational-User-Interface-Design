from gurobipy import GRB, quicksum

import numpy as np
from gurobi import Model


# Returns Euclidean distance between two element positions in a grid layout
def dist(columns, i, j):
    return np.sqrt(abs(j / columns - i / columns) ** 2 +
                   abs(i % columns - j % columns) ** 2)


def solve(elements, positions, frequency, distance):
    # ==== 1. Create the (empty) model ====
    model = Model("linear_menu")

    # ==== 2. Add decision variables ======
    x = {}
    # Create one binary variable for each element-position pair.
    # We give it a meaningful name so we later understand what it means
    # if it is set to 1
    for e in elements:
        for p in positions:
            x[(e, p)] = model.addVar(vtype=GRB.BINARY, name="%s_%i" % (e, p))
    # Integrate new variables
    model.update()

    # ====3. Add Constraints ======
    # Add constraints
    # Each position is only assigned to one element
    for p in positions:
        model.addConstr(quicksum(x[(e, p)] for e in elements) == 1,
                        "uniqueness_constraint_%i" % p)
    # Each element is only assigned to one position
    for e in elements:
        model.addConstr(quicksum(x[(e, p)] for p in positions) == 1,
                        "uniqueness_constraint_%s" % e)
    model.update()

    # ==== 4. Specify Objective function ======
    reading_cost = 0.4  # assumed that scanning a single item takes 400 ms

    # Sum up the costs for mapping any element e to any position p
    cost = quicksum(frequency[e] * distance[p] * reading_cost * x[(e, p)]
                    for e in elements
                    for p in positions)
    model.setObjective(cost, GRB.MINIMIZE)

    # ==== 5. Optimize model ======
    model.optimize()

    # ====6. Extract solution ======
    layout = [None] * len(elements)
    # create the layout (ordered list of elements) from the variables
    # that are set to 1
    for v in model.getVars():
        if v.x == 1:
            element = v.varName.split("_")[0]
            position = int(v.varName.split("_")[1])
            layout[position] = element

    return layout, model.getObjective().getValue()


def solve2(elements, positions, f1, w1, f2, w2, distance):
    assert w1 > 0 and w2 > 0 and w1 + w2 == 1
    frequency = dict()
    for e in elements:
        frequency[e] = w1 * f1[e] + w2 * f2[e]
    return solve(elements, positions, frequency, distance)


# define elements and positions
elements = ['Open', 'About', 'Quit', 'Help', 'Close',
            'Save', 'Edit', 'Insert', 'Delete']
positions = list(range(len(elements)))

# define cost factors
distance = list(map(lambda p: dist(1, 0, p), positions))

f1 = {'Quit': 0.3, 'About': 0.2, 'Open': 0.1, 'Save': 0.1, 'Close': 0.05,
      'Help': 0.02, 'Edit': 0.08, 'Insert': 0.1, 'Delete': 0.05}
f2 = {'Quit': 0.02, 'About': 0.1, 'Open': 0.3, 'Save': 0.2, 'Close': 0.1,
      'Help': 0.05, 'Edit': 0.05, 'Insert': 0.1, 'Delete': 0.08}
w1 = 0.5
w2 = 1 - w1

# solve the problem
layout1, objective1 = solve(elements, positions, f1, distance)
layout2, objective2 = solve(elements, positions, f2, distance)
layout, objective = solve2(elements, positions, f1, w1, f2, w2, distance)

# Print the solution
print("Objective value (expected selection time):", objective)
print()
print("Layout 1:        ", layout1, "Objective value:", objective1)
print("Layout 2:        ", layout2, "Objective value:", objective1)
print("Combined Layout: ", layout, "Objective value:", objective)
