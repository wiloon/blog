---
title: MACD
author: "-"
date: 2013-12-06T15:46:47+00:00
url: /?p=6015
categories:
  - Uncategorized
tags:
  - MT4

---
## MACD
指数平滑移动平均线（Moving Average Convergence and Divergence) 


平滑异同移动平均线即MACD指标。MACD称为指数平滑移动平均线，是从双移动平均线发展而来的，由快的移动平均线减去慢的移动平均线，MACD的意义和双移动平均线基本相同，但阅读起来更方便。当MACD从负数转向正数，是买的信号。当MACD从正数转向负数，是卖的信号。当MACD以大角度变化，表示快的移动平均线和慢的移动平均线的差距非常迅速的拉开，代表了一个市场大趋势的转变。

MACD在应用上应先行计算出快速（一般选12日) 移动平均值与慢速（一般选26日) 移动平均值。以这两个数值作为测量两者（快速与慢速线) 间的"差离值"依据。所谓"差离值"（DIF) ，即12日EMA数值减去26日EMA数值。因此，在持续的涨势中，12日EMA在26日EMA之上。其间的正差离值（+DIF) 会愈来愈大。反之在跌势中，差离值可能变负（-DIF) ，也愈来愈大。 至于行情开始回转，正或负差离值要缩小到怎样的程度，才真正是行情反转的信号。MACD的反转信号界定为"差离值"的9日移动平均值（9日EMA) 。 在MACD的指数平滑移动平均线计算公式中，都分别加T+1交易日的份量权值，以现在流行的参数12和26为例，其公式如下:  12日EMA的计算: EMA12 = 前一日EMA12 X 11/13 + 今日收盘 X 2/13 26日EMA的计算: EMA26 = 前一日EMA26 X 25/27 + 今日收盘 X 2/27 差离值（DIF) 的计算:  DIF = EMA12 - EMA26 然后再根据差离值计算其9日的EMA，即"差离平均值"，"差离平均值"用DEA来表示。 DEA = （前一日DEA X 8/10 + 今日DIF X 2/10)  计算出的DIF与DEA为正或负值，因而形成在0轴上下移动的两条快速与慢速线。为了方便判断，用DIF减去DEA，用以绘制柱状图。目前国内学习MACD指标的网站有新浪财经，MACD股票论坛，腾讯财经，网易财经，上上若水，里面资源众多，适合大家学习参考用！

MACD指标是由两线一柱组合起来形成，快速线为DIF，慢速线为DEA，柱状图为MACD。在各类投资中，有以下方法供投资者参考: 

1. 当DIF和MACD均大于0(即在图形上表示为它们处于零线以上)并向上移动时，一般表示为行情处于多头行情中，可以买入开仓或多头持仓;

2. 当DIF和MACD均小于0(即在图形上表示为它们处于零线以下)并向下移动时，一般表示为行情处于空头行情中，可以卖出开仓或观望。

3. 当DIF和MACD均大于0(即在图形上表示为它们处于零线以上)但都向下移动时，一般表示为行情处于下跌阶段，可以卖出开仓和观望;

4. 当DIF和MACD均小于0时(即在图形上表示为它们处于零线以下)但向上移动时，一般表示为行情即将上涨，股票将上涨，可以买入开仓或多头持仓。

指数平滑异同移动平均线，简称MACD，它是一项利用短期指数平均数指标与长期指数平均数指标之间的聚合与分离状况，对买进、卖出时机作出研判的技术指标,电子现货之家有详细介绍。


根据移动平均线原理所发展出来的MACD，一来克服了移动平均线假信号频繁的缺陷，二来能确保移动平均线最大的战果。

其买卖原则为: 

1.DIF、DEA均为正，DIFF向上突破DEA，买入信号参考。

2.DIF、DEA均为负，DIFF向下跌破DEA，卖出信号参考。

3.DEA线与K线发生背离，行情可能出现反转信号。

4.MACD的值从正数变成负数，或者从负数变成正数并不是交易信号，因为它们落后于市场。

计算方法


MACD是计算两条不同速度（长期与中期) 的指数平滑移动平均线（EMA) 的差离状况来作为研判行情的基础。

DIFF


⒈首先分别计算出收市价SHORT日指数平滑移动平均线与LONG日指数平滑移动平均线，分别记为EMA(SHORT) 与EMA(LONG) 。

⒉求这两条指数平滑移动平均线的差，即: DIFF=EMA（SHORT) －EMA（LONG) 

DEA


⒊再计算DIFF的M日的平均的指数平滑移动平均线，记为DEA。

MACD


⒋最后用DIFF减DEA，得MACD。MACD通常绘制成围绕零轴线波动的柱形图。

在绘制的图形上，DIFF与DEA形成了两条快慢移动平均线，买进卖出信号也就决定于这两条线的交叉点。很明显，MACD是一个中长期趋势的投资技术工具。缺省时，系统在副图上绘制SHORT=12，LONG=26，MID=9时的DIFF线、DEA线、MACD线（柱状线) 。

构造原理


