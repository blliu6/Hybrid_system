clc;
clear;
tic;
sdpvar x1 x2 x3 x4 x5 x6 x7;

init = [0.0001-((x1-(1.0))^2+(x2-(1.0))^2+(x3-(1.0))^2+(x4-(1.0))^2+(x5-(1.0))^2+(x6-(1.0))^2+(x7-(1.0))^2)];
unsafe = [0.010000000000000002-((x1-(1.899999976158142))^2+(x2-(1.899999976158142))^2+(x3-(1.899999976158142))^2+(x4-(1.899999976158142))^2+(x5-(1.899999976158142))^2+(x6-(1.899999976158142))^2+(x7-(1.899999976158142))^2)];
inv = [-(x1 - (-2.0))*(x1-(2.0));-(x2 - (-2.0))*(x2-(2.0));-(x3 - (-2.0))*(x3-(2.0));-(x4 - (-2.0))*(x4-(2.0));-(x5 - (-2.0))*(x5-(2.0));-(x6 - (-2.0))*(x6-(2.0));-(x7 - (-2.0))*(x7-(2.0))];

f = [-0.4*x1 + 5*x3*x4; 0.4*x1 - x2; x2 - 5*x3*x4; -5*x3*x4 + 5*x5*x6; 5*x3*x4 - 5*x5*x6; -5*x5*x6 + 0.5*x7; 5*x5*x6 - 0.5*x7];

[B, b, v] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
par = [b];

[P1, p1, pv1] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
B_I = B - P1 * init(1);
con = [sos(B_I), sos(P1)];
par = [par; p1];

[Q1, q1, qv1] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
B_U = -B - Q1 * unsafe(1);
con = [con, sos(B_U), sos(Q1)];
par = [par; q1];

DB = jacobian(B, x1) * f(1) + jacobian(B, x2) * f(2) + jacobian(B, x3) * f(3) + jacobian(B, x4) * f(4) + jacobian(B, x5) * f(5) + jacobian(B, x6) * f(6) + jacobian(B, x7) * f(7);
[S1, s1, sv1] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
[S2, s2, sv2] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
[S3, s3, sv3] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
[S4, s4, sv4] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
[S5, s5, sv5] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
[S6, s6, sv6] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
[S7, s7, sv7] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
[R, r, rv] = polynomial([x1, x2, x3, x4, x5, x6, x7], 2);
DB = DB - R * B - S1 * inv(1) - S2 * inv(2) - S3 * inv(3) - S4 * inv(4) - S5 * inv(5) - S6 * inv(6) - S7 * inv(7);
con = [con, sos(DB), sos(S1), sos(S2), sos(S3), sos(S4), sos(S5), sos(S6), sos(S7)];
par = [par; r; s1; s2; s3; s4; s5; s6; s7];

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