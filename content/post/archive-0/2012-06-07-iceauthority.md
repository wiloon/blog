---
title: ICEAuthority
author: wiloon
type: post
date: 2012-06-06T23:33:26+00:00
url: /?p=3422
categories:
  - Linux

---
<http://serverfault.com/questions/119580/what-is-iceauthority-file-in-opensuse-11-2>

<a href="http://www.xfree86.org/current/ice.pdf" rel="nofollow">Here</a> is a good paper on what ICE is, and what it does.

Basically ICE is a inter process communication protocol, with authentication, protocol negotiation and potentially multiplexing built in.

It allows two X clients to talk directly to each other, for example, a video player program could potentially talk to a jukebox program to update each other.

As Richard Holloway says, the .ICEAuthority file is for authentication. It contains a number of random cookies. If two programs have the same cookie, then they&#8217;re allowed to talk to each other. In practice this either means that they&#8217;re reading the same .ICEAuthority file, or the cookies have been added.

In a lot of ways it&#8217;s similar to the xauth program & the .Xauthority file, except that .ICEAuthority is used for client to client, while .Xauthority is for client to server.