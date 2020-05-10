---
title: Installing Node.js and NPM on Ubuntu/Debian
author: wiloon
type: post
date: 2014-12-17T12:22:35+00:00
url: /?p=7117
categories:
  - Uncategorized
tags:
  - Node.js

---
<div class="row">
  <div class="col-sm-12">
    <div class="post">
      <h1 class="title">
      </h1>
      
      <p class="meta">
        Monday 24 October 2011
      </p>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-sm-12">
    <div class="post">
      <div class="body">
        <p>
          This is just short snippet on how to install Node.js (any version) and <span class="caps">NPM</span> (Node Package Manager) on your Ubuntu/Debian system.
        </p>
        
        <p>
          <strong>Step 1 &#8211; Update your system</strong>
        </p>
        
        <pre class="plaincode">sudo apt-get update
sudo apt-get install git-core curl build-essential openssl libssl-dev
</pre>
        
        <p>
          <strong>Step 2 &#8211; Install Node.js</strong>
        </p>
        
        <p>
          First, clone the Node.js repository:
        </p>
        
        <pre class="plaincode">git clone https://github.com/joyent/node.git
cd node
</pre>
        
        <p>
          Now, if you require a specific version of Node:
        </p>
        
        <pre class="plaincode">git tag # Gives you a list of released versions
git checkout v0.4.12
</pre>
        
        <p>
          Then compile and install Node like this:
        </p>
        
        <pre class="plaincode">./configure
make
sudo make install
</pre>
        
        <p>
          Then, check if node was installed correctly:
        </p>
        
        <pre class="plaincode">node -v
</pre>
        
        <p>
          <strong>Step 3 &#8211; Install <span class="caps">NPM</span></strong>
        </p>
        
        <p>
          Simply run the <span class="caps">NPM</span> install script:
        </p>
        
        <pre class="plaincode">curl https://npmjs.org/install.sh | sudo sh
</pre>
        
        <p>
          And then check it works:
        </p>
        
        <pre class="plaincode">npm -v
</pre>
        
        <p>
          That’s all.
        </p>
        
        <p>
          &nbsp;
        </p>
        
        <p>
          https://ariejan.net/2011/10/24/installing-node-js-and-npm-on-ubuntu-debian/
        </p>
      </div>
    </div>
  </div>
</div>