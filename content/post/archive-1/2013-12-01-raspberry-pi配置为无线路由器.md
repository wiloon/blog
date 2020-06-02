---
title: Raspberry Pi配置为无线路由器
author: wiloon
date: 2013-12-01T11:55:37.000+00:00
url: "/?p=5999"
categories:
- Uncategorized
tags:
- linux
- Network
- Raspberry Pi

---
[http://www.cnblogs.com/DaochenShi/p/3152981.html](http://www.cnblogs.com/DaochenShi/p/3152981.html)
    
      因为自己有个RPi，但是之前用的8188CUS芯片的无线网卡不支持，虽然当时买的时候是为了让笔记本连双WiFi的，因此只挑了个最便宜的。后来发现没法在RPi上面做AP，于是就又重新买了个。国内也有树梅派的论坛讨论过哪些无线网卡的支持，发现Ralink的芯片可以，因此就再花了34块钱买了个腾达的W331M，使用最新的Raspbian内核来进行操作（非最新的话可能需要自己编译驱动）。
    
    
    <p>
      以下是结合上面的参考链接给出的如何将RPi搭建为一个路由器：
    </p>
    
    <p>
      首先是必备材料：
    </p>
    
    <ul>
      <li>
        RaspberryPi B版（就是带有线网卡的那个版），内存512/256都可以，我的是256的。
      </li>
      <li>
        一个已经可以正常运行的SD卡，这个如何准备我在我的另外一篇随笔当中提到过，所以这里不再赘述。
      </li>
      <li>
        一个可以支持AP模式的无线网卡。
      </li>
      <li>
        有线网卡也得联网。
      </li>
    </ul>
    
    <p>
      然后是必备技能：
    </p>
    
    <ul>
      <li>
        如果你是无显示器运行的，则需要会使用nano（vi也可以）
      </li>
      <li>
        如果你是有显示器运行的，那么可以在图形界面下面以root或者sudo来运行文本编辑器
      </li>
      <li>
        总之，就是你得会编辑文本文件才可以进行下面的操作。
      </li>
    </ul>
    
    <p>
      感谢原文给出的驱动提示，这里也抄一下。请确认无线网卡支持AP模式或者Master模式，已知下列网卡的具体情况：
    </p>
    
    <ul>
      <li>
        Edimax  不支持 Access Point
      </li>
      <li>
        AirLink 101 / AWL5088 不支持 Access Point
      </li>
      <li>
        Ralink RT5370 支持 Access Point
      </li>
    </ul>
    
    <p>
      想看你使用的是那种芯片？用lsusb吧！(省略了部分输出）
    </p>
    
    <div>
      <pre>pi@raspberrypi ~ $ lsusb

...
Bus 001 Device 007: ID 148f:5370 Ralink Technology, Corp. <strong>RT5370</strong> Wireless Adapter</pre>
</div>

    <p>
      呼……一大波前提说完了，下面要干正事了！
    </p>
    
    <p>
      先说一下大概步骤：
    </p>
    
    <ul>
      <li>
        打开WiFi
      </li>
      <li>
        指定IP，也就是建立一个WiFi局域网
      </li>
      <li>
        使用NAT，也就是能让你WiFi网络和有线网络可以通信。
      </li>
    </ul>
    
    <p>
      正文开始了：
    </p>
    
    <ol>
      <li>
        安装软件 <div>
          <pre>sudo apt-get install hostapd udhcpd</pre>
        </div>
      </li>
      
      <li>
        配置DHCP，也就是编辑文件/etc/udhcpd.conf ，基本上按照下列内容来做： <div>
          <div>
            <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
          </div>
          
          <pre>start 192.168.42.2 # This is the range of IPs that the hostspot will give to client devices.

end 192.168.42.20
interface wlan0 # The device uDHCP listens on.
remaining yes
opt dns 8.8.8.8 4.2.2.2 # The DNS servers client devices will use.
opt subnet 255.255.255.0
opt router 192.168.42.1 # The Pi's IP address on wlan0 which we will set up shortly.
opt lease 864000 # 10 day DHCP lease time in seconds</pre>

          <div>
            <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
          </div>
        </div>
        
        <p>
          将/etc/default/udhcpd 当中的这一行 DHCPD_ENABLED=&#8221;no&#8221;  变为
        </p>
        
        <div>
          <pre>#DHCPD_ENABLED="no"</pre>
        </div>
        
        <p>
          当然，你需要给无线网卡指定一个地址（静态地址，不会变的），为了达到开机启动就设置好的目的，你需要编辑/etc/network/interfaces：
        </p>
        
        <div>
          <pre>iface wlan0 inet static

address 192.168.42.1
netmask 255.255.255.0</pre>
</div>

        <p>
          如果原来有“iface wlan0 inet dhcp”之类的那么就删除，“wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf”什么的也删除。
        </p>
        
        <p>
          &nbsp;</li> 
          
          <li>
            配置hostapd。在这一部你就可以创建一个无线网络，可以选加密或者不加密模式。建议选择WPA2加密，那么你需要编辑/etc/hostapd/hostapd.conf文件（若不存在则需要手动创建） <div>
              <div>
                按 Ctrl+C 复制代码
              </div>
              
              <p>
                &nbsp;
              </p>
              
              <div>
                按 Ctrl+C 复制代码
              </div>
            </div>
            
            <p>
              其中的wpa_passphrase可以使用
            </p>
            
            <div>
              <pre>wpa_passphrase &lt;ssid&gt; [明文密码]</pre>
            </div>
            
            <p>
              来进行生成，生成的结果为：（已经修改psk部分，这里仅做示意用）
            </p>
            
            <div>
              <div>
                <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
              </div>
              
              <pre>pi@raspberrypi ~ $ wpa_passphrase Daochen_AP DaochenShi

network={
ssid="Daochen_AP"
\#psk="DaochenShi"
psk=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
}</pre>

              <div>
                <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
              </div>
            </div>
            
            <p>
              也就是你把wpa_passphrase去掉，换为wpa_psk=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef即可
            </p>
            
            <p>
              如果你想使用开放网络（不含密码），那么就这样配置：
            </p>
            
            <div>
              <div>
                <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
              </div>
              
              <pre>interface=wlan0

ssid=Daochen_AP
hw_mode=g
channel=6
auth_algs=1
wmm_enabled=0</pre>

              <div>
                <a title="复制代码"><img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" /></a>
              </div>
            </div>
            
            <p>
              之后还要接着编辑 /etc/default/hostapd
            </p>
            
            <p>
              把原来的DAEMON_CONF=&#8221;/etc/hostapd/hostapd.conf&#8221; 变为：
            </p>
            
            <div>
              <pre>DAEMON_CONF="/etc/hostapd/hostapd.conf"</pre>
            </div>
            
            <p>
              &nbsp;</li> 
              
              <li>
                配置NAT，也就是路由了首先编辑/etc/sysctl.conf文件，主要是打开ipv4的转发功能。 <div>
                  <pre>net.ipv4.ip_forward=1</pre>
                </div>
                
                <p>
                  那么这就在内核当中开启了ipv4的转发，之后需要设置iptables来让数据包通过：
                </p>
                
                <div>
                  <pre>sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT</pre>
</div>

                <p>
                  为了以后重启之后可以自动加载，因此运行命令来保存为一个文件：
                </p>
                
                <div>
                  <pre>sudo sh -c "iptables-save &gt; /etc/iptables.ipv4.nat"</pre>
                </div>
                
                <p>
                  并在/etc/network/interfaces文件的末尾添加这么一句：
                </p>
                
                <div>
                  <pre>up iptables-restore &lt; /etc/iptables.ipv4.nat</pre>
                </div>
                
                <p>
                  &nbsp;</li> 
                  
                  <li>
                    启动服务，看看你的无线是否搭建好了？运行一下命令： <div>
                      <pre>sudo service hostapd start

sudo service udhcpd start</pre>
</div>

                    <p>
                      如果你想开机启动的话，那么就这么做：
                    </p>
                    
                    <div>
                      <pre>sudo update-rc.d hostapd enable

sudo update-rc.d udhcpd enable</pre>
</div>

                    <p>
                      &nbsp;</li> </ol> 
                      
                      <p>
                        当然，最开始用8188CUS的时候参考的是 http://sirlagz.net/2012/08/09/how-to-use-the-raspberry-pi-as-a-wireless-access-pointrouter-part-1/
                      </p>
                      
                      <p>
                        但是从hostapd那一步之后就失败了，所以我实际上在这次设置无线网络的时候很多地方都不需要怎么操作了。这个链接的是有三部分组成，有兴趣的也可以看一下。
                      </p>
                      
                      <p>
                        我自己遇到了安装好udhcpd之后死活启动不了，报错是：
                      </p>
                      
                      <p>
                        udhcpd: is interface wlan0 up and configured?: Cannot assign requested address
                      </p>
                      
                      <p>
                        而且sudo ifup wlan0的时候报错，不过它指出来了错误地点：
                      </p>
                      
                      <div>
                        <pre>pi@raspberrypi /etc/hostapd $ sudo ifup wlan0

ip6tables-restore v1.4.14: Couldn't load match \`icmp':No such file or directory

Error occurred at line: 17
Try \`ip6tables-restore -h' or 'ip6tables-restore --help' for more information.
Failed to bring up wlan0.</pre>
</div>

                      <p>
                        因为我也设置了ip6tables，而wlan0目前没有设置ipv6，所以就出错了，解决方法也很简单，把错的那一行删了就可以了。如果你也觉得udhcpd启动不了，可以使用
                      </p>
                      
                      <div>
                        <pre>sudo udhcpd -f</pre>
                      </div>
                      
                      <p>
                        来进行前端显示。
                      </p>
                      
                      <p>
                        最后，接下来需要做的是：将eth0的ipv6通过类似brouter之类的东西使得无线网也有ipv6. 查过说有ebtables可以，但是具体怎么弄我一直没搞明白过（这个问题1年前就在关注了，但是没做，太懒了……
                      </p>
                      
                      <p>
                        &nbsp;
                      </p>
                      
                      <p>
                        <a href="https://github.com/jenssegers/RTL8188-hostapd">https://github.com/jenssegers/RTL8188-hostapd</a>
                      </p>
                      
                      <p>
                        <a href="http://azug.minpet.unibas.ch/~lukas/bricol/olinuxino-imx233/index.html">http://azug.minpet.unibas.ch/~lukas/bricol/olinuxino-imx233/index.html</a>
                      </p></div> </div>