MACD指标是基于均线的构造原理，对价格收盘价进行平滑处理（求出算术平均值) 后的一种趋向类指标。它主要由两部分组成，即正负差（DIF) 、异同平均数（DEA) ，其中，正负差是核心，DEA是辅助。DIF是快速平滑移动平均线（EMA1) 和慢速平滑移动平均线（EMA2) 的差。在现有的技术分析软件中，MACD常用参数是快速平滑移动平均线为12，慢速平滑移动平均线参数为26。此外，MACD还有一个辅助指标——柱状线（BAR) 。在大多数技术分析软件中，柱状线是有颜色的，在低于0轴以下是绿色，高于0轴以上是红色，前者表示趋势向下，后者表示趋势向上，柱状线越长，趋势越强。

下面我们来说一下使用MACD指标所应当遵循的基本原则: 

⒈当DIF和DEA处于0轴以上时，属于多头市场。

⒉当DIF和DEA处于0轴以下时，属于空头市场。

⒊柱状线收缩和放大。

⒋牛皮市道中指标将失真。

缺点


⒈由于MACD是一项中、长线指标，买进点、卖出点和最低价、最高价之间的价差较大。当行情忽上忽下幅度太小或盘整时，按照信号进场后随即又要出场，买卖之间可能没有利润，也许还要赔点价差或手续费。

⒉一两天内涨跌幅度特别大时，MACD来不及反应，因为MACD的移动相当缓和，比较行情的移动有一定的时间差，所以一旦行情迅速大幅涨跌，MACD不会立即产生信号，此时，MACD无法发生作用。

2运用技巧


应用原理


在大多数期货技术分析软件中，柱状线是有颜色的，在低于0轴以下是绿色，高于0轴以上是红色，前者表示趋势向下，后者表示趋势向上，柱状线越长，趋势越强。

⒈当DIF和DEA处于0轴以上时，属于多头市场。

⒉当DIF和DEA处于0轴以下时，属于空头市场。

⒊柱状线收缩和放大。

⒋形态和背离情况。

⒌牛皮市道中指标将失真。

用DIF的曲线形状进行分析，主要是利用指标相背离的原则。具体为: 如果DIF的走向与股价走向相背离，则是采取具体行动的时间。但是，根据以上原则来指导实际操作，准确性并不能令人满意。经过实践、摸索和总结，综合运用5日、10日均价线，5日、10日均量线和MACD，其准确性大为提高。

6.当 MACD 与Trigger 线均为正值，即在 0 轴以上时，表示大势仍处多头市场，趋势线是向上的。而这时柱状垂直线图（Oscillators) 是由 0 轴往上升延，可以大胆买进。

7.当 MACD 与 Trigger 线均为负值，即在 0 轴以下时，表示大势仍处空头市场，趋势线是向下的。而这时柱状垂直线图 (Oscillators) 是由 0 轴上往下跌破中心 0 轴，而且是在 0 轴下展延，这时应该立即卖出。

8.当 MACD 与K 线图的走势出现背离时，应该视为股价即将反转的信号，必须注意盘中走势。

就其优点而言，MACD 可自动定义出股价趋势之偏多或偏空，避免逆向操作的危险。而在趋势确定之后，则可确立进出策略，避免无谓之进出次数，或者发生进出时机不当之后果。MACD 虽然适于研判中期走势，但不适于短线操作。再者，MACD 可以用来研判中期上涨或下跌行情的开始与结束，但对箱形的大幅振荡走势或胶灼不动的盘面并无价值。同理，MACD用于分析各股的走势时，较适用于狂跌的投机股，对于价格甚少变动的所谓牛皮股则不适用。总而言之，MACD 的作用是从市场的转势点找出市场的超买超卖点。

经典用法


一. 顺势操作-金叉/死叉战法

就是追涨杀跌，在多头市场时金叉买入，在空头市场时死叉卖出.

二. 逆市操作-顶底背离战法

就是逃顶抄底，在顶背离时卖空，在底背离时买多.

在一轮多头行情中，价格是创新高后还有新高，均线是完美的多头排列，光看价格和均线似乎上涨行情会没完没了. 然而，当市场情绪完全被当前趋势所感染的时候，市场往往已经运行在第五浪了.这时候上涨空间有限，而下行空间无限. 而用MACD的头肩顶模式（右肩背离) ----是一帖有效的清醒剂，往往可以提醒投机者行情随时有结束的可能性.

实战战法


一、"MACD低位两次金叉"

首先是"MACD低位两次金叉"出暴利机会。MACD指标的要素主要有红色柱、绿色柱、DIF指标、DEA指标。其中，当DIF、DEA指标处于O轴以下的时候，如果短期内（8或13个交易日内) 连续发生两次金叉，则发生第二次金叉的时候，可能发生暴涨。

