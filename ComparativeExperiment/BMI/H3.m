clc;
clear;
tic;
sdpvar x1 x2;

% local_1 = [-x1];
% local_2 = [x1];
init = [0.5^2 - (x1+2)^2 - (x2-2)^2];
unsafe = [0.5^2 - (x1-2)^2 - (x2-2)^2];
guard_1 = [0.75^2 - x1^2 -x2^2];
guard_2 = [0.5^2 - x1^2 -x2^2];

f_1 = [-x1+x1*x2,-x2];
f_2 = [-x1+2*x1^2*x2,-x2];


[B_1, b_1, v_1] = polynomial([x1, x2], 3);
[B_2, b_2, v_2] = polynomial([x1, x2], 3);

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
[R1, r1, rv1] = polynomial([x1, x2], 2);
[R2, r2, rv2] = polynomial([x1, x2], 2);

DB_1 = DB_1 - R1 * B_1 - S1 * (-x1);
DB_2 = DB_2 - R2 * B_2 - S2 * x1;

con = [con, sos(DB_1), sos(DB_2), sos(S1), sos(S2)];
par = [par; s1; s2; r1; r2];

[S3, s3, sv3] = polynomial([x1, x2], 2);
[S4, s4, sv4] = polynomial([x1, x2], 2);
[R3, r3, rv3] = polynomial([x1, x2], 2);
[R4, r4, rv4] = polynomial([x1, x2], 2);
H_1 = b_2' * monolist([-x1, x2], 3) - R3 * B_1 - S3 * guard_1(1);
H_2 = b_1' * monolist([x1 - 2, x2 + 1], 3) - R4 * B_2 - S4 * guard_2(2);
con = [con, sos(H_1), sos(H_2), sos(S3), sos(S4), sos(R3), sos(R4)];
par = [par; s3; s4; r3; r4];


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