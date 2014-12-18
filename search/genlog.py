# -*- coding: UTF-8 -*-

import syslog

syslog.openlog("test.py")
for i in range(0,10000):
    syslog.syslog(syslog.LOG_ERR, "The process is test.py %d" % i)

