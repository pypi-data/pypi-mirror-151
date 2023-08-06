'''
Created on May 19, 2020
@author: gioargyr
'''


class Sample(object):

    def __init__(self, timestamp, value, readable_string=""):
        self.t = timestamp
        self.v = value
        self.r = readable_string

    """
    Returns the timestamp of the Sample
    """
    def get_timestamp(self):
        return self.t

    """
    Returns the value of the Sample
    """
    def get_value(self):
        return self.v

    """
    Returns the readable_string of the Sample
    """
    def get_readable_string(self):
        return self.r

    """
    Sets the timestamp of the Sample
    """
    def set_timestamp(self, timestamp):
        self.t = timestamp

    """
    Sets the value of the Sample
    """
    def set_value(self, value):
        self.v = value

    """
    Prints the Sample in a meaningfull way
    """
    def print_Sample(self, ):
        print(str(self.t) + "\t" + str(self.v) + "\t\t" + str(self.r))


