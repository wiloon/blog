---
title: debian 7 xfce
author: wiloon
type: post
date: 2013-11-09T07:49:56+00:00
url: /?p=5916
categories:
  - Uncategorized

---
<http://www.binarytides.com/install-xfce-desktop-on-debian-7-wheezy/>

Xfce is a lightweight desktop environment system for linux, and is a good alternative to the complex and clumsy gnome.

In this post I am going to show you how to install xfce on debian. It is available in the debian default repositories and can be installed right away.

\# apt-get install xfce4

This will install the xfce desktop with all the necessary applications. The download size is around 20.4 MB and should finish in a few minutes on a fast broadband connection.

Along with the main xfce4 package you can also install additional useful applications by installing the package named xfce4-goodies.

\# sudo apt-get install xfce4-goodies

If you want to install all the application of the xfce desktop suite then use the following command instead

\# apt-get install xfce4-*

It will install a lot more applications. The download size is around 99MB and would take more time to complete.

So choose the right one for your needs.

Customise Xfce

After installing the XFCE desktop, you would want to customise the look and feel of it, to make it better. The default looks of any desktop are nothing great as such.

Get better themes

I personally find the greybird and bluebird themes to be great looking when it comes to xfce and lxde. On ubuntu they are present in the default repositories. However on debian we have to add the ubuntu ppa repository to get them.

Its easy, just run the following commands

\# add-apt-repository &#8216;deb http://ppa.launchpad.net/shimmerproject/ppa/ubuntu quantal main&#8217;

\# apt-get update

\# aptitude search shimmer

p shimmer-themes-greybird &#8211; Greybird Theme from the Shimmer Project

\# apt-get install shimmer-themes-greybird

Now go to

Applications Menu > Settings > Appearance

And from the style tab, select greybird theme.

Also switch to a better font like Droid Sans. Enable anti aliasing with full hinting and RGB subpixel order. Now that should make your fonts look a great deal better.