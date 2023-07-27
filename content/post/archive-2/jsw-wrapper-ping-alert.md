---
title: jsw wrapper.ping.alert
author: "-"
date: 2016-10-19T05:19:05+00:00
url: /?p=9314
categories:
  - Inbox
tags:
  - reprint
---
## placeholder

https://wrapper.tanukisoftware.com/doc/english/prop-ping-alert-x.html

The Wrapper uses a ping system as one of its methods of monitoring the JVM. The Wrapper will send a ping to the JVM and then wait for a ping response. If a response has not been received for more than the time configured in wrapper.ping.timeoutproperty, then the Wrapper will decide that the JVM is frozen and forcibly kill and restart it.

The ping system is fairly reliable, but in some cases when there is heavy disk swapping or another process is hogging resources, the Wrapper can potentially decide that the JVM is frozen when it is simply stuck temporarily. Obviously this is a bad thing as regardless of the cause, the JVM is not in a state where it can reply to requests. But it may be preferable to wait a bit longer rather than restarting the JVM in this case.

If you simply extend the length of the wrapper.ping.timeout property to a large value, false restarts will become much less likely, but at the same time, the Wrapper will also become much less responsive to actual freezes. But you have no idea how common the slow ping responses are or how much extra leeway you have given yourself.