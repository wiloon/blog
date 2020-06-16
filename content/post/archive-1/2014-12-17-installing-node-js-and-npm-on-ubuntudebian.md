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
      
    
  


<div class="row">
  <div class="col-sm-12">
    <div class="post">
      <div class="body">
        
          This is just short snippet on how to install Node.js (any version) and <span class="caps">NPM</span> (Node Package Manager) on your Ubuntu/Debian system.
        
        
        
          Step 1 - Update your system
        
        
        <pre class="plaincode">sudo apt-get update
sudo apt-get install git-core curl build-essential openssl libssl-dev

        
        
          Step 2 - Install Node.js
        
        
        
          First, clone the Node.js repository:
        
        
        <pre class="plaincode">git clone https://github.com/joyent/node.git
cd node

        
        
          Now, if you require a specific version of Node:
        
        
        <pre class="plaincode">git tag # Gives you a list of released versions
git checkout v0.4.12

        
        
          Then compile and install Node like this:
        
        
        <pre class="plaincode">./configure
make
sudo make install

        
        
          Then, check if node was installed correctly:
        
        
        <pre class="plaincode">node -v

        
        
          Step 3 - Install <span class="caps">NPM</span>
        
        
        
          Simply run the <span class="caps">NPM</span> install script:
        
        
        <pre class="plaincode">curl https://npmjs.org/install.sh | sudo sh

        
        
          And then check it works:
        
        
        <pre class="plaincode">npm -v

        
        
          That's all.
        
        
        
          
        
        
        
          https://ariejan.net/2011/10/24/installing-node-js-and-npm-on-ubuntu-debian/
        
      
    
  
