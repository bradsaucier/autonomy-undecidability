# Proof note: Undecidability of full computational autonomy

## 1 Goal

We want to formalize a strong notion of "full computational autonomy" and show that deciding whether an arbitrary program has this property is undecidable.

## 2 Modeling choice

Let programs be Turing-complete and interpret each program e as computing a partial function phi_e from inputs to outputs. A property A of programs is semantic if membership depends only on the function phi_e and not on the program's syntax.

Assume "full autonomy" corresponds to a semantic property A that is nontrivial. Nontrivial means there exists at least one program whose behavior is autonomous in this sense, and at least one program whose behavior is not.

## 3 Rice's Theorem argument

Rice's Theorem states that every nontrivial semantic property of partial computable functions is undecidable. Because A is assumed to be semantic and nontrivial, membership in A is undecidable.

This captures the main ceiling: if autonomy is defined as a global behavioral property of arbitrary programs, there is no general decision procedure.

## 4 Reduction sketch from halting

The same ceiling can be seen through a reduction.

### 4.1 Choose witnesses

Pick e_yes such that e_yes is in A.
Pick e_no such that e_no is not in A.

### 4.2 Define a transformation

Given an arbitrary program e and input x, construct a new program g(e, x) that behaves as follows on any input y.

4.2.1 Simulate e on input x.
4.2.2 If the simulation halts, run e_yes on input y and return its output.
4.2.3 If the simulation does not halt, behave like e_no on input y.

### 4.3 Correctness

If e halts on x, then g(e, x) computes the same function as e_yes, so g(e, x) is in A.
If e does not halt on x, then g(e, x) computes the same function as e_no, so g(e, x) is not in A.

Therefore, deciding whether g(e, x) is in A decides whether e halts on x. Since halting is undecidable, deciding A is undecidable.

## 5 Practical interpretation

The result does not prevent strong guarantees in restricted settings. It says there is no universal procedure that works for all programs with no bounds and no assumptions. Practical verification succeeds by adding structure and bounds, including time limits, finite state abstractions, restricted languages, and compositional guarantees.
