---
title: "Token Bucket: 令牌桶限流"
author: "-"
date: 2026-10-16T10:45:00+08:00
lastmod: 2026-10-16T10:45:00+08:00
url: token-bucket
categories:
  - Algorithm
tags:
  - rate-limiting
  - token-bucket
  - go
  - remix
  - AI-assisted
---

令牌桶（token bucket）是最常用的限流算法。它用两个数描述一条规则：令牌补充的速度，和桶最多能存多少个令牌。它要解决的问题是：既把长期的平均速度压住，又允许短时间内的一阵突发。

限流、熔断、降级三者的关系见 [限流、熔断与降级](../cloud/rate-limiting-circuit-breaker-degradation.md)，这篇只讲令牌桶。

## 原理

想象一个桶：

- 系统以恒定速度 r 往桶里放令牌，比如每秒 5 个；
- 桶最多装 b 个令牌，比如 60 个，满了再放的令牌直接丢掉；
- 每个请求进来先从桶里取一个令牌，取到就放行，桶空了就拒绝（或者排队等）。

所以 r 管的是长期平均速度，b 管的是一次最多能连发多少。b 也叫突发容量（burst）。

用 r = 5/s、b = 60 走一遍：

| 时刻 | 发生了什么 | 桶里的令牌 |
| ---- | ---- | ---- |
| 0 秒 | 用户闲了很久，桶是满的 | 60 |
| 0 秒 | 一口气发了 40 个请求，全部放行 | 20 |
| 0～4 秒 | 没有请求，每秒补 5 个 | 40 |
| 4 秒 | 又连发 50 个：前 40 个放行，后 10 个被拒 | 0 |
| 4 秒之后 | 每 0.2 秒补 1 个，只能按每秒 5 个的速度继续 | 0～1 |
| 停 12 秒 | 补满 | 60 |

规律：

- 闲下来的时间会攒成额度，但最多攒 b 个；
- 一直不停地发，长期只能达到 r；
- 被拒绝的请求不消耗令牌。

实现上不需要真的有一个定时器往桶里放令牌。只要记住「上次的令牌数」和「上次的时间」，请求来时按经过的时间补算：`tokens = min(b, tokens + r × 经过的秒数)`。所以每个桶只占两个数的内存，`x/time/rate` 就是这么做的。

## 解决什么问题

一个只按「一天最多多少次」计数的系统，管不住速度：一个脚本可以在一秒内把一天的额度打完，把数据库和下游服务一下子压垮。需要一个管速度的机制，同时又不能误伤正常用户。正常用户的请求是一阵一阵来的，打开一个页面时连发十几个请求，然后很久没有动静。

令牌桶正好对得上这种形状：

- 突发容量 b 让正常的一阵请求全部通过；
- 速率 r 让持续的高频请求（脚本）很快被压到 r。

## 和其他限流算法比较

| 算法 | 做法 | 优点 | 缺点 |
| ---- | ---- | ---- | ---- |
| 固定窗口计数 | 每个时间窗口（如每分钟）一个计数器，到点清零 | 最简单 | 窗口交界处能放过两倍：59 秒发 N 个，61 秒再发 N 个 |
| 滑动窗口日志 | 记下每个请求的时间戳，数最近 60 秒内有多少个 | 精确：任意 60 秒内严格不超过 N | 每个请求存一个时间戳，N 大时费内存 |
| 滑动窗口计数 | 用当前窗口和上一窗口的计数按比例估算 | 内存小，比固定窗口平滑 | 是近似值 |
| 令牌桶 | 见上文 | 允许突发，每个 key 只占两个数 | 不保证「任意窗口内最多 N 个」 |
| 漏桶（leaky bucket） | 请求进队列，以恒定速度流出，队列满了丢弃 | 输出速度绝对平稳 | 不容许突发，排队会增加延迟 |
| GCRA | 记录「下一个请求最早可以到达的理论时间」 | 效果等同令牌桶，只存一个时间戳，适合 Redis | 不如令牌桶直观 |

一个容易踩的坑：令牌桶不等于「每分钟最多 N 次」。r = N/60 秒、b = N 的令牌桶，在任意 60 秒内最多能放过 b + r × 60 ≈ 2N 次：先用满桶连发 N 个，再按速率补出 N 个。如果要的是严格的窗口上限，比如控制 AI 调用花费，用滑动窗口日志更合适。

## 适合和不适合的场景

适合：

- API 防刷：按用户或按 API key 一个桶，规则宽松，只拦脚本；
- 客户端调用第三方 API 时自我节流：对方限制每秒 10 次，就在自己这边用一个 r = 10 的桶，请求前先等令牌（Go 里是 `Wait(ctx)`），不去撞对方的 429；
- 网络流量整形：Linux `tc` 的 TBF（Token Bucket Filter）；
- 网关和云服务：AWS API Gateway 的 throttling 按令牌桶描述（rate 和 burst 两个参数），Envoy 的 local rate limit 也是令牌桶。Nginx 的 `limit_req` 是漏桶，配 `burst` 参数后效果接近令牌桶。

不适合：

- 配额和计费，比如「免费用户每天查 200 次词」：这是按天计数的产品规则，不是速度问题，用计数器；
- 需要严格窗口上限的场景：见上一节的坑；
- 需要排队削峰、保证下游绝对平稳的场景：用漏桶或消息队列。

## 单机还是分布式

