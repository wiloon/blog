---
title: angular basic
author: wiloon
type: post
date: 2017-10-11T08:59:55+00:00
url: /?p=11249
categories:
  - Uncategorized

---
## install angular
### install nodejs
@see nodejs basic
### install yarn

    http://blog.wiloon.com/?p=11228
    yarn basic

<iframe title="&#8220;yarn basic&#8221; &#8212; w1100n" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://blog.wiloon.com/?p=11228&#038;embed=true#?secret=unR6OIow3j" data-secret="unR6OIow3j" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

# install angular cli
yarn global add @angular/cli
yarn add angular-in-memory-web-api --dev

ng config -g cli.packageManager yarn
add yarn global bin to $PATH

### angular command

# 创建工作区
ng new project0
# 创建组件
ng generate component heroes
# 创建组件 简写
ng g c heroes

ng generate component hero -it
# 创建service
ng generate service hero

ng serve --host 0.0.0.0 --port 4200 --open
ng build --aot
ng build --prod --build-optimizer

ng generate module app-routing --flat --module=app
# --flat 把这个文件放进了 src/app 中，而不是单独的目录中。
# --module=app 告诉 CLI 把它注册到 AppModule 的 imports 数组中。

https://github.com/aralroca/helloworld-angular-with-golang

yarn:

<blockquote class="wp-embedded-content" data-secret="hZsn0JuLwj">
  <p>
    <a href="http://blog.wiloon.com/?p=11228">yarn basic</a>
  </p>
</blockquote>

<iframe title="&#8220;yarn basic&#8221; &#8212; w1100n" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://blog.wiloon.com/?p=11228&#038;embed=true#?secret=hZsn0JuLwj" data-secret="hZsn0JuLwj" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

### 修改angular编译输出目录

<pre><code class="language-bash line-numbers">vim angular.json
...builder/outputPath
</code></pre>

### 结构型指令

\*ngFor 是一个 &#8220;结构型指令&#8221;。结构型指令会通过添加、删除和操纵它们的宿主元素等方式塑造或重塑 DOM 的结构。任何带有 \* 的指令都是结构型指令。

#### 把 *ngFor 指令加到

<

div> 上, *ngFor 会导致

<

div> 被列表中的每个商品都重复渲染一次。<pre data-language=HTML>

<code class="language-markup line-numbers">&lt;div *ngFor="let product of products"&gt;
&lt;/div&gt;
</code></pre> 

*ngIf

### 插值语法 {{}}

插值会把属性的值作为文本渲染出来。

### 绑定语法 []<pre data-language=HTML>

<code class="language-markup line-numbers">&lt;a [title]="product.name + ' details'"&gt;
</code></pre> 

插值表达式 {{}} 允许你把属性值渲染为文本；而属性绑定语法 [] 则允许你在模板表达式中使用属性值。

### 事件绑定

事件绑定是通过把事件名称包裹在圆括号 () 中完成的<pre data-language=HTML>

<code class="language-markup line-numbers">&lt;button (click)="share()"&gt;
</code></pre> 

### 双向数据绑定

[(ngModel)] 是 Angular 的双向数据绑定语法。<pre data-language=HTML>

<code class="language-markup line-numbers">import { FormsModule } from '@angular/forms';
&lt;input [(ngModel)]="hero.name" placeholder="name"/&gt;
</code></pre> 

https://zhuanlan.zhihu.com/p/27696268
  
https://medium.com/@anshap1719/getting-started-with-angular-and-go-setting-up-a-boilerplate-project-8c273b81aa6