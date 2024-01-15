clc;
clear;
tic;
sdpvar x1 x2;

local_1 = [-(x1+5)*x1,-(x2+5)*(x2-5)];
local_2 = [-(x1-5)*x1,-(x2+5)*(x2-5)];
init = [-(x1+1)*(x1+2),-(x2+1)*(x2+2)];
unsafe = [-x1*(x1-1),-(x2+2)*(x2+1)];
guard_1 = [0.5^2 - (x1+0.5)^2 -(x2+0.5)^2];
guard_2 = [0.5^2 - (x1-1)^2 -(x2-1)^2];

f_1 = [x1-x1*x2,-x2+x1*x2];
f_2 = [x1+x1^2*x2,x2+x1*x2];


[B_1, b_1, v_1] = polynomial([x1, x2], 2);
[B_2, b_2, v_2] = polynomial([x1, x2], 2);

par = [b_1; b_2];

[P1, p1, pv1] = polynomial([x1, x2], 2);
[P2, p2, pv2] = polynomial([x1, x2], 2);
B_I = B_1 - P1 * init(1) - P2 * init(2);
con = [sos(P1), sos(B_I), sos(P1), sos(P2)];
par = [par; p1; p2];

[Q1, q1, qv1] = polynomial([x1, x2], 2);
[Q2, q2, qv2] = polynomial([x1, x2], 2);
B_U = -B_2 - Q1 * unsafe(1) - Q2 * unsafe(2);
con = [con, sos(Q1), sos(B_U), sos(Q2)];
par = [par; q1; q2];

DB_1 = jacobian(B_1, x1) * f_1(1) + jacobian(B_1, x2) * f_1(2);
DB_2 = jacobian(B_2, x1) * f_2(1) + jacobian(B_2, x2) * f_2(2);

[S1, s1, sv1] = polynomial([x1, x2], 2);
[S2, s2, sv2] = polynomial([x1, x2], 2);
[S3, s3, sv3] = polynomial([x1, x2], 2);
[S4, s4, sv4] = polynomial([x1, x2], 2);
[R1, r1, rv1] = polynomial([x1, x2], 2);
[R2, r2, rv2] = polynomial([x1, x2], 2);

DB_1 = DB_1 - R1 * B_1 - S1 * local_1(1) - S2 * local_1(2);
DB_2 = DB_2 - R2 * B_2 - S3 * local_2(1) - S4 * local_2(2);

con = [con, sos(DB_1), sos(DB_2), sos(S1), sos(S2), sos(S3), sos(S4)];
par = [par; s1; s2; r1; r2; s3; s4];

[S5, s5, sv5] = polynomial([x1, x2], 2);
[S6, s6, sv6] = polynomial([x1, x2], 2);
[R3, r3, rv3] = polynomial([x1, x2], 2);
[R4, r4, rv4] = polynomial([x1, x2], 2);
H_1 = b_2' * monolist([-x1 + 2, -x2 + 2], 2) - R3 * B_1 - S5 * guard_1(1);
H_2 = b_1' * monolist([x1 - 2, x2 - 2], 2) - R4 * B_2 - S6 * guard_2(1);
con = [con, sos(H_1), sos(H_2), sos(S5), sos(S6), sos(R3), sos(R4)];
par = [par; s5; s6; r3; r4];


ops = sdpsettings('solver', 'penbmi');
sol = solvesos(con,[],ops,par);

if sol.problem == 0
    fprintf('Solved successfully!');
    sdisplay((double(b_1))'*v_1)
    sdisplay((double(b_2))'*v_2)
elseif sol.problem == 1
    disp('Solver thinks it is infeasible');
else
    disp('Something else happened');
end
toc;