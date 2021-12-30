---
title: ruby helloworld
author: "-"
date: 2012-08-01T06:48:44+00:00
url: /?p=3883
categories:
  - Development

---
## ruby helloworld
**Question**: I would like to understand the basics of how to write and execute a **ruby program** on Linux OS. Can you explain it with a simple example?

**Answer**: In this article, let us review very quickly how to write a basic **Hello World ruby program** and execute *.rb program on Linux or Unix OS.

### 1. Write a Hello World Ruby Program

Create the helloworld.rb program using a Vim editor as shown below.

```bash
  
$ vim helloworld.rb

#!/usr/bin/ruby

# Hello world ruby program

puts "Hello World!";
  
```

### 2. Verify ruby Interpreter availability

Make sure ruby interpreter is installed on your system as shown below.

```bash
  
$ whereis ruby
  
ruby: /usr/bin/ruby /usr/bin/ruby1.8 /usr/lib/ruby /usr/share/man/man1/ruby.1.gz

$ which ruby
  
/usr/bin/ruby
  
```

### Installing Ruby

If you don't have Ruby, install it as shown below.

```bash
  
$ sudo apt-get install ruby
  
```

### 

### 3. Execute Ruby Program

You can either execute using "ruby helloworld.rb" or "./helloworld.rb".

  ```bash
 $ ruby helloworld.rb
 Hello World!
 ``` 
  
    ( or )
 ```bash
 $ chmod u+x helloworld.rb
  
  
    $ ./helloworld.rb
 Hello World!
 ```
  
  
    Note: As Ruby is an interpreted language, you don't have the compilation step similar to the C program.
  
  
    Executing Ruby one liner
  
  
    You can also execute Ruby from the command line as shown below. This will print Hello World!.
  
  
    ```bash
 $ ruby -e 'puts "Hello World!n"'
 ```
  
  
    http://www.thegeekstuff.com/2009/10/ruby-hello-world-example-how-to-write-and-execute-ruby-program-on-unix-os/
  