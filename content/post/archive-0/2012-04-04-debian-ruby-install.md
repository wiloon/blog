---
title: debian ruby install
author: "-"
type: post
date: 2012-04-04T08:27:10+00:00
url: /?p=2785
categories:
  - Linux

---
ruby
  
```bash
  
sudo apt-get install ruby
   
```
  
RubyGems
  
去http://rubyforge.org/projects/rubygems/下载最新版的RubyGems
  
解压后运行以下命令安装即可:
  
```bash
  
sudo ruby setup.rb
   
```
  
#create link
  
```bash
  
sudo ln -s gem1.8 gem
  
```

更换gem sources
  
由于国内网络原因（你懂的) ，导致 rubygems.org 存放在 Amazon S3 上面的资源文件间歇性连接失败。所以你会与遇到 gem install foo 或 bundle install 的时候半天没有响应.
  
http://ruby.taobao.org/是一个完整 rubygems.org 镜像，用这个代替官方版本，同步频率目前为30分钟一次.
  
```bash
  
$ gem sources -remove http://rubygems.org/
  
$ gem sources -a http://ruby.taobao.org/
  
$ gem sources -l
  
\*\\*\* CURRENT SOURCES \*\**

http://ruby.taobao.org
  
```
  
# 请确保只有 ruby.taobao.org

sudo gem install rails