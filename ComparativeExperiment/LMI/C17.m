clc;
clear;
tic;
pvar x1 x2 x3 x4 x5 x6 x7 x8 x9;
vars = [x1, x2, x3, x4, x5, x6, x7, x8, x9];
f = [-x1*x6 + 3*x3; -x2*x6 + x4; x1*x6 - 3*x3; x2*x6 - x4; 5*x1 + 3*x3 - x5; 3*x3 + x4 + 5*x5 - x6*(x1 + x2 + 2*x8 + 1); x2 + 5*x4 - 0.5*x7; -2*x6*x8 + 5*x7 - 0.2*x8 + x9; 2*x6*x8 - x9];

prog = sosprogram(vars);
[prog, B] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff1');

init = [0.010000000000000002-((x1-(1.0))^2+(x2-(1.0))^2+(x3-(1.0))^2+(x4-(1.0))^2+(x5-(1.0))^2+(x6-(1.0))^2+(x7-(1.0))^2+(x8-(1.0))^2+(x9-(1.0))^2)];
unsafe = [0.010000000000000002-((x1-(1.899999976158142))^2+(x2-(1.899999976158142))^2+(x3-(1.899999976158142))^2+(x4-(1.899999976158142))^2+(x5-(1.899999976158142))^2+(x6-(1.899999976158142))^2+(x7-(1.899999976158142))^2+(x8-(1.899999976158142))^2+(x9-(1.899999976158142))^2)];
inv = [-(x1 - (-2.0))*(x1-(2.0));-(x2 - (-2.0))*(x2-(2.0));-(x3 - (-2.0))*(x3-(2.0));-(x4 - (-2.0))*(x4-(2.0));-(x5 - (-2.0))*(x5-(2.0));-(x6 - (-2.0))*(x6-(2.0));-(x7 - (-2.0))*(x7-(2.0));-(x8 - (-2.0))*(x8-(2.0));-(x9 - (-2.0))*(x9-(2.0))];

[prog, P1] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff2');
prog = sosineq(prog,P1);
[prog, Q1] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff3');
prog = sosineq(prog,Q1);
[prog, S1] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff4');
prog = sosineq(prog,S1);
[prog, S2] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff5');
prog = sosineq(prog,S2);
[prog, S3] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff6');
prog = sosineq(prog,S3);
[prog, S4] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff7');
prog = sosineq(prog,S4);
[prog, S5] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff8');
prog = sosineq(prog,S5);
[prog, S6] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff9');
prog = sosineq(prog,S6);
[prog, S7] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff10');
prog = sosineq(prog,S7);
[prog, S8] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff11');
prog = sosineq(prog,S8);
[prog, S9] = sospolyvar(prog, monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]), 'wscoeff12');
prog = sosineq(prog,S9);
B_I = B - init(1) * P1;
prog = sosineq(prog,B_I);
B_U = - B - unsafe(1) * Q1;
prog = sosineq(prog,B_U);
DB = diff(B, x1) * f(1) + diff(B, x2) * f(2) + diff(B, x3) * f(3) + diff(B, x4) * f(4) + diff(B, x5) * f(5) + diff(B, x6) * f(6) + diff(B, x7) * f(7) + diff(B, x8) * f(8) + diff(B, x9) * f(9);
r=monomials([x1; x2; x3; x4; x5; x6; x7; x8; x9],[0,1,2]);
R = 0;
for i = 1:size(r)
    R = R + randn(1) * r(i);
end
DB = DB - R * B - inv(1) * S1 - inv(2) * S2 - inv(3) * S3 - inv(4) * S4 - inv(5) * S5 - inv(6) * S6 - inv(7) * S7 - inv(8) * S8 - inv(9) * S9;
prog = sosineq(prog, DB);
solver_opt.solver = 'sedumi';
prog = sossolve(prog, solver_opt);
SOLB = sosgetsol(prog,B)
toc;
