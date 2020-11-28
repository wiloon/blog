---
title: jquery attr
author: w1100n
type: post
date: 2013-06-06T04:12:46+00:00
url: /?p=5510
categories:
  - Web

---
    $('#WindowOpen').toggle(
        function()
        {
            $('#login_uname, #login_pass').attr("disabled","disabled");
        },
        function()
        {
            $('#login_uname, #login_pass').removeAttr("disabled");
        });