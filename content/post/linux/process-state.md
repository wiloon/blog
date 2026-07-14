---
title: "Linux Process State, 进程状态"
author: "-"
date: "2021-06-14T18:26:58+08:00"
lastmod: 2026-07-14T17:54:49+08:00
url: process-state
categories:
  - Linux
tags:
  - Linux
  - kernel
  - remix
  - AI-assisted
---

Linux（本文以 4.8.4 内核为例）下，进程状态大致有 7 种：

| 进程状态                | 说明                                       |
| ------------------------ | ------------------------------------------ |
| `TASK_RUNNING`            | 可运行状态。未必正在使用 CPU，也许是在等待调度 |
| `TASK_INTERRUPTIBLE`      | 可中断的睡眠状态。正在等待某个条件满足     |
| `TASK_UNINTERRUPTIBLE`    | 不可中断的睡眠状态。不会被信号中断         |
| `__TASK_STOPPED`          | 暂停状态。收到某种信号，运行被停止         |
| `__TASK_TRACED`           | 被跟踪状态。进程停止，被另一个进程跟踪     |
| `EXIT_ZOMBIE`             | 僵尸状态。进程已经退出，但尚未被父进程或者 init 进程收尸 |
| `EXIT_DEAD`               | 真正的死亡状态                             |

在 `include/linux/sched.h` 中，进程状态的定义并没有那么少：

```c
/*
 * Task state bitmask. NOTE! These bits are also
 * encoded in fs/proc/array.c: get_task_state().
 *
 * We have two separate sets of flags: task->state
 * is about runnability, while task->exit_state are
 * about the task exiting. Confusing, but this way
 * modifying one set can't modify the other one by
 * mistake.
 */
#define TASK_RUNNING            0
#define TASK_INTERRUPTIBLE      1
#define TASK_UNINTERRUPTIBLE    2
#define __TASK_STOPPED          4
#define __TASK_TRACED           8
/* in tsk->exit_state */
#define EXIT_DEAD               16
#define EXIT_ZOMBIE              32
#define EXIT_TRACE              (EXIT_ZOMBIE | EXIT_DEAD)
/* in tsk->state again */
#define TASK_DEAD               64
#define TASK_WAKEKILL            128
#define TASK_WAKING              256
#define TASK_PARKED              512
#define TASK_NOLOAD              1024
#define TASK_NEW                 2048
#define TASK_STATE_MAX            4096

#define TASK_STATE_TO_CHAR_STR "RSDTtXZxKWPNn"

extern char ___assert_task_state[1 - 2*!!(
                sizeof(TASK_STATE_TO_CHAR_STR)-1 != ilog2(TASK_STATE_MAX)+1)];

/* Convenience macros for the sake of set_task_state */
#define TASK_KILLABLE           (TASK_WAKEKILL | TASK_UNINTERRUPTIBLE)
#define TASK_STOPPED            (TASK_WAKEKILL | __TASK_STOPPED)
#define TASK_TRACED             (TASK_WAKEKILL | __TASK_TRACED)

#define TASK_IDLE               (TASK_UNINTERRUPTIBLE | TASK_NOLOAD)

/* Convenience macros for the sake of wake_up */
#define TASK_NORMAL             (TASK_INTERRUPTIBLE | TASK_UNINTERRUPTIBLE)
#define TASK_ALL                (TASK_NORMAL | __TASK_STOPPED | __TASK_TRACED)

/* get_task_state() */
#define TASK_REPORT             (TASK_RUNNING | TASK_INTERRUPTIBLE | \
                                 TASK_UNINTERRUPTIBLE | __TASK_STOPPED | \
                                 __TASK_TRACED | EXIT_ZOMBIE | EXIT_DEAD)
```

## TASK_RUNNING

`TASK_RUNNING` 是教科书中两种状态的结合：一种是正在占用 CPU 的 RUNNING 状态，一种是 RUNNING 状态的进程时间片耗尽、或者主动让出 CPU、或者被更高优先级进程抢占后，进入的 READY 状态。处于 `TASK_RUNNING` 状态的进程要么正在 CPU 上运行，要么随时都可以投入运行，只不过 CPU 资源有限，调度器暂时没有选中它们。

