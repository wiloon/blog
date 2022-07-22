---
title: json tool, jq command
author: "-"
date: 2020-04-19T13:17:58+00:00
url: /?p=16004
categories:
  - Inbox
tags:
  - reprint
---
## json tool, jq command

<https://stedolan.github.io/jq/>

<https://stedolan.github.io/jq/download/>

```bash
jq ".[0]|.releases| .[0]|.downloads.linux.link"
cat foo.txt|jq '.checklists|.[0]|.checkItems|.[].name'
cat foo.txt|jq '.checklists|.[0]|.checkItems|.[]|if .state == "incomplete" then .name else "" end'|grep -v '""'
```

jq 可以对 json 数据进行分片、过滤、映射和转换

jq 是用 C 编写，没有运行时依赖，所以几乎可以运行在任何系统上。预编译的二进制文件可以直接在Linux、OS X和windows系统上运行，当然在linux和OS X系统你需要赋与其可执行权限；在linux系统中也可以直接用yum安装。
下载页面：

## `.`

最简单的表达式 `.`，格式化输出

## `[index]`

输出列表中的第一个元素，可以使用`[0]`：

cat json.txt | jq '.[0]'

## 管道符 |

cat json.txt | jq '.[0] | .name '

### json格式化

```bash
echo '{"kind": "Service", "apiVersion": "v1", "status": {"loadBalancer": true}}' | jq .
{
  "kind": "Service",
  "apiVersion": "v1",
  "status": {
    "loadBalancer": true
  }
}
```

## jq 生成 json 字符串

```bash
BUCKET_NAME=testbucket
OBJECT_NAME=testworkflow-2.0.1.jar
TARGET_LOCATION=/opt/test/testworkflow-2.0.1.jar

JSON_STRING=$(jq -n \
                  --arg bucketname "$BUCKET_NAME" \
                  --arg objectname "$OBJECT_NAME" \
                  --arg targetlocation "$TARGET_LOCATION" \
                   '$ARGS.named')

jq -n \
--arg foo "bar" \
--arg bar "foo" \
  '$ARGS.named'
```

- --null-input | -n, 禁止 jq 读取输入, 在用 jq 生成 json 字符串时需要用这个选项把输入置空.
- --arg name value, 定义变量
- Named arguments are also available to the jq program as $ARGS.named.

<https://stackoverflow.com/questions/48470049/build-a-json-string-with-bash-variables>

作者: 网易云
链接: https://www.zhihu.com/question/20057446/answer/489588448
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

作者：软件测试技能栈
链接：<https://www.jianshu.com/p/6de3cfdbdb0e>
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

<https://www.jianshu.com/p/6de3cfdbdb0e>

<https://justcode.ikeepstudying.com/2018/02/shell%EF%BC%9A%E6%97%A0%E6%AF%94%E5%BC%BA%E5%A4%A7%E7%9A%84shell%E4%B9%8Bjson%E8%A7%A3%E6%9E%90%E5%B7%A5%E5%85%B7jq-linux%E5%91%BD%E4%BB%A4%E8%A1%8C%E8%A7%A3%E6%9E%90json-jq%E8%A7%A3%E6%9E%90-json/>