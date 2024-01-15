clc;
clear;
tic;
sdpvar x1 x2;

init = [-(x1 - (0.0))*(x1-(1.0));-(x2 - (1.0))*(x2-(2.0))];
unsafe = [-(x1 - (-2.0))*(x1-(-0.5));-(x2 - (-0.75))*(x2-(0.75))];
inv = [-(x1 - (-2.0))*(x1-(2.0));-(x2 - (-2.0))*(x2-(2.0))];

f = [2*x1*x2 + x2; 2*x1^2 - x1 - x2^2];

[B, b, v] = polynomial([x1, x2], 2);
par = [b];

[P1, p1, pv1] = polynomial([x1, x2], 2);
[P2, p2, pv2] = polynomial([x1, x2], 2);
B_I = B - P1 * init(1) - P2 * init(2);
con = [sos(B_I), sos(P1), sos(P2)];
par = [par; p1; p2];

[Q1, q1, qv1] = polynomial([x1, x2], 2);
[Q2, q2, qv2] = polynomial([x1, x2], 2);
B_U = -B - Q1 * unsafe(1) - Q2 * unsafe(2);
con = [con, sos(B_U), sos(Q1), sos(Q2)];
par = [par; q1; q2];

DB = jacobian(B, x1) * f(1) + jacobian(B, x2) * f(2);
[S1, s1, sv1] = polynomial([x1, x2], 2);
[S2, s2, sv2] = polynomial([x1, x2], 2);
[R, r, rv] = polynomial([x1, x2], 2);
DB = DB - R * B - S1 * inv(1) - S2 * inv(2);
con = [con, sos(DB), sos(S1), sos(S2)];
par = [par; r; s1; s2];

ops = sdpsettings('solver', 'penbmi');
sol = solvesos(con,[],ops,par);
if sol.problem == 0
    fprintf('Solved successfully!');
    sdisplay(v')
    value(b')
    sdisplay((double(b))'*v)
elseif sol.problem == 1
    disp('Solver thinks it is infeasible');
else
    disp('Something else happened');
end
toc;