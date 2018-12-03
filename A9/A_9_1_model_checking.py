# from transitions import Machine
from collections import defaultdict
from contextlib import redirect_stdout
from io import StringIO

from transitions.extensions import GraphMachine as Machine


def dfs(graph, start):
    # https://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


def test_visibility(model, states):
    # Check if moving to state outputs something
    for state in states:
        out = StringIO()
        with redirect_stdout(out):
            getattr(model, f'to_{state}')()
        if not out.getvalue():
            print(f"User input to state `{state}` is not associated with any "
                  f"feedback.")


def test_weak_task_completeness(transitions, start, goal):
    graph = defaultdict(set)
    for (_, u, v) in transitions:
        graph[u].add(v)
    print(f"Is {goal} reachable from {start}?: ", goal in dfs(graph, start))


class Model1(object):
    def on_enter_A(self): print("Moved to A")
    def on_enter_B(self): print("Moved to B")
    def on_enter_C(self): print("Moved to C")
    def on_enter_D(self): print("Moved to D")
    def on_enter_E(self): print("Moved to E")
    def __str__(self): return "Model1"


class Model2(object):
    def __str__(self): return "Model2"


states = ['A', 'B', 'C', 'D', 'E']
initial = 'A'

# trigger, source, dest
transitions = [
    ['action_1', 'A', 'B'],
    ['action_2', 'A', 'C'],
    ['action_3', 'B', 'C'],
    ['action_4', 'B', 'E'],
    ['action_5', 'C', 'D'],
    ['action_6', 'D', 'C'],
    ['action_7', 'E', 'D'],
]

for model in [Model1(), Model2()]:
    machine = Machine(model, states=states, initial=initial,
                      transitions=transitions)
    graph = machine.get_graph()
    graph.draw(f'figures/{model}.png', prog='dot')

    print(f"Testing model {model}")
    print("Testing visibility:")
    test_visibility(model, states)
    print("Testing weak task completeness:")
    test_weak_task_completeness(transitions, 'A', 'D')
    test_weak_task_completeness(transitions, 'E', 'A')
    print()
