---
title: Hibernate Validators
author: wiloon
type: post
date: 2012-03-27T06:24:34+00:00
url: /?p=2652
categories:
  - DataBase
  - Development

---
Annotations 是为域对象指定一个不变约束的便利而优雅的途径.例如通过它，你可以表示一个属性不应该是Null值，账户余额绝对不能是负值，等等。这些域模型的约束通过注释它的属性声明在bean自身。验证器可以读取这些注释并检查约束违反性。验证机制可以在没有重复这些规则的情况下在应用程序的不同层里执行(表示层，数据访问层).Hibernate验证器在遵循DRY规则的情况下设计.
  
Hibernate 验证器工作在两个级别。首先，它能检测位于内存的类实例的约束违反性.其次，它可以把约束应用在hibernate的元模型中并且把它们应用在生成的数据库中.
  
每一个约束注释都与一个为检查实体实例而实现的验证器对应关联。一个验证器也可以可选的应用约束到hibernate元模型，允许hibernate生成DDL来表达这些约束。利用合适的事件监听器，你可以通过hibernate在插入或更新的时候检查约束性。Hibernate验证器没有限定在必须配合hibernate执行验证。你也可以容易的把它用在其他java的持久化提供者上面(实现了实体监听器).
  
在运行期检查实例时，hibernate验证器把有关违反验证的信息放在一个InvalidValue类型的数组里返回.在其他信息中,InvalidValue所包含的错误描述消息可以嵌入参数值和注释绑定，并且消息字符串可以以资源文件的形式提供.

第一章 定义约束
  
1.1 什么是约束
  
约束是一个给定的元素(可以使field，property，或bean)所必须遵循的规则.规则的语义可以由注释表达。约束通常有一些属性用来参数化约束限制。这些约束应用到被注释的元素。

1.2 内建约束
  
与Hibernate 验证器一起内建了一些约束，他们已经覆盖了大多数基本的数据检查，当然我们后来会看到，你不一定使用它们，你可以在一分钟内写出你自己的约束。

@Length(min=, max=)
  
property (字符串)
  
检查是字符串长度范围
  
列长度被设置到最大

@Max(value=)
  
property (数字，或代表数字的字符串)
  
检查值是否=或min
  
在列上添加一个约束

@NotNull
  
property
  
是否null
  
列不为null

@NotEmpty
  
property
  
字符串不空或非NULl
  
链接不空或非null
  
对字符列非null约束

@Past
  
property (date 或 calendar)
  
检查是否日期在过去
  
在列上添加一个约束

@Future
  
property (date 或 calendar)
  
检查是否日期在将来

