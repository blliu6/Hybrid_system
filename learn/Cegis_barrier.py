import timeit

import torch
import numpy as np
from utils.Config import CegisConfig
from learn.generate_data import Data
from learn.Learner import Learner
from verify.SosVerify import SOS
from Counterexample.CounterExampleFind import CounterExampleFinder
from plot.plot import Draw


class Cegis:
    def __init__(self, config: CegisConfig):
        self.config = config
        self.max_cegis_iter = config.max_iter

    def solve(self):
        import mosek

        with mosek.Env() as env:
            with env.Task() as task:
                task.optimize()
                print('Mosek can be used normally.')

        data = Data(self.config).generate_data()
        learner = Learner(self.config)

        counter = CounterExampleFinder(self.config)

        t_learn = 0
        t_cex = 0
        t_sos = 0
        vis_sos = False
        for i in range(self.max_cegis_iter):
            print(f'第{i + 1}回合:')
            t1 = timeit.default_timer()
            learner.learn(data)
            t2 = timeit.default_timer()
            t_learn += t2 - t1

            barrier = learner.net.get_barriers()
            # for poly in barrier:
            #     print(poly)

            t3 = timeit.default_timer()
            sos = SOS(self.config, barrier)
            vis, state = sos.verify_all()

            if vis:
                print('SOS verification passed!')
                print(f'Number of iterations:{i + 1}')
                vis_sos = True
                t4 = timeit.default_timer()
                t_sos += t4 - t3
                break

            t4 = timeit.default_timer()
            t_sos += t4 - t3

            t5 = timeit.default_timer()
            res = counter.find_counterexample(state, barrier)
            t6 = timeit.default_timer()
            t_cex += t6 - t5

            data = self.merge_data(data, res)

        print('Total learning time:{}'.format(t_learn))
        print('Total counter-examples generating time:{}'.format(t_cex))
        print('Total sos verifying time:{}'.format(t_sos))
        end = timeit.default_timer()
        if vis_sos and self.config.example.n == 2:
            draw = Draw(self.config.example, barrier[0], barrier[1])
            # draw.draw()
            draw.draw_3d()
        return end

    def merge_data(self, data, add_res):
        res = []
        ans = 0
        for x, y in zip(data, add_res):
            if len(y) > 0:
                ans = ans + len(y)
                y = torch.Tensor(np.array(y))
                res.append(torch.cat([x, y], dim=0).detach())
            else:
                res.append(x)
        print(f'加入{ans}个反例!')
        return tuple(res)
