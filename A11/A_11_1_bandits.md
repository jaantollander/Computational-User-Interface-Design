---
title: A11.1 - Modifying the Bandits Problem and the \(ε\)-Greedy Solver
author: Jaan Tollander de Balsch - 452056
date: \today
---
## Multi-Armed Bandit
A tuple of \(⟨A,R⟩\), where:

* \(A\) is a set of **actions**.
* \(R\) is a **reward function**.

At each time step \(t\), we take an action \(a∈A\) on one slot machine and receive a rewards \(r∈R\).


## Reward and Regret
**Action-Value** is the mean reward for action \(a\)
\[
Q(a) = 𝔼[r∣a]
\]

**Optimal reward** of the optimal action \(a^*\)
\[
Q(a^*) = \max_{a∈A} Q(a)
\]

The **regret** is the opportunity loss for one step
\[
l_t = 𝔼[Q(a^*)-Q(a_t)]
\]

## Epsilon-Greedy
* Eplore with probability \(ε\)
* Eploit with probability \(1-ε\)
* Estimated action-value for arm \(a\) is \[\hat{Q}_t(a)=\frac{1}{N_t(a)}\sum_{t=1}^T r_t 𝟙[a_t=a]\]
* Arm to exploit: \[a_t^*=\operatorname{argmax}_{a∈A}\hat{Q}_t(a)\]


## Bernoulli-Uniform Bandit
The **reward** \(r\) is a random number sampled from a probability distribution. The distributions are assumed to be known and independent, but the parameters unknown. For example, the reward for *Bernoulli-Uniform* bandit is
\[
r∼\operatorname{Bernoulli}(θ)⋅\operatorname{Uniform}(l,h)
\]
where \(θ∈[0,1]\) and \(l,h∈ℝ, l≤h\). The expected reward for action \(a\) is
\[
\begin{aligned}
𝔼[r∣a] & = 𝔼[\operatorname{Bernoulli}(θ)]⋅𝔼[\operatorname{Uniform}(l,h)] \\ & =
θ ⋅ (l+h)/2.
\end{aligned}
\]

Other distributions could be used in similar way.


## Epsilon-Greedy with Decreasing Epsilon
The Epsilon-Greedy should be modified such that initially it explores more in order to estimate the action values and as time increases and the evidence for action value estimates increase, the epsilon should decrease such that the best arm is exploited more often.

A naive formulation of epsilon \(ε_t\) is to formulate it as a decreasing function \(ε_{t+1}<ε_t\) of time \(t\) starting from initial epsilon \(ε_0\) decreasing towards zero as time tends towards infinity \(t→∞\). For example,
\[
ε_t=ε_0/t^{c}
\]
where \(c∈ℝ\) is a parameter that controls the rate of the decrease. For larger number of bandits the rate of decrease should be set lower. If \(c=0\) the approach reduces to normal Epsilon-Greedy.

<!-- **NOTE**: The confidence interval approach is the non-naive -- but not epsilon-greedy -- approach. It takes into account the amount of times each action has been taken \(N_t(a)\). -->
