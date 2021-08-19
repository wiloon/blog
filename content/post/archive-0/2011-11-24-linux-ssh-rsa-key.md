---
title: rsa ssh keygen
author: "-"
type: post
date: 2011-11-24T04:41:17+00:00
url: ssh-keygen
categories:
  - Linux

---
在~/.ssh目录下生成私钥id_rsa和公钥id_rsa.pub文件

```bash
ssh-keygen -t rsa
ssh-keygen -t rsa -b 4096
ssh-keygen -t ecdsa -b 521
# -t type 指定要创建的密钥类型。可以使用："rsa1"(SSH-1) "rsa"(SSH-2) "dsa"(SSH-2)

ssh-keygen -t rsa -C "Michael Ledin" -b 4096 -m "PEM"

# -C comment
# -b key 长度
# -t 类型: dsa | ecdsa | ecdsa-sk | ed25519 | ed25519-sk | rsa

scp /root/.ssh/id_rsa.pub root@192.168.10.184:/root
ssh 192.168.10.184
cat /root/id_rsa.pub >> /root/.ssh/authorized_keys
# ok,you will login 192.168.10.184 without input password.

```
### print SHA256 fingerprint
    ssh-keygen -lf /path/to/ssh/key

### 
    ssh-keygen -A
    
public key file: authorized_keys

this command will generating public/private rsa key pair.
  
Your identification has been saved in /root/.ssh/id_rsa
  
Your public key has been saved in /root/.ssh/id_rsa.pub

### WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
    ssh-keygen -f "/home/wiloon/.ssh/known_hosts" -R "192.168.1.2"


### multiple ssh private keys

by **Karanbir Singh**

http://www.karan.org/blog/index.php/2009/08/25/multiple-ssh-private-keys
  
    
      In quite a few situations its preferred to have ssh keys dedicated for a service or a specific role. Eg. a key to use for home / fun stuff and another one to use for Work things, and another one for Version Control access etc. Creating the keys is simple, just use
    
    
    <blockquote>
      ssh-keygen -t rsa -f ~/.ssh/id_rsa.work -C "Key for Word stuff"
    </blockquote>
    
    
      Use different file names for each key. Lets assume that there are 2 keys, ~/.ssh/id_rsa.work and ~/.ssh/id_rsa.misc . The simple way of making sure each of the keys works all the time is to now create config file for ssh:
    
    
    <blockquote>
      
        touch ~/.ssh/config
 chmod 600 ~/.ssh/config
 echo "IdentityFile ~/.ssh/id_rsa.work" >> ~/.ssh/config
 echo "IdentityFile ~/.ssh/id_rsa.misc" >> ~/.ssh/config
      
    </blockquote>
    
    
      This would make sure that both the keys are always used whenever ssh makes a connection. However, ssh config lets you get down to a much finer level of control on keys and other per-connection setups. And I recommend, if you are able to, to use a key selection based on the Hostname. My ~/.ssh/config looks like this :
    
    
    <blockquote>
      Host *.home.lan
  IdentityFile ~/.ssh/id_dsa.home
  User kbsingh

Host *.vpn
  IdentityFile ~/.ssh/id_rsa.work
  User karanbir
  Port 44787

Host *.d0.karan.org
  IdentityFile ~/.ssh/id_rsa.d0
  User admin
  Port 21871
    </blockquote>
    
    
      Ofcourse, if I am connecting to a remote host that does not match any of these selections, ssh will default back to checking for and using the 'usual' key, ~/.ssh/id_dsa or ~/.ssh/id_rsa
  


