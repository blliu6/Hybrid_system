clc;
clear;
tic;
sdpvar x1 x2 x3 x4;

init = [-(x1 - (-0.20000000298023224))*(x1-(0.20000000298023224));-(x2 - (-1.2000000476837158))*(x2-(-0.800000011920929));-(x3 - (-1.5))*(x3-(1.5));-(x4 - (-1.5))*(x4-(1.5))];
unsafe = [-(x1 - (-1.2000000476837158))*(x1-(-0.800000011920929));-(x2 - (-0.20000000298023224))*(x2-(0.20000000298023224));-(x3 - (-1.5))*(x3-(1.5));-(x4 - (-1.5))*(x4-(1.5))];
inv = [-(x1 - (-1.5))*(x1-(1.5));-(x2 - (-1.5))*(x2-(1.5));-(x3 - (-1.5))*(x3-(1.5));-(x4 - (-1.5))*(x4-(1.5))];

f = [-0.5*x1^2 - 2*x2^2 - 2*x3^2 + 2*x4^2; -x1*x2 - 1; -x1*x3; -x1*x4];

[B, b, v] = polynomial([x1, x2, x3, x4], 2);
par = [b];

[P1, p1, pv1] = polynomial([x1, x2, x3, x4], 2);
[P2, p2, pv2] = polynomial([x1, x2, x3, x4], 2);
[P3, p3, pv3] = polynomial([x1, x2, x3, x4], 2);
[P4, p4, pv4] = polynomial([x1, x2, x3, x4], 2);
B_I = B - P1 * init(1) - P2 * init(2) - P3 * init(3) - P4 * init(4);
con = [sos(B_I), sos(P1), sos(P2), sos(P3), sos(P4)];
par = [par; p1; p2; p3; p4];

[Q1, q1, qv1] = polynomial([x1, x2, x3, x4], 2);
[Q2, q2, qv2] = polynomial([x1, x2, x3, x4], 2);
[Q3, q3, qv3] = polynomial([x1, x2, x3, x4], 2);
[Q4, q4, qv4] = polynomial([x1, x2, x3, x4], 2);
B_U = -B - Q1 * unsafe(1) - Q2 * unsafe(2) - Q3 * unsafe(3) - Q4 * unsafe(4);
con = [con, sos(B_U), sos(Q1), sos(Q2), sos(Q3), sos(Q4)];
par = [par; q1; q2; q3; q4];

DB = jacobian(B, x1) * f(1) + jacobian(B, x2) * f(2) + jacobian(B, x3) * f(3) + jacobian(B, x4) * f(4);
[S1, s1, sv1] = polynomial([x1, x2, x3, x4], 2);
[S2, s2, sv2] = polynomial([x1, x2, x3, x4], 2);
[S3, s3, sv3] = polynomial([x1, x2, x3, x4], 2);
[S4, s4, sv4] = polynomial([x1, x2, x3, x4], 2);
[R, r, rv] = polynomial([x1, x2, x3, x4], 2);
DB = DB - R * B - S1 * inv(1) - S2 * inv(2) - S3 * inv(3) - S4 * inv(4);
con = [con, sos(DB), sos(S1), sos(S2), sos(S3), sos(S4)];
par = [par; r; s1; s2; s3; s4];

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