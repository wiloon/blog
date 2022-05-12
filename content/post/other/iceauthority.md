---
title: ICEAuthority
author: "-"
date: 2012-06-06T23:33:26+00:00
url: /?p=3422
categories:
  - Linux
tags:$
  - reprint
---
## ICEAuthority
<http://serverfault.com/questions/119580/what-is-iceauthority-file-in-opensuse-11-2>

Here is a good paper on what ICE is, and what it does.

Basically ICE is a inter process communication protocol, with authentication, protocol negotiation and potentially multiplexing built in.

It allows two X clients to talk directly to each other, for example, a video player program could potentially talk to a jukebox program to update each other.

As Richard Holloway says, the .ICEAuthority file is for authentication. It contains a number of random cookies. If two programs have the same cookie, then they're allowed to talk to each other. In practice this either means that they're reading the same .ICEAuthority file, or the cookies have been added.

In a lot of ways it's similar to the xauth program & the .Xauthority file, except that .ICEAuthority is used for client to client, while .Xauthority is for client to server.