---
title: angular material
author: "-"
date: 2019-06-08T08:38:12+00:00
url: /?p=14477
categories:
  - Inbox
tags:
  - reprint
---
## angular material

```bash
yarn add @angular/material @angular/cdk @angular/animations

app.module.ts

import { MatSliderModule } from '@angular/material/slider';
  
import 'hammerjs';
  
…
  
@NgModule ({....

imports: [...,

MatSliderModule,
  
…]
  
})
```

app.component.html
  
<mat-slider min="1" max="100" step="1" value="1"></mat-slider>

styles.css

@import '@angular/material/prebuilt-themes/deeppurple-amber.css';

<https://material.angular.io/>
  
<https://material.angular.cn/guides>
  
<https://github.com/stbui/angular-material-app/tree/master/src/app>
  
<https://material.io/>
  
<https://material.angular.io/components/categories>
