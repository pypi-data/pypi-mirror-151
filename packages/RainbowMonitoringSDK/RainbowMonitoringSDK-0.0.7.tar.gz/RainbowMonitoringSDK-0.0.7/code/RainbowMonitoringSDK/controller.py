import logging
import os
import RainbowMonitoringSDK.exporters as exporters
import RainbowMonitoringSDK.probes as probes
import time

from RainbowMonitoringSDK.utils.basics import time_to_seconds


class Controller(object):
    """
    The controller is responsible to orchestrate the execution of:
    - Sensing Units (Metric Collectors)
    - Dissemination Units
    """
    sensing_units: dict = {}
    dissemination_units: dict = {}
    configs: dict = {}
    periodicity_dict: dict = {}

    class MonitoringControllerException(Exception):
        pass

    def __init__(self, configs: dict = None):
        self.configs = configs if configs is not None else {}
        node_id = os.getenv('NODE_ID', self.configs.get('node_id', None))
        if not node_id: raise Controller.MonitoringControllerException("The node id is not defined")
        os.environ['NODE_ID'] = node_id

    def instantiate_sensing_units(self):
        """
        This function instantiates the sensing units and initialize their parameters
        :return:
        """
        res = self.configs['sensing-units'] if 'sensing-units' in self.configs else {}
        for i in res:
            metric_collector_class = getattr(probes, i, None)
            if metric_collector_class:
                print("Sensing Unit %s is instantiating" % i)
                adaptivity = self.configs.get('adaptivity', {}).get('sensing')
                current_conf = self.configs['sensing-units'][i]
                current_conf['periodicity'] = time_to_seconds(current_conf['periodicity'])
                self.sensing_units[i] = metric_collector_class(**current_conf, adaptivity=adaptivity)

    def instantiate_dissemination_units(self):
        """
        It instantiates the dissemination channels and injects their configuration parameters
        :return:
        """
        res = self.configs['dissemination-units'] if 'dissemination-units' in self.configs else {}
        for i in res:
            extractor_class = getattr(exporters, i, None)
            if extractor_class:
                print("Dissemination Unit %s is instantiating" % i)
                adaptivity = self.configs.get('adaptivity', {}).get('dissemination')
                self.dissemination_units[i] = extractor_class(**self.configs['dissemination-units'][i], adaptivity=adaptivity)

    def start_sensing_units(self):
        """
        Starts, if it is necessary, the threads of the sensing units
        :return:
        """
        for i in self.sensing_units:
            print("Sensing Unit %s is starting" % i)
            self.sensing_units[i].activate()

    def start_dissemination_units(self):
        """
        Starts, if it is necessary, the dissemination channels connections e.g. starting Restful server, connection with kafka, etc
        :return:
        """
        for i in self.dissemination_units:
            print("Dissemination Unit %s is starting" % i)
            self.dissemination_units[i].activate()

    def start_control(self):  # TODO update it to encaptulate Queue
        """
        The main control loop of the monitoring system.
        In the loop, system captures one-by-one all metrics from metric collectors, combines them and
        disseminates them to all channels.
        :return:
        """
        running = True
        # adaptive_metric_val = ""
        while running:
            try:
                res = {}
                for i in self.sensing_units:
                    sensing_unit = self.sensing_units[i]
                    periodicity = self.periodicity_dict.get(i, 0)
                    periodicity -= 1
                    self.periodicity_dict[i] = periodicity
                    # target_name = sensing_unit.get_adaptivity_conf().get("target_name", "")
                    # metric = sensing_unit.get_metric_from_adaptivity_target_metric(
                    #     target_name)
                    sensing_unit.collect()
                    # is_skipped = True
                    if self.periodicity_dict[i] <= 0:
                        # is_skipped = False
                        self.periodicity_dict[i] = sensing_unit.periodicity
                        # adaptive_metric=sensing_unit.get_metric_from_adaptivity_target_metric(target_name)
                        # adaptive_metric_val = adaptive_metric.get_val() if adaptive_metric else ""
                        # sensing_unit.collect()
                        metrics = sensing_unit.get_metrics()
                        res.update({i: metrics})
                    # if metric:
                    #     with open(f'/data/{target_name}.csv', 'a') as f:
                    #         f.write(f'{metric.get_timestamp()},{metric.get_val()}, {adaptive_metric_val}, {is_skipped}\n')
                    # sensing_unit.update()  # TODO Add adaptiveness functionality to update
                for i in self.dissemination_units:
                    self.dissemination_units[i].update(res)
                periodicity = self.configs['sensing-units']['general-periodicity']
                time.sleep(time_to_seconds(periodicity))
            except Exception as ex:
                logging.error("Error at start_control",
                              exc_info=True)
                print(ex)
        exit(0)
