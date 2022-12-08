---
title: angular 8, ngx-echarts, echart
author: "-"
date: 2019-07-28T15:09:46+00:00
url: /?p=14734
categories:
  - Inbox
tags:
  - reprint
---
## angular 8, ngx-echarts, echart

```bash
# 新建 angular项目后， 在项目目录下执行
yarn add echarts
yarn add ngx-echarts
yarn add @types/echarts -D
```

### src/app/app.module.ts

import { NgxEchartsModule } from 'ngx-echarts';
@NgModule({
  imports: [
    ...,
    NgxEchartsModule
  ],
})
export class AppModule { }

### angular.json

{
    ...
    projects
    //...
    project-name-0
    //...
    architect
    //...
            "scripts": [
              "node_modules/echarts/dist/echarts.min.js"
            ],
```

### app.component.ts

import {Component} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Tour of Heroes';
  public chartOption = {
    backgroundColor: '#2c343c',
    title: {
      text: 'Customized Pie',
      left: 'center',
      top: 20,
      textStyle: {
        color: '#ccc'
      }
    },

    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    visualMap: {
      show: false,
      min: 80,
      max: 600,
      inRange: {
        colorLightness: [0, 1]
      }
    },
    series: [
      {
        name: '访问来源',
        type: 'pie',
        radius: '55%',
        center: ['50%', '50%'],
        data: [
          {value: 335, name: '直接访问'},
          {value: 310, name: '邮件营销'},
          {value: 274, name: '联盟广告'},
          {value: 235, name: '视频广告'},
          {value: 400, name: '搜索引擎'}
        ],
        roseType: 'radius',
        label: {
          normal: {
            textStyle: {
              color: 'rgba(255, 255, 255, 0.6)'
            }
          }
        },
        labelLine: {
          normal: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            },
            smooth: 0.2,
            length: 10,
            length2: 20
          }
        },
        itemStyle: {
          normal: {
            color: '#c23531',
            shadowBlur: 200,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        animationType: 'scale',
        animationEasing: 'elasticOut'
      }
    ]
  };

}

```

### app.component.html

```xml
</div>
```

### app.component.css

.chart {
    height: 400px;
}

```

https://xieziyu.github.io/ngx-echarts/#/home
  
https://blog.csdn.net/qq_36822018/article/details/81504823
