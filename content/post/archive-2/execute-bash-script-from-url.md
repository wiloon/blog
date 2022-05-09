---
title: Execute bash script from URL
author: "-"
date: 2018-09-24T12:19:45+00:00
url: /?p=12677
categories:
  - Inbox
tags:
  - reprint
---
## Execute bash script from URL
```bash
  
bash <(curl -s http://mywebsite.com/myscript.txt)
  
curl -s https://myurl.com/script.sh | bash /dev/stdin param1 param2
  
```

Directly run bash scripts in Github Gists locally in Terminal.

Get the raw version of it and copy the link. Now we are going to curl that link to get the content in the file and then pass that content to bash.
  
https://stackoverflow.com/questions/5735666/execute-bash-script-from-url