---
title: application start script
author: "-"
date: 2019-10-21T02:56:24+00:00
url: /?p=15026
categories:
  - Inbox
tags:
  - reprint
---
## application start script
```bash
#! /usr/bin/env bash

APP_HOME=/data/server/app0
APP_NAME=app0
PID_FILE=/var/run/app0.pid

startApp(){
    cd ${APP_HOME}
    nohup java -jar ${APP_NAME}.jar > log 2>&1 &
    echo $! > ${PID_FILE};
}

stopApp(){
    kill `cat ${PID_FILE}`
}

case $1 in
    start)
        startApp
        ;;
    stop)
        stopApp
        ;;
    restart)
        stopApp
        startApp
        ;;
    *)
        echo "usage: wrapper {start|stop|restart}" ;;
esac
exit 0
```