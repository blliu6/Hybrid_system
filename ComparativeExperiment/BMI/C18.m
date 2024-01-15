clc;
clear;
tic;
sdpvar x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12;

init = [0.010000000000000002-((x1-(0.0))^2+(x2-(0.0))^2+(x3-(0.0))^2+(x4-(0.0))^2+(x5-(0.0))^2+(x6-(0.0))^2+(x7-(0.0))^2+(x8-(0.0))^2+(x9-(0.0))^2+(x10-(0.0))^2+(x11-(0.0))^2+(x12-(0.0))^2)];
unsafe = [0.010000000000000002-((x1-(1.0))^2+(x2-(1.0))^2+(x3-(1.0))^2+(x4-(1.0))^2+(x5-(1.0))^2+(x6-(1.0))^2+(x7-(1.0))^2+(x8-(1.0))^2+(x9-(1.0))^2+(x10-(1.0))^2+(x11-(1.0))^2+(x12-(1.0))^2)];
inv = [-(x1 - (-2.0))*(x1-(2.0));-(x2 - (-2.0))*(x2-(2.0));-(x3 - (-2.0))*(x3-(2.0));-(x4 - (-2.0))*(x4-(2.0));-(x5 - (-2.0))*(x5-(2.0));-(x6 - (-2.0))*(x6-(2.0));-(x7 - (-2.0))*(x7-(2.0));-(x8 - (-2.0))*(x8-(2.0));-(x9 - (-2.0))*(x9-(2.0));-(x10 - (-2.0))*(x10-(2.0));-(x11 - (-2.0))*(x11-(2.0));-(x12 - (-2.0))*(x12-(2.0))];

f = [x4; x5; x6; -7253.4927*x1 + 1936.3639*x11 - 1338.7624*x4 + 1333.3333*x8; -1936.3639*x10 - 7253.4927*x2 - 1338.7624*x5 + 1333.3333*x7; -769.2308*x3 - 770.2301*x6; x10; x11; x12; 9.81*x2; -9.81*x1; -16.3541*x12 - 15.3846*x9];

[B, b, v] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
par = [b];

[P1, p1, pv1] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
B_I = B - P1 * init(1);
con = [sos(B_I), sos(P1)];
par = [par; p1];

[Q1, q1, qv1] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
B_U = -B - Q1 * unsafe(1);
con = [con, sos(B_U), sos(Q1)];
par = [par; q1];

DB = jacobian(B, x1) * f(1) + jacobian(B, x2) * f(2) + jacobian(B, x3) * f(3) + jacobian(B, x4) * f(4) + jacobian(B, x5) * f(5) + jacobian(B, x6) * f(6) + jacobian(B, x7) * f(7) + jacobian(B, x8) * f(8) + jacobian(B, x9) * f(9) + jacobian(B, x10) * f(10) + jacobian(B, x11) * f(11) + jacobian(B, x12) * f(12);
[S1, s1, sv1] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S2, s2, sv2] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S3, s3, sv3] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S4, s4, sv4] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S5, s5, sv5] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S6, s6, sv6] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S7, s7, sv7] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S8, s8, sv8] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S9, s9, sv9] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S10, s10, sv10] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S11, s11, sv11] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[S12, s12, sv12] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
[R, r, rv] = polynomial([x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12], 2);
DB = DB - R * B - S1 * inv(1) - S2 * inv(2) - S3 * inv(3) - S4 * inv(4) - S5 * inv(5) - S6 * inv(6) - S7 * inv(7) - S8 * inv(8) - S9 * inv(9) - S10 * inv(10) - S11 * inv(11) - S12 * inv(12);
con = [con, sos(DB), sos(S1), sos(S2), sos(S3), sos(S4), sos(S5), sos(S6), sos(S7), sos(S8), sos(S9), sos(S10), sos(S11), sos(S12)];
par = [par; r; s1; s2; s3; s4; s5; s6; s7; s8; s9; s10; s11; s12];

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