clc;
clear;
tic;
sdpvar x1 x2 x3 x4 x5 x6;

init = [-(x1 - (0.5))*(x1-(1.5));-(x2 - (0.5))*(x2-(1.5));-(x3 - (0.5))*(x3-(1.5));-(x4 - (0.5))*(x4-(1.5));-(x5 - (0.5))*(x5-(1.5));-(x6 - (0.5))*(x6-(1.5))];
unsafe = [-(x1 - (-2.0))*(x1-(-1.600000023841858));-(x2 - (-2.0))*(x2-(-1.600000023841858));-(x3 - (-2.0))*(x3-(-1.600000023841858));-(x4 - (-2.0))*(x4-(-1.600000023841858));-(x5 - (-2.0))*(x5-(-1.600000023841858));-(x6 - (-2.0))*(x6-(-1.600000023841858))];
inv = [-(x1 - (-2.0))*(x1-(2.0));-(x2 - (-2.0))*(x2-(2.0));-(x3 - (-2.0))*(x3-(2.0));-(x4 - (-2.0))*(x4-(2.0));-(x5 - (-2.0))*(x5-(2.0));-(x6 - (-2.0))*(x6-(2.0))];

f = [x2; x3; x4; x5; x6; -576*x1 - 2400*x2 - 4180*x3 - 3980*x4 - 2273*x5 - 800*x6];

[B, b, v] = polynomial([x1, x2, x3, x4, x5, x6], 2);
par = [b];

[P1, p1, pv1] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[P2, p2, pv2] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[P3, p3, pv3] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[P4, p4, pv4] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[P5, p5, pv5] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[P6, p6, pv6] = polynomial([x1, x2, x3, x4, x5, x6], 2);
B_I = B - P1 * init(1) - P2 * init(2) - P3 * init(3) - P4 * init(4) - P5 * init(5) - P6 * init(6);
con = [sos(B_I), sos(P1), sos(P2), sos(P3), sos(P4), sos(P5), sos(P6)];
par = [par; p1; p2; p3; p4; p5; p6];

[Q1, q1, qv1] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[Q2, q2, qv2] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[Q3, q3, qv3] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[Q4, q4, qv4] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[Q5, q5, qv5] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[Q6, q6, qv6] = polynomial([x1, x2, x3, x4, x5, x6], 2);
B_U = -B - Q1 * unsafe(1) - Q2 * unsafe(2) - Q3 * unsafe(3) - Q4 * unsafe(4) - Q5 * unsafe(5) - Q6 * unsafe(6);
con = [con, sos(B_U), sos(Q1), sos(Q2), sos(Q3), sos(Q4), sos(Q5), sos(Q6)];
par = [par; q1; q2; q3; q4; q5; q6];

DB = jacobian(B, x1) * f(1) + jacobian(B, x2) * f(2) + jacobian(B, x3) * f(3) + jacobian(B, x4) * f(4) + jacobian(B, x5) * f(5) + jacobian(B, x6) * f(6);
[S1, s1, sv1] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[S2, s2, sv2] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[S3, s3, sv3] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[S4, s4, sv4] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[S5, s5, sv5] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[S6, s6, sv6] = polynomial([x1, x2, x3, x4, x5, x6], 2);
[R, r, rv] = polynomial([x1, x2, x3, x4, x5, x6], 2);
DB = DB - R * B - S1 * inv(1) - S2 * inv(2) - S3 * inv(3) - S4 * inv(4) - S5 * inv(5) - S6 * inv(6);
con = [con, sos(DB), sos(S1), sos(S2), sos(S3), sos(S4), sos(S5), sos(S6)];
par = [par; r; s1; s2; s3; s4; s5; s6];

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