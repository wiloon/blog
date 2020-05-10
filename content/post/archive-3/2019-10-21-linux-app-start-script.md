---
title: application start script
author: wiloon
type: post
date: 2019-10-21T02:56:24+00:00
url: /?p=15026
categories:
  - Uncategorized

---
<pre><code class="language-bash line-numbers">#! /usr/bin/env bash

APP_HOME=/data/server/app0
APP_NAME=app0
PID_FILE=/var/run/app0.pid

startApp(){
    cd ${APP_HOME}
    nohup java -jar ${APP_NAME}.jar &gt; log 2&gt;&1 &
    echo $! &gt; ${PID_FILE};
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
</code></pre>