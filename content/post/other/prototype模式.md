---
title: 原型模式 Prototype
author: "-"
date: 2012-10-10T03:25:48+00:00
url: /?p=4418
categories:
  - pattern
tags:
  - DesignPattern

---
## 原型模式 Prototype
Prototype模式是一种对象创建型模式，它跟工厂模式，Builder模式等一样，都用来创建类的实例对象。

但Prototype模式的对象创建方法，**具有以下特点: **
  
- 由原型对象自身创建目标对象。也就是说，对象创建这一动作发自原型对象本身。
  
- 目标对象是原型对象的一个克隆。也就是说，通过Prototype模式创建的对象，不仅仅与原型对象具有相同的结构，还与原型对象具有相同的值。
  
- 根据对象克隆深度层次的不同，有浅度克隆与深度克隆。

简单一点说，
  
**Prototype模式提供一种方法，让类的对象可以实现对自身的复制。**


  Prototype模式的应用场景: 

- 在创建对象的时候，我们不只是希望被创建的对象继承其基类的基本结构，还希望继承原型对象的数据。
  
- 希望对目标对象的修改不影响既有的原型对象 (深度克隆的时候可以完全互不影响) 。
  
- 隐藏克隆操作的细节。很多时候，对对象本身的克隆需要涉及到类本身的数据细节。

现实生活中，就有许多这样的例子: 
  
生物细胞的自身复制；根据产品模型生产产品等等


  Prototype模式的模型定义: 

Prototype {
  
+clone():Prototype
  
}
  
即: 原型类Prototype 提供clone()方法，实现对对象自身的复制 (克隆) 。


  Prototype模式的实现范例

下面我们使用Prototype模式来实现细胞 (Cell) 的自身复制过程。
  
Java语言提供了对象复制的机制，Prototype模式的Java实现一般也通过实现Cloneable接口来实现。
  
这里我们也通过实现Cloneable接口来说明Prototype模式。
  
    
      
        public   class  Cell  implements  Cloneable {
      
      
            //细胞壁
      
      
            private  String cellWall;
      
      
            //细胞膜
      
      
            private  String cellMembrane;
      
      
            //细胞组织
      
      
            private  String cellularTissue;
      
      
      
      
            ...//这里省略掉了对成员变量的setter/getter方法的定义
      
      
      
      
            //细胞的自身复制
      
      
            //这里重载了Obect#clone()方法，为了方便外部调用，把返回值由Object修改为Cell，并把访问级别设置为public
      
      
            public  Cell clone() {
      
      
                try  {
      
      
                    //只需简单地调用super.clone();即可
      
      
                    return  (Cell) super .clone();
      
      
                } catch  (CloneNotSupportedException e) {
      
      
                    throw  ( new  InternalError(e.getMessage()));
      
      
                }
      
      
            }
      
      
      
      
        }
      
      
      
      
        //调用方: 
      
      
        public   class  Client {
      
      
            public   static   void  main(String[] args) {
      
      
                //准备原型细胞
      
      
                Cell cell = new  Cell();
      
      
                cell.setCellWall("cell wall 1" );
      
      
                ...
      
      
                //克隆原型细胞
      
      
                Cell clonedCell = cell.clone();
      
      
                ...
      
      
                //操作被克隆的细胞 (略) 
      
      
            }
      
      
        }
      
    
  

这里使用了一个简单的例子说明了Prototype模式的对象创建过程与方法。里面省略了某些无关紧要的代码。