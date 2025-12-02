# Start Here

## 1 The question

Many goals can be phrased like this: given a program that controls an agent, decide whether it will reliably reach its objective without unsafe behavior. If we ask for a universal algorithm that answers this question correctly for every possible program, we run into a formal barrier.

## 2 The formal barrier

A property is semantic when it depends on what a program does as a function from inputs to outputs, not on its surface syntax. Rice's Theorem states that every nontrivial semantic property of partial computable functions is undecidable. "Nontrivial" means the property holds for at least one program and fails for at least one program.

If "full computational autonomy" is modeled as a nontrivial semantic property of program behavior, then there is no algorithm that can decide that property for all programs.

## 3 The reduction idea

One way to see the barrier is to connect an autonomy decision procedure to the Halting Problem. If we could decide autonomy for all programs, we could decide whether an arbitrary program halts on an input, which is impossible.

A standard structure is:

1. Choose one program that clearly satisfies the autonomy property.
2. Choose one program that clearly fails the autonomy property.
3. Given an arbitrary program and input, build a new program that behaves like the first if the original halts, and like the second if it does not halt.
4. A correct autonomy decider would therefore decide halting.

## 4 What the demo implements

The Python demo implements this structure in a bounded way. It simulates a simple machine for at most B steps. If the simulated machine halts within B steps, the controller switches to a policy that reaches the goal while avoiding hazards. If it does not halt within B steps, the controller switches to a policy that never reaches the goal.

Because of the bound, the demo does not decide halting. It demonstrates why unbounded guarantees are not available in general, and why bounded guarantees are the practical alternative.

## 5 Where to look next

See theory/proof_note.md for a proof sketch.
See theory/definitions.md for terms.
Read src/computational_autonomy/reduction.py for the construction used by the demo.
Run autonomy-demo to see the bounded reduction behavior.