@Pattern(regex=&#8221;regexp&#8221;, flag=) or @Patterns( {@Pattern(&#8230;)} )
  
property (字符串)
  
检查是否属性匹配规则表达式给定的匹配标志 (see java.util.regex.Pattern )

@Range(min=, max=)
  
property (数字，或代表数字的字符串)
  
是否值min
  
在列上添加一个约束

@Size(min=, max=)
  
property (数组, 集合, map)
  
Min

@AssertFalse
  
property
  
检查方法计算到false (多用在代码里检查约束)

@AssertTrue
  
property
  
检查方法计算到true (多用在代码里检查约束)
  
none

@Valid

property (对象)

在一个关联对象上递归的执行检验.如果对象是一个数组或者集合，对象将被递归的检验. 如果对象是一个map，元素将被递归的验证.

none

@Email

property (String)

检查是否字符创符合email规范

none

@CreditCardNumber

property (String)

字符串是否一个格式好的信誉卡号码(derivative of the Luhn algorithm)

none

@Digits

property (数字，或代表数字的字符串)

数字是否符合整数部分和小数部分的精度

定义列精度和范围

@EAN

property (字符串)

字符是否是格式化的 EAN 或者 UPC-A 编码

none

@Digits

property (numeric or string representation of a numeric)

check whether the property is a number having up to integerDigits integer digits and fractionalDigits fractonal digits

define column precision and scale

1.3.错误消息

随Hibernate 验证器一起的有一个被翻译成十种语言的默认错误消息(如果没有你所在地区的语言，请发送给我们一个补丁)你可以通过创建一个ValidatorMessages.properties( ValidatorMessages_loc.properties )文件覆盖这些消息，甚至当你在写你的验证器注释的时候你可以添加你自己的消息集合。如果hibernate验证器在你的资源文件里或者ValidatorMessage里不能找到一个key的对应值，那么他将返回默认的内建值。

作为选择，当你程序化在一个bean上检查验证规则或者你要一个完全不同的修改机制时你可以提供一个资源绑定，你可以提供一个org.hibernate.validator.MessageInterpolator接口的实现。

1.4. 定义你的约束

扩展内建的约束集合非常容易，任何约束有两个固定的部分:约束描述器(注释)

和约束验证器(实现的类)下面是一个简单的用户定义的描述器，

@ValidatorClass(CapitalizedValidator.class)

@Target(METHOD)

@Retention(RUNTIME)

@Documented

public @interface Capitalized {

CapitalizeType type() default Capitalize.FIRST;

String message() default "has incorrect capitalization&#8221;

}

Type 是一个描述属性如何被使用的参数，这是一个用户的参数完全依赖注释业务

Message用来描述约束违反强制性的默认字符串，你可以硬编码或者部分或者全部利用资源绑定机制。参数值将被注入消息里面当{parameter}字符串被找到(在我们的例子Capitalization is not {type} 将产生 Capitalization is not FIRST )把所有字符串都放在属性文件ValidatorMessages.properties是个好的实践.

@ValidatorClass(CapitalizedValidator.class)

@Target(METHOD)

@Retention(RUNTIME)

@Documented

public @interface Capitalized {

CapitalizeType type() default Capitalize.FIRST;

String message() default "{validator.capitalized}&#8221;;

}

#in ValidatorMessages.properties

validator.capitalized = Capitalization is not {type}

然后你可以看见{}符号是递归的

为了链接一个描述器到他的验证器实现我们用@ValidatorClass元注释验证器类必须命名一个实现了Validator的类。

public class CapitalizedValidator

implements Validator, PropertyConstraint {

private CapitalizeType type;

//part of the Validatorcontract,

//allows to get and use the annotation values

public void initialize(Capitalized parameters) {

type = parameters.type();

}

//part of the property constraint contract

public boolean isValid(Object value) {

if (value==null) return true;

if ( !(value instanceof String) ) return false;

String string = (String) value;

if (type == CapitalizeType.ALL) {

return string.equals( string.toUpperCase() );

}

else {

String first = string.substring(0,1);

return first.equals( first.toUpperCase();

}

}

}

isValid()方法应该返回false如果约束已经被违反,更多的例子请参考内建验证器实现.

我们明白属性级别的验证,但是你可以写一个bean级别的验证注释。替代于接受返回的实例属性，bean自身将被传进验证器。为了激活验证检查，仅仅替代的注释bean自身。在单元测试里有一个小的例子。

如果你的约束可以在一些属性或者类型上被应用多次(用不同的参数)你可以用下面的注释形式

@Target(METHOD)

@Retention(RUNTIME)

@Documented

public @interface Patterns {

Pattern[] value();

}

@Target(METHOD)

@Retention(RUNTIME)

@Documented

@ValidatorClass(PatternValidator.class)

public @interface Pattern {

String regexp();

}

基本上，注释以一个验证器注释数组的形式包含值属性

1.5 注释域模型

由于你现在已经熟悉了注释，下面语法应该是非常熟悉的

public class Address {

private String line1;

private String line2;

private String zip;

private String state;

private String country;

private long id;

// a not null string of 20 characters maximum

@Length(max=20)

@NotNull

public String getCountry() {

return country;

}

// a non null string

@NotNull

public String getLine1() {

return line1;

}

//no constraint

public String getLine2() {

return line2;

}

// a not null string of 3 characters maximum

@Length(max=3) @NotNull

public String getState() {

return state;

}

// a not null numeric string of 5 characters maximum

// if the string is longer, the message will

//be searched in the resource bundle at key &#8216;long&#8217;

@Length(max=5, message=&#8221;{long}&#8221;)

@Pattern(regex=&#8221;[0-9]+&#8221;)

@NotNull

public String getZip() {

return zip;

}

// should always be true

@AssertTrue

public boolean isValid() {

return true;

}

// a numeric between 1 and 2000

@Id @Min(1)

@Range(max=2000)

public long getId() {

return id;

}

}

然而这个例子仅仅演示了共用的属性验证，你也可以以可见的形式注释

@MyBeanConstraint(max=45

public class Dog {

@AssertTrue private boolean isMale;

@NotNull protected String getName() { &#8230; };

&#8230;

}

也可以注释接口,hibernate验证器将检查所有实现此接口的子类或子接口通过一个给定的bean来读取合适的验证注释。

public interface Named {

@NotNull String getName();

&#8230;

}

public class Dog implements Named {

@AssertTrue private boolean isMale;

public String getName() { &#8230; };

}

Dog类的Name属性将被检查null约束

第一章 使用验证框架

Hibernate验证器有意被用来实现多层数据验证，这些数据约束位于仅一个地方(被注释的域模型)并且在应用的不同层被检查。

这章我们将涵盖hibernate验证器在不同层的使用

2.1数据库模式级别验证

Out of the box ,hibernate验证器将把你为你的实体定义的约束传进映射元数据，例如，如果你实体的一个属性被注释为@NotNull 他的列将被声明为 not null 在由hibernate生成的 DDL 里。

使用 hbm2ddl,域模型约束将被在数据库中表示。

如果 ，因为某些原因，这些特征需要禁用，设置

hibernate.validator.apply\_to\_ddl 为 false

2.2 ORM 集成

Hibernate 验证器与hibernate和所有纯java的持久化提供者集成。

2．2.1基于hibernate事件的验证

Hibernate验证器已经内置两个hibernate事件监听器，任何时候一个PreInsertEvent 或者 PreUpdateEvent事件发生，监听器将确认这个实例的所

有约束并且在当任何约束被违反的时候抛出一个异常。一般地，对象将在由hibernate进行的插入和更新前被检查。这个将被级联的应用。这是激活验证流程最方便和容易的途径。在验证违反发生时，事件将抛出一个包含了用来描述每个失败消息的InvalidValues类型的数组的InvalidStateException类型的运行期异常。

如果hibernate 验证器被放在类路径里，Hibernate Annonations(或Hibernate EntityManager)将透明的使用他，如果由于某些原因需要禁用这个集成特征设置hibernate.validator.autoregister_listeners 为 false

注意:如果beans没有用验证注释注释，将不会有运行时性能消耗

在这种情况下你需要手工为hibernate设置事件监听器，下面是配置

&#8230;

2.2.2 基于事件的java持久化验证

Hibernate 验证器与hibernate在基于事件的验证上没有关联，一个java持久化实体监听器是可用的。任何时候一个被监听的实体被持久化或者更新，hibernate验证器将确认所有此实体实例的约束并且在约束别违反的时候抛出异常，一般地，对象将在由java持久化提供者进行的插入和更新前被检查。这个将被级联的应用。在验证违反发生时，事件将抛出一个包含了用来描述每个失败消息的InvalidValues类型的数组的InvalidStateException类型的运行期异常。

如何使一个类可验证

@Entity

@EntityListeners( JPAValidateListener.class )

public class Submarine {

&#8230;

}

注意:与hibernate事件相比 java 持久化监听器有两个缺点。你需要为每个可验证的实体定义一个实体监听器。由你的提供者生成的DDL 将不会反射这些约束.

2.3 应用程序级别的验证

Hibernate 验证器可被应用到代码的任何地方

ClassValidator personValidator = new ClassValidator( Person.class );

ClassValidator addressValidator = new ClassValidator( Address.class, ResourceBundle.getBundle("messages&#8221;, Locale.ENGLISH) );

InvalidValue[] validationMessages = addressValidator.getInvalidValues(address);

前两行为类检查预备hibernate验证器，第一个的错误消息依赖于内嵌的hibernate验证器，第二个用一个资源文件的错误消息。执行一次并且缓存这些验证器实例是好的实践。

第三行实际上验证了address类的实例并且返回了一个InvalidValues类型的数组。应用程序逻辑将能重激活到失败。

你也可以检查一个属性而非整个bean 这对属性对属性的用户交互是有用的。

ClassValidator addressValidator = new ClassValidator( Address.class, ResourceBundle.getBundle("messages&#8221;, Locale.ENGLISH) );

//only get city property invalid values

InvalidValue[] validationMessages = addressValidator.getInvalidValues(address, "city&#8221;);

//only get potential city property invalid values

InvalidValue[] validationMessages = addressValidator.getPotentialInvalidValues("city&#8221;, &#8221;
  
Paris
  
")

2.4 表示层验证

当使用jsf和jboss seam 时，你可以触发验证流程在表示层使用seam的jsf标签

和让约束表示在模型里，违反出现在表示层。





  
    Country:
  



  
    Zip code:
  





不久将来，将添加Ajax4JSF 到循环将带来客户端验证利用一对附加的jsf标签，避免验证定义重复。请看jboss seam 更多信息。

2.5. 验证信息

作为一个验证信息携带者，hibernate提供了一个InvalidValue类型的数组，每一个InvalidValue 有许多方法来描述独立的发布

As a validation information carrier, hibernate provide an array of InvalidValue. Each InvalidValue has a buch of methods describing the individual issues.

getBeanClass() 得到失败的bean类型

getBean()retrieves the failing instance (if any ie not when using getPotentianInvalidValues())

getValue() retrieves the failing value

getMessage() retrieves the proper internationalized error message

getRootBean() retrieves the root bean instance generating the issue (useful in conjunction with @Valid), is null if getPotentianInvalidValues() is used.

getPropertyPath() retrieves the dotted path of the failing property starting from the root bean

原文来在：http://www.duduwolf.com/wiki/2007/345.html 注意：版权归原作者所有