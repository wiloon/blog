---
title: respberry pi error
author: "-"
date: 2015-05-04T03:56:10+00:00
url: respberry-pi-error
categories:
  - Inbox
tags:
  - Raspberry Pi

aliases:
  - /p7599/
---
## respberry pi error
omxplayer.bin: SubtitleRenderer.cpp:154: SubtitleRenderer::load_glyph(SubtitleRenderer::InternalChar)::<lambda(FT_Face, VGFont, bool)>: Assertion \`!vgGetError()' failed.
  
/usr/bin/omxplayer: line 67: 5199 Aborted LD_LIBRARY_PATH="$OMXPLAYER_LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" $OMXPLAYER_BIN "$@"


run raspi-config and up the gpu mem to 128

https://www.raspberrypi.org/forums/viewtopic.php?f=35&t=19979&start=25