使用"MACD低位二次金叉"寻找短线暴涨股，需注意下列事项: （一) MACD低位一次金叉的，未必不能出暴涨股，但"MACD低位二次金叉"出暴涨股的概率和把握更高一些。（二) "MACD低位二次金叉"出暴涨股的概率之所以更高一些，是因为经过"第一次金叉"之后，空头虽然再度小幅进攻、造成又一次死叉，但是，空头的进攻在多方的"二次金叉"面前，遭遇溃败。从而造成多头力量的喷发。（三) "MACD低位二次金叉"，如果结合K线形态上的攻击形态研判，则可信度将提高，操盘手盘中将更容易下决心介入。形成了"两阳吃一阴"，当天并且温和放量，综合研判的可信度明显增加。也即: "MACD低位二次金叉"和K线形态、量价关系可以综合起来考虑，以增加确信度。

二、MACD选股实际应用

在股市投资中，MACD指标作为一种技术分析的手段，得到了投资者的认知。但如何使用MACD指标，才能使投资收益达到最佳境界，却是知者甚微。技术分析作为股市一种投资分析的工具，有两大功能。首先是发现股市的投资机会，其次则是保护股市中的投资收益不受损失。在股市操作中，MACD指标在保护投资者利益方面，远超过它发现投资机会的功效，MACD指标作为中长期分析的手段，它所产生的交叉信号，对短线买卖比较滞后。MACD指标属于大势趋势类指标，它由长期均线DEA，短期均线DIF，红色能量柱（多头) ，绿色能量柱（空头) ，0轴（多空分界线) 五部分组成。它是利用短期均线DIF与长期均线DEA交叉作为信号。MACD指标所产生的交叉信号较迟钝，而作为制定相应的交易策略使用效果较好，具体使用方法如下: 

1 当DIF,DEA两数值位于0轴上方时，说明大势处于多头市场，投资者应当以持股为主要策略。若DIF由下向上与DEA产生交叉，并不代表是一种买入信号，而此时的大盘走势，已是一个短期高点，应当采用高抛低吸的策略。一般情况下，在交叉信号产生后的第二天或第三天，会有一个回调低点，此刻可以再行买入，达到摊低成本的目的。若DIF由上向下交叉DEA时，说明该波段上升行情已经结束，通常行情会在交叉信号产生后，有波像样的反弹，已确认短期顶部的形成，此时投资者可以借机平仓出局。在之后的调整中，利用随机指标KDJ，强弱指标RSI再伺机介入，摊低成本。若DIF第二次由下向上与DEA交叉，预示着将产生一波力度较大的上升行情，在交叉信号产生后，投资者应当一路持股，直到DIF再次由上向下交叉DEA时，再将所有的股票清仓，就可以扛着钱袋回家休息了。由于股市行情的变化多端，MACD指标常会与K线走势图呈背离的走势，通常称为熊背离。既K线走势图创出的第二个或第三个高点，MACD指标并不配合出现相应的高点，却出现相反的走势，顶点在逐步降低。此种现象应引起投资者的警觉，因为它预示着今后将有大跌行情产生，所以投资者宜采用清仓离场的策略，使自己的股票避免被套，资金避免受到损失。

2 当DIF与DEA两指标位于0轴的下方时，说明的大势属于空头市场，投资者应当以持币为主要策略。若DIF由上向下交叉DEA时，会产生一个调整低点。一般情况下，在此之后由一波反弹行情产生，这是投资者一次很好的平仓机会。在中国股市中，还没有建立作空机制，因此股市一旦进入空头市场，投资者最好的策略就是离场观望。投资者可以在股票贬值的同时，使手中的资金得到增值。若DIF由下向上交叉DEA时，会产生的一个高点，投资者应当果断平仓。这种信号的产生，一般以反弹的性质居多。在空头市场中，每次反弹都应当视为出货的最佳良机。尤其需要引起注意的是，若DIF第二次由上向下交叉DEA时，预示着今后会有一波较大的下跌行情产生。投资者应当在交叉信号产生后，坚决清仓出局。通常产生的这段下跌，属于波浪理论中的C浪下跌，是最具杀伤力的一波下跌。只有躲过C浪下跌，才可以说真正在股市中赚到了钱。在空头市场经过C浪下跌以后，偶尔也会发生MACD指标与K线走势图产生背离的现象，通常称为牛背离。既K线走势图出现第二或第三个低点，MACD指标并没有相应的低点产生，却出现一底高过一底的相反走势，这种现象的产生，预示着行情在今后会发生反转走势，投资者应当积极介入，因为市场根本没有风险。

3 当MACD指标作为单独系统使用时，短线可参考DIF走势研判。若DIF由上向下跌穿O轴时可看作大势可能步入空头市场，预示着大势将走弱，应当引起投资者的警觉。在空头市场中，投资者承受的风险高于收益。若MACD由上向下跌空O轴时，确认大势进入空头市场。投资者应采用离场观望的策略，以回避市场风险，使牛市中赚到的利润得到保障。若DIF由下向上穿越O轴时，可看作大势可能步入多头市场。预示着大势将走强，操作上应部分资金参与。若MACD由下向上穿越O轴时确认大势进入多头市场。投资者可以大胆持股，积极介入。在多头市场中，获得的收益高于承担的风险。

