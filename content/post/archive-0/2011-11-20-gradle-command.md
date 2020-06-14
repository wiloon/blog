---
title: Gradle command
author: wiloon
type: post
date: 2011-11-20T07:58:09+00:00
url: /?p=1548
bot_views:
  - 6
views:
  - 1
categories:
  - Java
tags:
  - Gradle

---
```bash# 更新依赖包
gradle build --refresh-dependencies

# publish to maven
gradle publish

#create project structure
gradle init --type java-library --project-name jvm-library --dsl kotlin
gradle init --type java-library
gradle init --type java-application

#check module dependency
gradle dependencies --configuration compileClasspath
gradle :core:dependencies

#specifies the build file. 
gradle -b xxx/xxx/build.gradle 

#The Application Plugin
#apply plugin: 'application'
# 打包-tar
gradle distTar
gradle distZip
# 安装到本地
gradle installDist


#convert maven project to gradle project
gradle init --type pom
#eclipse 
gradle eclipse 
gradle cleanEclipse 
#idea gradle idea 
gradle cleanIdea 
#skip test gradle build -x test 
#load local jars compile files('libs/jfx-2.3.8.jar') 
```

<pre><code class="line-numbers">// project dependency
dependencies {
    compile project(":project-name")
}
```

// 设置 maven 库地址
  
repositories {
  
    maven { url &#8216;http://maven.oschina.net/content/groups/public/&#8217; }
  
}

exclude jar
  
compile("comxxx:xxx:xxx&#8221;) {
      
exclude group: &#8216;ch.qos.logback&#8217;, module: &#8216;logback-classic&#8217;
  
}
  
http://stackoverflow.com/questions/20707543/gradle-how-to-exclude-jar-from-a-war