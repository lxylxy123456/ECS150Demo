## Compiling Linux

### Debian
I am using
"[Building a custom kernel from Debian kernel source](https://kernel-team.pages.debian.net/kernel-handbook/ch-common-tasks.html#s-common-building)"
to compile a Linux kernel with `CONFIG_STRICT_DEVMEM=n`. The Linux version I
compiled is 4.9.189.

Following the instructions, at the step of `make nconfig`, go to "Kernel
hacking" and uncheck "Filter access to /dev/mem" (at about line 50). Then
the `CONFIG_STRICT_DEVMEM` macro will be set correctly.

Steps:
```
sudo apt-get install linux-source-4.9 libncurses5-dev libncursesw5-dev
tar xaf /usr/src/linux-source-4.9.tar.xz
cd linux-source-4.9/
make nconfig
make clean
time make deb-pkg
dpkg -i ../linux-image-4.9.189_4.9.189-1_amd64.deb
shutdown -r now
```

### Fedora
Reference links:
* [https://docs.fedoraproject.org/en-US/quick-docs/kernel/build-custom-kernel/](https://docs.fedoraproject.org/en-US/quick-docs/kernel/build-custom-kernel/)
* [https://fedoraproject.org/wiki/Building_a_custom_kernel/Source_RPM](https://fedoraproject.org/wiki/Building_a_custom_kernel/Source_RPM)

Steps:
```
$ git clone git://git.kernel.org/pub/scm/linux/kernel/git/jwboyer/fedora.git
$ cd fedora
$ make nconfig
$ time make rpm-pkg
$ dnf install ~/rpmbuild/RPMS/x86_64/kernel-5.0.0+-1.x86_64.rpm
```

Note:
* The git repository I cloned was at commit 3717f613f48d. 
* The kernel package downloaded is called "kernel-5.0.0+.tar.gz". 
* At `make nconfig`, go to "Kernel hacking" and uncheck "Filter access to
  /dev/mem" (same as in Debian)