处于 `TASK_RUNNING` 状态的进程是调度器的调度对象（调度器的整体介绍见 [Linux 进程调度](./scheduler.md)）。在 Linux 中，每个 CPU 都有自己的运行队列集合：如果是实时进程，则根据优先级落在相应优先级的队列上；如果是普通进程，则根据虚拟运行时间落在红黑树相应位置上（详见 [CFS 完全公平调度器](./cfs.md)）。

Linux 提供了 `time` 命令可以统计进程在用户态和内核态消耗的 CPU 时间，`time` 命令提供了三种计时：实际时间、用户 CPU 时间和内核 CPU 时间。下面的输出可以看出 `real` 不一定等于 `user + sys`，在多核处理器上，两边的大小是不确定的：

```bash
$ time ntpdate pool.ntp.org
# ... ntpdate output ...

real    0m8.710s
user    0m0.002s
sys     0m0.013s
```

如果想在进程尚未结束时获得程序的执行时间，可以查看 procfs 中的信息，`/proc/<PID>/stat` 中字段 13 是用户态 CPU 时间，字段 14 是内核态 CPU 时间，两者单位是时钟嘀嗒。在配置内核的时候，有 100HZ、250HZ、300HZ 和 1000HZ 这 4 个选项，一个时钟嘀嗒对应的时间可以通过下面的命令获得：

```bash
$ grep CONFIG_HZ /boot/config-*
```

`pidstat` 命令也可以获取各个进程的 CPU 使用情况。如果想获取进程的实际运行时间，可以使用 `ps` 命令：

```bash
$ ps -p 20590 -o etime,cmd,pid
    ELAPSED CMD                            PID
   01:21:57 emacs taskstatus.org         20590
```

## TASK_INTERRUPTIBLE 和 TASK_UNINTERRUPTIBLE

当进程和慢速设备打交道，或者需要等待条件满足时，这种等待时间是不可预估的，这种情况下，内核会将该进程从 CPU 的运行队列中移除，从而进程进入睡眠状态。

Linux 的进程有两种睡眠状态：`TASK_INTERRUPTIBLE` 和 `TASK_UNINTERRUPTIBLE`，这两种状态的区别是能否响应收到的信号。处于 `TASK_INTERRUPTIBLE` 状态的进程遇到下面两种情况会返回到 `TASK_RUNNING` 状态：

- 等待条件满足；
- 收到未被屏蔽的信号（收到信号时会返回 `EINTR`，需要检测返回值以作出正确处理）。

对于 `TASK_UNINTERRUPTIBLE`，只有等待条件满足才有可能返回运行状态，任何信号都无法打断它。如果这种状态的进程出错，无法被杀死，只能重启。

`TASK_UNINTERRUPTIBLE` 的存在是因为内核中某些处理是不能被打断的，比如 `read` 系统调用正在操作磁盘，就要用 `TASK_UNINTERRUPTIBLE` 将其保护起来，以免受到打扰而陷入不可控的状态。

`khungtaskd` 内核线程（源码在 `kernel/hung_task.c`）会定期唤醒（120 秒）检查所有 `TASK_UNINTERRUPTIBLE` 进程，如果有进程超过 120 秒没有被调度，那么内核就会打印进程的堆栈信息。通过下面的命令可以查看 `khungtaskd` 周期：

```bash
$ sysctl kernel.hung_task_timeout_secs
kernel.hung_task_timeout_secs = 120
```

通过 `/proc/<pid>/wchan`（what channel 的缩写）、`/proc/<pid>/stack`，或者 `/proc/<pid>/status` 可以知道进程处于什么状态。

### 等待队列

睡眠状态的进程都保存在等待队列中，队列在 `include/linux/wait.h` 中定义：

