---
title: Triggering a hudson build to run when git is updated
author: wiloon
type: post
date: 2011-09-27T14:37:51+00:00
url: /?p=941
bot_views:
  - 9
views:
  - 2
categories:
  - CI
tags:
  - Git

---
http://www.danstraw.com/triggering-a-hudson-build-to-run-when-git-is-updated/2010/11/23/
  
&#8212;
  
Hudson CI lets you configure a build so that it periodically polls git to check whether anything’s changed. This is something of a waste of time & resources – it’s polling git when nothing has changed and there may be a lag between when you check something in and when it builds.

Below are instructions on how to get git to trigger the build once it has had changes pushed to it. I’m assuming here that you have:

A central git repository on server A
  
A hudson server set up on server B (which may, or may not, be the same server as server A)
  
Note that it is simplest if you have set hudson up on the same server as git as per these instructions as then we can trigger the build via a call to localhost without going over the network, and you can keep port 8081 closed on your server.

On the git server, in the git repository, you should edit the post-receive hook which contains the following text:
  
(maybe you only have a file named post-receive.sample, rename it!!)
  
emacs /path/to/your/git/repository.git/hooks/post-receive
  
With the following lines:

#e.g. the URL of you hudson is :
  
#http://localhost:8080/hudson/job/xxx/
  
#xxx is your job name
  
URL=&#8217;http://localhost:8080/hudson/job/xxx/build&#8217;

echo "Run Hudson build at $URL&#8221;
  
wget $URL > /dev/null 2>&1

Finally, you will need to make the hook executable by whoever will be checking code in. As an example, assuming that the git repository is owned by a user called “git”, and a user called “userA” will be checking in via their own ssh account, you should:

sudo usermod -G git userA
  
If they’re not already a member of the “git” group, and then

chmod ug+x /path/to/your/git/repository.git/hooks/post-receive
  
To make the hook executable by the git group.