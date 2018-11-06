def pareto_optimal_design2(u1, iterations):
    assert 0 <= u1 <= 1
    u2 = 1 - u1

    e_weights_N = normalized(e_weights)
    associations_N = normalized(associations)

    x1, zU1 = random_search(
        iterations, seed_layout, columns, f1, normalized(e_weights))
    x2, zU2 = random_search(
        iterations, seed_layout, columns, f2, normalized(associations))
    zN1 = max(f1(x1, columns, [e_weights]),
              f2(x1, columns, [associations]))
    zN2 = max(f1(x2, columns, [e_weights]),
              f2(x2, columns, [associations]))

    def normalized_objective(u1, u2, layout, columns, o_inputs):
        return u1 * f1(layout, columns, o_inputs[0:]) / (zN1 - zU1) + \
               u2 * f2(layout, columns, o_inputs[1:]) / (zN2 - zU2)

    winner, winner_score = random_search(
        iterations, seed_layout, columns,
        partial(normalized_objective, u1, u2),
        normalized(e_weights), normalized(associations))
    return winner, winner_score
