'''
Created on June 03, 2020
@author: gioargyr
'''

class Datapoint:

    def __init__(self, timestamp, orig_value):
        self.ts = timestamp
        self.orig_val = orig_value
        self.id = None
        self.forec_val = None
        self.tag = None
        self.isFiltered = False


    def get_id(self):
        return self.id

    def get_timestamp(self):
        return self.ts

    def get_orig_val(self):
        return self.orig_val

    def get_forec_val(self):
        return self.forec_val

    def get_tag(self):
        return self.tag

    def get_isFiltered(self):
        return self.isFiltered

    def set_id(self, id):
        self.id = id

    def set_timestamp(self, timestamp):
        self.ts = timestamp

    def set_orig_val(self, orig_value):
        self.orig_val = orig_value

    def set_forec_val(self, forec_value):
        self.forec_val = forec_value

    def set_tag(self, tag):
        self.tag = tag

    def set_isFiltered(self, isFiltered):
        self.isFiltered = isFiltered

    def adam_printer(self):
        print(str(self.get_id()) + "\t"
              + str(self.get_timestamp()) + "\t"
              + str(self.get_orig_val()) + "\t"
              + str(self.get_forec_val()) + "\t"
              + self.get_tag() + "\t"
              + str(self.get_isFiltered()))


    def adam_write_out(self):
        datapoint_str = str(self.get_id()) + "\t" \
                        + str(self.get_timestamp()) + "\t"\
                        + str(self.get_orig_val()) + "\t"\
                        + str(self.get_forec_val()) + "\t"\
                        + self.get_tag() + "\t"\
                        + str(self.get_isFiltered())
        return datapoint_str


"""
    public void printDatapoint()
    if (this.forecVal == -1000.0)
    System.out.println(this.id + "\t" + this.ts  + "\t" + this.origVal + "\t" + this.forecVal + "\t" + this.isExpected + "\t" + "TRAIN" + "\t" + this.origVal + "\t\t\t" + this.origVal)
    else if (this.isExpected == false)
    System.out.println(this.id + "\t" + this.ts  + "\t" + this.origVal + "\t" + this.forecVal + "\t" + this.isExpected + "\t" + "UNEXP" + "\t\t" + this.origVal + "\t\t" + this.origVal);
    else
    System.out.println(this.id + "\t" + this.ts  + "\t" + this.origVal + "\t" + this.forecVal + "\t" + this.isExpected + "\t" + "FOREC" + "\t\t\t" + this.forecVal + "\t" + this.forecVal)
"""