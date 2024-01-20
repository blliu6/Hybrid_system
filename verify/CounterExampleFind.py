import cvxpy as cp
import numpy as np
import sympy as sp
from utils.Config import CegisConfig
from benchmarks.Examplers import Zone, Example
from scipy.optimize import minimize, NonlinearConstraint


def split_bounds(bounds, n):
    """
    Divide an n-dimensional cuboid into 2^n small cuboids, and output the upper and lower bounds of each small cuboid.

    parameter: bounds: An array of shape (n, 2), representing the upper and lower bounds of each dimension of an
    n-dimensional cuboid.

    return:
        An array with a shape of (2^n, n, 2), representing the upper and lower bounds of the divided 2^n small cuboids.
    """

    if n == bounds.shape[0]:
        return bounds.reshape((-1, *bounds.shape))
    else:
        # Take the middle position of the upper and lower bounds of the current dimension as the split point,
        # and divide the cuboid into two small cuboids on the left and right.
        if n > 5 and np.random.random() > 0.5:
            subbounds = split_bounds(bounds, n + 1)
        else:
            mid = (bounds[n, 0] + bounds[n, 1]) / 2
            left_bounds = bounds.copy()
            left_bounds[n, 1] = mid
            right_bounds = bounds.copy()
            right_bounds[n, 0] = mid
            # Recursively divide the left and right small cuboids.
            left_subbounds = split_bounds(left_bounds, n + 1)
            right_subbounds = split_bounds(right_bounds, n + 1)
            # Merge the upper and lower bounds of the left and right small cuboids into an array.
            subbounds = np.concatenate([left_subbounds, right_subbounds])

        return subbounds


