---
title: 'chromeos linux,  crostini'
author: wiloon
type: post
date: 2018-05-11T16:49:21+00:00
url: /?p=12236
categories:
  - Uncategorized

---
```bash
  
vmc start dev
  
run\_container.sh -container\_name=stretch -user=wiloon -shell
  
```

switch to dev channel, chrome os version >=67
  
chrome os will start to download an update
  
update and restart

Launch crosh (ctrl-alt-t)
  
Create crostini VM vmc start dev. This'll download the termina component, and open a shell.
  
Launch a container run\_container.sh -container\_name=stretch -user=wiloon -shell

<https://www.youtube.com/watch?v=s9mrR2tqVbQ>

<blockquote class="reddit-card" >
  
    <a href="https://www.reddit.com/r/Crostini/comments/89q1cu/crostini_101/?ref_source=embed&ref=share">Crostini 101</a> from <a href="https://www.reddit.com/r/Crostini/">Crostini</a>
  
</blockquote>

  
https://github.com/lstoll/cros-crostini/blob/master/README.md
  
https://support.google.com/chromebook/answer/1086915?hl=en