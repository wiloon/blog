---
title: ssh-agent, forward
author: "-"
date: 2018-05-11T01:04:23+00:00
url: ssh-agent

---
## ssh-agent, forward

### 查看 ssh agent 进程
    ps -ef | grep ssh-agent
### ssh agent

### 查看 缓存的密钥
```bash
#查看本地SSH agent 缓存的密钥
ssh-add -L
### 查看缓存的私钥 sha256值
    ssh-add -l
```

### 环境变量
    echo $SSH_AGENT_PID
    echo $SSH_AUTH_SOCK

### 测试密钥是否可用
    ssh -T git@github.com

### 临时运行, 直接执行的话不能导入 环境 变量
    ssh-agent
#### 回显
    SSH_AUTH_SOCK=/tmp/ssh-XXXXXXmfJNRj/agent.43061; export SSH_AUTH_SOCK;
    SSH_AGENT_PID=43062; export SSH_AGENT_PID;
    echo Agent pid 43062;

### 导入环境变量
    eval $(ssh-agent)

ssh-agent 是用于管理SSH private keys的, 长时间持续运行的守护进程（daemon) . 唯一目的就是对解密的私钥进行高速缓存。
ssh-add 提示并将用户的使用的私钥添加到由ssh-agent 维护的列表中. 此后, 当使用公钥连接到远程 SSH 或 SCP 主机时,不再提示相关信息.
使用步骤如下:

```bash  
eval `ssh-agent`
ssh-add Path/to/your private_key files
ssh-keygen -f ~/.ssh/id_rsa -p
```

