'''
Created on May 22, 2020
@author: gioargyr
'''

import math

class HoltsLinearSophisticTrendwithPEWMA:

    def __init__(self, t=0):
        self.g = 0.45

        self.t = t
        self.isFirst = True
        self.confidence = 1.96

        self.phi = 0.9
        self.t_phase = 5
        self.a = 0.45
        self.b = 1
        # self.calculate(value)


    def calculate(self, cur_val):
        # print("flag = " + str(self.isFirst))
        if not self.isFirst:
            if self.get_est_sd() > 0:
                # print("@if est_sd = " + str(self.get_est_sd()))
                z = (cur_val - self.get_est_avg()) / self.get_est_sd()
                # print("@if z = " + str(z))
            else:
                z = 0
            p = self.get_prob_norm(z)
            # print("p = " + str(p))

            if self.t <= self.t_phase:
                at = 1 - (1.0 / self.t)
            else:
                at = self.a * (1 - self.b * p)
            self.s1 = at * (self.s1 + self.bt) + (1 - at) * cur_val
            self.s2 = at * self.s2 + (1 - at) * math.pow(cur_val, 2)


            self.bt = self.g * (self.s1 - self.est_avg) + (1 - self.g) * self.est_trend

            self.set_est_avg(self.s1)
            self.set_est_sd(math.sqrt(abs(self.s2 - math.pow(self.s1, 2))))
            self.est_trend = self.bt
        else:
            self.s1 = cur_val
            self.s2 = math.pow(cur_val, 2)
            self.set_est_avg(cur_val)
            self.set_est_sd(0)
            self.est_trend = 0
            self.bt = 0
            self.isFirst = False

        self.t += 1

    def do_forecast(self, k, first):
        if first:
            self.fAvg = self.get_est_avg()
            # print("fAvg1 = " + str(self.fAvg))
            self.fTrend = self.est_trend

        self.fAvg = self.fAvg + math.pow(self.phi, k) * self.fTrend

        return self.fAvg


    def isDatapointExpected(self, value):
        m = self.get_est_avg()
        e = self.get_est_sd()
        c = self.confidence

        if m - c * e < value < m + c * e:
            return True
        else:
            return False


    def set_est_avg(self, value):
        self.est_avg = value

    def set_est_sd(self, value):
        self.est_sd = value

    def set_confidence(self, value):
        self.confidence = value

    def get_est_sd(self):
        return self.est_sd

    def get_est_avg(self):
        return self.est_avg


    """
    instead of this we can import "from scipy import stats as st"
    and get probability from normal distro using: "st.norm.cdf(#put z score to be prob)"
    """
    def get_prob_norm(self, z):
        return (1 / math.sqrt(2 * math.pi)) * math.exp(-math.pow(z, 2) / 2)
