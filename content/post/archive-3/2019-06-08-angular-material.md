---
title: angular material
author: wiloon
type: post
date: 2019-06-08T08:38:12+00:00
url: /?p=14477
categories:
  - Uncategorized

---
```bash
yarn add @angular/material @angular/cdk @angular/animations
```

app.module.ts

import { MatSliderModule } from &#8216;@angular/material/slider&#8217;;
  
import &#8216;hammerjs&#8217;;
  
…
  
@NgModule ({&#8230;.
    
imports: [&#8230;,
    
MatSliderModule,
  
…]
  
})

app.component.html
  
<mat-slider min="1" max="100" step="1" value="1"></mat-slider>

styles.css
    
@import &#8216;@angular/material/prebuilt-themes/deeppurple-amber.css&#8217;;

https://material.angular.io/
  
https://material.angular.cn/guides
  
https://github.com/stbui/angular-material-app/tree/master/src/app
  
https://material.io/
  
https://material.angular.io/components/categories