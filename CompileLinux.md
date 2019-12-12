## Compiling Linux
I am using
"[Building a custom kernel from Debian kernel source](https://kernel-team.pages.debian.net/kernel-handbook/ch-common-tasks.html#s-common-building)"
to compile a Linux kernel with `CONFIG_STRICT_DEVMEM=n`. The Linux version I
compiled is 4.9.189.

Following the instructions, at the step of `make nconfig`, go to "Kernel
hacking" and uncheck "Filter access to /dev/mem" (at about line 50). Then
the `CONFIG_STRICT_DEVMEM` macro will be set correctly.

