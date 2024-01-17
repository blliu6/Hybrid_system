clc;
clear;
tic;
sdpvar x1 x2 x3;

local_1 = [-(x1+1.1)*(x1-1.1),-(x2+11)*(x2-11),-(x3+11)*(x3-11)];
local_2 = [-(x1-0.17)*(x1-12),-(x2-0.17)*(x2-12),-(x3-0.17)*(x3-12)];
init = [0.01 - x1^2-x2^2-x3^2];
unsafe = [-(x1-5)*(x1-5.1)];
guard_1 = [-(x1-0.99)*(x1-1.01),-(x2-9.95)*(x2-10.05),-(x3-9.95)*(x3-10.05)];
guard_2 = [-(x1-0.17)*(x1-0.23),-(x2-0.17)*(x2-0.23),-(x3-0.17)*(x3-0.23)];

f_1 = [-x2,-x1+x3,x1+(2*x2+3*x3)*(1+x3^2)];
f_2 = [-x2,-x1+x3,-x1-2*x2-3*x3];


[B_1, b_1, v_1] = polynomial([x1, x2, x3], 2);
[B_2, b_2, v_2] = polynomial([x1, x2, x3], 2);

par = [b_1; b_2];

[P1, p1, pv1] = polynomial([x1, x2, x3], 2);
B_I = B_1 - P1 * init(1);
con = [sos(P1), sos(B_I), sos(P1)];
par = [par; p1];

[Q1, q1, qv1] = polynomial([x1, x2, x3], 2);
B_U = -B_2 - Q1 * unsafe(1);
con = [con, sos(Q1), sos(B_U)];
par = [par; q1];

DB_1 = jacobian(B_1, x1) * f_1(1) + jacobian(B_1, x2) * f_1(2) + jacobian(B_1, x3) * f_1(3);
DB_2 = jacobian(B_2, x1) * f_2(1) + jacobian(B_2, x2) * f_2(2) + jacobian(B_2, x3) * f_2(3);

[S1, s1, sv1] = polynomial([x1, x2, x3], 2);
[S2, s2, sv2] = polynomial([x1, x2, x3], 2);
[S3, s3, sv3] = polynomial([x1, x2, x3], 2);
[S4, s4, sv4] = polynomial([x1, x2, x3], 2);
[S5, s5, sv5] = polynomial([x1, x2, x3], 2);
[S6, s6, sv6] = polynomial([x1, x2, x3], 2);

[R1, r1, rv1] = polynomial([x1, x2, x3], 2);
[R2, r2, rv2] = polynomial([x1, x2, x3], 2);

DB_1 = DB_1 - R1 * B_1 - S1 * local_1(1) - S2 * local_1(2) - S3 * local_1(3);
DB_2 = DB_2 - R2 * B_2 - S4 * local_2(1) - S5 * local_2(2) - S6 * local_2(3);

con = [con, sos(DB_1), sos(DB_2), sos(S1), sos(S2), sos(S3), sos(S4), sos(S5), sos(S6)];
par = [par; s1; s2; r1; r2; s3; s4; s5; s6];

[W1, w1, wv1] = polynomial([x1, x2, x3], 2);
[W2, w2, wv2] = polynomial([x1, x2, x3], 2);
[W3, w3, wv3] = polynomial([x1, x2, x3], 2);
[W4, w4, wv4] = polynomial([x1, x2, x3], 2);
[W5, w5, wv5] = polynomial([x1, x2, x3], 2);
[W6, w6, wv6] = polynomial([x1, x2, x3], 2);
[R3, r3, rv3] = polynomial([x1, x2, x3], 2);
[R4, r4, rv4] = polynomial([x1, x2, x3], 2);
H_1 = b_2' * monolist([x1, x2, x3], 2) - R3 * B_1 - W1 * guard_1(1) - W2 * guard_1(2) - W3 * guard_1(3);
H_2 = b_1' * monolist([x1, x2, x3], 2) - R4 * B_2 - W4 * guard_2(1) - W5 * guard_2(2) - W6 * guard_2(3);
con = [con, sos(H_1), sos(H_2), sos(W1), sos(W2), sos(R3), sos(R4), sos(W3), sos(W4), sos(W5), sos(W6)];
par = [par; w1; w2; r3; r4; w3; w4; w5; w6];


ops = sdpsettings('solver', 'penbmi');
sol = solvesos(con,[],ops,par);

if sol.problem == 0
    fprintf('Solved successfully!\n');
    sdisplay((double(b_1))'*v_1)
    sdisplay((double(b_2))'*v_2)
elseif sol.problem == 1
    disp('Solver thinks it is infeasible');
else
    disp('Something else happened');
end
toc;