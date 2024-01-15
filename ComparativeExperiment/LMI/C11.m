clc;
clear;
tic;
pvar x1 x2 x3 x4;
vars = [x1, x2, x3, x4];
f = [-0.5*x1^2 - 2*x2^2 - 2*x3^2 + 2*x4^2; -x1*x2 - 1; -x1*x3; -x1*x4];

prog = sosprogram(vars);
[prog, B] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff1');

init = [-(x1 - (-0.20000000298023224))*(x1-(0.20000000298023224));-(x2 - (-1.2000000476837158))*(x2-(-0.800000011920929));-(x3 - (-1.5))*(x3-(1.5));-(x4 - (-1.5))*(x4-(1.5))];
unsafe = [-(x1 - (-1.2000000476837158))*(x1-(-0.800000011920929));-(x2 - (-0.20000000298023224))*(x2-(0.20000000298023224));-(x3 - (-1.5))*(x3-(1.5));-(x4 - (-1.5))*(x4-(1.5))];
inv = [-(x1 - (-1.5))*(x1-(1.5));-(x2 - (-1.5))*(x2-(1.5));-(x3 - (-1.5))*(x3-(1.5));-(x4 - (-1.5))*(x4-(1.5))];

[prog, P1] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff2');
prog = sosineq(prog,P1);
[prog, P2] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff3');
prog = sosineq(prog,P2);
[prog, P3] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff4');
prog = sosineq(prog,P3);
[prog, P4] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff5');
prog = sosineq(prog,P4);
[prog, Q1] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff6');
prog = sosineq(prog,Q1);
[prog, Q2] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff7');
prog = sosineq(prog,Q2);
[prog, Q3] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff8');
prog = sosineq(prog,Q3);
[prog, Q4] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff9');
prog = sosineq(prog,Q4);
[prog, S1] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff10');
prog = sosineq(prog,S1);
[prog, S2] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff11');
prog = sosineq(prog,S2);
[prog, S3] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff12');
prog = sosineq(prog,S3);
[prog, S4] = sospolyvar(prog, monomials([x1; x2; x3; x4],[0,1,2]), 'wscoeff13');
prog = sosineq(prog,S4);
B_I = B - init(1) * P1 - init(2) * P2 - init(3) * P3 - init(4) * P4;
prog = sosineq(prog,B_I);
B_U = - B - unsafe(1) * Q1 - unsafe(2) * Q2 - unsafe(3) * Q3 - unsafe(4) * Q4;
prog = sosineq(prog,B_U);
DB = diff(B, x1) * f(1) + diff(B, x2) * f(2) + diff(B, x3) * f(3) + diff(B, x4) * f(4);
r=monomials([x1; x2; x3; x4],[0,1,2]);
R = 0;
for i = 1:size(r)
    R = R + randn(1) * r(i);
end
DB = DB - R * B - inv(1) * S1 - inv(2) * S2 - inv(3) * S3 - inv(4) * S4;
prog = sosineq(prog, DB);
solver_opt.solver = 'sedumi';
prog = sossolve(prog, solver_opt);
SOLB = sosgetsol(prog,B)
toc;