4在MACD指标中，红色能量柱和绿色能量柱，分别代表了多头和空头能量的强弱盛衰。它们对市场的反应，要比短期均线DIF在时间上提前。在MACD指标中，能量释入的过程，是一个循序渐近的过程，通常是呈逐渐放大的。在东方哲学中讲求，"阳盛则衰、阴盛则强"。在使用能量柱时，利用红色能量柱结合K线走势图就得出，当K线走势图近乎90度的上升，加之红色能量柱的快速放大，预示着大势的顶部已近。尤其是相邻的两段红色能量柱产生连片时，所爆发的行情将更加迅猛。反之，在空头市场中，这种现象也成立。在熟悉了这种操作手法后，对投资者逃顶和抄底将大有益处。

5在使用MACD指标过程中，有两点需要注意，第一，MACD指标对于研判短期顶部和底部，并不一定可信，只有结合中期乖离率和静态中的ADR指标，才可以判定。第二，利用周线中的MACD指标分析比日线的MACD指标效果好。

总之，在使用MACD指标时必须判定市场的属性。即市场是多头市场，还是空头市场。根据不同的市场属性，采取不同的操作策略，以回避风险，保障利润的目的。具体操作中，MACD的黄金交叉一般是重要的买入时机。首先，就其要点分析，当DIF和MACD两线在0轴之下且较远时由下行转为走平，且快线DIF上穿慢线MACD形成的金叉是较佳的短线买入时机，但必须注意DIF和MACD距离0轴远近的判断主要根据历史记录作为参考。而发生在0轴之上的金叉则不能离0轴太远，否则其可靠性将大大降低。比较倾向于在红海洋既红柱连成一片区，在0轴上方DIF正向交叉MACD形成金叉，其中线可靠性较好。同时这也符合强势市场机会多，弱势市场难赚钱的股市道理。

三、活用"探底器"，寻觅真底部

在此介绍一种利用MACD与30日均线配合起来寻找底部的办法，可剔除绝大多数的无效信号，留下最真最纯的买入信号。其使用法则: MACD指标中DIF线在0轴以下与MACD线金叉后没有上升至0轴以上，而是很快又与MACD线死叉，此时投资者可等待两线何时再重新金叉，若两线再度金叉（在0轴以下) 前后，30日平均线亦拐头上行，这表明底部构筑成功，随后出现一波行情的可能性较大。

四、MACD背离深探

MACD背弛抄底法（一) : 基础要点篇

MACD指标是最著名的趋势性指标，其主要特点是稳健性，这种指标不过度灵敏的特性对短线而言固然有过于缓慢的缺点，但正如此也决定其能在周期较长、数据数目较多行情中给出相对稳妥的趋势指向。若以此类推，将MACD在周相对较长的分时图如15分钟以上中尤其是在交易日午市运用，则可化长为短，成为几个交易内做短线的极佳工具。值得注意的是，在股票交易系统里，快速参数多取12日，慢速参数多取26日，这是因为中国股市在早期是一周6个交易日、一月平均26个交易日而如此沿袭下来，投资者可改为10和22。但基本差别不大，所以，之后也没引起重视而一直沿袭至今。指标背离原则是整个MACD运用的精髓所在，也是这个指标准确性较高的地方。其中细分为顶背弛和底背弛。其基础要点如下: 

⒈背弛形成原理: 往往是在市场多空中一方运行出现较长时期后出现的（图象上即为DIF和DEA交叉开口后呈近平行同向运行一段时间) ，因为这代表一方的力量较强，在此情况下往往容易走过了头，这种股价和指标的不对称就形成了背弛！

⒉背弛原点取值十分重要，强调要具有明显的高（低) 点性！注意要在同一上升（下降) 趋势里中取值，且在最高（低) 点之后运行一段（一般在下跌末段、股价与指标出现第三浪低点) 后才出现原点；

⒊连续性原则。注意: 1、必须在复权价位下运用指标；2、停牌阶段指标运动失效；3、涨跌停板指标失效。背弛是一种能量积累过程，只有震荡交易才能利于能量的积累与转换！故此，停牌期间MACD指标容易失灵！就形成方式看，只有以股价震荡盘升（跌) 方式形成的背弛具有较高的判顶（底) 信号，那种指标暴涨（跌) 后形成的背弛往往是反弹（回调) 行情。因为只有逐步震荡的方式才能是能量完全释放完毕而确立顶（底) 部，但暴动的方式却使市场一方扩大了发挥的范围，其之后至少还会出现多次背弛才能真正反转。

MACD背弛抄底法（二) : 底背弛三大常性

一、事不过三。在大跌行情中，底背弛低点后连续出现2次顺次的背弛时，基本可以确定下跌行情已快结束。但此时往往由于空头力量的顽强而向下假突破，指标也随其突破，虽然有可能打穿前两次背弛的底部，也即相对前两次没有形成背弛，但其和最初的背弛原点仍是形成了背弛，而且是第三次背弛，操作上反而可大胆反手操作抄底。三背弛后的反转行情幅度往往较大且安全性高，其中暴涨后期需要连续的大量支持。ST板块个股在下跌过程中的60分钟图就形成了明显的三背弛，从而也支持其反弹行情的展开。

