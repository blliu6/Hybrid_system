clc;
clear;
tic;
sdpvar x1 x2;

local_1 = [-(x1+2)*x1,-(x2+2)*(x2-2)];
local_2 = [-x1*(x1-2),-(x2+2)*(x2-2)];
init = [0.5^2 - (x1+1)^2 - (x2+1)^2];
unsafe = [0.5^2 - (x-1)^2 - (x2-1)^2];
guard_1 = [-x1*(x1-2),-(x2+2)*(x2-2)];
guard_2 = [-(x1+2)*x1,-(x2+2)*(x2-2)];

f_1 = [x2,x1-0.25*x1^2];
f_2 = [x2,-x1-0.5*x1^3];


[B_1, b_1, v_1] = polynomial([x1, x2], 2);
[B_2, b_2, v_2] = polynomial([x1, x2], 2);

par = [b_1; b_2];

[P1, p1, pv1] = polynomial([x1, x2], 2);
B_I = B_1 - P1 * init(1);
con = [sos(P1), sos(B_I), sos(P1)];
par = [par; p1];

[Q1, q1, qv1] = polynomial([x1, x2], 2);
B_U = -B_2 - Q1 * unsafe(1);
con = [con, sos(Q1), sos(B_U)];
par = [par; q1];

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
par = [par; s1; s2; s3; s4; r1; r2];

[W1, w1, wv1] = polynomial([x1, x2], 2);
[W2, w2, wv2] = polynomial([x1, x2], 2);
[W3, w3, wv3] = polynomial([x1, x2], 2);
[W4, w4, wv4] = polynomial([x1, x2], 2);
[R3, r3, rv3] = polynomial([x1, x2], 2);
[R4, r4, rv4] = polynomial([x1, x2], 2);
H_1 = b_2' * monolist([x1, x2], 2) - R3 * B_1 - W1 * guard_1(1) - W2 * guard_1(2);
H_2 = b_1' * monolist([x1, x2], 2) - R4 * B_2 - W3 * guard_2(1) - W4 * guard_2(2);
con = [con, sos(H_1), sos(H_2), sos(W1), sos(W2), sos(W3), sos(W4), sos(R3), sos(R4)];
par = [par; w1; w2; w3; w4; r3; r4];


ops = sdpsettings('solver', 'penbmi','penbmi.PBM_MAX_ITER',500);
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