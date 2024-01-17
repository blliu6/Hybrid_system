import numpy as np


class Zone:
    def __init__(self, shape: str, low=None, up=None, center=None, r=None, verify_zone=None):
        self.shape = shape
        self.verify_zone = verify_zone
        if shape == 'ball':
            self.center = np.array(center, dtype=np.float32)
            self.r = r  # radius squared
        elif shape == 'box':
            self.low = np.array(low, dtype=np.float32)
            self.up = np.array(up, dtype=np.float32)
        else:
            raise ValueError(f'There is no area of such shape!')


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
        name='H2_easy'
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
        name='H2'  # Safety Verification of Nonlinear Hybrid Systems Based on Bilinear Programming->H3
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
        name='H4'  # Safety Verification of Nonlinear Hybrid Systems Based on Bilinear Programming->H2
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
        name='H4_easy'
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
        name='H3_hard'
        # Darboux-type_barrier_certificates_for_safety_verification_of_nonlinear_hybrid_systems->EXAMPLE2
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
        name='H3'
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
        name='H5'
        # Safety Verification of Nonlinear Hybrid Systems Based on Invariant Clusters
    ),
    7: Example(
        n=2,
        local_1=Zone(shape='box', low=[0, 0], up=[40, 60]),
        local_2=Zone(shape='box', low=[0, 0], up=[40, 60]),
        init=Zone(shape='ball', center=[9, 20], r=2 ** 2),
        unsafe=Zone(shape='box', low=[0, 48], up=[40, 60], verify_zone=[lambda x: (x[1] - 48) * (60 - x[1])]),
        guard_1=Zone(shape='box', low=[35, 0], up=[40, 48]),
        guard_2=Zone(shape='box', low=[0, 0], up=[5, 48]),
        reset_1=[lambda x: x[0], lambda x: x[1]],
        reset_2=[lambda x: x[0], lambda x: x[1]],
        f_1=[lambda x: x[1] ** 2 - 10 * x[1] + 25,
             lambda x: 2 * x[0] * x[1] + 10 * x[0] - 40 * x[1] - 200],
        f_2=[lambda x: -x[1] ** 2 - 10 * x[1] - 25,
             lambda x: 8 * x[0] * x[1] + 40 * x[0] - 160 * x[1] - 800],
        name='H5_easy'
        # Safety Verification of Nonlinear Hybrid Systems Based on Invariant Clusters
    ),
    8: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2, -2], up=[0, 2]),
        local_2=Zone(shape='box', low=[0, -2], up=[2, 2]),
        init=Zone(shape='ball', center=[-1, -1], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[1, 1], r=0.5 ** 2),
        guard_1=Zone(shape='box', low=[0, -2], up=[2, 2]),
        guard_2=Zone(shape='box', low=[-2, -2], up=[0, 2]),
        reset_1=[lambda x: x[0], lambda x: x[1]],
        reset_2=[lambda x: x[0], lambda x: x[1]],
        f_1=[lambda x: x[1],
             lambda x: x[0] - 0.25 * x[0] ** 2],
        f_2=[lambda x: x[1],
             lambda x: -x[0] - 0.5 * x[0] ** 3],
        name='H1'
        # fossil
    ),
    37: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2] * 2, up=[2] * 2),
        init=Zone(shape='ball', center=[1.125, 0.625], r=0.0125),
        unsafe=Zone(shape='ball', center=[0.875, 0.125], r=0.0125),
        f_1=[
            lambda x: x[0],
            lambda x: x[1]
        ],
        name='C1',
        continuous=True
    ),
    21: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2] * 2, up=[2] * 2),
        init=Zone(shape='ball', center=[-1, 0.5], r=0.4 ** 2),
        unsafe=Zone(shape='ball', center=[-1, -0.5], r=0.4 ** 2),
        f_1=[
            lambda x: -2 * x[1],
            lambda x: x[0] ** 2
        ],
        name='C2',
        continuous=True
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
        name='C3',
        continuous=True
    ),
    43: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2] * 2, up=[2] * 2),
        init=Zone(shape='box', low=[-1 / 4, 3 / 4], up=[1 / 4, 3 / 2]),
        unsafe=Zone(shape='box', low=[1, 1], up=[2, 2]),
        f_1=[
            lambda x: - x[0] + 2 * (x[0] ** 2) * x[1],
            lambda x: -x[1]
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
        name='C5',
        continuous=True
    ),
    27: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2] * 2, up=[2] * 2),
        init=Zone(shape='ball', center=[0, 0.5], r=0.2 ** 2),
        unsafe=Zone(shape='ball', center=[-1.5, -1.5], r=0.5 ** 2),
        f_1=[
            lambda x: -x[0] + 2 * (x[0] ** 3) * x[1] ** 2,
            lambda x: -x[1],
        ],
        name='C6',
        continuous=True
    ),
    22: Example(
        n=3,
        local_1=Zone(shape='box', low=[-20] * 3, up=[20] * 3),
        init=Zone(shape='ball', center=[-14.5, -14.5, 12.5], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[-16.5, -14.5, 2.5], r=0.5 ** 2),
        f_1=[
            lambda x: 10.0 * (-x[0] + x[1]),
            lambda x: -x[1] + x[0] * (28.0 - x[2]),
            lambda x: x[0] * x[1] - 8 / 3 * x[2]
        ],
        name='C7',
        continuous=True
    ),
    36: Example(
        n=3,
        local_1=Zone(shape='box', low=[-2] * 3, up=[2] * 3),
        init=Zone(shape='ball', center=[0, 0, 0], r=1 ** 2),
        unsafe=Zone(shape='ball', center=[1.5, 1.5, 1.5], r=1.5 ** 2),
        # 非安全区域改动
        f_1=[
            lambda x: -x[0] + x[1] - x[2],
            lambda x: -x[0] * (x[2] + 1) - x[1],
            lambda x: 0.76524 * x[0] - 4.7037 * x[2]
        ],
        name='C8',
        continuous=True
    ),
    26: Example(
        n=3,
        local_1=Zone(shape='box', low=[-2] * 3, up=[2] * 3),
        init=Zone(shape='ball', center=[0.25, 0.25, 0.25], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[1.5, -1.5, -1.5], r=0.5 ** 2),
        f_1=[
            lambda x: -x[1],
            lambda x: -x[2],
            lambda x: -x[0] - 2 * x[1] - x[2] + x[0] ** 3
        ],
        name='C9',
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
        name='C10',
        continuous=True
    ),
    38: Example(
        n=4,
        local_1=Zone(shape='box', low=[-1.5] * 4, up=[1.5] * 4),
        init=Zone(shape='box', low=[-0.2, -1.2, -1.5, -1.5],
                  up=[0.2, -0.8, 1.5, 1.5]),
        unsafe=Zone(shape='box', low=[-1.2, -0.2, -1.5, -1.5],
                    up=[-0.8, 0.2, 1.5, 1.5]),
        f_1=[
            lambda x: -0.5 * x[0] ** 2 - 2 * (x[1] ** 2 + x[2] ** 2 - x[3] ** 2),
            lambda x: -x[0] * x[1] - 1,
            lambda x: -x[0] * x[2],
            lambda x: -x[0] * x[3]
        ],
        name='C11',
        continuous=True
    ),
    49: Example(
        n=6,
        local_1=Zone(shape='box', low=[-2] * 6, up=[2] * 6),
        init=Zone(shape='box', low=[0.5] * 6, up=[1.5] * 6),
        unsafe=Zone(shape='box', low=[-2] * 6, up=[-1.6] * 6),
        f_1=[
            lambda x: x[1],
            lambda x: x[2],
            lambda x: x[3],
            lambda x: x[4],
            lambda x: x[5],
            lambda x: - 800 * x[5] - 2273 * x[4] - 3980 * x[3] - 4180 * x[2] - 2400 * x[1] - 576 * x[0]
        ],
        name='C12',
        continuous=True
    ),
    45: Example(
        n=6,
        local_1=Zone(shape='box', low=[-2] * 6, up=[2] * 6),
        init=Zone(shape='box', low=[1] * 6, up=[2] * 6),
        unsafe=Zone(shape='box', low=[-1] * 6, up=[-0.5] * 6),
        f_1=[
            lambda x: x[0] * x[2],
            lambda x: x[0] * x[4],
            lambda x: (x[3] - x[2]) * x[2] - 2 * x[4] * x[4],
            lambda x: -(x[3] - x[2]) ** 2 - x[0] * x[0] + x[5] * x[5],
            lambda x: x[1] * x[5] + (x[2] - x[3]) * x[4],
            lambda x: 2 * x[1] * x[4] - x[2] * x[5],
        ],
        name='C13',
        continuous=True
    ),
    46: Example(
        n=6,
        local_1=Zone(shape='box', low=[0] * 6, up=[10] * 6),
        init=Zone(shape='box', low=[3] * 6, up=[3.1] * 6),
        unsafe=Zone(shape='box', low=[4, 4.1, 4.2, 4.3, 4.4, 4.5], up=[4.1, 4.2, 4.3, 4.4, 4.5, 4.6]),
        f_1=[
            lambda x: -x[0] ** 3 + 4 * x[1] ** 3 - 6 * x[2] * x[3],
            lambda x: -x[0] - x[1] + x[4] ** 3,
            lambda x: x[0] * x[3] - x[2] + x[3] * x[5],
            lambda x: x[0] * x[2] + x[2] * x[5] - x[3] ** 3,
            lambda x: -2 * x[1] ** 3 - x[4] + x[5],
            lambda x: -3 * x[2] * x[3] - x[4] ** 3 - x[5],
        ],
        name='C14',
        continuous=True
    ),
    40: Example(
        n=7,
        local_1=Zone(shape='box', low=[-2] * 7, up=[2] * 7),
        init=Zone(shape='ball', center=[1, 1, 1, 1, 1, 1, 1], r=0.01 ** 2),
        unsafe=Zone(shape='ball', center=[1.9, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9], r=0.1 ** 2),
        f_1=[
            lambda x: -0.4 * x[0] + 5 * x[2] * x[3],
            lambda x: 0.4 * x[0] - x[1],
            lambda x: x[1] - 5 * x[2] * x[3],
            lambda x: 5 * x[4] * x[5] - 5 * x[2] * x[3],
            lambda x: -5 * x[4] * x[5] + 5 * x[2] * x[3],
            lambda x: 0.5 * x[6] - 5 * x[4] * x[5],
            lambda x: -0.5 * x[6] + 5 * x[4] * x[5],
        ],
        name='C15',
        continuous=True
    ),
    50: Example(
        n=8,
        local_1=Zone(shape='box', low=[-2] * 8, up=[2] * 8),
        init=Zone(shape='box', low=[0.5] * 8, up=[1.5] * 8),
        unsafe=Zone(shape='box', low=[-2] * 8, up=[-1.6] * 8),
        f_1=[
            lambda x: x[1],
            lambda x: x[2],
            lambda x: x[3],
            lambda x: x[4],
            lambda x: x[5],
            lambda x: x[6],
            lambda x: x[7],
            lambda x: -20 * x[7] - 170 * x[6] - 800 * x[5] - 2273 * x[4] - 3980 * x[3] - 4180 * x[2] - 2400 * x[
                1] - 576 * x[0]
        ],
        name='C16',
        continuous=True
    ),
    41: Example(
        n=9,
        local_1=Zone(shape='box', low=[-2] * 9, up=[2] * 9),
        init=Zone(shape='ball', center=[1, 1, 1, 1, 1, 1, 1, 1, 1], r=0.1 ** 2),
        unsafe=Zone(shape='ball', center=[1.9, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9, 1.9], r=0.1 ** 2),
        f_1=[
            lambda x: 3 * x[2] - x[0] * x[5],
            lambda x: x[3] - x[1] * x[5],
            lambda x: x[0] * x[5] - 3 * x[2],
            lambda x: x[1] * x[5] - x[3],
            lambda x: 3 * x[2] + 5 * x[0] - x[4],
            lambda x: 5 * x[4] + 3 * x[2] + x[3] - x[5] * (x[0] + x[1] + 2 * x[7] + 1),
            lambda x: 5 * x[3] + x[1] - 0.5 * x[6],
            lambda x: 5 * x[6] - 2 * x[5] * x[7] + x[8] - 0.2 * x[7],
            lambda x: 2 * x[5] * x[7] - x[8],
        ],
        name='C17',
        continuous=True
    ),
    42: Example(
        n=12,
        local_1=Zone(shape='box', low=[-2] * 12, up=[2] * 12),
        init=Zone(shape='ball', center=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], r=0.1 ** 2),
        unsafe=Zone(shape='ball', center=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], r=0.1 ** 2),
        f_1=[
            lambda x: x[3],
            lambda x: x[4],
            lambda x: x[5],
            lambda x: -7253.4927 * x[0] + 1936.3639 * x[10] - 1338.7624 * x[3] + 1333.3333 * x[7],
            lambda x: -7253.4927 * x[1] - 1936.3639 * x[9] - 1338.7624 * x[4] + 1333.3333 * x[6],
            lambda x: -769.2308 * x[2] - 770.2301 * x[5],
            lambda x: x[9],
            lambda x: x[10],
            lambda x: x[11],
            lambda x: 9.81 * x[1],
            lambda x: -9.81 * x[0],
            lambda x: -16.3541 * x[11] - 15.3846 * x[8]
        ],
        name='C18',
        continuous=True
    ),
    53: Example(
        n=13,
        local_1=Zone(shape='box', low=[-0.3] * 13, up=[0.3] * 13),
        init=Zone(shape='box', low=[-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2],
                  up=[0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
        unsafe=Zone(shape='box', low=[-0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3],
                    up=[-0.15, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]),
        f_1=[
            lambda x: (x[1] + x[2] + x[2] + x[3] + x[3] + x[4] + x[4] + x[5] + x[5] + x[6] + x[6] + x[7]) / 100 + 1,
            lambda x: x[2],
            lambda x: -10 * (x[1] - x[1] ** 3 / 6) - x[1],
            lambda x: x[4],
            lambda x: -10 * (x[3] - x[3] ** 3 / 6) - x[1],
            lambda x: x[6],
            lambda x: -10 * (x[5] - x[5] ** 3 / 6) - x[1],
            lambda x: x[8],
            lambda x: -10 * (x[7] - x[7] ** 3 / 6) - x[1],
            lambda x: x[10],
            lambda x: -10 * (x[9] - x[9] ** 3 / 6) - x[1],
            lambda x: x[12],
            lambda x: -10 * (x[11] - x[11] ** 3 / 6) - x[1],
        ],
        name='C19',
        continuous=True
    ),
    54: Example(
        n=15,
        local_1=Zone(shape='box', low=[-0.3] * 15, up=[0.3] * 15),
        init=Zone(shape='box',
                  low=[-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2],
                  up=[0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
        unsafe=Zone(shape='box',
                    low=[-0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3],
                    up=[-0.15, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                        -0.25, -0.25]),
        f_1=[
            lambda x: (x[1] + x[2] + x[2] + x[3] + x[3] + x[4] + x[4] + x[5] + x[5] + x[6] + x[6] + x[7] + x[7] + x[
                8]) / 100 + 1,
            lambda x: x[2],
            lambda x: -10 * (x[1] - x[1] ** 3 / 6) - x[1],
            lambda x: x[4],
            lambda x: -10 * (x[3] - x[3] ** 3 / 6) - x[1],
            lambda x: x[6],
            lambda x: -10 * (x[5] - x[5] ** 3 / 6) - x[1],
            lambda x: x[8],
            lambda x: -10 * (x[7] - x[7] ** 3 / 6) - x[1],
            lambda x: x[10],
            lambda x: -10 * (x[9] - x[9] ** 3 / 6) - x[1],
            lambda x: x[12],
            lambda x: -10 * (x[11] - x[11] ** 3 / 6) - x[1],
            lambda x: x[14],
            lambda x: -10 * (x[13] - x[13] ** 3 / 6) - x[1],
        ],
        name='C20',
        continuous=True
    ),
    55: Example(
        n=17,
        local_1=Zone(shape='box', low=[-0.3] * 17, up=[0.3] * 17),
        init=Zone(shape='box',
                  low=[-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                       -0.2], up=[0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
        unsafe=Zone(shape='box',
                    low=[-0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3,
                         -0.3],
                    up=[-0.15, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                        -0.25, -0.25, -0.25, -0.25]),
        f_1=[
            lambda x: (x[1] + x[2] + x[2] + x[3] + x[3] + x[4] + x[4] + x[5] + x[5] + x[6] + x[6] + x[7] + x[7] + x[8] +
                       x[8] + x[9]) / 100 + 1,
            lambda x: x[2],
            lambda x: -10 * (x[1] - x[1] ** 3 / 6) - x[1],
            lambda x: x[4],
            lambda x: -10 * (x[3] - x[3] ** 3 / 6) - x[1],
            lambda x: x[6],
            lambda x: -10 * (x[5] - x[5] ** 3 / 6) - x[1],
            lambda x: x[8],
            lambda x: -10 * (x[7] - x[7] ** 3 / 6) - x[1],
            lambda x: x[10],
            lambda x: -10 * (x[9] - x[9] ** 3 / 6) - x[1],
            lambda x: x[12],
            lambda x: -10 * (x[11] - x[11] ** 3 / 6) - x[1],
            lambda x: x[14],
            lambda x: -10 * (x[13] - x[13] ** 3 / 6) - x[1],
            lambda x: x[16],
            lambda x: -10 * (x[15] - x[15] ** 3 / 6) - x[1],
        ],
        name='C21',
        continuous=True
    ),

    56: Example(
        n=19,
        local_1=Zone(shape='box', low=[-0.3] * 19, up=[0.3] * 19),
        init=Zone(shape='box',
                  low=[-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                       -0.2, -0.2, -0.2],
                  up=[0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
        unsafe=Zone(shape='box',
                    low=[-0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3,
                         -0.3, -0.3, -0.3],
                    up=[-0.15, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                        -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]),
        f_1=[
            lambda x: (x[1] + x[2] + x[2] + x[3] + x[3] + x[4] + x[4] + x[5] + x[5] + x[6] + x[6] + x[7] + x[7] + x[8] +
                       x[8] + x[9] + x[9] + x[10]) / 100 + 1,
            lambda x: x[2],
            lambda x: -10 * (x[1] - x[1] ** 3 / 6) - x[1],
            lambda x: x[4],
            lambda x: -10 * (x[3] - x[3] ** 3 / 6) - x[1],
            lambda x: x[6],
            lambda x: -10 * (x[5] - x[5] ** 3 / 6) - x[1],
            lambda x: x[8],
            lambda x: -10 * (x[7] - x[7] ** 3 / 6) - x[1],
            lambda x: x[10],
            lambda x: -10 * (x[9] - x[9] ** 3 / 6) - x[1],
            lambda x: x[12],
            lambda x: -10 * (x[11] - x[11] ** 3 / 6) - x[1],
            lambda x: x[14],
            lambda x: -10 * (x[13] - x[13] ** 3 / 6) - x[1],
            lambda x: x[16],
            lambda x: -10 * (x[15] - x[15] ** 3 / 6) - x[1],
            lambda x: x[18],
            lambda x: -10 * (x[17] - x[17] ** 3 / 6) - x[1],
        ],
        name='C22',
        continuous=True
    ),
    57: Example(
        n=21,
        local_1=Zone(shape='box', low=[-0.3] * 21, up=[0.3] * 21),
        init=Zone(shape='box',
                  low=[-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                       -0.2, -0.2, -0.2, -0.2, -0.2],
                  up=[0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                      0.3]),
        unsafe=Zone(shape='box',
                    low=[-0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3,
                         -0.3, -0.3, -0.3, -0.3, -0.3],
                    up=[-0.15, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                        -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]),
        f_1=[
            lambda x: (x[1] + x[2] + x[2] + x[3] + x[3] + x[4] + x[4] + x[5] + x[5] + x[6] + x[6] + x[7] + x[7] + x[8] +
                       x[8] + x[9] + x[9] + x[10] + x[10] + x[11]) / 100 + 1,
            lambda x: x[2],
            lambda x: -10 * (x[1] - x[1] ** 3 / 6) - x[1],
            lambda x: x[4],
            lambda x: -10 * (x[3] - x[3] ** 3 / 6) - x[1],
            lambda x: x[6],
            lambda x: -10 * (x[5] - x[5] ** 3 / 6) - x[1],
            lambda x: x[8],
            lambda x: -10 * (x[7] - x[7] ** 3 / 6) - x[1],
            lambda x: x[10],
            lambda x: -10 * (x[9] - x[9] ** 3 / 6) - x[1],
            lambda x: x[12],
            lambda x: -10 * (x[11] - x[11] ** 3 / 6) - x[1],
            lambda x: x[14],
            lambda x: -10 * (x[13] - x[13] ** 3 / 6) - x[1],
            lambda x: x[16],
            lambda x: -10 * (x[15] - x[15] ** 3 / 6) - x[1],
            lambda x: x[18],
            lambda x: -10 * (x[17] - x[17] ** 3 / 6) - x[1],
            lambda x: x[20],
            lambda x: -10 * (x[19] - x[19] ** 3 / 6) - x[1],
        ],
        name='C23',
        continuous=True
    ),
    58: Example(
        n=23,
        local_1=Zone(shape='box', low=[-0.3] * 23, up=[0.3] * 23),
        init=Zone(shape='box',
                  low=[-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                       -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2],
                  up=[0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                      0.3, 0.3, 0.3]),
        unsafe=Zone(shape='box',
                    low=[-0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3,
                         -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3],
                    up=[-0.15, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                        -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]),
        f_1=[
            lambda x: (x[1] + x[2] + x[2] + x[3] + x[3] + x[4] + x[4] + x[5] + x[5] + x[6] + x[6] + x[7] + x[7] + x[8] +
                       x[8] + x[9] + x[9] + x[10] + x[10] + x[11] + x[11] + x[12]) / 100 + 1,
            lambda x: x[2],
            lambda x: -10 * (x[1] - x[1] ** 3 / 6) - x[1],
            lambda x: x[4],
            lambda x: -10 * (x[3] - x[3] ** 3 / 6) - x[1],
            lambda x: x[6],
            lambda x: -10 * (x[5] - x[5] ** 3 / 6) - x[1],
            lambda x: x[8],
            lambda x: -10 * (x[7] - x[7] ** 3 / 6) - x[1],
            lambda x: x[10],
            lambda x: -10 * (x[9] - x[9] ** 3 / 6) - x[1],
            lambda x: x[12],
            lambda x: -10 * (x[11] - x[11] ** 3 / 6) - x[1],
            lambda x: x[14],
            lambda x: -10 * (x[13] - x[13] ** 3 / 6) - x[1],
            lambda x: x[16],
            lambda x: -10 * (x[15] - x[15] ** 3 / 6) - x[1],
            lambda x: x[18],
            lambda x: -10 * (x[17] - x[17] ** 3 / 6) - x[1],
            lambda x: x[20],
            lambda x: -10 * (x[19] - x[19] ** 3 / 6) - x[1],
            lambda x: x[22],
            lambda x: -10 * (x[21] - x[21] ** 3 / 6) - x[1],
        ],
        name='C24',
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
        name='T1',
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
        name='T2',
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
        name='T3',
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
        name='T4',
        continuous=True
    ),

    17: Example(
        n=2,
        local_1=Zone(shape='box', low=[-1] * 2, up=[1] * 2),
        init=Zone(shape='box', low=[-0.1] * 2, up=[0.1] * 2),
        unsafe=Zone(shape='box', low=[0.5] * 2, up=[1] * 2),
        f_1=[
            lambda x: -2 * x[0] + x[0] * x[0] + x[1],
            lambda x: x[0] - 2 * x[1] + x[1] * x[1]
        ],
        name='T5',
        continuous=True
    ),
    20: Example(
        n=2,
        local_1=Zone(shape='box', low=[0] * 2, up=[2] * 2),
        init=Zone(shape='ball', center=[1.125, 0.625], r=0.0125),
        unsafe=Zone(shape='ball', center=[0.875, 0.125], r=0.0125),
        f_1=[
            lambda x: -x[0] + x[1],
            lambda x: -x[1]
        ],
        name='Exp3',
        continuous=True
    ),

    23: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2] * 2, up=[2] * 2),
        init=Zone(shape='ball', center=[1.125, 0.625], r=0.125 ** 2),
        unsafe=Zone(shape='ball', center=[-1.5, -1.25], r=0.25 ** 2),
        f_1=[
            lambda x: -0.1 * x[0] - 10 * x[1],
            lambda x: 4 * x[0] - 2 * x[1]
        ],
        name='Exp6',
        continuous=True
    ),
    24: Example(
        n=3,
        local_1=Zone(shape='box', low=[-2] * 3, up=[2] * 3),
        init=Zone(shape='ball', center=[1, 1, 0], r=0.8 ** 2),
        unsafe=Zone(shape='box', low=[-0.5, -1.5, -1], up=[0.5, -0.5, 1]),
        f_1=[
            lambda x: x[0] * (1 - x[2]),
            lambda x: x[1] * (1 - 2 * x[2]),
            lambda x: x[2] * (-1 + x[0] + x[1])
        ],
        name='Exp7',
        continuous=True
    ),
    25: Example(
        n=2,
        local_1=Zone(shape='box', low=[-1.5] * 2, up=[5.5] * 2),
        init=Zone(shape='box', low=[4, -1], up=[4.25, 1]),
        unsafe=Zone(shape='ball', center=[1.5, 2.5], r=0.5 ** 2),
        f_1=[
            lambda x: -x[0] + 2 * x[1] * x[0] ** 2,
            lambda x: -x[1]
        ],
        name='Exp8',
        continuous=True
    ),

    28: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2] * 2, up=[2] * 2),
        init=Zone(shape='ball', center=[-0.5, -0.5], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[-1.5, -1.5], r=0.5 ** 2),
        f_1=[
            lambda x: x[0] ** 2 + x[1] ** 2 - 1,
            lambda x: 5 * (x[0] * x[1] - 1),
        ],
        name='Exp11',
        continuous=True
    ),
    29: Example(
        n=2,
        local_1=Zone(shape='box', low=[-3] * 2, up=[3] * 2),
        init=Zone(shape='ball', center=[0, 0], r=0.2 ** 2),
        unsafe=Zone(shape='ball', center=[2.5, 2.5], r=0.5 ** 2),
        f_1=[
            lambda x: x[0] - x[0] ** 3 + x[1] - x[0] * x[1] ** 2,
            lambda x: -x[0] + x[1] - x[1] * x[0] ** 2 - x[1] ** 3
        ],
        name='Exp12',
        continuous=True
    ),
    30: Example(
        n=2,
        local_1=Zone(shape='box', low=[-0.5] * 2, up=[1] * 2),
        init=Zone(shape='ball', center=[0, 0], r=0.1 ** 2),
        unsafe=Zone(shape='ball', center=[0.75, 0.75], r=0.25 ** 2),
        f_1=[
            lambda x: -2 * x[0] + x[0] ** 2 + x[1],
            lambda x: x[0] - 2 * x[1] + x[1] ** 2
        ],
        name='Exp13',
        continuous=True
    ),
    31: Example(
        n=2,
        local_1=Zone(shape='box', low=[-4] * 2, up=[4] * 2),
        init=Zone(shape='ball', center=[1.5, 0], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[-1, -1], r=0.4 ** 2),
        f_1=[
            lambda x: x[1],
            lambda x: -x[0] + 1 / 3 * x[0] ** 3 - x[1]
        ],
        name='Exp14',
        continuous=True
    ),
    32: Example(
        n=2,
        local_1=Zone(shape='box', low=[0] * 2, up=[1.5] * 2),
        init=Zone(shape='ball', center=[1.125, 0.625], r=0.125 ** 2),
        unsafe=Zone(shape='ball', center=[0.875, 0.125], r=0.075 ** 2),
        f_1=[
            lambda x: -x[0] + x[0] * x[1],
            lambda x: -x[1]
        ],
        name='Exp15',
        continuous=True
    ),
    33: Example(
        n=2,
        local_1=Zone(shape='box', low=[-2] * 2, up=[2] * 2),
        init=Zone(shape='ball', center=[-1, -1], r=0.5 ** 2),
        unsafe=Zone(shape='ball', center=[0, 1], r=0.5 ** 2),
        f_1=[
            lambda x: -x[0] + x[0] * x[1],
            lambda x: -x[1]
        ],
        name='Exp16',
        continuous=True
    ),
    34: Example(
        n=2,
        local_1=Zone(shape='box', low=[-1] * 2, up=[3] * 2),
        init=Zone(shape='ball', center=[0, 9 / 8], r=27 / 8),
        unsafe=Zone(shape='ball', center=[2, 2], r=0.5 ** 2),
        f_1=[
            lambda x: -x[0] + 2 * (x[0] ** 2) * x[1],
            lambda x: -x[1]
        ],
        name='Exp17',
        continuous=True
    ),
    35: Example(
        n=2,
        local_1=Zone(shape='box', low=[-5] * 2, up=[5] * 2),
        init=Zone(shape='ball', center=[-0.75, 1.25], r=0.25 ** 2),
        unsafe=Zone(shape='ball', center=[-2.25, -1.75], r=0.25 ** 2),
        f_1=[
            lambda x: -1 / 3 * x[0] ** 3 + x[0] - x[1] + 0.875,
            lambda x: 0.08 * (x[0] - 0.8 * x[1] + 0.7)
        ],
        name='Exp18',
        continuous=True
    ),

    39: Example(
        n=2,
        local_1=Zone(shape='box', low=[1.5] * 2, up=[3.5] * 2),
        init=Zone(shape='ball', center=[2.75, 2], r=0.25 ** 2),
        unsafe=Zone(shape='box', low=[1.5, 1.5], up=[2, 3.5]),
        f_1=[
            lambda x: x[0] - x[1],
            lambda x: x[0] + x[1]
        ],
        name='Exp22',
        continuous=True
    ),

    44: Example(
        n=4,
        local_1=Zone(shape='box', low=[-2] * 4, up=[2] * 4),
        init=Zone(shape='box', low=[0.5] * 4, up=[1.5] * 4),
        unsafe=Zone(shape='box', low=[-1.5] * 4, up=[-0.5] * 4),
        f_1=[
            lambda x: -0.5 * x[0] ** 2 - 0.5 * x[1] ** 2 - 0.125 * x[2] ** 2 - 2 * x[1] * x[2] + 2 * x[3] ** 2 + 1,
            lambda x: -x[0] * x[1] - 1,
            lambda x: -x[0] * x[2],
            lambda x: -x[0] * x[3]
        ],
        name='T9',
        continuous=True
    ),

    47: Example(
        n=8,
        local_1=Zone(shape='box', low=[-2] * 8, up=[2] * 8),
        init=Zone(shape='box', low=[-0.1] * 8, up=[0.1] * 8),
        unsafe=Zone(shape='box', low=[0, 0, 0.5, 0.5, 0.5, -1.5, 0.5, -1.5],
                    up=[0.5, 0.5, 1.5, 1.5, 1.5, -0.5, 1.5, -0.5]),
        f_1=[
            lambda x: x[2],
            lambda x: x[3],
            lambda x: -7253.4927 * x[0] + 1936.3639 * x[7] - 1338.7624 * x[2] + 1333.3333 * x[5],
            lambda x: -1936.3639 * x[6] - 7253.4927 * x[1] - 1338.7624 * x[3] - 1333.3333 * x[4],
            lambda x: x[6],
            lambda x: x[7],
            lambda x: 9.81 * x[1],
            lambda x: -9.81 * x[0]
        ],
        name='T13',
        continuous=True
    ),
    48: Example(
        n=10,
        local_1=Zone(shape='box', low=[-2] * 10, up=[2] * 10),
        init=Zone(shape='box', low=[-0.1] * 10, up=[0.1] * 10),
        unsafe=Zone(shape='box', low=[0, 0, 0, 0.5, 0.5, 0.5, 0.5, -1.5, 0.5, -1.5],
                    up=[0.5, 0.5, 0.5, 1.5, 1.5, 1.5, 1.5, -0.5, 1.5, -0.5]),
        f_1=[
            lambda x: x[3],
            lambda x: x[4],
            lambda x: x[5],
            lambda x: -7253.4927 * x[0] + 1936.3639 * x[9] - 1338.7624 * x[3] + 1333.3333 * x[7],
            lambda x: -1936.3639 * x[8] - 7253.4927 * x[1] - 1338.7624 * x[4] - 1333.3333 * x[6],
            lambda x: -769.2308 * x[2] - 770.2301 * x[5],
            lambda x: x[8],
            lambda x: x[9],
            lambda x: 9.81 * x[1],
            lambda x: -9.81 * x[0]
        ],
        name='T15',
        continuous=True
    ),

    51: Example(
        n=9,
        local_1=Zone(shape='box', low=[-2] * 9, up=[2] * 9),
        init=Zone(shape='box', low=[0.99] * 9, up=[1.01] * 9),
        unsafe=Zone(shape='box', low=[1.8] * 9, up=[2] * 9),
        f_1=[
            lambda x: 3 * x[2] - x[0] * x[5],
            lambda x: x[3] - x[1] * x[5],
            lambda x: x[0] * x[5] - 3 * x[2],
            lambda x: x[1] * x[5] - x[3],
            lambda x: 3 * x[2] + 5 * x[0] - x[4],
            lambda x: 5 * x[4] + 3 * x[2] + x[3] - x[5] * (x[0] + x[1] + 2 * x[7] + 1),
            lambda x: 5 * x[3] + x[1] - 0.5 * x[6],
            lambda x: 5 * x[6] - 2 * x[5] * x[7] + x[8] - 0.2 * x[7],
            lambda x: 2 * x[5] * x[7] - x[8],
        ],
        name='T14',
        continuous=True
    ),
    52: Example(
        n=12,
        local_1=Zone(shape='box', low=[-2] * 12, up=[2] * 12),
        init=Zone(shape='box', low=[-0.1] * 12, up=[0.1] * 12),
        unsafe=Zone(shape='box', low=[0, 0, 0, 0.5, 0.5, 0.5, 0.5, -1.5, 0.5, -1.5, 0.5], up=[0.1] * 12),
        f_1=[
            lambda x: x[3],
            lambda x: x[4],
            lambda x: x[5],
            lambda x: -7253.4927 * x[0] + 1936.3639 * x[10] - 1338.7624 * x[3] + 1333.3333 * x[7],
            lambda x: -7253.4927 * x[1] - 1936.3639 * x[9] - 1338.7624 * x[4] + 1333.3333 * x[6],
            lambda x: -769.2308 * x[2] - 770.2301 * x[5],
            lambda x: x[9],
            lambda x: x[10],
            lambda x: x[11],
            lambda x: 9.81 * x[1],
            lambda x: -9.81 * x[0],
            lambda x: -16.3541 * x[11] - 15.3846 * x[8]
        ],
        name='T16',
        continuous=True
    ),

    59: Example(
        n=25,
        local_1=Zone(shape='box', low=[-0.3] * 25, up=[0.3] * 25),
        init=Zone(shape='box',
                  low=[-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2,
                       -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2],
                  up=[0, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                      0.3, 0.3, 0.3, 0.3, 0.3]),
        unsafe=Zone(shape='box',
                    low=[-0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3,
                         -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3],
                    up=[-0.15, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25,
                        -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]),
        f_1=[
            lambda x: (x[1] + x[2] + x[2] + x[3] + x[3] + x[4] + x[4] + x[5] + x[5] + x[6] + x[6] + x[7] + x[7] + x[8] +
                       x[8] + x[9] + x[9] + x[10] + x[11] + x[12] + x[13]) / 100 + 1,
            lambda x: x[2],
            lambda x: -10 * (x[1] - x[1] ** 3 / 6) - x[1],
            lambda x: x[4],
            lambda x: -10 * (x[3] - x[3] ** 3 / 6) - x[1],
            lambda x: x[6],
            lambda x: -10 * (x[5] - x[5] ** 3 / 6) - x[1],
            lambda x: x[8],
            lambda x: -10 * (x[7] - x[7] ** 3 / 6) - x[1],
            lambda x: x[10],
            lambda x: -10 * (x[9] - x[9] ** 3 / 6) - x[1],
            lambda x: x[12],
            lambda x: -10 * (x[11] - x[11] ** 3 / 6) - x[1],
            lambda x: x[14],
            lambda x: -10 * (x[13] - x[13] ** 3 / 6) - x[1],
            lambda x: x[16],
            lambda x: -10 * (x[15] - x[15] ** 3 / 6) - x[1],
            lambda x: x[18],
            lambda x: -10 * (x[17] - x[17] ** 3 / 6) - x[1],
            lambda x: x[20],
            lambda x: -10 * (x[19] - x[19] ** 3 / 6) - x[1],
            lambda x: x[22],
            lambda x: -10 * (x[21] - x[21] ** 3 / 6) - x[1],
            lambda x: x[24],
            lambda x: -10 * (x[23] - x[23] ** 3 / 6) - x[1],
        ],
        name='R12',
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