二、对称原理。在股市中，对称原理的存在面很广，MACD背弛也不例外。一般而言，出现底背弛尤其是多次背弛之后的行情见顶多以成交或者股价顶背弛结束。因为底背弛代表能量的过分集中，在反弹行情展开后压抑的能量容易产生报复行情，而强大的惯性作用也就往往容易造成顶背弛。

三、形态分析。MACD属于趋势性指标，而传统形态分析中绝大部分也都是根据趋势理论逐步总结出来的，故此从原理上看两者有较大的共通性，这也决定了MACD底背弛也可用一般的形态理论进行分析，如头肩底、双底、三底、圆弧底、平台扎底等，此类形态分析中常用的量度幅度、阻力或支持位等评判理论也可适用，顶背弛则反之运用。如今年年初大盘产生反弹的原因之一，就是MACD刚好8月份以来形成三重底。

MACD背弛抄底法三: 寻找弹幅最大的底背弛！

背弛理论之所以受到关注，就是其能提前性预知反转的可能性。从本质意义上而言，背弛表明了股价超常运动，而回归正常水平的自然运动原理正是反转力量产生的内在原因，一旦反转力量积聚到足以抗衡原有趋势动力时，反转随即产生。由此可见，背弛中蕴藏的反转能量大小是反转行情潜力最关键的因素！

在股市中，运动能量最直接的表象就是幅度和成交量的合力！由于未来反弹中的成交量是很难提前预测，故此判断底背弛反弹潜力更主要还是取决于背弛过程中振幅的大小！一般而言，应积极寻找弹幅最大的底背弛，即: 在股价大跌中产生背弛原点后，因股价有所盘稳或反弹而使指标大幅反弹，但之后股价继续大幅下跌并创新低时，使指标再次打回原点水平，从而形成弹幅大的背弛形态！因为，指标弹幅大就好比弹性好的弹簧，在背弛时一时受到压制，但一旦取消压制，其自然继续爆发出良好的弹性！同时，由于弹簧最初弹动时并不需要外力的辅助就能自然完成，故此此类底背弛后的反弹行情初段往往是缩量展开的！反而到了相对高位再放量时，已表明有抛压出现，弹簧运动受到相反力量的压制，顶部即将出现。

例如: 大盘在8月份见到MACD背弛原点后，10月份以及2月份的下跌都形成了幅度较大的底背弛，反弹如期展开，而且幅度较客观，同时都是在高位出现大成交时开始进入顶部构筑阶段。

MACD背弛抄底法四: 背弛扎底放量反弹

扎底背弛出现的机会相对较少，但由于其出现后的反弹行情往往可观而值得关注。

此种背弛现象产生的特征有: 

⒈ 前期上升趋势中已产生多次顶背弛，一旦正式见顶将导致股价连续大幅跳水；

⒉ 在跳水后的盘跌过程中形成底背弛，但背弛过程振幅极小，形成扎底形态；

⒊ 扎底末段一旦出现放量则是正式反弹信号，反弹持续性强、幅度大；

⒋ 高位反弹一旦成交大幅缩小则反弹顶部逐步出现；

MACD背弛产生的本质原因在于逆反能量的囤积！就扎底背弛而言，其之前的上升趋势中顶背弛次数多而蕴藏的空头能量巨大，即使暴跌也难一次性释放作空动力，故此指标虽然见底并出现背弛原点，但仍被强大空方压制而只能窄幅震荡，此时底背弛蕴藏的多头能量就好比弹簧被绳子绑紧而在不断积蓄.但是，一旦空头能量施放完毕，且多头能量出现首次放大量反攻，意味着弹簧绑绳已被挑断，积蓄的多头动力使弹簧大幅弹开，故此形成连续反弹行情.由此可见，背弛扎底放量反弹操作策略最关键之处在于挑断绑绳的首次大放量反弹信号的出现！其之后的反弹成交其实正是积蓄的多头能量表征，从上述弹簧动能原理可知，在反弹过程中成交应该是逐步缩减的。但一旦在高位成交明显缩小，也表明弹簧反弹动能基本释放完毕，顶部即将出现.

例如: 深万山（000049) 在2001年初的跳水行情后的V型反弹过程中，MACD出现了明显的背弛扎底放量反弹！大盘连续下跌，投资者不妨积极留意背弛扎底股以作好下来的反弹行情！

MACD背弛抄底法五: MACD结合波浪理论抄底！

MACD指标和波浪理论都是著名的趋势类分析理论工具，其性质上的相同性也从原理上说明其运用中具有一定的共通性，结合起来运用效果往往更佳。从波浪理论多年的应用效果看，其最有价值的功效就在于指出一般5浪后会有3浪反转走势！若结合到运用MACD抄底中，也即当MACD出现明显的下跌5浪时，说明指标反弹即将出现，介入信号已相当明显。

从走势上看，此种情况下的MACD浪型特征主要有: 

⒈ 从1浪开跌到反弹2浪为止形成依次降低的两个高点，结合当时的上升或者走平股价而言，已经形成典型顶背弛；

⒉ 3浪到5浪属于下跌释放期，但5浪一旦形成，短线介入信号已发出。

