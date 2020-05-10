---
title: install gitolite
author: wiloon
type: post
date: 2011-08-19T00:19:59+00:00
url: /?p=445
bot_views:
  - 4
categories:
  - Linux
tags:
  - Git

---
<http://davedevelopment.co.uk/2010/12/05/how-to-install-gitolite-on-ubuntu-10-10-maverick-meerkat.html>

At work we recently switched from subversion to Git for our version control. I wont go into it too much, but the main reasons where:

<div id="post">
  <ul>
    <li>
      We wanted a distributed system, for the flexibility it offers individuals
    </li>
    <li>
      We wanted the enhanced branch/merge
    </li>
    <li>
      Just for fun really, broaden our horizons
    </li>
  </ul>
  
  <p>
    Anyway, I love GitHub, but it’s not the answer to everything! I wanted a central repository that I could control, so having had a brief glimpse at Gitorious and gitosis, I settled on gitolite. Now, I’m usually quite a lazy sys admin, and unless I desperately need a feature in the latest version of an application, I’m usually happy to fall back on the my chosen package manager, in this caseUbuntu’s APT. Gitolite got a package as of version 10.10 Maverick Meerkat, so I told our local Ubuntu mirror to download all the 10.10 packages and after that, upgraded the server I had in mind so that I could use the gitolite package.
  </p>
  
  <h4>
    Install Gitolite
  </h4>
  
  <p>
    Nice and easy this part, on the server:
  </p>
  
  <pre>server&gt; sudo apt-get update
server&gt; sudo apt-get install gitolite</pre>
  
  <h4>
    Creating a Public/Private key pair
  </h4>
  
  <p>
    If you already have one, send the public halve over to the server and skip this part. Otherwise, take a look at ssh key based authentication, then create your key pair on your client machine:
  </p>
  
  <pre>client&gt; ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/davem/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/davem/.ssh/id_rsa.
Your public key has been saved in /home/davem/.ssh/id_rsa.pub.
The key fingerprint is:
61:bf:f5:2d:f6:ed:cd:10:b7:0c:be:5d:4d:8f:a3:0d davem@client
The key's randomart image is:
+--[ RSA 2048]----+
|                 |
|                 |
|        o        |
|       . o       |
|        S . ... o|
|           o..o*+|
|          . E.Bo=|
|             =o*+|
|            ...o*|
+-----------------+</pre>
  
  <p>
    Once created, send the public halve to the gitolite server. Be sure to use the name you provided when creating the key. In this example, I’ve called the key davem.pub on the target machine, so I can differentiate between myself and other developers.
  </p>
  
  <pre>client&gt; scp ~/.ssh/id_rsa.pub server:davem.pub</pre>
  
  <h4>
    Configure gitolite
  </h4>
  
  <p>
    On the server, copy the public halve to a convenient location and run the gl-setup tool.
  </p>
  
  <pre>server&gt; mv davem.pub /tmp/davem.pub
server&gt; chmod 666 /tmp/davem.pub
server&gt; sudo su gitolite
server&gt; gl-setup /tmp/davem.pub
...</pre>
  
  <p>
    That’s gitolite setup, we now need to go back to the client machine to fully configure it. First edit your <tt>.ssh/config</tt> file, so that ssh knows how to connect to the server. Again, be careful to use the correct name for your key pair:
  </p>
  
  <pre>Host servername
IdentityFile ~/.ssh/id_rsa</pre>
  
  <p>
    Now we can clone the git repository that is used to configure gitolite:
  </p>
  
  <pre>client&gt; git clone gitolite@server:gitolite-admin
Initialized empty Git repository in /home/davem/gitolite-admin/.git/
remote: Counting objects: 6, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 6 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (6/6), done.
client&gt; cd gitolite-admin</pre>
  
  <h4>
    Adding repositories
  </h4>
  
  <p>
    The gitolite admin contains two folders. The first, <tt>conf</tt> contains a single config file. Open that and create a new repository by adding:
  </p>
  
  <pre>        repo    mytest
                  RW+     =   @all</pre>
  
  <p>
    You then need to commit the changes and push them to the gitolite server:
  </p>
  
  <pre>client&gt; git commit -m "Added mytest repo" conf/gitolite.conf
client&gt; git push</pre>
  
  <p>
    We then should be able to clone our new repository:
  </p>
  
  <pre>client&gt; git clone gitolite@server:mytest</pre>
  
  <h4>
    Adding users
  </h4>
  
  <p>
    To add a new user, simply add their public key halve to your clone of the <tt>gitolite-admin</tt> repo, add, commit and push.
  </p>
  
  <pre>client&gt; cd gitolite-admin
client&gt; cp ~/Downloads/another.pub keydir/
client&gt; git add keydir/another.pub
client&gt; git commit -m "Added another as a user" keydir/another.pub
client&gt; git push</pre>
  
  <p>
    I wont go any further than that, you can configure fine grain access control and other things in the<tt>conf/gitolite.conf</tt> file, check out the documentation. Hope it’s been helpful, comments (especially corrections) are appreciated.
  </p>
  
  <p>
    #push
  </p>
  
  <p>
    git push origin master
  </p>
</div>