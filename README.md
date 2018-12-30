# raspi-test

Some few test example for rasberry pi model 3 B+

## gpio-monitor

gpio-monitor will monitor GPIO state. We will need to initialize GPIO function before monitoring. All code are ready
for multiple GPIO monitoring but I have a weird issue with waiting_for_edge during runtime

```
Exception in thread Thread-1:                                                                                                                                                                                                                 
Traceback (most recent call last):                                                                                                                                                                                                            
  File "/usr/lib/python3.5/threading.py", line 914, in _bootstrap_inner                                                                                                                                                                       
    self.run()                                                                                                                                                                                                                                
  File "/home/pi/raspi-test/examples/gpio_monitor/cli/display.py", line 36, in run                                                                                                                                                            
    value = self.gpio.monitor()                                                                                                                                                                                                               
  File "/home/pi/raspi-test/examples/gpio_monitor/gpio.py", line 31, in monitor                                                                                                                                                               
    GPIO.wait_for_edge(self.channel, GPIO.BOTH)                                                                                                                                                                                               
RuntimeError: Error waiting for edge
```
