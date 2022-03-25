---
title: JVM 操作数栈 Operand Stack
author: "-"
date: 2012-09-19T08:53:36+00:00
url: /?p=4101
categories:
  - Java

tags:
  - reprint
---
## JVM 操作数栈 Operand Stack
<http://denverj.iteye.com/blog/1218359>

Like the local variables, the operand stack is organized as an array of words. But unlike the local variables, which are accessed via array indices, the operand stack is accessed by pushing and popping values. If an instruction pushes a value onto the operand stack, a later instruction can pop and use that value.

和局部变量区一样，操作数栈也是被组织成一个以字长为单位的数组。但是和前者不同的是，它不是通过索引来访问，而是通过标准的栈操作—压栈和出栈—来访问的。比如，如果某个指令把一个值压入到操作数栈中，稍后另一个指令就可以弹出这个值来使用。

The virtual machine stores the same data types in the operand stack that it stores in the local variables: int,long, float, double, reference, and returnType. It converts values of type byte, short, and char to int before pushing them onto the operand stack.

虚拟机在操作数栈中存储数据的方式和在局部变量区中是一样的: 如int、long、float、double、reference和returnType的存储。对于byte、short以及char类型的值在压入到操作数栈之前，也会被转换为int。

Other than the program counter, which canít be directly accessed by instructions, the Java Virtual Machine has no registers. The Java Virtual Machine is stack-based rather than register-based because its instructions take their operands from the operand stack rather than from registers. Instructions can also take operands from other places, such as immediately following the opcode (the byte representing the instruction) in the bytecode stream, or from the constant pool. The Java Virtual Machine instruction set's main focus of attention, however, is the operand stack.

不同于程序计数器，Java虚拟机没有寄存器，程序计数器也无法被程序指令直接访问。Java虚拟机的指令是从操作数栈中而不是从寄存器中取得操作数的，因此它的运行方式是基于栈的而不是基于寄存器的。虽然指令也可以从其他地方取得操作数，比如从字节码流中跟随在操作码 (代表指令的字节) 之后的字节中或从常量池中，但是主要还是从操作数栈中获得操作数。

The Java Virtual Machine uses the operand stack as a work space. Many instructions pop values from the operand stack, operate on them, and push the result. For example, the iadd instruction adds two integers by popping two ints off the top of the operand stack, adding them, and pushing the int result. Here is how a Java Virtual Machine would add two local variables that contain ints and store the int result in a third local variable:

虚拟机把操作数栈作为它的工作区——大多数指令都要从这里弹出数据，执行运算，然后把结果压回操作数栈。比如，iadd指令就要从操作数栈中弹出两个整数，执行加法运算，其结果又压回到操作数栈中，看看下面的示例，它演示了虚拟机是如何把两个int类型的局部变量相加，再把结果保存到第三个局部变量的: 

begin

iload_0 // push the int in local variable 0 onto the stack

iload_1 // push the int in local variable 1 onto the stack

iadd // pop two ints, add them, push result

istore_2 // pop int, store into local variable 2

end

In this sequence of bytecodes, the first two instructions, iload_0 and iload_1, push the ints stored in local variable positions zero and one onto the operand stack. The iadd instruction pops those two int values, adds them, and pushes the int result back onto the operand stack. The fourth instruction, istore_2, pops the result of the add off the top of the operand stack and stores it into local variable position two. In Figure 5-10, you can see a graphical depiction of the state of the local variables and operand stack while executing the above instructions. In this figure, unused slots of the local variables and operand stack are left blank.

在这个字节码序列里，前两个指令iload_0和iload_1将存储在局部变量中索引为0和1的整数压入操作数栈中，其后iadd指令从操作数栈中弹出那两个整数相加，再将结果压入操作数栈。第四条指令istore_2则从操作数栈中弹出结果，并把它存储到局部变量区索引为2的位置。