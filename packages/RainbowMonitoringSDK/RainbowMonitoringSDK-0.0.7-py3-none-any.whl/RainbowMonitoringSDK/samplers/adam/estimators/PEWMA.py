'''
Created on May 20, 2020
@author: gioargyr
'''

import math

class PEWMA():

    def __init__(self):
        self.t_phase = 5
        self.s1 = 0
        self.s2 = 0
        self.a = 0.45
        self.b = 1
        self.isFirst = True


    def calculate(self, t, cur_val):
        if not self.isFirst:
            if self.get_est_sd() > 0:
                z = (cur_val - self.get_est_avg()) / self.get_est_sd()
            else:
                z = 0
            p = self.get_prob_norm(z)

            if t <= self.t_phase:
                at = 1 - (1.0 / t)
            else:
                at = self.a * (1 - self.b * p)
            self.s1 = at * self.s1 + (1 - at) * cur_val
            self.s2 = at * self.s2 + (1 - at) * math.pow(cur_val, 2)

            self.set_est_avg(self.s1)
            self.set_est_sd(math.sqrt(self.s2 - math.pow(self.s1, 2)))
        else:
            s1 = cur_val
            s2 = math.pow(cur_val, 2)
            self.set_est_avg(cur_val)
            self.set_est_sd(0)
            self.isFirst = False



    def set_est_avg(self, value):
        self.est_avg = value

    def set_est_sd(self, value):
        self.est_sd = value

    def get_est_sd(self):
        return self.est_sd

    def get_est_avg(self):
        return self.est_avg


    """
    instead of this we can import "from scipy import stats as st"
    and get probability from normal distro using: "st.norm.cdf(#put z score to be prob)"
    """
    def get_prob_norm(self, z):
        return (1 / math.sqrt(2 * math.pi)) * math.exp(-math.pow(z, 2) / 2 )


