import numpy as np


class Zone:
    def __init__(self, shape: str, low=None, up=None, center=None, r=None, verify_zone=None):
        self.shape = shape
        self.verify_zone = verify_zone
        if shape == 'ball':
            self.center = np.array(center, dtype=np.float32)
            self.r = r  # 半径的平方
        elif shape == 'box':
            self.low = np.array(low, dtype=np.float32)
            self.up = np.array(up, dtype=np.float32)
        else:
            raise ValueError(f'没有形状为{shape}的区域!')


class Example:
    def __init__(self, n, local_1, init, unsafe, f_1, name, local_2=None, guard_1=None, guard_2=None, reset_1=None,
                 reset_2=None, f_2=None, continuous=False):
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
        self.continuous = continuous


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
        local_1=Zone(shape='box', low=[-10, -10], up=[0, 10], verify_zone=[lambda x: -x[0]]),
        local_2=Zone(shape='box', low=[0, -10], up=[10, 10], verify_zone=[lambda x: x[0]]),
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
    10: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2, -2], up=[2, 2]),
        init=Zone(shape='box', low=[0, 1], up=[1, 2]),
        unsafe=Zone(shape='box', low=[-2, -0.75], up=[-0.5, 0.75]),
        f_1=[
            lambda x: x[1] + 2 * x[0] * x[1],
            lambda x: -x[0] - x[1] ** 2 + 2 * x[0] ** 2
        ],
        name='F1',
        continuous=True
    ),
    11: Example(
        n=2,
        local_1=Zone(shape='box', low=[1, 1], up=[5, 5]),
        init=Zone(shape='box', low=[4, 0.9], up=[4.5, 1.1]),
        unsafe=Zone(shape='box', low=[1, 2], up=[2, 3]),
        f_1=[lambda x: -5.5 * x[1] + x[1] * x[1],
             lambda x: 6 * x[0] - x[0] * x[0],
             ],
        name='C1',
        continuous=True
    ),
    12: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2, -2], up=[2, 2]),
        init=Zone(shape='box', low=[-0.2, 0.3], up=[0.2, 0.7]),
        unsafe=Zone(shape='box', low=[-2, -2], up=[-1, -1]),
        f_1=[lambda x: -x[0] + 2 * x[0] * x[0] * x[0] * x[1] * x[1],
             lambda x: -x[1]
             ],
        name='C2',
        continuous=True
    ),
    13: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2, -2], up=[2, 2]),
        init=Zone(shape='box', low=[-1, -1], up=[0, 0]),
        unsafe=Zone(shape='box', low=[1, 1], up=[2, 2]),
        f_1=[lambda x: -1 + x[0] * x[0] + x[1] * x[1],
             lambda x: 5 * (-1 + x[0] * x[1])
             ],
        name='C3',
        continuous=True
    ),
    14: Example(
        n=2,
        local_1=Zone(shape='box', low=[-3, -3], up=[3, 3]),
        init=Zone(shape='box', low=[-0.2, -0.2], up=[0.2, 0.2]),
        unsafe=Zone(shape='box', low=[2, 2], up=[3, 3]),
        f_1=[
            lambda x: x[0] - x[0] * x[0] * x[0] + x[1] - x[0] * x[1] * x[1],
            lambda x: -x[0] + x[1] - x[0] * x[0] * x[1] - x[1] * x[1] * x[1]
        ],
        name='C4',
        continuous=True
    ),
    15: Example(
        n=2,
        local_1=Zone(shape='box', low=[-3.5, -2], up=[2, 1]),
        init=Zone(shape='box', low=[1, -0.5], up=[2, 0.5]),
        unsafe=Zone(shape='box', low=[-1.4, -1.4], up=[-0.6, -0.6]),
        f_1=[
            lambda x: x[1],
            lambda x: -x[0] - x[1] + 1 / 3.0 * x[0] ** 3
        ],
        name='F2',
        continuous=True
    ),
    16: Example(
        n=4,
        local_1=Zone(shape='box', low=[-2.5] * 4, up=[2] * 4),
        init=Zone(shape='box', low=[0.5] * 4, up=[1.5] * 4),
        unsafe=Zone(shape='box', low=[-2.4] * 4, up=[-1.6] * 4),
        f_1=[
            lambda x: x[0],
            lambda x: x[1],
            lambda x: x[2],
            lambda x: - 3980 * x[3] - 4180 * x[2] - 2400 * x[1] - 576 * x[0]
        ],
        name='F3',
        continuous=True
    ),
    17: Example(
        n=2,
        local_1=Zone(shape='box', low=[-1] * 2, up=[1] * 2),
        init=Zone(shape='box', low=[-0.1] * 2, up=[0.1] * 2),
        unsafe=Zone(shape='box', low=[0.5]*2 , up=[1] * 2),
        f_1=[
            lambda x: -2 * x[0] + x[0] * x[0] + x[1],
            lambda x: x[0] - 2 * x[1] + x[1] * x[1]
           ],
        name='C5',
        continuous=True
    ),
}


def get_example_by_id(id: int):
    return examples[id]


def get_example_by_name(name: str):
    for ex in examples.values():
        if ex.name == name:
            return ex
    raise ValueError('The example {} was not found.'.format(name))