```c
typedef struct __wait_queue wait_queue_t;
typedef int (*wait_queue_func_t)(wait_queue_t *wait, unsigned mode, int flags, void *key);
int default_wake_function(wait_queue_t *wait, unsigned mode, int flags, void *key);

/* __wait_queue::flags */
#define WQ_FLAG_EXCLUSIVE       0x01
#define WQ_FLAG_WOKEN           0x02

struct __wait_queue {
        unsigned int            flags;
        void                    *private;
        wait_queue_func_t       func; // wakeup callback
        struct list_head        task_list;
};

struct wait_bit_key {
        void                    *flags;
        int                     bit_nr;
#define WAIT_ATOMIC_T_BIT_NR    -1
        unsigned long           timeout;
};

struct wait_bit_queue {
        struct wait_bit_key     key;
        wait_queue_t            wait;
};

struct __wait_queue_head {
        spinlock_t              lock;
        struct list_head        task_list;
};
typedef struct __wait_queue_head wait_queue_head_t;
```

等待队列元素 `private` 在 `__WAITQUEUE_INITIALIZER` 中指向了进程描述符 `task_struct`，这就可以将进程加入到对应的队列上了。使用 `add_wait_queue` 或者 `add_wait_queue_exclusive` 将队列元素加到相应队列，这两个函数的区别在于：一个将队列元素设置 `WQ_FLAG_EXCLUSIVE` 标志位，另一个没有；一个将元素放到队列尾部，另一个放到队列头部。这是因为有时候当等待条件满足时，可以将队列中的所有进程唤醒，有时唤醒操作是排他的（EXCLUSIVE）则只能唤醒一个。

内核使用 `wait_event` 系列宏和函数等待条件是否满足：

```c
#define ___wait_is_interruptible(state)                                 \
        (!__builtin_constant_p(state) ||                                \
                state == TASK_INTERRUPTIBLE || state == TASK_KILLABLE)  \

/*
 * The below macro ___wait_event() has an explicit shadow of the __ret
 * variable when used from the wait_event_*() macros.
 *
 * This is so that both can use the ___wait_cond_timeout() construct
 * to wrap the condition.
 *
 * The type inconsistency of the wait_event_*() __ret variable is also
 * on purpose; we use long where we can return timeout values and int
 * otherwise.
 */

#define ___wait_event(wq, condition, state, exclusive, ret, cmd)        \
({                                                                      \
        __label__ __out;                                                \
        wait_queue_t __wait;                                            \
        long __ret = ret;       /* explicit shadow */                   \
                                                                        \
        INIT_LIST_HEAD(&__wait.task_list);                              \
        if (exclusive)                                                  \
                __wait.flags = WQ_FLAG_EXCLUSIVE;                       \
        else                                                            \
                __wait.flags = 0;                                       \
                                                                        \
        for (;;) {                                                      \
                long __int = prepare_to_wait_event(&wq, &__wait, state);\
                                                                        \
                if (condition)                                          \
                        break;                                          \
                                                                        \
                if (___wait_is_interruptible(state) && __int) {         \
                        __ret = __int;                                  \
                        if (exclusive) {                                \
                                abort_exclusive_wait(&wq, &__wait,      \
                                                     state, NULL);      \
                                goto __out;                             \
                        }                                               \
                        break;                                          \
                }                                                       \
                                                                        \
                cmd;                                                    \
        }                                                               \
        finish_wait(&wq, &__wait);                                      \
__out:  __ret;                                                          \
})

#define __wait_event(wq, condition)                                     \
        (void)___wait_event(wq, condition, TASK_UNINTERRUPTIBLE, 0, 0,  \
                            schedule())

/**
 * wait_event - sleep until a condition gets true
 * @wq: the waitqueue to wait on
 * @condition: a C expression for the event to wait for
 *
 * The process is put to sleep (TASK_UNINTERRUPTIBLE) until the
 * @condition evaluates to true. The @condition is checked each time
 * the waitqueue @wq is woken up.
 *
 * wake_up() has to be called after changing any variable that could
 * change the result of the wait condition.
 */
#define wait_event(wq, condition)                                       \
do {                                                                    \
        might_sleep();                                                  \
        if (condition)                                                  \
                break;                                                  \
        __wait_event(wq, condition);                                    \
} while (0)
```

