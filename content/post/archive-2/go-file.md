---
title: go file
author: "-"
date: 2017-10-31T03:11:46+00:00
url: /?p=11343
categories:
  - Inbox
tags:
  - reprint
---
## go file

```go
if srcFile, err = os.Open(localPath); err != nil {
		logger.Errorf("failed to read src file: %v", err)
		return
	}
defer srcFile.Close()
fileInfo, err := srcFile.Stat()
	fileSize := fileInfo.Size() // file size

os.PathSeparator

file, _ := os.Getwd()

log.Println("current path:", file)

file, _ = exec.LookPath(os.Args[0])
log.Println("exec path:", file)

dir,_ := path.Split(file)
log.Println("exec folder relative path:", dir)

os.Chdir(dir)
wd, _ := os.Getwd()
log.Println("exec folder absolute path:", wd)

```

## 文件复制进度

[https://go.dev/play/p/N6xL8_fnV2](https://go.dev/play/p/N6xL8_fnV2)
