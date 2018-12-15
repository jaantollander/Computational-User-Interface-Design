# Cheatsheet
## Combinatorial Optimization
1) Understanding of uses and assumptions of computational interaction and design
2) Ability to cast simple design problems as combinatorial optimization tasks, including design space, objectives, constraints.

---

**Computational interaction** applies computational methods to explain, enhance, and learn from interaction with a human.

1) Relies on a formal description of the problem.
2) Relies on data and algorithms.

Data influenced a model, which is used by an algorithm to do the design work.

The **combinatorial design problem** finds an optimal design \(d\) from design space \(D\) measured by objective function \(g\) given constraints \(θ\) \[\max_{d∈D}g(d,θ).\]

* **Design task**. The description of the design task.
* **Objective function** \(g\). Measures the goodness of the design.
* **Design space** \(D\). In combinatorial design problems, the size of the design space grows into the factorial of the number of elements, \(O(n!)\).
* **Task instance** \(θ\). Constraints of the design task.

Example:

* Design task: Letter assignment to a keyboard.
* Objective function: Fitt's law.
* Design space: All possible different letter assignments.
* Task Instance: The type of keyboard.
* Optimization can be done using an optimizer such as simulated annealing.


## Perception and Attention
1) Windows of visibility
2) Rosenholtz' clutter model
3) Ability to predict how bottom-up (saliency) and top-down attention would proceed for a given layout.

---

**Human visual system** (HSV)

1) Sensation (1-100 ms)
2) Detection (30-300 ms)
3) Organization (30-500 ms)
4) Selection (200-400 ms)
5) Adaptation (seconds to years)

**Windows of visibility**: Limits to HVS

1) Wavelength (380-780 nm)
2) Field of view (190 degrees horizontal, 125 degrees vertical)
3) Trichromaticity (perception of blue, green and red wavelengths)
4) Luminance (100 max/min)
5) Spatial frequency
6) Local contrast
7) Fixation

Clutter as feature congestion:

* HVS has evolved to spot unusual items in scenes
* Clutter is the state in which excess items, or their representation or organization, lead to a degratation of performance at some task.

**Rosenholz' clutter model**: If a feature vector is an outlier to the local distribution of feature vectors, then that feature is **salient**.


## Control
1) Ability to predict movement with Fitts' law and steering law when parameters are given
2) Ability to model (block diagram) a pointing gesture using control theory, in particular, a block diagram implementing 2OL or similar model

---

* **Fitt's law**
* **Steering law**


## Input
1) Ability to tell what kinds of filtering are needed for different issues in raw sensor data
2) Understanding of operating principles of a filter (e.g. 1€ filter) and a recognizer (e.g. 1$ recognizer)
3) Ability to construct a decoder for single or sequential input


## Bayesian human-in-the-loop optimization
Understanding of core concepts in Bayesian optimization, including surrogate mode, prior update, acquisition function


## Integer Programming
Ability to formulate a menu and keyboard design problem as a mixed integer linear program.


## Biomechanics
Ability to evaluate the fatiguability of a given posture or movement using the Consumed Endurance model (when parameter values are given).


## Formal Methods
1) Ability to  draw a finite state diagram for simple interactive devices
2) Ability to interpret a simple verification statement expressed with temporal logic.


## Cognitive Models
Ability to formulate an information foraging diagram (patch model) for a given application case.


## Bandits
1) Understanding the bandit problem
2) Understanding how exploration/exploitation is solved
3) Understanding  bandits


## Reinforcement Learning
1) Ability to formulate a navigation or decision-making task in interaction as a reinforcement learning problem, including the Markov decision process (MDP).
2) Understanding of difference between POMDP and MDP.