⒊ 在相对较长的分时图如15分钟以上中尤其是在交易日午市运用，则可化长为短，成为几个交易内做短线的极佳工具。

一般而言，MACD结合波浪理论抄底在连续回调型整理中有较好的运用效果。如陕西金叶在9月初的短线回调中15分钟MACD就出现了明显的下跌5浪，之后反弹应声而起。而大盘30分钟图已是出现下跌3浪型，且与大低点形成背弛，故此一旦下跌5浪（大约在1540点左右) 完成，则反弹行情出现的可能性极大！具体到板块上，ST类大部分个股走势也已具有此特征，投资者不妨在超跌后关注。

MACD背弛抄底法六: 背弛陷阱

任何技术工具都有其独特优势之处，但优势有时也容易转化为缺陷，而这经常也成为庄家骗线制造陷阱的入手点！

MACD背弛在应用中虽然成功率比较高，但同样存在背弛陷阱的可能。其中主要表现在: 在连续暴跌后形成底背弛原点后，指标开始斜向上形成底背弛，但股价并没有因此而反弹，只是盘平甚至盘跌，而且在指标盘升到压力位后却继续向下突破，底背弛陷阱显现！值得注意的是，背弛陷阱之后再次出现的指标高级别底背弛，这往往就是真正的底部出现。最明显的例子就是8月到9月大盘暴跌后在市场一片企稳反弹呼声中，指数仍盘滑且MACD指标也开始盘升，但最终仍是继续暴跌到年初指标再次出现高级别底背弛时，中期底部才真正出现！同理，股价在连续暴涨后也容易出现类似的顶背弛陷阱。

究其原理，主要还是能量级别与指标反映程度难以配比有关。MACD运行主要特点就在于稳健性，但这恰恰暴露其在暴涨暴跌行情中的缺陷，即其对此类行情中蕴藏的能量无法靠一次性背弛就释放完毕， 进而需要多次背弛或者形成更高级别背弛后，才能给出真正的反转点信号。有鉴于此，投资者在股价连续暴跌暴涨同时MACD出现大开口突破之际，仍不适宜马上应用一般背弛原理进行反转操作，最好是等待出现多次背弛并重回低点形成高级别背弛后，再动手的安全性才较高。

五、大盘背离所发出的买卖信号

MACD主要用于对大势中长期的上涨或下跌趋势进行判断。当股价处于盘局或指数波动不明显时，MACD发出的买卖信号不是很明显，当股价在短时间内上下波动较大时，因MACD移动相当缓慢，所以不会立即对股价的变动产生买卖信号。现实当中运用最多的是利用其与大盘背离所发出的买卖信号，对大盘的未来趋势作出判断。然而MACD没有创出新高，相反出现了二次向下死叉，出现了顶背离，市场又一次发出了卖出信号。根据MACD的应用原则，高位出现二次向下死叉，其后都将有一波较大的跌势。抛开基本面不说，如果对这个重要的卖出信号也视而不见的话，那么市场留给你的将是无尽的痛苦和折磨了。

六、MACD最有效、最常用的逃顶方法

MACD最有效、最常用的逃顶方法。"第一卖点"形成之时，应该卖出或减仓。虚浪卖点或称绝对顶.

MACD最有效、最常用的逃顶方法 在实际投资中，MACD是指标不但具备抄底（背离是底) 、捕捉极强势上涨点（MACD连续二次翻红买入) 、捕捉"洗盘结束点"（上下背离买入) 的功能。这里介绍两种最有效、最常用的逃顶方法: 第一卖点或称相对顶 其含义是指股价在经过大幅拉升后出现横盘，从而形成的一个相对高点。

虚浪卖点或称绝对顶 判断绝对顶成立技巧是"价格、MACD背离卖出"，即当股价进行虚浪拉升创出新高时，MACD却不能同步创出新高，二者的走势产生背离，这是股价见顶的明显信号。必然说明的是在绝对顶卖股票时，决不能等MACD死叉后再卖，因为当MACD死叉时股价已经下跌了许多，在虚浪顶卖股票必须参考K线组合。

捕捉卖点


在股市投资中，MACD指标不但具备抄底（背离是底) 、捕捉极强势上涨点（MACD) 连续二次翻红买入、捕捉洗盘的结束点（上下背离买入) 的功能。运用MACD捕捉最佳卖点的方法如下: 

首先是调整MACD的有关参数，将MACD的快速E-MA参数设定为8，将慢速E-MA参数设定为13，将D IF参数设定为9，移动平均线参数分别为5、10、30。设定好参数后，便可找卖点。由于一个股票的卖点有许多，这里只给大家介绍两种最有效、最常用的逃顶方法: 

第一卖点或称相对顶 这是股价在经过大幅拉升后出现横盘，从而形成的一个相对高点，投资者尤其是资金最较大的投资者必须在第一卖点出货或减仓。判断第一卖点是否成立的技巧是"股价横盘、MACD死叉"，也就是说，当股价经过连续的上涨出现横盘时，5日、10日移动平均线尚未形成死*，但MACD率先死叉，死叉之日便是第一卖点形成之时，应该卖出或减仓。

