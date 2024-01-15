clc;
clear;
tic;
pvar x1 x2 x3;
vars = [x1, x2, x3];
f = [-10.0*x1 + 10.0*x2; x1*(28.0 - x3) - x2; x1*x2 - 2.66666666666667*x3];

prog = sosprogram(vars);
[prog, B] = sospolyvar(prog, monomials([x1; x2; x3],[0,1,2]), 'wscoeff1');

init = [0.25-((x1-(-14.5))^2+(x2-(-14.5))^2+(x3-(12.5))^2)];
unsafe = [0.25-((x1-(-16.5))^2+(x2-(-14.5))^2+(x3-(2.5))^2)];
inv = [-(x1 - (-20.0))*(x1-(20.0));-(x2 - (-20.0))*(x2-(20.0));-(x3 - (-20.0))*(x3-(20.0))];

[prog, P1] = sospolyvar(prog, monomials([x1; x2; x3],[0,1,2]), 'wscoeff2');
prog = sosineq(prog,P1);
[prog, Q1] = sospolyvar(prog, monomials([x1; x2; x3],[0,1,2]), 'wscoeff3');
prog = sosineq(prog,Q1);
[prog, S1] = sospolyvar(prog, monomials([x1; x2; x3],[0,1,2]), 'wscoeff4');
prog = sosineq(prog,S1);
[prog, S2] = sospolyvar(prog, monomials([x1; x2; x3],[0,1,2]), 'wscoeff5');
prog = sosineq(prog,S2);
[prog, S3] = sospolyvar(prog, monomials([x1; x2; x3],[0,1,2]), 'wscoeff6');
prog = sosineq(prog,S3);
B_I = B - init(1) * P1;
prog = sosineq(prog,B_I);
B_U = - B - unsafe(1) * Q1;
prog = sosineq(prog,B_U);
DB = diff(B, x1) * f(1) + diff(B, x2) * f(2) + diff(B, x3) * f(3);
r=monomials([x1; x2; x3],[0,1,2]);
R = 0;
for i = 1:size(r)
    R = R + randn(1) * r(i);
end
DB = DB - R * B - inv(1) * S1 - inv(2) * S2 - inv(3) * S3;
prog = sosineq(prog, DB);
solver_opt.solver = 'sedumi';
prog = sossolve(prog, solver_opt);
SOLB = sosgetsol(prog,B)
toc;
