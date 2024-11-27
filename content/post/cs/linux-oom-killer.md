---
title: 'Linux oom killer'
author: "-"
date: 2018-06-04T08:32:56+00:00
url: /?p=12273
categories:
  - Inbox
tags:
  - reprint
---
## 'Linux oom killer'

[https://blog.csdn.net/GugeMichael/article/details/24017515](https://blog.csdn.net/GugeMichael/article/details/24017515)

Linux - 内存控制之oom killer机制及代码分析
  
2014年04月18日 15:04:29
  
阅读数: 28048

最近,线上一些内存占用比较敏感的应用,在访问峰值的时候,偶尔会被kill掉,导致服务重启。发现是Linux的out-of-memory kiiler的机制触发的。

[http://linux-mm.org/OOM_Killer](http://linux-mm.org/OOM_Killer)

oom kiiler会在内存紧张的时候,会依次kill内存占用较高的进程,发送Sig15(SIGTERM)或Sig9(SIGKILL),取决于内核版本(可见uname -a,>= 2.6.32只会发送sigkill [https://elixir.free-electrons.com/linux/v2.6.18/source/mm/oom_kill.c),。并在/var/log/message中进行记录。里面会记录一些如pid,process](https://elixir.free-electrons.com/linux/v2.6.18/source/mm/oom_kill.c),。并在/var/log/message中进行记录。里面会记录一些如pid,process) name,cpu mask,trace等信息,通过监控可以发现类似问题。今天特意分析了一下oom killer相关的选择机制,挖了一下代码,感觉该机制简单粗暴,不过效果还是挺明显的,给大家分享出来。

oom killer初探

一个简单分配 heap memroy 的代码片段 (big_mm.c):
  
```c++
#define block (1024L_1024L_MB)
  
#define MB 64L
      
unsigned long total = 0L;
      
for(;;) {
          
// malloc big block memory and ZERO it !!
          
char\* mm = (char\*) malloc(block);
          
usleep(100000);
          
if (NULL == mm)
              
continue;
          
bzero(mm,block);
          
total += MB;
          
fprintf(stdout,"alloc %lum mem\n",total);
      
}
```

这里有2个地方需要注意:

1、malloc是分配虚拟地址空间,如果不memset或者bzero,那么就不会触发physical allocate,不会映射物理地址,所以这里用bzero填充
2、每次申请的block大小比较有讲究,Linux内核分为LowMemroy和HighMemroy,LowMemory为内存紧张资源,LowMemroy有个阀值,通过free -lm和

/proc/sys/vm/lowmem_reserve_ratio来查看当前low大小和阀值low大小。低于阀值时候才会触发oom killer,所以这里block的分配小雨默认的256M,否则如果每次申请512M(大于128M),malloc可能会被底层的brk这个syscall阻塞住,内核触发page cache回写或slab回收。

测试:

gcc big_mm.c -o big_mm ; ./big_mm & ./big_mm & ./big_mm &

(同时启动多个big_mm进程争抢内存)

启动后,部分big_mm被killed,在/var/log/message下tail -n 1000 | grep -i oom 看到:

```c++
  
Apr 18 16:56:16 v125000100.bja kernel: : [22254383.898423] Out of memory: Kill process 24894 (big_mm) score 277 or sacrifice child
  
Apr 18 16:56:16 v125000100.bja kernel: : [22254383.899708] Killed process 24894, UID 55120, (big_mm) total-vm:2301932kB, anon-rss:2228452kB, file-rss:24kB
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738942] big_mm invoked oom-killer: gfp_mask=0x280da, order=0, oom_adj=0, oom_score_adj=0
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738947] big_mm cpuset=/ mems_allowed=0
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738950] Pid: 24893, comm: big_mm Not tainted 2.6.32-220.23.2.ali878.el6.x86_64 #1
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738952] Call Trace:
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738961] [<ffffffff810c35e1>] ? cpuset_print_task_mems_allowed+0x91/0xb0
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738968] [<ffffffff81114d70>] ? dump_header+0x90/0x1b0
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738973] [<ffffffff810e1b2e>] ? __delayacct_freepages_end+0x2e/0x30
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738979] [<ffffffff81213ffc>] ? security_real_capable_noaudit+0x3c/0x70
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738982] [<ffffffff811151fa>] ? oom_kill_process+0x8a/0x2c0
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738985] [<ffffffff81115131>] ? select_bad_process+0xe1/0x120
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738989] [<ffffffff81115650>] ? out_of_memory+0x220/0x3c0
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.738995] [<ffffffff81125929>] ? __alloc_pages_nodemask+0x899/0x930
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.739001] [<ffffffff81159c6a>] ? alloc_pages_vma+0x9a/0x150
```

通过标红的部分可以看到big_mm占用了2301932K,anon-rss全部是mmap分配的大内存块。后面红色的CallTrace标识出来kernel oom-killer的stack,后面我们会针对该call trace分析一下oom killer的代码。

oom killer机制分析
  
我们触发了oom killer的机制,那么oom killer是计算出选择哪个进程kill呢？我们先来看一下kernel提供给用户态的/proc下的一些参数:

/proc/[pid]/oom_adj ,该pid进程被oom killer杀掉的权重,介于 [-17,15]之间,越高的权重,意味着更可能被oom killer选中,-17表示禁止被kill掉。

        /proc/[pid]/oom_score,当前该pid进程的被kill的分数,越高的分数意味着越可能被kill,这个数值是根据oom_adj运算后的结果,是oom_killer的主要参考。
    
        sysctl 下有2个可配置选项: 
    
                vm.panic_on_oom = 0         #内存不够时内核是否直接panic
                vm.oom_kill_allocating_task = 1        #oom-killer是否选择当前正在申请内存的进程进行kill
    
    
    
         触发oom killer时/var/log/message打印了进程的score:

Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758297] [ pid ] uid tgid total_vm rss cpu oom_adj oom_score_adj name
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758311] [ 399] 0 399 2709 133 2 -17 -1000 udevd
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758314] [ 810] 0 810 2847 43 0 0 0 svscanboot
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758317] [ 824] 0 824 1039 21 0 0 0 svscan
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758320] [ 825] 0 825 993 17 1 0 0 readproctitle
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758322] [ 826] 0 826 996 16 0 0 0 supervise
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758325] [ 827] 0 827 996 17 0 0 0 supervise
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758327] [ 828] 0 828 996 16 0 0 0 supervise
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758330] [ 829] 0 829 996 17 2 0 0 supervise
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758333] [ 830] 0 830 6471 152 0 0 0 run
  