- 单个进程、单个实例：桶放在内存里就够了。进程重启后每个人拿到一个满桶，最多多放过 b 个请求，通常可以接受。
- 多个实例：每个实例各管一个桶，相当于把限额乘以实例数。要共享状态就放到 Redis，常见做法是 Redis + Lua 脚本，或者直接用 GCRA 的实现。

Go 里的选择：

| 库 | 存储 | 算法 |
| ---- | ---- | ---- |
| `golang.org/x/time/rate` | 进程内存 | 令牌桶，Go 团队维护，事实标准 |
| `github.com/go-redis/redis_rate` | Redis | GCRA |
| `github.com/ulule/limiter` | 内存或 Redis | 固定窗口计数，自带 gin 等框架的中间件 |

令牌桶本身几十行就能写出来，但并发、补充时机、取消预留这些边界情况，`x/time/rate` 都处理好了，没有必要自己写。

## Go 示例：x/time/rate

`rate.NewLimiter(r, b)` 创建一个桶，初始是满的。三种用法：

```go
package main

import (
	"context"
	"fmt"
	"time"

	"golang.org/x/time/rate"
)

func main() {
	// 5 tokens per second, bucket holds at most 60.
	lim := rate.NewLimiter(rate.Limit(5), 60)

	// 1. Allow: take a token or refuse right away. A refusal costs nothing.
	if !lim.Allow() {
		fmt.Println("429")
	}

	// 2. Wait: block until a token arrives (client-side throttling).
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	if err := lim.Wait(ctx); err != nil {
		fmt.Println("gave up:", err)
	}

	// 3. Reserve: learn how long until a token arrives, e.g. for Retry-After.
	r := lim.Reserve()
	if d := r.Delay(); d > 0 {
		r.Cancel() // give the token back; we are refusing, not waiting
		fmt.Println("retry after", d)
	}
}
```

`rate.Every(200 * time.Millisecond)` 和 `rate.Limit(5)` 等价，按「多久补一个」写更直观。测试里要控制时间时，用 `AllowN(now, 1)`、`ReserveN(now, 1)` 传入假时钟，不用 sleep。

## 按用户限流的中间件

服务端最常见的是「每个用户一个桶」。要注意三件事：

1. 用一个 map 存每个 key 的桶，加锁；
2. 定期删掉闲置的桶，不然 map 会一直长。闲置超过 b / r 秒的桶早就补满了，删掉再新建是等价的；
3. 拒绝时返回 429 和 `Retry-After`，让客户端知道等多久。

```go
type userLimiter struct {
	lim      *rate.Limiter
	lastSeen time.Time
}

type PerUser struct {
	mu    sync.Mutex
	users map[string]*userLimiter
	r     rate.Limit
	b     int
}

// Allow reports whether userID may proceed and, if not, how long to wait.
func (p *PerUser) Allow(userID string, now time.Time) (bool, time.Duration) {
	p.mu.Lock()
	defer p.mu.Unlock()
	u, ok := p.users[userID]
	if !ok {
		u = &userLimiter{lim: rate.NewLimiter(p.r, p.b)}
		p.users[userID] = u
	}
	u.lastSeen = now

	res := u.lim.ReserveN(now, 1)
	if d := res.DelayFrom(now); d > 0 {
		res.CancelAt(now) // refused requests do not use up tokens
		return false, d
	}
	return true, 0
}
```

HTTP 层：

```go
ok, wait := limiter.Allow(userID, time.Now())
if !ok {
	secs := int(math.Ceil(wait.Seconds()))
	c.Header("Retry-After", strconv.Itoa(max(secs, 1)))
	c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{"code": "too_many_requests"})
	return
}
```

客户端也要配合：收到 429 后至少等 `Retry-After` 秒再重试，不要立即重试；如果系统里有好几种 429（比如限流和每日配额用完），用响应里的错误码区分，不要只看状态码。

## 实例：Catglish 的已登录接口限流

我在 Catglish（ENX）里用的就是上面这套，决策记录在 [ADR-060](https://github.com/wiloon/enx/blob/main/docs/architecture/adr-060-per-user-request-rate-limit.md)（issue [#185](https://github.com/wiloon/enx/issues/185)）。要点：

- 所有已登录接口都过一个 gin 中间件，按用户 ID 分桶，用 `x/time/rate`，放在进程内存里；
- 规则全员一样：每秒 5 个、桶容量 60，不分免费和付费。按套餐区分用量是每日配额的事；
- 按扩展的真实请求量估算：在一篇普通文章上启用学习模式约 5 个请求，很长的文章约 20 个，浏览器恢复 10 个标签页约 50 个，都在 60 以内；点词查词每次 1～4 个，人点词的间隔远大于 0.2 秒；
- 被限的请求在 Grafana 上看次数（Prometheus counter），在 Loki 日志里按 `rate_limited=true` 查是哪个用户、哪个接口；
- AI 接口另有一层滑动窗口日志限制，因为那里要的是严格的「每分钟最多 N 次」，令牌桶会放过将近两倍。

## 参考

- [golang.org/x/time/rate](https://pkg.go.dev/golang.org/x/time/rate)
- [Token bucket - Wikipedia](https://en.wikipedia.org/wiki/Token_bucket)
- [Generic cell rate algorithm - Wikipedia](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm)
- [Stripe: Scaling your API with rate limiters](https://stripe.com/blog/rate-limiters)
- [Amazon API Gateway: Throttle requests](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
- [NGINX: Rate Limiting](https://blog.nginx.org/blog/rate-limiting-nginx)
