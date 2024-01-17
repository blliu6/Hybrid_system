import timeit
import torch
import numpy as np
from utils.Config import CegisConfig
from Examplers import get_example_by_name, get_example_by_id
from learn.Learner import Learner
from learn.Cegis_barrier import Cegis


def main():
    start = timeit.default_timer()
    b1_activations = ['SKIP']  # Only "SQUARE","SKIP","MUL" are optional.
    b1_hidden_neurons = [10] * len(b1_activations)

    b2_activations = ['SKIP']  # Only "SQUARE","SKIP","MUL" are optional.
    b2_hidden_neurons = [10] * len(b1_activations)

    example = get_example_by_name('H5')

    start = timeit.default_timer()
    opts = {
        'b1_act': b1_activations,
        'b1_hidden': b1_hidden_neurons,
        'b2_act': b2_activations,
        'b2_hidden': b2_hidden_neurons,
        "example": example,
        'bm1_hidden': [10],
        'bm2_hidden': [10],
        'bm1_act': ['SKIP'],
        'bm2_act': ['SKIP'],
        'rm1_act': [],
        'rm2_act': [],
        "batch_size": 500,
        'lr': 0.01,
        'loss_weight': (1, 1, 1, 1, 1, 1, 1, 1),
        'R_b': 0.5,
        'margin': 1,
        "DEG": [2, 2, 2, 2, 2, 2, 2, 2],  # Respectively represent the times of init, unsafe, diffB,
        # and unconstrained multipliers when verifying sos.
        "learning_loops": 100,
        'max_iter': 10
    }
    Config = CegisConfig(**opts)
    cegis = Cegis(Config)
    end = cegis.solve()
    print('Elapsed Time: {}'.format(end - start))


if __name__ == '__main__':
    torch.manual_seed(2024)
    np.random.seed(2024)
    main()
