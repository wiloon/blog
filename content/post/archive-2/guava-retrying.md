---
title: guava-retrying
author: "-"
date: 2017-07-20T02:45:40+00:00
url: /?p=10873
categories:
  - Inbox
tags:
  - reprint
---
## guava-retrying
http://blog.csdn.net/aitangyong/article/details/53840719
  
https://github.com/rholder/guava-retrying

对于开发过网络应用程序的程序员来说,重试并不陌生,由于网络的拥堵和波动,此刻不能访问服务的请求,也许过一小段时间就可以正常访问了。比如下面这段给某个手机号发SMS的伪代码: 

```java
// 发送SMS  
public boolean sendSMS(String phone, String content)  
{  
    int retryTimes = 3;  
    for(int i=0; i<=3; i++)  
    {  
        try  
        {  
            boolean result = doSomething(phone, content);  
            // 发送成功直接返回  
            if(result == true)  
            {  
                return true;  
            }  
        }  
        catch(IOException e)  
        {  
            // 可能是网络问题导致IOException,所以我们继续重试  
            logger.error("send sms error", e);  
        }  
        catch(Exception e)  
        {  
            // 未知异常,与网络无关,有可能是代码出现问题,这个时候重试没用,我们直接返回false  
            logger.error("unknown exception", e);  
            return false;  
        }  
    }  

    return false;  
}  

// 给某人发短信  
private boolean doSomething(String phone, String content)  
{  

}  
```

这段代码有什么问题呢？看起来很丑,为了实现重试逻辑,各种if-else,各种try-catch。重试逻辑太简单,只是控制了重试次数,并没有控制2次重试之间的时间间隔。因为重试代码与业务代码耦合在一起,所以看起来很复杂。

试想如果我们要改变重试逻辑: 比如我们希望每次重试过后,随机等待一段时间后再重试；比如我们希望重试次数不超过10次,而且总共的重试时间不超过1分钟；比如我们希望每次重试的时候,都给我们监控系统发一条消息...随着重试逻辑的不断变化,上面代码会越来越复杂。而且重试逻辑,其实是各个模块是差别不大的。

最近遇到2个开源项目,都是将重试代码封装成专门的工具,方便使用,比如guava-retrying和spring-retry。后面的文章,会介绍下如何使用guava-retrying。下面这段代码使用的是guava-retrying,明显可以感到代码变简单了。

```java
public boolean sendSMS(final String phone, final String content)  
{  
    Retryer<Boolean> retryer = RetryerBuilder.<Boolean>newBuilder()  
            .retryIfResult(Predicates.equalTo(false)) // 返回false时重试  
            .retryIfExceptionOfType(IOException.class) // 抛出IOException时重试  
            .withWaitStrategy(WaitStrategies.fixedWait(200, TimeUnit.MILLISECONDS)) // 200ms后重试  
            .withStopStrategy(StopStrategies.stopAfterAttempt(3)) // 重试3次后停止  
            .build();  
    try {  
        return retryer.call(new Callable<Boolean>() {  

            @Override  
            public Boolean call() throws Exception {  
                return doSomething(phone, content);  
            }  
        });  
    } catch (Exception e) {  
        return false;  
    }  
}  
```

这2个项目github地址是: 

https://github.com/rholder/guava-retrying

https://github.com/spring-projects/spring-retry

guava-retrying博文如下: 

guava-retrying重试工具库: 什么时候重试

guava-retrying重试工具库: 什么时候终止

guava-retrying重试工具库: 隔多长时间重试

guava-retrying重试工具库: 阻塞策略BlockStrategy

guava-retrying重试工具库: AttemptTimeLimiter

guava-retrying重试工具库: RetryListener

guava-retrying重试工具库: Retryer.call()使用注意事项