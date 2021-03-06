import math
from typing import Dict, List, Iterable

letter_distribution = [
    ['a', 0.08167], ['b', 0.01492], ['c', 0.02782], ['d', 0.04253],
    ['e', 0.12702], ['f', 0.02228], ['g', 0.02015], ['h', 0.06094],
    ['i', 0.06966], ['j', 0.00153], ['k', 0.00772], ['l', 0.04025],
    ['m', 0.02406], ['n', 0.06749], ['o', 0.07507], ['p', 0.01929],
    ['q', 0.00095], ['r', 0.05987], ['s', 0.06327], ['t', 0.09056],
    ['u', 0.02758], ['v', 0.00978], ['w', 0.02360], ['x', 0.00150],
    ['y', 0.01974], ['z', 0.00074],
]

default_layout = {
    2: ['a', 'b', 'c'],
    3: ['d', 'e', 'f'],
    4: ['g', 'h', 'i'],
    5: ['j', 'k', 'l'],
    6: ['m', 'n', 'o'],
    7: ['p', 'q', 'r', 's'],
    8: ['t', 'u', 'v'],
    9: ['w', 'x', 'y', 'z'],
}


def entropy(probabilities: Iterable):
    return -sum((p * math.log2(p)) for p in probabilities)


def optimized_multi_tap_layout(keys: List, distribution: List):
    # Sort the disribution by probability, in decreasing order.
    distribution_sorted = sorted(distribution, key=lambda x: x[1], reverse=True)
    score = 0  # Expected number of keypresses
    layout = {k: [] for k in keys}
    for (i, (l, p)) in enumerate(distribution_sorted):
        d, m = divmod(i, len(keys))
        layout[keys[m]].append(l)
        score += p * (d+1)
    return layout, score


def expected_number_of_keypresses(layout: Dict, distribution: List):
    d = dict(distribution)
    score = 0
    for letters in layout.values():
        for (i, l) in enumerate(letters):
            score += (i+1) * d[l]
    return score


s = entropy([p for (l, p) in letter_distribution])
keys1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
keys2 = [2, 3, 4, 5, 6, 7, 8, 9]
layout1, score1 = optimized_multi_tap_layout(keys1, letter_distribution)
layout2, score2 = optimized_multi_tap_layout(keys2, letter_distribution)
score_default = expected_number_of_keypresses(default_layout,
                                              letter_distribution)

print(f"Entropy of English letter:\n{s}")
print(f"Expected number of key presses with keys {keys1}:\n{score1}")
print(f"Expected number of key presses with keys {keys2}:\n{score2}")
print(f"Expected number of key presses with keys {keys2}:\n{score_default}")
print(f"Ration between score2 and score_default:\n{score2/score_default}")

print(f"Optimal layout 1:{layout1}")
print(f"Optimal layout 2:{layout2}")
print(f"Default layout: {default_layout}")
