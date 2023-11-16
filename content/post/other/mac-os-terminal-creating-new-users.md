---
title: 'mac os terminal,  Creating New Users'
author: "-"
date: 2015-02-06T03:53:00+00:00
url: /?p=7330
categories:
  - Inbox
tags:
  - Mac OS

---
## 'mac os terminal,  Creating New Users'

[http://www.maclife.com/article/columns/terminal_101_creating_new_users](http://www.maclife.com/article/columns/terminal_101_creating_new_users)

Every Monday, we'll show you how to do something new and simple with Apple's built-in command line application. You don't need any fancy software, or a knowledge of coding to do any of these. All you need is a keyboard to type 'em out!

Adding users through the GUI in OS X is an easy process, but sometimes, you may just need to quickly create an SSH user, or a user that is allowed to SFTP or FTP into the system. You can easily create a stripped-down account in OS X using the dscl command, and we'll show you how in this week's Terminal 101. Continue reading to learn all about creating new users through the Terminal.

In order to create a complete user, we'll type the following commands one-at-a-time into the Terminal. These commands need to be run as either the root user or with the "sudo" prefix.

First, we'll create a new entry for the user under /Users:

dscl . create /Users/corybohon
  
Next, we'll create and set the shell property to bash:

dscl . create /Users/corybohon UserShell /bin/bash
  
Next, we'll add some user credentials, and set the user's full name:

dscl . create /Users/corybohon RealName "Cory Bohon"
  
Now, we'll create and set a unique ID for the user. Pick whatever works for you here, ensuring that it hasn't been used by previous users:

dscl . create /Users/corybohon UniqueID 503
  
Next, we'll create and set the user's group ID property:

dscl . create /Users/corybohon PrimaryGroupID 1000
  
Now, we'll set the user's home directory by running the following command. Ensure that you replace both instances of the shortname in the command below:

dscl . create /Users/corybohon NFSHomeDirectory /Local/Users/corybohon
  
Now we'll add some security to the user account and set their password. Here, you'll replace "PASSWORD" with the actual password that will be used initially for their account. The user can always change the password later:

dscl . passwd /Users/corybohon PASSWORD
  
If the user will have administrator privileges, then we'll run the following account to assign that title to the newly minted user:

dscl . append /Groups/admin GroupMembership corybohon
  
And, that's it. The most simple way to create a user through the command line, and assign all of the OS X account privileges to the new account.
