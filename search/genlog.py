# -*- coding: UTF-8 -*-

import syslog

syslog.openlog("test1.py")
for i in range(0, 100000):
    syslog.syslog(syslog.LOG_ERR, "The process is test1.py %d" % i)

