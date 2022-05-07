---
title: linux run-parts
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=11086
categories:
  - Inbox
tags:
  - reprint
---
## linux run-parts
https://superuser.com/questions/402781/what-is-run-parts-in-etc-crontab-and-how-do-i-use-it
  
http://manpages.ubuntu.com/manpages/zesty/en/man8/run-parts.8.html

Basically, run-parts(8) takes a directory as an argument.

It will run every script that is found in this directory. For example, if you do a listing of /etc/cron.hourly, you'll see that it's a directory where you can put executable files to be run every hour.

As you can see, in cron it's used for convenience, since you only have to specify one directory and everything in that directory will be executed. This makes it easy to maintain scripts in one of the etc/cron* directories.

See its manpage for more options that could be exploited for your own use cases. You could for example do a simple check and show which scripts would be run:

run-parts -v –-test /etc/cron.hourly
  
The -v flag might not be available everywhere.