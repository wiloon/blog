---
title: Gradle basic, command
author: "-"
date: 2011-11-20T07:58:09+00:00
url: /?p=1548

---
## Gradle basic, command
### command
    gradle build
    
### install
download latest version of gradle from http://www.gradle.org/downloads.html
  
extract the gradle package

sudo emacs ~/.bashrc
  
add the gradle to path.
  
set PATH=$JAVA_HOME/bin:/home/wiloon/program/gradle-1.0-milestone-3/bin:$PATH
  
export PATH
  
restart the system

```bash
# 更新依赖包
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
gradle eclipse 
gradle cleanEclipse 
#idea gradle idea 
gradle cleanIdea 
#skip test gradle build -x test 
#load local jars compile files('libs/jfx-2.3.8.jar') 
```

// project dependency
dependencies {
    compile project(":project-name")
}
```

// 设置 maven 库地址
  
repositories {
  
    maven { url 'http://maven.oschina.net/content/groups/public/' }
  
}

exclude jar
  
compile("comxxx:xxx:xxx") {
      
exclude group: 'ch.qos.logback', module: 'logback-classic'
  
}

### gralde > maven
https://www.huaweicloud.com/articles/5a4acb62fa2204db2dc7b08b8b151d32.html

http://stackoverflow.com/questions/20707543/gradle-how-to-exclude-jar-from-a-war