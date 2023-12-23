import numpy as np


class Zone:
    def __init__(self, shape: str, low=None, up=None, center=None, r=None, verify_zone=None):
        self.shape = shape
        self.verify_zone = verify_zone
        if shape == 'ball':
            self.center = np.array(center)
            self.r = r  # 半径的平方
        elif shape == 'box':
            self.low = np.array(low)
            self.up = np.array(up)
        else:
            raise ValueError(f'没有形状为{shape}的区域!')


class Example:
    def __init__(self, n, local_1, local_2, init, unsafe, guard_1, guard_2, reset_1, reset_2, f_1, f_2, name):
        self.n = n  # number of variables
        self.l1 = local_1
        self.l2 = local_2
        self.I = init
        self.U = unsafe
        self.g1 = guard_1
        self.g2 = guard_2
        self.r1 = reset_1
        self.r2 = reset_2
        self.f1 = f_1
        self.f2 = f_2
        self.name = name  # name or identifier


examples = {
    0: Example(
        n=2,
        local_1=Zone(shape='box', low=[-5, -5], up=[0, 5]),
        local_2=Zone(shape='box', low=[0, -5], up=[5, 5]),
        init=Zone(shape='ball', center=[-2, 2], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[2, 2], r=0.5 ** 2),
        guard_1=Zone(shape='ball', center=[0, 0], r=0.75 ** 2),
        guard_2=Zone(shape='ball', center=[0, 0], r=0.5 ** 2),
        reset_1=[lambda x: -x[0], lambda x: x[1]],
        reset_2=[lambda x: x[0] - 2, lambda x: x[1] + 1],
        f_1=[lambda x: -x[0] + x[0] * x[1],
             lambda x: -x[1]],
        f_2=[lambda x: -x[0] + 2 * x[0] ** 2 * x[1],
             lambda x: -x[1]],
        name='H3_easy'
    ),
    1: Example(
        n=2,
        local_1=Zone(shape='box', low=[-5, -5], up=[0, 5], verify_zone=[lambda x: -x[0]]),
        local_2=Zone(shape='box', low=[0, -5], up=[5, 5], verify_zone=[lambda x: x[0]]),
        init=Zone(shape='ball', center=[-2, 2], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[2, 2], r=0.5 ** 2),
        guard_1=Zone(shape='ball', center=[0, 0], r=0.75 ** 2),
        guard_2=Zone(shape='ball', center=[0, 0], r=0.5 ** 2),
        reset_1=[lambda x: -x[0], lambda x: x[1]],
        reset_2=[lambda x: x[0] - 2, lambda x: x[1] + 1],
        f_1=[lambda x: -x[0] + x[0] * x[1],
             lambda x: -x[1]],
        f_2=[lambda x: -x[0] + 2 * x[0] ** 2 * x[1],
             lambda x: -x[1]],
        name='H3'  # Safety Verification of Nonlinear Hybrid Systems Based on Bilinear Programming->H3
    ),
    2: Example(
        n=3,
        local_1=Zone(shape='box', low=[-1.1, -11, -11], up=[1.1, 11, 11]),
        local_2=Zone(shape='box', low=[0.17, 0.17, 0.17], up=[12, 12, 12]),
        init=Zone(shape='ball', center=[0, 0, 0], r=0.01),
        unsafe=Zone(shape='box', low=[5, -100, -100], up=[5.1, 100, 100],
                    verify_zone=[lambda x: (x[0] - 5) * (5.1 - x[0])]),
        guard_1=Zone(shape='box', low=[0.99, 9.95, 9.95], up=[1.01, 10.05, 10.05]),
        guard_2=Zone(shape='box', low=[0.17] * 3, up=[0.23] * 3),
        reset_1=[lambda x: x[0], lambda x: x[1], lambda x: x[2]],
        reset_2=[lambda x: x[0], lambda x: x[1], lambda x: x[2]],
        f_1=[lambda x: -x[1], lambda x: -x[0] + x[2], lambda x: x[0] + (2 * x[1] + 3 * x[2]) * (1 + x[2] ** 2)],
        f_2=[lambda x: -x[1], lambda x: -x[0] + x[2], lambda x: -x[0] - 2 * x[1] - 3 * x[2]],
        name='H2'  # Safety Verification of Nonlinear Hybrid Systems Based on Bilinear Programming->H2
    ),
    3: Example(
        n=3,
        local_1=Zone(shape='box', low=[-1.1, -11, -11], up=[1.1, 11, 11]),
        local_2=Zone(shape='box', low=[0.17, 0.17, 0.17], up=[12, 12, 12]),
        init=Zone(shape='ball', center=[0, 0, 0], r=0.01),
        unsafe=Zone(shape='box', low=[5, -11, -11], up=[5.1, 11, 11]),
        guard_1=Zone(shape='box', low=[0.99, 9.95, 9.95], up=[1.01, 10.05, 10.05]),
        guard_2=Zone(shape='box', low=[0.17] * 3, up=[0.23] * 3),
        reset_1=[lambda x: x[0], lambda x: x[1], lambda x: x[2]],
        reset_2=[lambda x: x[0], lambda x: x[1], lambda x: x[2]],
        f_1=[lambda x: -x[1], lambda x: -x[0] + x[2], lambda x: x[0] + (2 * x[1] + 3 * x[2]) * (1 + x[2] ** 2)],
        f_2=[lambda x: -x[1], lambda x: -x[0] + x[2], lambda x: -x[0] - 2 * x[1] - 3 * x[2]],
        name='H2_easy'
    ),
    4: Example(
        n=2,
        local_1=Zone(shape='box', low=[-10, -10], up=[0, 10]),
        local_2=Zone(shape='box', low=[0, -10], up=[10, 10]),
        init=Zone(shape='box', low=[-2, -2], up=[-1, -1]),
        unsafe=Zone(shape='box', low=[0, -2], up=[1, -1]),
        guard_1=Zone(shape='ball', center=[-0.5, -0.5], r=0.5 ** 2),
        guard_2=Zone(shape='ball', center=[1, 1], r=0.5 ** 2),
        reset_1=[lambda x: -x[0] + 2, lambda x: -x[1] + 2],
        reset_2=[lambda x: x[0] - 2, lambda x: x[1] - 2],
        f_1=[lambda x: x[0] - x[0] * x[1],
             lambda x: -x[1] + x[0] * x[1]],
        f_2=[lambda x: x[0] + x[0] ** 2 * x[1],
             lambda x: x[1] + x[0] * x[1]],
        name='H4'  # Darboux-type_barrier_certificates_for_safety_verification_of_nonlinear_hybrid_systems->EXAMPLE2
    ),
    5: Example(
        n=2,
        local_1=Zone(shape='box', low=[-5, -5], up=[0, 5]),
        local_2=Zone(shape='box', low=[0, -5], up=[5, 5]),
        init=Zone(shape='box', low=[-2, -2], up=[-1, -1]),
        unsafe=Zone(shape='box', low=[0, -2], up=[1, -1]),
        guard_1=Zone(shape='ball', center=[-0.5, -0.5], r=0.5 ** 2),
        guard_2=Zone(shape='ball', center=[1, 1], r=0.5 ** 2),
        reset_1=[lambda x: -x[0] + 2, lambda x: -x[1] + 2],
        reset_2=[lambda x: x[0] - 2, lambda x: x[1] - 2],
        f_1=[lambda x: x[0] - x[0] * x[1],
             lambda x: -x[1] + x[0] * x[1]],
        f_2=[lambda x: x[0] + x[0] ** 2 * x[1],
             lambda x: x[1] + x[0] * x[1]],
        name='H4_easy'
        # Darboux-type_barrier_certificates_for_safety_verification_of_nonlinear_hybrid_systems->EXAMPLE2
    ),
    6: Example(
        n=2,
        local_1=Zone(shape='box', low=[0, 0], up=[40, 60], verify_zone=[lambda x: (x[0] - 5) * (35 - x[0])]),
        local_2=Zone(shape='box', low=[0, 0], up=[40, 60], verify_zone=[lambda x: (x[0] - 5) * (35 - x[0])]),
        init=Zone(shape='ball', center=[9, 20], r=2 ** 2),
        unsafe=Zone(shape='box', low=[0, 48], up=[40, 60], verify_zone=[lambda x: (x[1] - 48) * (60 - x[1])]),
        guard_1=Zone(shape='box', low=[34.9, 0], up=[35.1, 60]),
        guard_2=Zone(shape='box', low=[4.9, 0], up=[5.1, 60]),
        reset_1=[lambda x: x[0], lambda x: x[1]],
        reset_2=[lambda x: x[0], lambda x: x[1]],
        f_1=[lambda x: x[1] ** 2 - 10 * x[1] + 25,
             lambda x: 2 * x[0] * x[1] + 10 * x[0] - 40 * x[1] - 200],
        f_2=[lambda x: -x[1] ** 2 - 10 * x[1] - 25,
             lambda x: 8 * x[0] * x[1] + 40 * x[0] - 160 * x[1] - 800],
        name='H1'
        # Safety Verification of Nonlinear Hybrid Systems Based on Invariant Clusters
    ),
    7: Example(
        n=2,
        local_1=Zone(shape='box', low=[0, 0], up=[40, 60]),
        local_2=Zone(shape='box', low=[0, 0], up=[40, 60]),
        init=Zone(shape='ball', center=[9, 20], r=2 ** 2),
        unsafe=Zone(shape='box', low=[0, 48], up=[40, 60], verify_zone=[lambda x: (x[1] - 48) * (60 - x[1])]),
        guard_1=Zone(shape='box', low=[34.9, 0], up=[35.1, 48]),
        guard_2=Zone(shape='box', low=[4.9, 0], up=[5.1, 48]),
        reset_1=[lambda x: x[0], lambda x: x[1]],
        reset_2=[lambda x: x[0], lambda x: x[1]],
        f_1=[lambda x: x[1] ** 2 - 10 * x[1] + 25,
             lambda x: 2 * x[0] * x[1] + 10 * x[0] - 40 * x[1] - 200],
        f_2=[lambda x: -x[1] ** 2 - 10 * x[1] - 25,
             lambda x: 8 * x[0] * x[1] + 40 * x[0] - 160 * x[1] - 800],
        name='H1_easy'
        # Safety Verification of Nonlinear Hybrid Systems Based on Invariant Clusters
    ),
}


def get_example_by_id(id: int):
    return examples[id]


def get_example_by_name(name: str):
    for ex in examples.values():
        if ex.name == name:
            return ex
    raise ValueError('The example {} was not found.'.format(name))