`prepare_to_wait` 函数将队列元素添加到对应的等待队列，同时将进程状态设置成 `TASK_UNINTERRUPTIBLE`，完成 `prepare_to_wait` 后，检查条件是否满足，如果不满足则调用 `schedule()` 主动让出 CPU 使用权。`prepare_to_wait` 在 `/kernel/sched/wait.c` 中。

内核是通过 `wake_up` 系列宏实现唤醒操作的，这些宏最终调用 `__wake_up` 函数，这个函数在 `kernel/sched/wait.c` 中，`wake_up` 最终调用 `try_to_wake_up`：

```c
/*
 * The core wakeup function. Non-exclusive wakeups (nr_exclusive == 0) just
 * wake everything up. If it's an exclusive wakeup (nr_exclusive == small +ve
 * number) then we wake all the non-exclusive tasks and one exclusive task.
 *
 * There are circumstances in which we can try to wake a task which has already
 * started to run but is not in state TASK_RUNNING. try_to_wake_up() returns
 * zero in this (rare) case, and we handle it by continuing to scan the queue.
 */
static void __wake_up_common(wait_queue_head_t *q, unsigned int mode,
                        int nr_exclusive, int wake_flags, void *key)
{
        wait_queue_t *curr, *next;

        list_for_each_entry_safe(curr, next, &q->task_list, task_list) {
                unsigned flags = curr->flags;

                if (curr->func(curr, mode, wake_flags, key) &&
                                (flags & WQ_FLAG_EXCLUSIVE) && !--nr_exclusive)
                        break;
        }
}

/**
 * __wake_up - wake up threads blocked on a waitqueue.
 * @q: the waitqueue
 * @mode: which threads
 * @nr_exclusive: how many wake-one or wake-many threads to wake up
 * @key: is directly passed to the wakeup function
 *
 * It may be assumed that this function implies a write memory barrier before
 * changing the task state if and only if any tasks are woken up.
 */
void __wake_up(wait_queue_head_t *q, unsigned int mode,
                        int nr_exclusive, void *key)
{
        unsigned long flags;

        spin_lock_irqsave(&q->lock, flags);
        __wake_up_common(q, mode, nr_exclusive, 0, key);
        spin_unlock_irqrestore(&q->lock, flags);
}
EXPORT_SYMBOL(__wake_up);
```

## TASK_KILLABLE

有人认为使用 `vfork` 函数时子进程在调用 `exec` 或者退出之前，父进程处于 `TASK_UNINTERRUPTIBLE` 状态，事实并非如此，因为进程可以轻易被 Kill 命令杀死。但是此时 `ps` 命令显示这个进程确实是 D+ 状态。内核自 2.6.25 开始，引入了 `TASK_KILLABLE`，处于 `TASK_UNINTERRUPTIBLE` 和 `TASK_INTERRUPTIBLE` 之间，进程收到致命信号 `SIGKILL` 时会被唤醒。

## __TASK_STOPPED 和 __TASK_TRACED

`SIGSTOP`、`SIGTSTP`、`SIGTTIN`、`SIGTTOUT` 等信号会将进程暂时停止，进入 `__TASK_STOPPED` 状态。这 4 种信号不可被忽略、不可被屏蔽、不能安装新的处理函数。在收到 `SIGCONT` 后进程可以恢复执行。

使用 gdb 跟踪进程可以进入 `__TASK_TRACED` 状态。调试进程下达 `PTRACE_CONT` 或者 `PTRACE_DETACH` 等可将其重新执行。

## EXIT_ZOMBIE 和 EXIT_DEAD

这两种状态下，进程已经死掉了，只是 `EXIT_ZOMBIE` 状态中的进程没有被收尸——父进程没有设置 `SIGCHLD` 处理函数为 `SIG_IGN`，或者没有为 `SIGCHLD` 设置 `SA_NOCLDWAIT` 标志位。

进程的状态可以在 `/proc/<pid>/status` 中看到，对应关系如下：

