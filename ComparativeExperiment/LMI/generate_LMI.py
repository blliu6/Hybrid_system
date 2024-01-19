import sympy as sp
from benchmarks.Examplers import get_example_by_name, Example, Zone

name = 'R12'
ex = get_example_by_name(name)


def write_zone(zone: Zone):
    global s
    if zone.shape == 'box':
        s = ''
        for i, (l, u) in enumerate(zip(zone.low, zone.up)):
            s += f'-(x{i + 1} - ({l}))*(x{i + 1}-({u}));'
        s = s[:-1]
    elif zone.shape == 'ball':
        s = f'{zone.r}-('
        for i in range(len(zone.center)):
            s += f'(x{i + 1}-({zone.center[i]}))^2+'
        s = s[:-1]
        s += ')'
    return s


def get_number(zone: Zone):
    if zone.shape == 'box':
        return len(zone.low)
    elif zone.shape == 'ball':
        return 1


cnt = 1
with open(f'./{ex.name}.m', 'w') as f:
    x = [f'x{i + 1}' for i in range(ex.n)]
    expr = ' '.join(x)
    f.write(f'clc;\nclear;\ntic;\npvar {expr};\n')
    expr = ', '.join(x)
    f.write(f'vars = [{expr}];\n')
    x_ = sp.symbols(x)
    ff = '; '.join([str(e(x_)).replace('**', '^') for e in ex.f1])
    f.write(f'f = [{ff}];\n\n')

    f.write('prog = sosprogram(vars);\n')

    expr = '; '.join(x)
    f.write(f'[prog, B] = sospolyvar(prog, monomials([{expr}],[0,1,2]), \'wscoeff{cnt}\');\n\n')
    cnt += 1

    f.write(f'init = [{write_zone(ex.I)}];\n')
    f.write(f'unsafe = [{write_zone(ex.U)}];\n')
    f.write(f'inv = [{write_zone(ex.l1)}];\n\n')

    for i in range(get_number(ex.I)):
        f.write(f'[prog, P{i + 1}] = sospolyvar(prog, monomials([{expr}],[0,1,2]), \'wscoeff{cnt}\');\n')
        cnt += 1
        f.write(f'prog = sosineq(prog,P{i + 1});\n')

    for i in range(get_number(ex.U)):
        f.write(f'[prog, Q{i + 1}] = sospolyvar(prog, monomials([{expr}],[0,1,2]), \'wscoeff{cnt}\');\n')
        cnt += 1
        f.write(f'prog = sosineq(prog,Q{i + 1});\n')

    for i in range(get_number(ex.l1)):
        f.write(f'[prog, S{i + 1}] = sospolyvar(prog, monomials([{expr}],[0,1,2]), \'wscoeff{cnt}\');\n')
        cnt += 1
        f.write(f'prog = sosineq(prog,S{i + 1});\n')

    v = [f'init({i + 1}) * P{i + 1}' for i in range(get_number(ex.I))]
    I = ' - '.join(v)
    f.write(f'B_I = B - {I};\n')
    f.write('prog = sosineq(prog,B_I);\n')

    v = [f'unsafe({i + 1}) * Q{i + 1}' for i in range(get_number(ex.U))]
    U = ' - '.join(v)
    f.write(f'B_U = - B - {U};\n')
    f.write('prog = sosineq(prog,B_U);\n')

    v = [f'diff(B, x{i + 1}) * f({i + 1})' for i in range(ex.n)]
    D = ' + '.join(v)
    f.write(f'DB = {D};\n')

    f.write(f'r=monomials([{expr}],[0,1,2]);\nR = 0;\n')
    f.write('for i = 1:size(r)\n')
    f.write('    R = R + randn(1) * r(i);\nend\n')

    v = [f'inv({i + 1}) * S{i + 1}' for i in range(get_number(ex.l1))]
    U = ' - '.join(v)
    f.write(f'DB = DB - R * B - {U};\n')
    f.write('prog = sosineq(prog, DB);\n')
    f.write('solver_opt.solver = \'sedumi\';\n')
    f.write('prog = sossolve(prog, solver_opt);\n')
    f.write('SOLB = sosgetsol(prog,B)\n')
    f.write('toc;\n')
