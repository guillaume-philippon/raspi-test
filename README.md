# raspi-test

Some few test example for rasberry pi model 3 B+

## gpio-monitor

gpio-monitor will monitor GPIO state. If you want to monitor your pin,
you need to start gpio-monitor before the real code as gpio-monitor need
the pin to be in GPIO.IN mode which can crash your code.

To install gpio_monitor
```
pi@raspi:~ $ mkdir -p ~/.venv/gpio-monitor
pi@raspi:~ $ python3 -m venv ~/.venv/gpio-monitor
pi@raspi:~ $ source ~/.venv/gpio-monitor/bin/activate
(gpio-monitor) pi@raspi:~ $ pip install -r requirements.txt
```

To launch gpio-monitor
```
(gpio-monitor) pi@raspi:~ $./gpio-monitor channel1 channel2 ...
(gpio-monitor) pi@raspi:~ $./gpio-monitor -h
```