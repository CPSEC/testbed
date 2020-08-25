import time
import numpy as np
import math

class Estimator:
    def __init__(self, Ad: np.array, Bd: np.array, max_k, epsilon):
        self.on = True
        # optional, parameter p1
        self.Ad = Ad
        self.Bd = Bd
        self.m = np.size(self.Ad, 0)
        self.epsilon = epsilon
        self.max_k = max_k
        # initiate your data
        self.Ad_k = [np.eye(self.m)]
        for i in range(max_k):
            self.Ad_k.append(self.Ad_k[-1].dot(Ad))
        self.Ad_k_Bd = [i.dot(Bd) for i in self.Ad_k]
        self.Ad_k_Ad_k_T = [i.dot(i.T) for i in self.Ad_k]
        self.epsilon_coef = []
        sqrt_term = np.zeros((self.m, 1))
        for k in range(max_k):
            for i in range(self.m):
                sqrt_term[i, 0] += math.sqrt(self.Ad_k_Ad_k_T[k][i, i])
            self.epsilon_coef.append(sqrt_term.copy())
        print(self.epsilon_coef)


    def estimate(self, x_a: np.array, control_lst: np.array):
        start = time.time()
        k = np.size(control_lst, 1)
        assert k < self.max_k
        assert np.size(x_a, 0) == self.m
        control_sum_term = np.zeros((self.m, 1))
        for j in range(k):
            control_sum_term += self.Ad_k_Bd[j].dot(control_lst[:, k-1-j:k-j])
        x_0 = self.Ad_k[k].dot(x_a) + control_sum_term
        print('x_0=', x_0)
        e = np.ones((self.m, 1)) * self.epsilon * self.epsilon_coef[k]
        x_0_lo = x_0 - e
        x_0_up = x_0 + e
        end = time.time()
        print('Use', end-start, 'seconds for', k, 'steps')
        return x_0_lo, x_0_up


# test
if __name__ == "__main__":
    from recovery import Recovery
    Ad = np.array([[0.818727296278566, 0.017757312092950], [-3.551462418590050e-04, 0.960785793022168]])
    Bd = np.array([[3.695886905026150e-04], [0.039210511090927]])

    # Ad = np.array([[1,2],[3,4]])
    # Bd = np.array([[5,6],[7,8]])

    initial_set_lo = [7.999902067622, 79.998780693465]
    initial_set_up = [7.999902067622887, 79.998780693465960]
    target_set_lo = [3.9, -100]
    target_set_up = [4.1, 100]
    safe_set_lo = [1, -150]
    safe_set_up = [8, 150]
    control_lo = [-150]
    control_up = [150]
    t = Recovery(Ad, Bd)
    control_lst = t.poll(10, initial_set_lo, initial_set_up, target_set_lo, target_set_up, safe_set_lo, safe_set_up,
                         control_lo, control_up)

    t = Estimator(Ad, Bd, 20, 1e-7)
    x0_lo, x0_up = t.estimate(np.array([[7.999902067622887], [79.998780693465960]]), control_lst)
    print(x0_lo, x0_up)
