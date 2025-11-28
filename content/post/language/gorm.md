---
title: gorm
author: "-"
date: 2013-06-20T06:57:46+00:00
url: gorm
categories:
  - Go
tags:
  - reprint
---
## gorm

```go
db.Table("go_service_info").Select("go_service_info.serviceId as service_id, go_service_info.serviceName as service_name, go_system_info.systemId as system_id, go_system_info.systemName as system_name").Joins("left join go_system_info on go_service_info.systemId = go_system_info.systemId").Scan(&results)

```

```go
db.Table("table0").
Select("table0.field0, table0.field1").
Joins("join table1 on table0.field0=table1.field0").
Where("table0.field0=? and table1.field1=?", foo, bar).
First(&obj)

```

[https://gorm.io/zh_CN/docs/index.html](https://gorm.io/zh_CN/docs/index.html)

[https://cloud.tencent.com/developer/article/1674450](https://cloud.tencent.com/developer/article/1674450)
