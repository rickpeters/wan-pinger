import os
import sys
import signal
import datetime
import time
import colorsys
from blinkt import set_brightness, set_pixel, show, clear

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    # print('booyah! bye bye')
    # quit
    clear()
    show()
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

class Pinger(object):
    def __init__(self, ip, timeout=1200, max_latency=40):
        object.__init__(self)

        self.ip = ip
        self.latency = ShowLatency(max_latency)
        
    def run_scale(self):
        for i in range(121):
                latency = int(float(i))
                self.latency.show(latency)
             
    def run_test(self, number_of_times=100):
        i = 0
        while (i < number_of_times) | (number_of_times == -1):
            if number_of_times > -1:
                i += 1

            # Iterating the given number of times
            cmd = 'timeout 1 ping -c 1 ' + self.ip
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
                self.latency.show(self.latency.max_latency)
             
class ShowLatency(object):
    blinkt = __import__('blinkt')

    def __init__(self, max_latency = 40.0):

        object.__init__(self)

        self.bit = 0
        self.max_latency = max_latency if max_latency > 26.0 else 26.0
        ShowLatency.blinkt.set_clear_on_exit(True)

    def makeColor(self, latency):
        # use the hue system to create a nice colorscale
        # assumption is that latency above a certain value
        # is just plain bad. Below that it is normalized
        # to the hue scale of 360.0 degrees
        #
        # 0 is red, 120 is green
        #
        # everything below 25 ms is assumed to be great, so is green
        #
        latency = latency if latency <= self.max_latency else self.max_latency
        if latency <= 25.0:
            level = 1.0
        else:
            level = 1.0 - ((latency) / (max_latency))
        hue = (level * 120.0) / 360.0
        # print "latency: ", latency, " max_latency: ", self.max_latency, " level: ", level, " hue: ", hue
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
        return r, g, b


    def show(self, latency = 0):
        # from blinkt import set_brightness, set_pixel, show, clear set_clear_on_exit

        r, g, b = self.makeColor(latency)
        # print "r: ", r, " g: ", g, " b: ", b
        # 0.08 is a good value for low-light environments
        set_pixel(self.bit, r, g, b, 0.25)
        show()
        time.sleep(1.0)
        set_pixel(self.bit, r, g, b, 0.04)
        show()
        self.bit = self.bit + 1 if self.bit < 7 else 0

try:
    if __name__ == '__main__':
        import sys
    
        if len(sys.argv) < 2:
            print "usage: python pinger.py <ip> [n_sample=-1] [timeout=1200] [max_latency=40]"
            sys.exit(1)
    
        # Taking the args from command line
        nargs = len(sys.argv)
        host = sys.argv[1]

        if nargs > 2:
            number_of_times = int(sys.argv[2])
        else:
            number_of_times = -1
        timeout = int(sys.argv[3]) if nargs > 3 else 1200
        max_latency = float(sys.argv[4]) if nargs > 4 else 60.0
    
        pinger = Pinger(host, timeout, max_latency)
        pinger.run_test(number_of_times)
        #pinger.run_scale()

except KeyboardInterrupt:
    # quit
    clear()
    show()
    sys.exit()
