from gurobipy import GRB, quicksum
from math import log2

import numpy as np
from gurobi import Model


# Returns Euclidean distance between two element positions in a grid layout
def dist(columns, i, j):
    return np.sqrt(abs(j / columns - i / columns) ** 2 +
                   abs(i % columns - j % columns) ** 2)


def solve(elements, positions, frequency, distance, rows, columns, colocated):
    # ==== 1. Create the (empty) model ====
    if colocated is None:
        colocated = []
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

    # Add constraints to items that should be colocated.
    for (e1, e2) in colocated:
        # 1. same row
        # 2. same column
        model.addConstr(
            quicksum([x[(e1, i*columns+j)] * x[(e2, i*columns+(j+1))] +
                      x[(e2, i*columns+j)] * x[(e1, i*columns+(j+1))] +
                      x[(e1, i * columns + j)] * x[(e2, (i + 1) * columns + j)] +
                      x[(e2, i * columns + j)] * x[(e1, (i + 1) * columns + j)]
                      for i in range(rows-1)
                      for j in range(columns-1)]) == 1,
            f"Elements {e1}{e2} are colocated")

    model.update()

    # ==== 4. Specify Objective function ======
    # Sum up the costs for mapping any element e to any position p
    a = 0
    b = 1
    width = 1
    cost = quicksum(
        (a + b * log2(distance[p] / width + 1)) * frequency[e] * x[(e, p)]
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


def random_frequecies(n):
    s = np.random.sample(n)
    return s / np.sum(s)


# Set random state
# np.random.seed(2576)

# define elements and positions
n = 16
columns = 4
rows = n // columns

elements = list(range(n))
positions = list(range(len(elements)))
colocated = [(elements[1], elements[5])]

# define cost factors
frequency = {e: f for (e, f) in zip(elements, random_frequecies(n))}
distance = list(map(lambda p: dist(columns, 0, p), positions))

# solve the problem
layout1, objective1 = solve(elements, positions, frequency, distance, rows,
                            columns, [])
layout2, objective2 = solve(elements, positions, frequency, distance, rows,
                            columns, colocated)

# Print the solution
# print("Objective value (expected selection time):", objective)

# Lets reshape the result into 4x4 matrix and mirror the layout along x-axis
# because the distance should be measured from bottom-left corner.
print()
print(f"Layout with no colocated items:")
print(np.flip(np.array(layout1).reshape((rows, columns)), axis=0))
print("Objective value: ", objective1)
print()
print(f"Layout with colocated items {colocated}:")
print(np.flip(np.array(layout2).reshape((rows, columns)), axis=0))
print("Objective value: ", objective2)
