import os
import sys
import signal
import datetime
import time
import colorsys
import yaml
from blinkt import set_brightness, set_pixel, show, clear

class Config(object):
    '''
    global configuration parameters
    '''

    def __init__(self):
        object.__init__(self)

        # set reasonable defaults
        self.ip = "www.google.com"
        self.min_latency = 25
        self.max_latency = 60
        self.number_of_times = -1
        self.timeout = 1200
        self.dim = 0.04
        self.light = 0.08
        self.LR = False
        self.pause = 1

        # try if config.yaml is present (autoload)
        configfile = "config.yaml"
        if os.path.exists(configfile):
            print "reading config.yaml"
            fh = open(configfile)
            yd = yaml.safe_load(fh)
            # print "yamlfile", yd
            # use only values that are present
            if 'ip' in yd: self.ip = yd['ip']
            if 'min_latency' in yd: self.min_latency = yd['min_latency']
            if 'max_latency' in yd: self.max_latency = yd['max_latency']
            if 'number_of_times' in yd: self.number_of_times = yd['number_of_times']
            if 'timeout' in yd: self.timeout = yd['timeout']
            if 'dim' in yd: self.dim = yd['dim']
            if 'light' in yd: self.light = yd['light']
            if 'LR' in yd: self.LR = yd['LR']
            if 'pause' in yd: self.pause = yd['pause']
            fh.close()
        else:
            print "config.yaml not found, using defaults"

    def test(self):
        self.min_latency = 1
        self.max_latency = 80
        self.number_of_times = 80
        self.pause = 0.1


class Pinger(object):
    def __init__(self):
        object.__init__(self)

        self.latency = ShowLatency()
        
    def run_scale(self):
        for i in range(121):
                latency = int(float(i))
                self.latency.show(latency)
             
    def run_test(self):
        i = 0
        # Iterating the given number of times
        while (i < config.number_of_times) | (config.number_of_times == -1):
            if config.number_of_times > -1:
                i += 1

            if config.ip == "test":
                #print "ms: ", i
                self.latency.show(float(i))
            else:
                cmd = 'timeout 1 ping -c 1 ' + config.ip
                # forming command
                data = os.popen(cmd).read()
                # reading data return by popen
                # Displaying results
                if 'time=' in data and 'ms' in data:
                    ms = data.split('time=')[1].split(' ms')[0]
                    # print datetime.datetime.now().strftime("%H:%M:%S"), ms
                    latency = float(ms)
                    self.latency.show(latency)
                else:
                    # print datetime.datetime.now().strftime("%H:%M:%S"), -1
                    self.latency.show(config.max_latency)
             
class ShowLatency(object):
    blinkt = __import__('blinkt')

    def __init__(self):

        object.__init__(self)

        self.bit = 0 if config.LR else 7
        ShowLatency.blinkt.set_clear_on_exit(True)

    def makeColor(self, latency):
        # use the hue system to create a nice colorscale
        # assumption is that latency above a certain value
        # is just plain bad. Below that it is normalized
        # to the hue scale of 360.0 degrees
        #
        # 0 is red, 80 - 120 is almost the same green, so start at 80
        #
        # everything below config.min_latency  ms is assumed to be great, so is green
        #
        # print "latency: ", latency
        latency = latency if latency <= config.max_latency else config.max_latency
        if latency <= config.min_latency:
            level = 1.0
        else:
            level = 1.0 - ((latency) / (config.max_latency))
        hue = (level * 80.0) / 360.0
        # print "latency: ", latency, " max_latency: ", config.max_latency, " level: ", level, " hue: ", hue
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
        return r, g, b


    def show(self, latency = 0):
        # from blinkt import set_brightness, set_pixel, show, clear set_clear_on_exit

        r, g, b = self.makeColor(latency)
        set_pixel(self.bit, r, g, b, config.light)
        show()
        time.sleep(config.pause)
        set_pixel(self.bit, r, g, b, config.dim)
        show()
        if config.LR:
            self.bit = self.bit + 1 if self.bit < 7 else 0
        else:
            self.bit = self.bit - 1 if self.bit > 0 else 7

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    # quit
    print "signal received, quitting pinger.py"
    clear()
    show()
    sys.exit(0)

# globals
config = Config()

# setup interrupt handler
signal.signal(signal.SIGTERM, sigterm_handler)

# main program
try:
    if __name__ == '__main__':
    
        nargs = len(sys.argv)
        if nargs > 2:
            print "usage: python pinger.py [<ip> | test]"
            print "  or use config.yaml to do full config"
            sys.exit(1)
        # Taking the args from command line
        if nargs == 2:
            ip = sys.argv[1]
            if ip == "test": config.ip = "test"

        pinger = Pinger()
        if config.ip == "test":
            config.test()

        print "config: ", vars(config)
        pinger.run_test()

except KeyboardInterrupt:
    # quit
    clear()
    show()
    sys.exit()