虚浪卖点或称绝对顶 第一卖点形成之后有些股票价格并没有出现大跌，而是在回调之后主力为掩护出货假装向上突破。判断绝对顶成立的技巧是"价格与MACD背离"，即当股价进行虚浪拉升创出新高时，MACD却不能同步创出新高，二者走势产生背离，这是股价见顶的明显信号。说明在绝对顶卖股票时决不能等M ACD死叉后再卖，因为当MACD死*时股价已经下跌了许多，在虚浪顶卖股票必须参考K线组合。

最后需要提醒广大股民朋友的是，由于MACD指标具有滞后性，用MACD寻找最佳卖点逃顶特别适合那些大幅拉升后做平台的股票，没有进行过主升浪，那么不要用以上方法。

买卖策略


短线投资者的买卖策略: 

1.在移动平均汇聚背驰指针（MACD) 图表中，如DIF线由上向下转势，又或者DEA线由上向下转，则表示价位可能下跌，可考虑沽空。

2.反之，如DIF线由下向上转势，又或者DEA线由下向上转势，则表示价位可能上升，可考虑做多。

中短线投资者的买卖策略: 

1.在移动平均汇聚背驰指针（MACD) 图表中的一支支垂直线称为移动平均汇聚背驰指针（MACD) ，而绿色横线是柱状垂直线的分水岭，柱状垂直线出现在此分水岭之下，称为"负"，而出现在分水岭之上，则称为"正"。

2.对中短线投资者而言，当移动平均汇聚背驰指针（MACD) 柱状垂直线由负变正时，亦即垂直线由分水岭之下转为之上时，是做多讯号。如利用移动平均汇聚背驰指针（MACD) 来分析，则DIF线将会由下向上穿越DEA线。

3.反之，当柱状垂直线由正变负时，亦即垂直线由分水岭之上转为之下时，是做空讯号。同样地，DIF线将会由上向下穿越DEA线。

中线投资者的买卖策略: 

1.在移动平均汇聚背驰指针（MACD) 图表中，如DIF线和DEA线都处于零线之上，显示市况上升趋势未完。故DIF线和DEA线在零线之上向下转势，或者DIF线跌破DEA线，亦只能当作多头的平仓讯号。但如果DIF线是在零线之下，而跌破DEA线时，才能构成较为可靠的做空讯号。

2.反之，如果DIF线和DEA线都在零线之下，显示跌势未完。故此，DIF线和DEA线都在零线之下而向上转势时，或者DIF线升破DEA线，亦只能当作空头的平仓讯号。但如果DIF线是在零线之上，而升破DEA线，才能视作较为可靠的做多讯号。

短线实战


指标不是万能的，关键我们要怎么去运用才是正确的，在这里告诉你。研判大盘后市短线走向，应重点关注净买量、净卖量之间的辩证关系，以及净买量、净卖量搏斗之后的走向。在众多技术指标当中，MACD指标非常独特，用该指标预测盘面准确率很高。

一、MACD指标线: 

MACD指标中的MACD线(在股票软件中为黄颜色的线)，通常左右着后市的行进方向。而当该线经过较长时间的上涨之后，如出现上升角度变缓，甚至走平，则通常逢股指上涨时即是高抛良机。当该线经过较长时间的下跌勾头向上运行时，一旦股指回调至相对低点时，即是低吸良机。如股指走出阴线下跌,但MACD红柱却依然放大，因此预测大盘在次日将会止跌继续上涨。

二、研判净买量、净卖量之大小: 

伴随股价上升，如MACD指标红色柱状大幅度增高，超过前期股指相对高点时的红柱，而股指还未到达前期高点时，此时对短线后市应以看多为主。红柱增高表明净买量大，因此当短线上涨强度暂时受阻回落时，回调即是一个良好的买点，反之亦然。

三、如果MACD线勾头向上运行:

如果MACD线勾头向上运行,MACD红柱却较小，且股价也没有上涨，而只是横盘整理，则说明行情是假突破，应抛出手中股票。而当该线勾头向下，但绿柱较小，股价经过小幅下跌之后即止跌，则说明短线后市还有一个波段上扬行情会出现。

3组合指标运用


KDJ合作

市场最常用的技术指标是KDJ与MACD指标。KDJ指标是一种超前指标，运用上多以短线操作为主；而MACD又叫平滑异同移动平均线，是市场平均成本的离差值，一般反映中线的整体趋势。理论上分析，KDJ指标 的超前主要是体现在对股价的反映速度上，在80附近属于强势超买区，股价有一定风险；50为徘徊区；20附近则为较安全区域，属于超卖区，可以建仓，但由于其速度较快而往往造成频繁出现的买入卖出信号失误较多；MACD指标则因为基本与市场价格同步移动，使发出信号的要求和限制增加，从而避免了假信号的出现。这两者结合起来判断市场的好处是: 可以更为准确地把握住KDJ指标短线买入与卖出的信号。同时由于MACD指标的特性所反映的中线趋势，利用两个指标将可以判定股票价格的中、短期波动。

