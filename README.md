# Introduction

Have fun, always! This project was created based on the *Third Ideal* from *The Unicorn Project*, *Improvement of Daily Work*

I had a lot of fun creating this (Unicorn Project, Second Ideal: *Focus, Flow and Joy*), please use it for your convenience, positive feedback is appreciated and if you see or make improvements then pull requests are welcomed.

Since we experience regular ssh latency problems in our office location and use ping() to test for this problem
the idea was to create a simple raspberry pi solution to measure latency towards a configured
ip-address and show result on a *pomoroni blinkt* led-strip. A nice side-project that can easily
get out-of-hand :-)

The result of this is called wan-pinger

In it's current state it's quite flexible and functional and has some nice features, at the very least:

* it confirms visually what you already experience, you're wan connection sucks and terminal sessions will not work
* watching the wan-pinger is soothing your wait for getting back to normal
* the led-strip shows a history of results, just like an ECG (floating result)
* it uses sensible defaults
* it can be configured using a config.yaml in the working directory
* it contains a sample init.d script to enable running on boot (nice for raspberry pi W)
* documentation is not too bad and pull requests are welcomed
* a sample config.yaml is provided
* it is open-source and you are allowed to adapt it in any way you like but I would like to hear what you did :-)

## configuration

By default the script pings *www.google.com* each second, if latency is below 25 ms it is determined fine (green) and above 60 ms it is bad (red). Between minimum and maximum a scale between green and red on a hue scale is used with 80 discrete values. A lot of parameters can be customized in a config.yaml. A test mode is available, as is a debug mode.

These are the parameters:

```
ip:              ip-address or hostname, see ping command
min_latency:     minimum latency in ms, below min_latency is green
max_latency:     max_latency in ms, above max_latency is red
number_of_times: how often should we test, -1 is forever
dim:             brightness of led after signal
light:           brightness of led for actual result
LR:              direction of led-strip, True - left-to-right, False is right-to-left
pause:           time between ping tests
debug:           debug level, extra output statements for testing
```

## Startup script

`wanpinger` is the sample init.d script to start this pinger on boot. The script is based on the following article that also describes how to install:

* https://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html

the script supports `start` and `stop` command.

## installation

since this is a python program it has a few dependency's:

* The blinkt led-strip requires specific modules, google for [*pimoroni blinkt*](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-blinkt) to find out more, this will also check the python and pip installation that's necessary.
* There is a `requirements.txt`, so running a `sudo pip install -r requirements.txt` is enough


## usage

there are different ways to start the wan-pinger, the best way is to make it part of the boot process itself. other then that you can start it interactively or in the background.

**Interactive**

Just run: `python pinger.py`

**Background**

There is a nohup script present, just run: `run_pinger.sh`

There is also a kill script, this requires presence of `pkill`, just run: `kill_pinger.sh`

**Test mode**

Test mode will simulate ping latency on a scale from 1 till 120 ms and show the color-scale with minimum pause of 0.1 second. This gives a nice overview and makes sure your setup works (dependencies, python, blint). Just run `python pinger.py test`

**Debug mode**

If you doubt how it works configuring debug mode gives more output of what happens. Just configure `debug: True` in the `config.yaml`.

## Final notes

This is my first git repo that I see as true Open Source, so please be easy on me!
