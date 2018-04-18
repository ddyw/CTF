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