| procfs             | 进程状态                |
| ------------------ | ------------------------ |
| R (running)         | `TASK_RUNNING`            |
| S (sleeping)        | `TASK_INTERRUPTIBLE`      |
| D (disk sleeping)   | `TASK_UNINTERRUPTIBLE`    |
| T (stopped)         | `__TASK_STOPPED`          |
| t (tracing stop)    | `__TASK_TRACED`           |
| Z (zombie)          | `EXIT_ZOMBIE`             |
| X (dead)            | `EXIT_DEAD`               |

## 竞争条件与无效唤醒（missed wakeup）

几乎在所有的情况下，进程都会在检查了某些条件之后，发现条件不满足才进入睡眠。可是有的时候进程却会在条件已经变为真之后才开始检查，如果这样的话进程就会无限期地休眠下去，这就是所谓的**无效唤醒（missed wakeup / lost wakeup）问题**。在操作系统中，当多个进程都企图对共享数据进行某种处理，而最后的结果又取决于进程运行的顺序时，就会发生竞争条件，无效唤醒恰恰就是由竞争条件导致的。

设想有两个进程 A 和 B，A 进程正在处理一个链表，它需要检查这个链表是否为空，如果不空就对链表里面的数据进行一些操作，同时 B 进程也在往这个链表添加节点。当这个链表是空的时候，由于无数据可操作，A 进程就进入睡眠；当 B 进程向链表里面添加了节点之后，它就唤醒 A 进程，代码大致如下：

A 进程：

```c
spin_lock(&list_lock);
if (list_empty(&list_head)) {
        spin_unlock(&list_lock);
        set_current_state(TASK_INTERRUPTIBLE);
        schedule();
        spin_lock(&list_lock);
}
/* Rest of the code ... */
spin_unlock(&list_lock);
```

B 进程：

```c
spin_lock(&list_lock);
list_add_tail(&list_head, new_node);
spin_unlock(&list_lock);
wake_up_process(processa_task);
```

这里会出现一个问题：假如当 A 进程执行到 `spin_unlock` 之后、`set_current_state` 之前，B 进程被另一个处理器调度投入运行，在这个时间片内 B 进程执行完了它所有的指令，因此它试图唤醒 A 进程，而此时 A 进程还没有进入睡眠，所以唤醒操作无效。在这之后，A 进程继续执行，它会错误地认为这个时候链表仍然是空的，于是将自己的状态设置为 `TASK_INTERRUPTIBLE` 然后调用 `schedule()` 进入睡眠。由于错过了 B 进程的唤醒，它将会无限期地睡眠下去——即使链表中有数据需要处理，A 进程也还是睡眠了。

### 避免无效唤醒

无效唤醒主要发生在"检查条件"之后和"进程状态被设置为睡眠状态"之前这段间隙。要解决这个问题，必须使用一种保障机制，使判断链表为空和设置进程状态为睡眠状态成为一个不可分割的步骤，也就是必须消除竞争条件产生的根源。重新设计一下 A 进程的代码结构，就可以避免上面例子中的无效唤醒问题：

```c
set_current_state(TASK_INTERRUPTIBLE);
spin_lock(&list_lock);
if (list_empty(&list_head)) {
        spin_unlock(&list_lock);
        schedule();
        spin_lock(&list_lock);
}
set_current_state(TASK_RUNNING);
/* Rest of the code ... */
spin_unlock(&list_lock);
```

这段代码在测试条件之前就将当前执行进程状态设置成 `TASK_INTERRUPTIBLE` 了，并且在链表不为空的情况下又将自己置为 `TASK_RUNNING` 状态。这样一来，如果 B 进程在 A 进程检查了链表为空以后调用 `wake_up_process()`，那么 A 进程的状态就会自动由原来的 `TASK_INTERRUPTIBLE` 变成 `TASK_RUNNING`，此后即使进程又调用了 `schedule()`，由于它现在的状态是 `TASK_RUNNING`，所以仍然不会被从运行队列中移出，因而不会错误地进入睡眠，也就避免了无效唤醒问题。

### Linux 内核中的例子

为了避免无效唤醒问题，Linux 内核在需要进程睡眠的时候会使用类似如下的操作：

