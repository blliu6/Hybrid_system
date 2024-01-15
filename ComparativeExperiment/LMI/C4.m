clc;
clear;
tic;
pvar x1 x2;
vars = [x1, x2];
f = [2*x1^2*x2 - x1; -x2];

prog = sosprogram(vars);
[prog, B] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff1');

init = [-(x1 - (-0.25))*(x1-(0.25));-(x2 - (0.75))*(x2-(1.5))];
unsafe = [-(x1 - (1.0))*(x1-(2.0));-(x2 - (1.0))*(x2-(2.0))];
inv = [-(x1 - (-2.0))*(x1-(2.0));-(x2 - (-2.0))*(x2-(2.0))];

[prog, P1] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff2');
prog = sosineq(prog,P1);
[prog, P2] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff3');
prog = sosineq(prog,P2);
[prog, Q1] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff4');
prog = sosineq(prog,Q1);
[prog, Q2] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff5');
prog = sosineq(prog,Q2);
[prog, S1] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff6');
prog = sosineq(prog,S1);
[prog, S2] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff7');
prog = sosineq(prog,S2);
B_I = B - init(1) * P1 - init(2) * P2;
prog = sosineq(prog,B_I);
B_U = - B - unsafe(1) * Q1 - unsafe(2) * Q2;
prog = sosineq(prog,B_U);
DB = diff(B, x1) * f(1) + diff(B, x2) * f(2);
r=monomials([x1; x2],[0,1,2]);
R = 0;
for i = 1:size(r)
    R = R + randn(1) * r(i);
end
DB = DB - R * B - inv(1) * S1 - inv(2) * S2;
prog = sosineq(prog, DB);
solver_opt.solver = 'sedumi';
prog = sossolve(prog, solver_opt);
SOLB = sosgetsol(prog,B)
toc;
