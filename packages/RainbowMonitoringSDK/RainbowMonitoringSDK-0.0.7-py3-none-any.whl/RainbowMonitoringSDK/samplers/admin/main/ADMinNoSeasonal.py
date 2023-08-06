'''
Created on May 22, 2020
@author: gioargyr
'''

import os, sys
from utils import reader
from sampler.admin import change_detectors, estimators
import sampler

class ADMinNoSeasonal:

    def __init__(self, resources_dir):

        self.properties_reader = reader.PropertiesReader(resources_dir)
        self.samples = reader.FileReader().read_csv_file(os.path.join(resources_dir, self.properties_reader.dataset_name))
        self.confidence = 1.645
        self.k = 0

        self.model1 = estimators.HoltsLinearSophisticTrendwithPEWMA()
        self.model1.set_confidence(self.confidence)

        self.buffer = []

        h0 = 2
        self.changer = change_detectors.OnlineCUSUMv2(h0)
        self.first = True
        self.i = 0
        self.T = 5
        for sample in self.samples:
            self.update(sample)


### End of init ###


    def update(self, sample):
        # print(str(sample.get_value()))
        self.model1.calculate(sample.get_value())
        if self.i < self.T:
            self.i += 1
            return
        # print("k  first\t" + str(self.k) + "\t" + str(self.first))
        y1 = self.model1.do_forecast(self.k, self.first)
        self.k += 1

        # print("y1 = " + str(y1))
        if not self.model1.isDatapointExpected(y1):
            # print("unexp for y1 = " + str(y1))
            self.buffer.append(sampler.Sample(sample.get_timestamp(), sample.get_value(), ""))

        fdpoint = sampler.Sample(sample.get_timestamp(), y1, "")
        avg = self.model1.get_est_avg()
        sd = self.model1.get_est_sd()

        if self.changer.update(fdpoint, avg, sd):
            self.k = 0
            self.first = True
            self.i = 0

            for item in self.buffer:
                print("unexp datapoint: " + str(item.get_timestamp()) + ", " + str(item.get_value()))
            self.buffer = []
        else:
            self.first = False




if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("\nAdaM.properties and dataset file for AdaM should be in directory: " + sys.argv[1])
        runADMin = ADMinNoSeasonal(sys.argv[1])
    else:
        print("AdaM should run with 1 argument defining the directory that holds the necessary files.")
        sys.exit(2)