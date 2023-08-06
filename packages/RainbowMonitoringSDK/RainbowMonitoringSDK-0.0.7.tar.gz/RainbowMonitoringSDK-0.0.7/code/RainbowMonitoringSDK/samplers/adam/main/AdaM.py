'''
Created on May 20, 2020
@author: gioargyr
'''
import copy
import sys, math
from RainbowMonitoringSDK.samplers.adam import estimators

from RainbowMonitoringSDK.samplers.Sample import Sample
from RainbowMonitoringSDK.samplers.Datapoint import Datapoint


class AdaM(object):

    def __init__(self, Tmin, Tmax, g, lamda, Rmin = None, Rmax = None, isFiltering = False):
        self.isFirst = True
        self.isFiltering = bool(isFiltering)
        self.avenger = estimators.PEWMA()
        self.confidence = 0
        self.sd = 0
        self.lamda = float(lamda)
        self.g = 1 - float(g)
        self.T = int(Tmin)
        self.Tmin = int(Tmin)
        self.Tmax = float(Tmax)
        self.Rmin = float(Rmin) if Rmin else 0.0
        self.Rmax = float(Rmax) if Rmax else 0.0
        self.R = float(self.Rmin)
        self.count = 0

        self.default_learning_interval = 5
        self.counter = 1
        self.prev_sample = Sample(-1, sys.float_info.max, "")
        self.flt_prev_sample = Sample(-1, sys.float_info.max, "")


    def do_filtering(self, prev_sample, cur_sample, R):
        rh = prev_sample.get_value() + R
        rl = prev_sample.get_value() - R
        if cur_sample.get_value() > rh or cur_sample.get_value() < rl:
            return False
        else:
            return True




    def update(self, sample):
        datapoint = Datapoint(sample.get_timestamp(), sample.get_value())
        self.update_sampling_period(sample)
        self.update_filter_range()
        if self.isFiltering:
            R = self.get_filter_range()
            if self.do_filtering(self.flt_prev_sample, sample, R):
                self.count += 1
                datapoint.set_tag("FLTRD")
                datapoint.set_isFiltered(True)
            self.flt_prev_sample = sample

        return datapoint



    def update_sampling_period(self, sample):
        # print("update_sampling_period using sample:" + str(sample.get_timestamp()) + "\t" + str(sample.get_value()))
        if not self.isFirst:
            d = abs(sample.get_value() - self.prev_sample.get_value())
        else:
            d = 0
        self.isFirst = False
        # print("d =\t" + str(d))

        self.avenger.calculate(sample.get_timestamp(), d)

        if self.sd != 0:
            self.confidence = 1 - (abs(self.avenger.get_est_sd() - self.sd) / self.sd)
        if self.sd == 0 or self.confidence == 0:
            self.confidence = 1

        temp = self.lamda * (1 + abs(self.confidence - self.g) / self.confidence)

        Tcandidate = self.T

        if self.counter > self.default_learning_interval:
            print("COUNTER:", self.confidence, self.g, temp)
            if self.confidence > 1 - self.g:
                Tcandidate += round(temp)
            else:
                Tcandidate = self.get_Tmin()
            if Tcandidate < self.get_Tmin():
                Tcandidate = self.get_Tmin()
            if Tcandidate > self.get_Tmax():
                Tcandidate = self.get_Tmax()
        else:
            self.counter += 1

        self.sd = self.avenger.get_est_sd()
        self.prev_sample = copy.deepcopy(sample)
        self.T = Tcandidate
        return self.T


    def update_filter_range(self):
        if self.avenger.get_est_avg() != 0:
            fano_factor = math.pow(self.avenger.get_est_sd(), 2) / self.avenger.get_est_avg()
        else:
            fano_factor = sys.float_info.max

        if fano_factor < self.g:
            self.R = self.R + self.lamda * (self.g - fano_factor) / self.g
        if self.R > self.Rmax:
            self.R = self.Rmax
        if self.R < self.Rmin:
            self.R = self.Rmin

        return self.R





    def get_Tmin(self):
        return self.Tmin

    def get_Tmax(self):
        return self.Tmax

    def get_sampling_period(self):
        return self.T

    def get_filter_range(self):
        return self.R








