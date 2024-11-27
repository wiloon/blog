---
title: tp20 for can bus
author: "-"
date: 2017-08-14T04:01:11+00:00
url: /?p=11041
categories:
  - Inbox
tags:
  - reprint
---
## tp20 for can bus
VW Transport Protocol 2.0 (TP 2.0) for CAN bus

CAN allows for data packets with a payload of up to 8 bytes, to send messages longer than 8 bytes it is necessary to use a transport protocol. The OBD-II specification for example makes use of ISO-TP (ISO 15765-2). Volkswagen however uses it's own transport protocol in its vehicles, known as VW TP 2.0.

This page gives a run down on how TP 2.0 works. Please note that there is an older VW TP 1.6 which was used in some vehicles. TP 1.6 is fairly similar but some of the parameters are fixed. Its also worth noting that I have worked all of this out from various presentations and documents that I have found on the net and from logging data. I have not had any access to the official documentation from VW so take any information with a grain of salt.

Typically the payload of TP 2.0 will be ISO 14230-3, Keyword Protocol 2000 (KWP2000) application layer messages.

https://jazdw.net/tp20