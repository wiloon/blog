---
title: respberry pi error
author: wiloon
type: post
date: 2015-05-04T03:56:10+00:00
url: /?p=7599
categories:
  - Uncategorized
tags:
  - Raspberry Pi

---
omxplayer.bin: SubtitleRenderer.cpp:154: SubtitleRenderer::load\_glyph(SubtitleRenderer::InternalChar)::<lambda(FT\_Face, VGFont, bool)>: Assertion \`!vgGetError()' failed.
  
/usr/bin/omxplayer: line 67: 5199 Aborted LD\_LIBRARY\_PATH="$OMXPLAYER\_LIBS${LD\_LIBRARY\_PATH:+:$LD\_LIBRARY\_PATH}" $OMXPLAYER\_BIN "$@"


run raspi-config and up the gpu mem to 128

https://www.raspberrypi.org/forums/viewtopic.php?f=35&t=19979&start=25