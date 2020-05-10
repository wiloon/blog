---
title: linux下的cpu温度监控软件 lm-sensors
author: wiloon
type: post
date: 2012-04-15T14:06:43+00:00
url: /?p=2942
categories:
  - Linux

---
原贴:http://goodfifagun.pixnet.net/blog/post/21587839

<div id="article_content">
  現在購買主機板時都會有廠商提供的監控軟體可以使用，而最常使用到到功<br /> 能像溫度監控，系統狀態等等，但是這些軟體都只能在windows 下使用，所<br /> 以如果要在 linux下監控CPU溫度，可以透過 lm-sensor這套軟體來監控。安裝環境：<br /> ubuntu 8.04.1 LTS</p> 
  
  <p>
    安裝步驟：<br /> 1. 安裝lm-sensors<br /> # apt-get install lm-sensors
  </p>
  
  <p>
    2. 設定監控選項<br /> # sensors-detect
  </p>
  
  <p>
    通常都是回答yes即可，注意最後一項，例如下面的資訊
  </p>
  
  <p>
    To load everything that is needed, add this to /etc/modules:
  </p>
  
  <p>
    #&#8212;-cut here&#8212;-<br /> # I2C adapter drivers<br /> # modprobe unknown adapter NVIDIA i2c adapter<br /> # modprobe unknown adapter NVIDIA i2c adapter<br /> # modprobe unknown adapter NVIDIA i2c adapter<br /> i2c-i801<br /> # Chip drivers<br /> # no driver for Winbond W83L785R/G yet<br /> lm85<br /> #&#8212;-cut here&#8212;-
  </p>
  
  <p>
    3. 出現如上訊息後，載入模組，<br /> 例如我的是 i2c-i801 與 lm85，
  </p>
  
  <p>
    # modprobe i2c-i801<br /> # modprobe lm85
  </p>
  
  <p>
    4. 之後再輸入：<br /> # sensors
  </p>
  
  <p>
    5. 就會出現cpu溫度之類的監控訊息。
  </p>
  
  <p>
    adm1027-i2c-3-2e<br /> Adapter: SMBus I801 adapter at e000<br /> V1.5: +1.31 V (min = +0.00 V, max = +3.32 V)<br /> VCore: +1.49 V (min = +0.00 V, max = +2.99 V)<br /> V3.3: +3.30 V (min = +0.00 V, max = +4.38 V)<br /> V5: +5.08 V (min = +0.00 V, max = +6.64 V)<br /> V12: +11.97 V (min = +0.00 V, max = +15.94 V) ALARM<br /> CPU_Fan: 3941 RPM (min = 0 RPM)<br /> fan2: 0 RPM (min = 0 RPM)<br /> fan3: 0 RPM (min = 0 RPM)<br /> fan4: 1882 RPM (min = 0 RPM)<br /> CPU Temp: +48.8°C (low = -127.0°C, high = +127.0°C)<br /> Board Temp: +46.0°C (low = -127.0°C, high = +127.0°C)<br /> Remote Temp: +45.5°C (low = -127.0°C, high = +127.0°C)<br /> cpu0_vid: +1.525 V
  </p>
</div>