```c
/* 'q' is the waitqueue we want to sleep on */
DECLARE_WAITQUEUE(wait, current);
add_wait_queue(q, &wait);
set_current_state(TASK_INTERRUPTIBLE);
/* or TASK_UNINTERRUPTIBLE */
while (!condition) /* condition is what we're waiting for */
        schedule();
set_current_state(TASK_RUNNING);
remove_wait_queue(q, &wait);
```

这段代码使进程通过下面的一系列步骤安全地将自己加入到一个等待队列中进行睡眠：首先调用 `DECLARE_WAITQUEUE()` 创建一个等待队列的项，然后调用 `add_wait_queue()` 把自己加入到等待队列中，并且将进程的状态设置为 `TASK_INTERRUPTIBLE` 或者 `TASK_UNINTERRUPTIBLE`，然后循环检查条件是否为真：如果是的话就没有必要睡眠；如果条件不为真，就调用 `schedule()`。当进程检查的条件满足后，进程又将自己设置为 `TASK_RUNNING` 并调用 `remove_wait_queue()` 将自己移出等待队列。

同样地，Linux 内核代码维护者也是在进程检查条件之前就设置进程的状态为睡眠状态，然后才循环检查条件。如果在进程开始睡眠之前条件就已经达成了，那么循环会退出并用 `set_current_state()` 将自己的状态设置为就绪，这样同样保证了进程不会因为竞争条件而错误地进入睡眠。

下面是 Linux 2.6 内核中迁移服务线程 `migration_thread` 的例子（`linux-2.6.11/kernel/sched.c: 4254`），可以看到它遵循了同样的模式：

```c
/* Wait for kthread_stop */
set_current_state(TASK_INTERRUPTIBLE);
while (!kthread_should_stop()) {
        schedule();
        set_current_state(TASK_INTERRUPTIBLE);
}
__set_current_state(TASK_RUNNING);
return 0;
```

这段代码不断地检查 `kthread_should_stop()`，直到它返回真才退出循环，也就是说只要 `kthread_should_stop()` 返回假该进程就会一直睡眠。检查 `kthread_should_stop()` 确实是在进程的状态被置为 `TASK_INTERRUPTIBLE` 后才开始执行的，因此，如果在条件检查之后但是在 `schedule()` 之前有其他进程试图唤醒它，那么该进程的唤醒操作不会失效。

### 小结

在 Linux 中避免进程无效唤醒的关键是：在进程检查条件之前就将进程的状态置为 `TASK_INTERRUPTIBLE` 或 `TASK_UNINTERRUPTIBLE`，并且如果检查的条件满足的话就应该将其状态重新设置为 `TASK_RUNNING`。这样无论进程等待的条件是否满足，进程都不会因为被移出就绪队列而错误地进入睡眠状态，从而避免了无效唤醒问题。

## 参考

- [quant67.com：Linux Task Status](https://quant67.com/post/linux/taskstatus.html)
- 「竞争条件与无效唤醒」一节作者：chumojing，原文地址：[http://blog.chinaunix.net/uid-12461657-id-3178775.html](http://blog.chinaunix.net/uid-12461657-id-3178775.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-14 | 文件由 `进程状态.md` 重命名为 `process-state.md`，补充 url: `process-state`；标题改为「Linux Process State, 进程状态」；`categories` 由 `inbox` 改为 `Linux`；所有代码块补充 `c`/`bash` 语言标识（原文完全没有代码围栏）；进程状态列表、procfs 对照表改写为 Markdown 表格；修复"real ≠ user + sys"一处因排版问题被拆成逐字符换行的乱码；数字编号小标题（如"2 TASK_RUNNING"）改为规范的二级/三级标题；新增「竞争条件与无效唤醒（missed wakeup）」一节，内容整理自 `调度策略.md` 末尾「Linux 进程的睡眠和唤醒」一节 | 调度器相关文章整理时发现 `调度策略.md` 的无效唤醒内容与本文主题（进程睡眠状态）高度相关，且本文当时缺少这部分内容，遂合并进来，避免维护两份重复主题的文章；顺带修复本文长期存在的代码块无语言标识、乱码等格式问题 |
