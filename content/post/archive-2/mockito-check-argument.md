---
title: mockito check argument
author: "-"
date: 2016-11-25T02:11:30+00:00
url: /?p=9435
categories:
  - Inbox
tags:
  - reprint
---
## mockito check argument
```bash

Channel channel = Mockito.mock(XxxClass.class);
  
Mockito.when(channel.writeAndFlush((XxxClass) Mockito.argThat(new ArgMatcher()))).
  
thenReturn((ChannelFuture) anyObject());

private class ArgMatcher extends ArgumentMatcher {
  
@Override
  
public boolean matches(Object o) {
  
String arg = o.toString();
  
Assert.xxx

return true;
  
}
  
}

```