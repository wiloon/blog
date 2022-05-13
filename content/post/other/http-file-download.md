---
title: golang http 文件下载
author: "-"
date: 2014-02-26T06:23:12+00:00
url: /?p=6291
categories:
  - inbox
tags:
  - reprint
---
## golang http 文件下载

### golang + gin

```go
    c.Writer.WriteHeader(http.StatusOK)
    c.Header("Content-Disposition", fmt.Sprintf("attachment; filename=%s.bin", "foo"))
    c.Header("Content-Type", "application/octet-stream")
    c.Header("Content-Transfer-Encoding", "binary")
    c.Header("Accept-Ranges", "bytes")
    c.Header("Connection", "keep-alive")
    c.Header("Content-Length", fmt.Sprintf("%d", len(paramsBytes)))

    c.Writer.Write(paramsBytes)
```

### vuetify
```typescript
    import fileDownload from 'js-file-download'
    exportCsv (): void {
      Axios.get('/export',
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('JWT_TOKEN')
          },
          params: {
            foo: this.foo,
            start: this.dateStart + ' ' + this.timeStart,
            end: this.dateEnd + ' ' + this.timeEnd
          },
          responseType: 'blob'
        }).then(response => {
        const fileName = response.headers['content-disposition'].match(/filename=(.*)/)[1]
        console.log('data: ' + response.data)
        fileDownload(response.data, fileName)
      }).catch(error => {
        console.log({ error })
      })
    }
```

http://blog.csdn.net/androidmylove/article/details/8881573

查了好多资料,发现还是不全,干脆自己整理吧,至少保证在我的做法正确的,以免误导读者,也是给自己做个记录吧！

  // Ajax 文件下载
jQuery.download = function(url, data, method){
    // 获得url和data
    if( url && data ){ 
        // data 是 string 或者 array/object
        data = typeof data == 'string' ? data : jQuery.param(data);
        // 把参数组装成 form的  input
        var inputs = '';
        jQuery.each(data.split('&'), function(){ 
            var pair = this.split('=');
            inputs+='<input type="hidden" name="'+ pair[0] +'" value="'+ pair[1] +'" />'; 
        });
        // request发送请求
        jQuery('<form action="'+ url +'" method="'+ (method||'post') +'">'+inputs+'</form>')
        .appendTo('body').submit().remove();
    };
};


---

春蚕死去了,但留下了华贵丝绸；蝴蝶死去了,但留下了漂亮的衣裳；画眉飞去了,但留下了美妙的歌声；花朵凋谢了,但留下了缕缕幽香；蜡烛燃尽了,但留下一片光明；雷雨过去了,但留下了七彩霓虹。

文章结束给大家分享下程序员的一些笑话语录:  一个合格的程序员是不会写出 诸如 "摧毁地球" 这样的程序的,他们会写一个函数叫 "摧毁行星"而把地球当一个参数传进去。