注音: 使用的是反引号 backquote (`), 位于波浪号 tilde (~)下面, 不是单引号 quote (').
  
当登出主机后,使用下列命令,以清楚缓存的key list:
    
kill $SSH_AGENT_PID

如果使用 csh ortcsh, 可将上述命令放到.logout 文件中 ;如果使用bash, 可将命令放到.bash_logout 文件中.

http://xstarcd.github.io/wiki/shell/fork_exec_source.html
## ssh-agent
    # vim ~/.bashrc

    if ! pgrep -u "$USER" ssh-agent > /dev/null; then
      ssh-agent -t 1h > "$XDG_RUNTIME_DIR/ssh-agent.env"
    fi
    if [[ ! "$SSH_AUTH_SOCK" ]]; then
        source "$XDG_RUNTIME_DIR/ssh-agent.env" >/dev/null
    fi

    # start the ssh-agent in the background
    eval "$(ssh-agent -s)"
    # Add the SSH key to the ssh-agent
    ssh-add ~/.ssh/id_rsa
### check ssh agent
    echo "$SSH_AUTH_SOCK"
    ssh-add -L
    ssh-add -l


### 开启ssh forward
#### vim /etc/ssh/ssh_config
    Host *
            ForwardAgent yes

### 重启sshd
    sudo systemctl restart sshd

---

https://www.jianshu.com/p/12de50582e63

ssh到node1
  
由node1跳板到任意机器。
  
然而失败了。

XiaoleideMacBook-Pro:~ professor$ vi .bashrc
  
alias go-node1='ssh -p 1046 hzlixiaolei@10.165.xxx.xxx'
  
XiaoleideMacBook-Pro:~ professor$ go-node1
  
-bash: go-node1: command not found
  
XiaoleideMacBook-Pro:~ professor$ source .bashrc
  
-bash: SSH_AUTH_SOCK=/var/folders/9x/7zl7w59n55s3wb_wjg7d5zfh0000gn/T//ssh-XpUY3kpYkJnP/agent.9483;: No such file or directory
  
XiaoleideMacBook-Pro:~ professor$ go-node1

The programs included with the Debian GNU/Linux system are free software;
  
the exact distribution terms for each program are described in the
  
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
  
permitted by applicable law.
  
Last login: Mon Feb 6 15:51:21 2017 from 10.165.xx.xx
  
hzlixiaolei@node1:~$go-node2
  
(public key denied)
  
如图所示,我从node1往node2跳的时候出现公钥无效。

解决办法
  
其实这里的问题就在于我没有开ssh-agent.

正确配置ssh-agent forwardi配置即可成功: 

  
2, 配置云主机的SSH-agent forwarding
  
配置步骤同上

3,查看本地SSH agent是否携带本地的ssh key
  
Mac特有的一个问题,要注意
  
On Mac OS X, ssh-agent will "forget" this key, once it gets restarted during reboots. But you can import your SSH keys into Keychain using this command:

XiaoleideMacBook-Pro:ssh professor$ ssh-add -L
  
好了,问题解决。

### SSH, SSH agent & SSH agent Forwarding
这里,必须需要说下这三者的联系。

#### 我们常用的SSH工作原理,通过publickey access: 
- Step1,用户发起连接,携带者用户名
- Step2,ssh守护进程（sshd) 在Server上查看authorized_keys文件,基于publickey构造一个口令盘问发送给SSH client 
The ssh daemon on the server looks in the user's authorized_keys file, constructs a challenge based on the public key found there, and sends this challenge back to the user's ssh client.
- Step3,SSH client收到后,在本地查询privatekey（默认id_rsa文件) ,此时如果有密码,会要求输入密码。
- Step4,ssh client通过privatekey构造一个响应。发送给sshd。注意: 这里并不会发送privatekey本身。
- Step5,验证,授权成功

### SSH agent是干嘛的
如果每次我们都SSH到某个server,我们如果privatekey有密码,如果没有ssh agent,每次我们都会需要被告知要输入密码。有了ssh Agent,就不需要了。因为它负责管理key。

与上面相比,唯一的区别在第三步和第四步: 
  
根据privatekey构造响应的操作有ssh-agent来做了。ssh client没有和privatekey有联系。所以后面的访问,都是ssh-agent来管理,又因为我们之前输入过密码,ssh-agent仍然记录这个状态,所以之后就不用再输入密码了。
  
可谓一劳永逸。

### ssh agent forwarding
简单来说,agent forwarding运行一串的ssh连接。将sshd的口令盘问直接发送到最初始的ssh client,而不需要任何中间集群的认证。
  
如果按照我们上面的配置,配置好了agent forwarding,它是如何工作的: 
  
- Step1,基于上面的ssh到server1,用户在server1上开始发起到server2的链接（这一步和之前一样) 
- Step2: server2的sshd查询用户的authorized_keys文件,并像之前一样构造一个口令盘问发回给server1的ssh。下面神奇的事情就发生了: server1的ssh发送给自己的sshd,并再一次relay给我们pc的ssh。
- Step3: 后面的步骤就是PC的ssh agent根据privatekey构造key response并串行的发到server2的sshd上。然后完成鉴权。
- Step4: 如果需要在往Server3,4,N,仍然有效。

### archlinux ssh-agent
Start ssh-agent with systemd user

```bash
vim ~/.config/systemd/user/ssh-agent.service
[Unit]
Description=SSH key agent

[Service]
Type=simple
Environment=SSH_AUTH_SOCK=%t/ssh-agent.socket
ExecStart=/usr/bin/ssh-agent -D -a $SSH_AUTH_SOCK

[Install]
WantedBy=default.target
```

### .pam_environment 没有的话就创建一个新文件
```bash
vim  ~/.pam_environment
SSH_AUTH_SOCK DEFAULT="${XDG_RUNTIME_DIR}/ssh-agent.socket"

```

```bash
# Then enable or start the service.
systemctl --user enable ssh-agent
systemctl --user start ssh-agent
# 检查环境变量 SSH_AUTH_SOCK
env | fgrep SSH_
# 如果看不到SSH_AUTH_SOCK , 重启再试一下 
```

---

https://blog.csdn.net/vizts/article/details/47043695
https://www.fythonfang.com/blog/2017/12/27/ssh-agent-and-ssh-agent-forwarding
https://wiki.archlinux.org/index.php/Systemd/User
https://wiki.archlinux.org/index.php/SSH_keys
https://www.jianshu.com/p/12de50582e63