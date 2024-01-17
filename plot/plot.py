import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle
from utils.Config import CegisConfig
from benchmarks.Examplers import Zone, Example
import mpl_toolkits.mplot3d.art3d as art3d


class Draw:
    def __init__(self, example: Example, b1, b2=None):
        self.ex = example
        self.b1 = b1
        self.b2 = b2

    def draw(self):
        fig = plt.figure()
        ax = plt.gca()

        ax.add_patch(self.draw_zone(self.ex.l1, 'b', 'local_1'))
        ax.add_patch(self.draw_zone(self.ex.l2, 'purple', 'local_2'))
        ax.add_patch(self.draw_zone(self.ex.I, 'g', 'init'))
        ax.add_patch(self.draw_zone(self.ex.U, 'r', 'unsafe'))
        ax.add_patch(self.draw_zone(self.ex.g1, 'bisque', 'guard_1'))
        ax.add_patch(self.draw_zone(self.ex.g2, 'orange', 'guard_2'))

        l1, l2 = self.ex.l1, self.ex.l2

        self.plot_vector_field(l1, self.ex.f1)
        self.plot_vector_field(l2, self.ex.f2)

        self.plot_barrier(l1, self.b1, 'lime')
        self.plot_barrier(l2, self.b2, 'aqua')

        plt.xlim(min(l1.low[0], l2.low[0]) - 1, max(l1.up[0], l2.up[0]) + 1)
        plt.ylim(min(l1.low[1], l2.low[1]) - 1, max(l1.up[1], l2.up[1]) + 1)
        ax.set_aspect(1)
        plt.legend()
        plt.show()

    def draw_continuous(self):
        fig = plt.figure()
        ax = plt.gca()

        ax.add_patch(self.draw_zone(self.ex.l1, 'b', 'local_1'))
        ax.add_patch(self.draw_zone(self.ex.I, 'g', 'init'))
        ax.add_patch(self.draw_zone(self.ex.U, 'r', 'unsafe'))

        l1 = self.ex.l1

        self.plot_vector_field(l1, self.ex.f1)

        self.plot_barrier(l1, self.b1, 'lime')

        plt.xlim(l1.low[0] - 1, l1.up[0] + 1)
        plt.ylim(l1.low[1] - 1, l1.up[1] + 1)
        ax.set_aspect(1)
        plt.legend()
        plt.show()

    def draw_3d(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        self.plot_barrier_3d(ax, self.ex.l1, self.b1, 'gold')
        self.plot_barrier_3d(ax, self.ex.l2, self.b2, 'plum')

        init = self.draw_zone(self.ex.I, color='g', label='init')
        ax.add_patch(init)
        art3d.pathpatch_2d_to_3d(init, z=0, zdir="z")

        unsafe = self.draw_zone(self.ex.U, color='r', label='unsafe')
        ax.add_patch(unsafe)
        art3d.pathpatch_2d_to_3d(unsafe, z=0, zdir="z")
        plt.show()

    def draw_3d_continuous(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        self.plot_barrier_3d(ax, self.ex.l1, self.b1, 'gold')

        init = self.draw_zone(self.ex.I, color='g', label='init')
        ax.add_patch(init)
        art3d.pathpatch_2d_to_3d(init, z=0, zdir="z")

        unsafe = self.draw_zone(self.ex.U, color='r', label='unsafe')
        ax.add_patch(unsafe)
        art3d.pathpatch_2d_to_3d(unsafe, z=0, zdir="z")
        plt.show()

    def plot_barrier_3d(self, ax, zone, b, color):
        low, up = zone.low, zone.up
        x = np.linspace(low[0], up[0], 100)
        y = np.linspace(low[1], up[1], 100)
        X, Y = np.meshgrid(x, y)
        s_x = sp.symbols(['x1', 'x2'])
        lambda_b = sp.lambdify(s_x, b, 'numpy')
        plot_b = lambda_b(X, Y)
        # ax.plot_surface(X, Y, plot_b, rstride=5, cstride=5, alpha=0.5, cmap=cm.jet)
        ax.plot_surface(X, Y, plot_b, rstride=5, cstride=5, alpha=0.5, color=color)

    def plot_barrier(self, zone, hx, color):
        low, up = zone.low, zone.up
        x = np.linspace(low[0], up[0], 100)
        y = np.linspace(low[1], up[1], 100)

        X, Y = np.meshgrid(x, y)

        s_x = sp.symbols(['x1', 'x2'])
        fun_hx = sp.lambdify(s_x, hx, 'numpy')
        value = fun_hx(X, Y)
        plt.contour(X, Y, value, 0, alpha=0.8, colors=color)

    def plot_vector_field(self, zone: Zone, f):
        low, up = zone.low, zone.up
        xv = np.linspace(low[0], up[0], 10)
        yv = np.linspace(low[1], up[1], 10)
        Xd, Yd = np.meshgrid(xv, yv)

        DX, DY = f[0]([Xd, Yd]), f[1]([Xd, Yd])
        DX = DX / np.linalg.norm(DX, ord=2, axis=1, keepdims=True)
        DY = DY / np.linalg.norm(DY, ord=2, axis=1, keepdims=True)

        plt.streamplot(Xd, Yd, DX, DY, linewidth=0.3,
                       density=0.5, arrowstyle='-|>', arrowsize=1.5, color='grey')

    def draw_zone(self, zone: Zone, color, label, fill=False):
        if zone.shape == 'ball':
            circle = Circle(zone.center, np.sqrt(zone.r), color=color, label=label, fill=fill, linewidth=1.5)
            return circle
        else:
            w = zone.up[0] - zone.low[0]
            h = zone.up[1] - zone.low[1]
            box = Rectangle(zone.low, w, h, color=color, label=label, fill=fill, linewidth=1.5)
            return box


if __name__ == '__main__':
    from benchmarks.Examplers import get_example_by_name

    ex = get_example_by_name('H3')
    b1 = '0.0400758160260908*x1**2 - 2.40897372979335*x1*x2 - 1.24390362040234*x1 - 1.43151614875389*x2**2 + 0.259768727895773*x2 + 0.831009430574983'
    b2 = '0.13928392864101*x1**2 + 1.01008702869913*x1*x2 - 1.33612375376827*x1 - 1.19809153148389*x2**2 - 1.9334641802199*x2 + 3.94266860834908'

    d = Draw(ex, b1, b2)
    d.draw_3d()
    d.draw()
