import sympy as sp
from benchmarks.Examplers import get_example_by_name, Example, Zone

name = 'C24'
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


with open(f'./{ex.name}.m', 'w') as f:
    x = [f'x{i + 1}' for i in range(ex.n)]
    expr = ' '.join(x)
    f.write(f'clc;\nclear;\ntic;\nsdpvar {expr};\n\n')

    f.write(f'init = [{write_zone(ex.I)}];\n')
    f.write(f'unsafe = [{write_zone(ex.U)}];\n')
    f.write(f'inv = [{write_zone(ex.l1)}];\n\n')

    x_ = sp.symbols(x)
    ff = '; '.join([str(e(x_)).replace('**', '^') for e in ex.f1])
    f.write(f'f = [{ff}];\n\n')

    expr = ', '.join(x)
    f.write(f'[B, b, v] = polynomial([{expr}], 2);\n')
    f.write('par = [b];\n\n')

    for i in range(get_number(ex.I)):
        f.write(f'[P{i + 1}, p{i + 1}, pv{i + 1}] = polynomial([{expr}], 2);\n')
    v = [f'P{i + 1} * init({i + 1})' for i in range(get_number(ex.I))]
    I = ' - '.join(v)
    f.write(f'B_I = B - {I};\n')
    v = [f'sos(P{i + 1})' for i in range(get_number(ex.I))]
    I = ', '.join(v)
    f.write(f'con = [sos(B_I), {I}];\n')
    v = [f'p{i + 1}' for i in range(get_number(ex.I))]
    I = '; '.join(v)
    f.write(f'par = [par; {I}];\n\n')

    for i in range(get_number(ex.U)):
        f.write(f'[Q{i + 1}, q{i + 1}, qv{i + 1}] = polynomial([{expr}], 2);\n')
    v = [f'Q{i + 1} * unsafe({i + 1})' for i in range(get_number(ex.U))]
    I = ' - '.join(v)
    f.write(f'B_U = -B - {I};\n')
    v = [f'sos(Q{i + 1})' for i in range(get_number(ex.U))]
    I = ', '.join(v)
    f.write(f'con = [con, sos(B_U), {I}];\n')
    v = [f'q{i + 1}' for i in range(get_number(ex.U))]
    I = '; '.join(v)
    f.write(f'par = [par; {I}];\n\n')

    v = [f'jacobian(B, x{i + 1}) * f({i + 1})' for i in range(ex.n)]
    I = ' + '.join(v)
    f.write(f'DB = {I};\n')

    for i in range(get_number(ex.l1)):
        f.write(f'[S{i + 1}, s{i + 1}, sv{i + 1}] = polynomial([{expr}], 2);\n')
    v = [f'S{i + 1} * inv({i + 1})' for i in range(get_number(ex.l1))]
    I = ' - '.join(v)

    f.write(f'[R, r, rv] = polynomial([{expr}], 2);\n')
    f.write(f'DB = DB - R * B - {I};\n')

    v = [f'sos(S{i + 1})' for i in range(get_number(ex.l1))]
    I = ', '.join(v)
    f.write(f'con = [con, sos(DB), {I}];\n')
    v = [f's{i + 1}' for i in range(get_number(ex.l1))]
    I = '; '.join(v)
    f.write(f'par = [par; r; {I}];\n\n')

    f.write('ops = sdpsettings(\'solver\', \'penbmi\');\n')
    f.write('sol = solvesos(con,[],ops,par);\n')
    f.write('if sol.problem == 0\n')
    f.write('    fprintf(\'Solved successfully!\');\n')
    f.write('    sdisplay(v\')\n')
    f.write('    value(b\')\n')
    f.write('    sdisplay((double(b))\'*v)\n')
    f.write('elseif sol.problem == 1\n')
    f.write('    disp(\'Solver thinks it is infeasible\');\n')
    f.write('else\n')
    f.write('    disp(\'Something else happened\');\n')
    f.write('end\ntoc;')
