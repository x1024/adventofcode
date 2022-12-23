:- use_module(library(clpq)).
:- assert(clpfd:full_answer).

p1(A):- A #> 0, A #< 100.
B :- B #> 0, B #< 100.
p2(Z):- Z #= B + 2, format('B = ~w', [B]).
