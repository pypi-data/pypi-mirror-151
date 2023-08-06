'''
Created on May 21, 2020
@author: gioargyr
'''

import sampler

class OnlineCUSUMv2:

    def __init__(self, threshold, detect_actual_changepoints=False):
        self.h = threshold
        self.change_points = []

        self.reset()
        self.first = True

        self.detect_actual_changepoints = detect_actual_changepoints
        if self.detect_actual_changepoints:
            self.cusum_array_high = []
            self.cusum_array_low = []
            self.accual_change_points = []


    def find_change(self, cusum_list):
        minim = cusum_list[0]
        for i in range(1, len(cusum_list) - 1):
            if cusum_list[i].get_value() < minim.get_value():
                minim = cusum_list[i]
            self.accual_change_points.append(minim.get_timestamp())


    def reset(self):
        self.dist = 0
        self.temp_high = 0
        self.temp_low = 0
        self.cusum_high = 0
        self.cusum_low = 0
        self.decision_high = 0
        self.decision_low = 0
        self.first = True
        self.cusum_array_high = None
        self.cusum_array_low = None


    def update(self, sample, act_avg, cur_sd):
        decision = False
        dist = sample.get_value() - act_avg

        temp_high = 0
        temp_low = 0
        if cur_sd != 0:
            temp_high = abs(dist) / cur_sd * (sample.get_value() - act_avg - abs(dist / 2))
            temp_low = (-1 * abs(dist)) / cur_sd * (sample.get_value() - act_avg + abs(dist / 2))

        self.cusum_high += temp_high
        self.cusum_low += temp_low

        if self.detect_actual_changepoints:
            self.cusum_array_high.append(sampler.Sample(sample.get_timestamp(), self.cusum_high))
            self.cusum_array_high.append(sampler.Sample(sample.get_timestamp(), self.cusum_low))

        self.decision_high += temp_high
        if self.decision_high < 0:
            self.decision_high = 0

        self.decision_low += temp_low
        if self.decision_low < 0:
            self.decision_low = 0

        # print(str(sample.get_value()) + ", " + str(act_avg) + ", " + str(temp_high) + ", " + str(temp_low) + ", " + str(self.cusum_low) + ", " + str(self.cusum_high) + ", " + str(self.decision_low) + ", " + str(self.decision_high));

        self.first = False

        if self.decision_high > self.h:
            self.change_points.append(sample)           ## EXEIS KSEXASEI POLLA!!!
            if self.detect_actual_changepoints:
                self.find_change(self.cusum_array_high)
            self.reset()
            decision = True

        if self.decision_low > self.h:
            self.change_points.append(sample)           ## EXEIS KSEXASEI POLLA!!!
            if self.detect_actual_changepoints:
                self.find_change(self.cusum_array_low)
            self.reset()
            decision = True

        return decision