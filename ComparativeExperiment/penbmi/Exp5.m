clc;
clear;
tic;
sdpvar x1 x2 x3;

init = [0.25-((x1-(-14.5))^2+(x2-(-14.5))^2+(x3-(12.5))^2)];
unsafe = [0.25-((x1-(-16.5))^2+(x2-(-14.5))^2+(x3-(2.5))^2)];
inv = [-(x1 - (-20.0))*(x1-(20.0));-(x2 - (-20.0))*(x2-(20.0));-(x3 - (-20.0))*(x3-(20.0))];

f = [-10.0*x1 + 10.0*x2; x1*(28.0 - x3) - x2; x1*x2 - 2.66666666666667*x3];

[B, b, v] = polynomial([x1, x2, x3], 2);
par = [b];

[P1, p1, pv1] = polynomial([x1, x2, x3], 2);
B_I = B - P1 * init(1);
con = [sos(B_I), sos(P1)];
par = [par; p1];

[Q1, q1, qv1] = polynomial([x1, x2, x3], 2);
B_U = -B - Q1 * unsafe(1);
con = [con, sos(B_U), sos(Q1)];
par = [par; q1];

DB = jacobian(B, x1) * f(1) + jacobian(B, x2) * f(2) + jacobian(B, x3) * f(3);
[S1, s1, sv1] = polynomial([x1, x2, x3], 2);
[S2, s2, sv2] = polynomial([x1, x2, x3], 2);
[S3, s3, sv3] = polynomial([x1, x2, x3], 2);
[R, r, rv] = polynomial([x1, x2, x3], 2);
DB = DB - R * B - S1 * inv(1) - S2 * inv(2) - S3 * inv(3);
con = [con, sos(DB), sos(S1), sos(S2), sos(S3)];
par = [par; r; s1; s2; s3];

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