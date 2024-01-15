clc;
clear;
tic;
pvar x1 x2;
vars = [x1, x2];
f = [x1; x2];

prog = sosprogram(vars);
[prog, B] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff1');

init = [0.0125-((x1-(1.125))^2+(x2-(0.625))^2)];
unsafe = [0.0125-((x1-(0.875))^2+(x2-(0.125))^2)];
inv = [-(x1 - (-2.0))*(x1-(2.0));-(x2 - (-2.0))*(x2-(2.0))];

[prog, P1] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff2');
prog = sosineq(prog,P1);
[prog, Q1] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff3');
prog = sosineq(prog,Q1);
[prog, S1] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff4');
prog = sosineq(prog,S1);
[prog, S2] = sospolyvar(prog, monomials([x1; x2],[0,1,2]), 'wscoeff5');
prog = sosineq(prog,S2);
B_I = B - init(1) * P1;
prog = sosineq(prog,B_I);
B_U = - B - unsafe(1) * Q1;
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
