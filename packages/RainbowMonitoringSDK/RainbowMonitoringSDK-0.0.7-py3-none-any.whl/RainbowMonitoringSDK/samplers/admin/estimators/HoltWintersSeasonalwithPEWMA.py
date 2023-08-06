'''
Created on May 21, 2020
@author: gioargyr
'''

import sys, math

class HoltWintersSeasonalwithPEWMA:

    def __init__(self, season_dict, season_divider, t, cur_val):
        self.season_dict = season_dict
        self.season_divider = season_divider
        self.t = t
        self.isFirst = True
        self.confidence = 1.96      # default for 0.95
        self.t_limit = 5
        self.a = 0.45
        self.b = 1
        self.temp1 = 0
        self.temp2 = 0
        self.bt = 0
        self.g = 0.45
        self.w = 0.7

        if cur_val != -sys.float_info.max:
            self.calculate(cur_val)


    def calculate(self, value):
        print("\nflag = " + str(self.isFirst))
        print("value = " + str(value))
        if not self.isFirst:
            print("if is running")
            if self.get_est_sd() > 0:
                # print("@if est_sd = " + str(self.get_est_sd()))
                z = (value - self.get_est_avg()) / self.get_est_sd()
                # print("@if z = " + str(z))
            else:
                z = 0
            p = self.get_prob_norm(z)
            # print("p = " + str(p))

            if self.t < self.t_limit:
                at = 1 - (1 / self.t)
            else:
                at = self.a * (1 - self.b * p)

            self.temp1 = at * (self.temp1 + self.bt) + (1 - at) * value
            self.temp2 = at * self.temp2 + (1 - at) * math.pow(value, 2)

            print("\tg = " + str(self.g))
            print("\ttemp1 = " + str(self.temp1))
            print("\test_avg = " + str(self.est_avg))
            print("\test_trend = " + str(self.est_trend))

            self.bt = self.g * (self.temp1 - self.est_avg) + (1 - self.g) * self.est_trend

            self.s = self.w * (value - self.get_est_avg() - self.est_trend) + (1 - self.w) * (value - self.season_dict[round(self.t / self.season_divider)].get_value())

            self.set_est_avg(self.temp1)
            self.set_est_sd(math.sqrt(abs(self.temp2 - math.pow(self.temp1, 2))))
            self.est_trend = self.bt
            self.estSeasonality = self.s
        else:
            print("else is running")
            self.temp1 = value
            self.temp2 = math.pow(value, 2)
            self.set_est_avg(value)
            self.set_est_sd(0)
            self.est_trend = 0
            self.bt = 0
            self.estSeasonality = 0
            self.s = 0
            self.isFirst = False

        self.t += 1

        print("@final temp1 = " + str(self.temp1))
        print("@final temp2 = " + str(self.temp2))
        print("@final est_avg = " + str(self.get_est_avg()))
        print("@final est_sd = " + str(self.get_est_sd()))
        print("@final est_trend = " + str(self.est_trend))
        print("@final bt = " + str(self.bt))
        print("@final estSeasonality = " + str(self.estSeasonality))
        print("@final s = " + str(self.s))
        print("@final isFirst = " + str(self.isFirst))


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