Apr 18 16:56:18 v125000100.bja kernel: : [22254386.758335] [ 831] 99 831 1032 21 0 0 0 multilog

        所以,如果想修改被oom killer选中的概率,修改上树参数即可。

oom killer 代码分析

上面已经给出了相应策略,下面剖析一下kernel对应的代码,有个清晰认识。代码选择的是kernel 3.0.12的代码,源码文件 mm/oom_kill.c,首先看一下call trace调用关系:

__alloc_pages_nodemask分配内存 -> 发现内存不足(或低于low memory)out_of_memory -> 选中一个得分最高的processor进行select_bad_process -> kill

```c++
  
/**
   
* out_of_memory - kill the "best" process when we run out of memory
   
*/
  
void out_of_memory(struct zonelist *zonelist, gfp_t gfp_mask,
          
int order, nodemask_t *nodemask, bool force_kill)
  
{
      
// 等待notifier调用链返回,如果有内存了则返回
      
blocking_notifier_call_chain(&oom_notify_list, 0, &freed);
      
if (freed > 0)
          
return;

    // 如果进程即将退出,则表明可能会有内存可以使用了,返回  
    if (fatal_signal_pending(current) || current->flags & PF_EXITING) {  
        set_thread_flag(TIF_MEMDIE);  
        return;  
    }  
    
    // 如果设置了sysctl的panic_on_oom,则内核直接panic  
    check_panic_on_oom(constraint, gfp_mask, order, mpol_mask);  
    
    // 如果设置了oom_kill_allocating_task  
    // 则杀死正在申请内存的process  
    if (sysctl_oom_kill_allocating_task && current->mm &&  
        !oom_unkillable_task(current, NULL, nodemask) &&  
        current->signal->oom_score_adj != OOM_SCORE_ADJ_MIN) {  
        get_task_struct(current);  
        oom_kill_process(current, gfp_mask, order, 0, totalpages, NULL,  
                 nodemask,  
                 "Out of memory (oom_kill_allocating_task)");  
        goto out;  
    }  
    
    // 用select_bad_process()选择badness指  
    // 数(oom_score)最高的进程  
    p = select_bad_process(&points, totalpages, mpol_mask, force_kill);  
    
    
    if (!p) {  
        dump_header(NULL, gfp_mask, order, NULL, mpol_mask);  
        panic("Out of memory and no killable processes...\n");  
    }  
    if (p != (void *)-1UL) {  
        // 查看child process, 是否是要被killed,则直接影响当前这个parent进程   
        oom_kill_process(p, gfp_mask, order, points, totalpages, NULL,  
                 nodemask, "Out of memory");  
        killed = 1;  
    }  
    

out:

    if (killed)  
        schedule_timeout_killable(1);  
    

}

        select_bad_process() 调用oom_badness计算权值: 
    

```c++
  
/**
   
* oom_badness - heuristic function to determine which candidate task to kill
   
*
   
*/
  
unsigned long oom_badness(struct task_struct \*p, struct mem_cgroup \*memcg,
                
const nodemask_t *nodemask, unsigned long totalpages)
  
{
      
long points;
      
long adj;

    // 内部判断是否是pid为1的initd进程,是否是kthread内核线程,是否是其他cgroup,如果是则跳过  
    if (oom_unkillable_task(p, memcg, nodemask))  
        return 0;  
    
    p = find_lock_task_mm(p);  
    if (!p)  
        return 0;  
    
    // 获得/proc/[pid]/oom_adj权值,如果是OOM_SCORE_ADJ_MIN则返回  
    adj = (long)p->signal->oom_score_adj;  
    if (adj == OOM_SCORE_ADJ_MIN) {  
        task_unlock(p);  
        return 0;  
    }  
    
    // 获得进程RSS和swap内存占用  
    points = get_mm_rss(p->mm) + p->mm->nr_ptes +  
         get_mm_counter(p->mm, MM_SWAPENTS);  
    task_unlock(p);  
    
    // 计算步骤如下,【计算逻辑比较简单,不赘述了】  
    if (has_capability_noaudit(p, CAP_SYS_ADMIN))  
        adj -= 30;  
    adj *= totalpages / 1000;  
    points += adj;  
    
    return points > 0 ? points : 1;  
    

}

           总结,大家可以根据上述策略调整oom killer,禁止或者给oom_adj最小或偏小的值,也可以通过sysctl调节oom killer行为！！