class CounterExampleFinder:
    def __init__(self, config: CegisConfig):
        self.config = config
        self.ex = self.config.example
        self.n = self.ex.n
        self.nums = config.counterexample_nums

    def find_counterexample(self, state, poly_list):
        expr = self.get_expr(poly_list)

        l1, l2, I, U, g1, g2, l1_dot, l2_dot = [], [], [], [], [], [], [], []

        if not state[0]:
            vis, x = self.get_extremum_scipy(self.ex.I, expr[0])
            if vis:
                x = self.enhance(x)
                x = self.filter(x, expr[0])
                I.extend(x)

        if not state[7]:
            vis, x = self.get_extremum_scipy(self.ex.U, expr[7])
            if vis:
                x = self.enhance(x)
                x = self.filter(x, expr[7])
                U.extend(x)

        if not state[1]:
            vis, x = self.get_extremum_scipy(self.ex.l1, expr[1])
            if vis:
                x = self.enhance(x)
                x = self.filter(x, expr[1])
                l1.extend(x)
                l1_dot.extend(self.x2dotx(x, self.ex.f1))

        if not state[2]:
            vis, x = self.get_extremum_scipy(self.ex.l2, expr[2])
            if vis:
                x = self.enhance(x)
                x = self.filter(x, expr[2])
                l2.extend(x)
                l2_dot.extend(self.x2dotx(x, self.ex.f2))

        if not state[3]:
            vis, x = self.get_extremum_scipy(self.ex.g1, expr[3])
            if vis:
                x = self.enhance(x)
                x = self.filter(x, expr[3])
                g1.extend(x)

        if not state[4]:
            vis, x = self.get_extremum_scipy(self.ex.g2, expr[4])
            if vis:
                x = self.enhance(x)
                x = self.filter(x, expr[4])
                g2.extend(x)

        res = (l1, l2, I, U, g1, g2, l1_dot, l2_dot)
        return res

    def find_counterexample_for_continuous(self, state, poly_list):
        expr = self.get_expr_for_continuous(poly_list)

        l1, I, U, l1_dot = [], [], [], []

        if not state[0]:
            vis, x = self.get_extremum_scipy(self.ex.I, expr[0])
            if vis:
                print(f'Counterexample found:{x}')
                x = self.enhance(x)
                x = self.filter(x, expr[0])
                I.extend(x)

        if not state[2]:
            vis, x = self.get_extremum_scipy(self.ex.U, -expr[0])
            if vis:
                print(f'Counterexample found:{x}')
                x = self.enhance(x)
                x = self.filter(x, -expr[0])
                U.extend(x)

        if not state[1]:
            if self.config.split:
                bounds = self.split_zone(self.ex.l1)
            else:
                bounds = [self.ex.l1]
            cnt = 0
            for e in bounds:
                if self.config.lie_counterexample == 1:
                    vis, x = self.get_lie_examples(expr[0], e)
                else:
                    vis, x = self.get_extremum_scipy(e, expr[1])
                if vis:
                    cnt += 1
                    x = self.enhance(x)
                    x = self.filter(x, expr[1])
                    l1.extend(x)
                    l1_dot.extend(self.x2dotx(x, self.ex.f1))
            if cnt > 0:
                print(f'Counterexamples for Lie found')

        res = (l1, I, U, l1_dot)
        return res

    def get_lie_examples(self, expr, zone: Zone):
        x = sp.symbols([f'x{i + 1}' for i in range(self.n)])
        db = sum([sp.diff(expr, x[i]) * self.config.example.f1[i](x) for i in range(self.n)])
        opt_b = sp.lambdify(x, expr)
        opt_db = sp.lambdify(x, db)
        margin = 0.00
        con = NonlinearConstraint(lambda x: opt_b(*x), -margin, margin)

        result = None
        if zone.shape == 'box':
            bound = tuple(zip(zone.low, zone.up))
            res = minimize(lambda x: opt_db(*x), np.zeros(self.ex.n), bounds=bound, constraints=con)
            if res.fun < 0 and res.success:
                result = res.x
        elif zone.shape == 'ball':
            poly = zone.r
            for i in range(self.ex.n):
                poly = poly - (x[i] - zone.center[i]) ** 2
            poly_fun = sp.lambdify(x, poly)
            con1 = {'type': 'ineq', 'fun': lambda x: poly_fun(*x)}
            res = minimize(lambda x: opt_db(*x), np.zeros(self.ex.n), constraints=(con, con1))
            if res.fun < 0 and res.success:
                # print(f'Counterexample found:{res.x}')
                result = res.x
        if result is None:
            return False, []
        else:
            return True, result

    def split_zone(self, zone: Zone):
        bound = list(zip(zone.low, zone.up))
        bounds = split_bounds(np.array(bound), 0)
        ans = [Zone(shape='box', low=e.T[0], up=e.T[1]) for e in bounds]
        return ans

    def x2dotx(self, X, f):
        f_x = []
        for x in X:
            f_x.append([f[i](x) for i in range(self.n)])
        return f_x

    def filter(self, data, expr):
        x = sp.symbols([f'x{i + 1}' for i in range(self.n)])
        fun = sp.lambdify(x, expr, 'numpy')
        res = [e for e in data if fun(*e) < 0]
        return res

    def enhance(self, x):
        nums = self.nums
        eps = 0.05
        result = [x]
        for i in range(nums - 1):
            rd = (np.random.random(self.n) - 0.5) * eps
            rd = rd + x
            result.append(rd)
        return result

    def get_expr(self, poly_list):
        b1, b2, bm1, bm2, rm1, rm2 = poly_list
        ans = [b1]
        x = sp.symbols([f'x{i + 1}' for i in range(self.n)])
        expr = sum([sp.diff(b1, x[i]) * self.ex.f1[i](x) for i in range(self.n)])
        expr = expr - bm1 * b1
        ans.append(expr)

        expr = sum([sp.diff(b2, x[i]) * self.ex.f2[i](x) for i in range(self.n)])
        expr = expr - bm2 * b2
        ans.append(expr)

        b2_fun = sp.lambdify(x, b2)
        x_ = [self.ex.r1[i](x) for i in range(self.n)]
        bl2 = b2_fun(*x_)
        expr = bl2 - rm1 * b1
        ans.append(expr)

        b1_fun = sp.lambdify(x, b1)
        x_ = [self.ex.r2[i](x) for i in range(self.n)]
        bl1 = b1_fun(*x_)
        expr = bl1 - rm2 * b2
        ans.append(expr)

        ans.append(rm1)
        ans.append(rm2)
        ans.append(-b2)
        return ans

    def get_expr_for_continuous(self, poly_list):
        b1, bm1 = poly_list
        ans = [b1]
        x = sp.symbols([f'x{i + 1}' for i in range(self.n)])
        expr = sum([sp.diff(b1, x[i]) * self.ex.f1[i](x) for i in range(self.n)])
        expr = expr - bm1 * b1
        ans.append(expr)

        return ans

    def get_extremum_scipy(self, zone: Zone, expr):
        x_ = sp.symbols([f'x{i + 1}' for i in range(self.ex.n)])
        opt = sp.lambdify(x_, expr)
        result = None
        if zone.shape == 'box':
            bound = tuple(zip(zone.low, zone.up))
            res = minimize(lambda x: opt(*x), np.zeros(self.ex.n), bounds=bound)
            if res.fun < 0 and res.success:
                # print(f'Counterexample found:{res.x}')
                result = res.x
        elif zone.shape == 'ball':
            poly = zone.r
            for i in range(self.ex.n):
                poly = poly - (x_[i] - zone.center[i]) ** 2
            poly_fun = sp.lambdify(x_, poly)
            con = {'type': 'ineq', 'fun': lambda x: poly_fun(*x)}
            res = minimize(lambda x: opt(*x), np.zeros(self.ex.n), constraints=con)
            if res.fun < 0 and res.success:
                # print(f'Counterexample found:{res.x}')
                result = res.x
        if result is None:
            return False, []
        else:
            return True, result

    def get_extremum_cvxpy(self, zone: Zone, expr):
        x_ = sp.symbols([f'x{i + 1}' for i in range(self.ex.n)])
        opt = sp.lambdify(x_, expr)

        x = [cp.Variable(name=f'x{i + 1}') for i in range(self.ex.n)]
        con = []

        if zone.shape == 'box':
            for i in range(self.ex.n):
                con.append(x[i] >= zone.low[i])
                con.append(x[i] <= zone.up[i])
        elif zone.shape == 'ball':
            poly = zone.r
            for i in range(self.ex.n):
                poly = poly - (x[i] - zone.center[i]) ** 2
            con.append(poly >= 0)

        obj = cp.Minimize(opt(*x))
        prob = cp.Problem(obj, con)
        prob.solve(solver=cp.GUROBI)
        if prob.value < 0 and prob.status == 'optimal':
            ans = [e.value for e in x]
            print(f'Counterexample found:{ans}')
            return True, np.array(ans)
        else:
            return False, []


if __name__ == '__main__':
    from benchmarks.Examplers import get_example_by_name

    ex = get_example_by_name('H3')
    par = {'example': ex}
    config = CegisConfig(**par)
    count = CounterExampleFinder(config)
    zone = Zone(shape='ball', center=[0, 0], r=1)
    # count.get_extremum_scipy(zone, 'x1 + x2')
    count.find_counterexample([False] * 8, [])