当MACD保持原有方向时，KDJ指标在超买或超卖状态下，股价仍将按照已定的趋势运行。因此在操作上，投资者可以用此判断市场是调整还是反转，同时也可以适当地回避短期调整风险，以博取短差。而观察该股，横盘调整已经接近尾声，可以看到MACD仍然在维持原有的上升趋势，而KDJ指标经过调整后也已在50上方向上即将形成金叉，预示着股价短线上依然有机会再次上扬。总的来说，对于短期走势的判断，KDJ发出的买卖信号需要用MACD来验证配合，一旦二者均发出同一指令，则买卖准确率将较高。

4一般研判标准


MACD指标是市场上绝大多数投资者熟知的分析工具，但在具体运用时，投资者可能会觉得MACD指标的运用的准确性、实效性、可操作性上有很多茫然的地方，有时会发现用从书上学来的MACD指标的分析方法和技巧去研判股票走势，所得出的结论往往和实际走势存在着特别大的差异，甚至会得出相反的结果。这其中的主要原因是市场上绝大多数论述股市技术分析的书中关于MACD的论述只局限在表面的层次，只介绍MACD的一般分析原理和方法，而对MACD分析指标的一些特定的内涵和分析技巧的介绍鲜有涉及。

MACD指标的一般研判标准主要是围绕快速和慢速两条均线及红、绿柱线状况和它们的形态展开。一般分析方法主要包括DIF指标和MACD值及它们所处的位置、DIF和MACD的交叉情况、红柱状的收缩情况和MACD图形的形态这四个大的方面分析。

一、DIF和MACD的值及线的位置

1. 当DIF和MACD均大于0（即在图形上表示为它们处于零线以上) 并向上移动时，一般表示为股市处于多头行情中，可以买入或持股；

2. 当DIF和MACD均小于0（即在图形上表示为它们处于零线以下) 并向下移动时，一般表示为股市处于空头行情中，可以卖出股票或观望。

3. 当DIF和MACD均大于0（即在图形上表示为它们处于零线以上) 但都向下移动时，一般表示为股票行情处于退潮阶段，股票将下跌，可以卖出股票和观望；

4. 当DIF和MACD均小于0时（即在图形上表示为它们处于零线以下) 但向上移动时，一般表示为行情即将启动，股票将上涨，可以买进股票或持股待涨。

二、DIF和MACD的交叉情况[1]

1. 当DIF与MACD都在零线以上，而DIF向上突破MACD时，表明股市处于一种强势之中，股价将再次上涨，可以加码买进股票或持股待涨，这就是MACD指标"黄金交叉"的一种形式。

2. 当DIF和MACD都在零线以下，而DIF向上突破MACD时，表明股市即将转强，股价跌势已尽将止跌朝上，可以开始买进股票或持股，这是MACD指标"黄金交叉"的另一种形式。

3. 当DIF与MACD都在零线以上，而DIF却向下突破MACD时，表明股市即将由强势转为弱势，股价将大跌，这时应卖出大部分股票而不能买股票，这就是MACD指标的"死亡交叉"的一种形式。

4. 当DIF和MACD都在零线以上，而DIF向下突破MACD时，表明股市将再次进入极度弱市中，股价还将下跌，可以再卖出股票或观望，这是MACD指标"死亡交叉"的另一种形式。

三、MACD指标中的柱状图分析

在股市电脑分析软件中（如钱龙软件) 通常采用DIF值减DEA（即MACD、DEM) 值而绘制成柱状图，用红柱状和绿柱状表示，红柱表示正值，绿柱表示负值。用红绿柱状来分析行情，既直观明了又实用可靠。

1. 当红柱状持续放大时，表明股市处于牛市行情中，股价将继续上涨，这时应持股待涨或短线买入股票，直到红柱无法再放大时才考虑卖出。

2. 当绿柱状持续放大时，表明股市处于熊市行情之中，股价将继续下跌，这时应持币观望或卖出股票，直到绿柱开始缩小时才可以考虑少量买入股票。

3. 当红柱状开始缩小时，表明股市牛市即将结束（或要进入调整期) ，股价将大幅下跌，这时应卖出大部分股票而不能买入股票。

4. 当绿柱状开始收缩时，表明股市的大跌行情即将结束，股价将止跌向上（或进入盘整) ，这时可以少量进行长期战略建仓而不要轻易卖出股票。

5. 当红柱开始消失、绿柱开始放出时，这是股市转市信号之一，表明股市的上涨行情（或高位盘整行情) 即将结束，股价将开始加速下跌，这时应开始卖出大部分股票而不能买入股票。

6. 当绿柱开始消失、红柱开始放出时，这也是股市转市信号之一，表明股市的下跌行情（或低位盘整) 已经结束，股价将开始加速上升，这时应开始加码买入股票或持股待涨。

大趋势的转变。


http://baike.baidu.com/view/1073868.htm?fromtitle=%E5%B9%B3%E6%BB%91%E5%BC%82%E5%90%8C%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF&fromid=1982903&type=syn

http://www.icbc.com.cn/ICBCCollege/client/page/KnowledgeDetail.aspx?ItemID=633787143353893914