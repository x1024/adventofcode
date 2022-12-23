:- use_module(library(clpq)).
:- assert(clpfd:full_answer).

pred(slln, 19).

pred(trcj, A) :- p1(B), pred(asdf, C), A #= B + C, format("qwer = ~w, asdf = ~w | ~w", [B, C, B + C]).

pred(bbls, 30) :- pred(slln, A), pred(asdf, B), 30 #= A + B.

?- pred(bbls, C).
