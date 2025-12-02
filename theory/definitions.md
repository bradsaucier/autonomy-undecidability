# Definitions

## 1 Partial computable function

A partial computable function is a function computed by a program that may fail to halt on some inputs. On inputs where it halts, it produces an output.

## 2 Semantic property

A property of programs is semantic if it depends only on the input-output behavior of the function the program computes, not on the specific source code form.

## 3 Nontrivial property

A property is nontrivial if there exists at least one program that has the property and at least one program that does not.

## 4 Rice's Theorem

Rice's Theorem states that every nontrivial semantic property of partial computable functions is undecidable. In other words, there is no algorithm that can decide such a property correctly for all programs.

## 5 Halting Problem

The Halting Problem asks whether a given program halts on a given input. It is undecidable.

## 6 Many-one reduction

A many-one reduction from problem A to problem B is a computable function f such that x is in A if and only if f(x) is in B. If such an f exists and B is decidable, then A would be decidable.

## 7 Autonomy property (for this repository)

The demo uses a concrete property over bounded runs in a toy environment.

7.1 Safety: the agent never enters a hazard cell.
7.2 Liveness: within the step limit, the agent reaches the goal and signals success.

This bounded property is used to illustrate the structure of a reduction. It is not a claim that real autonomy is fully captured by this definition.
