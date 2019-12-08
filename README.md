# ECS 150 Demo
* Some demo programs related to the operating systems class
  ([ECS 150](https://www.cs.ucdavis.edu/blog/ecs-150-operating-systems-system-programming/)). 

## Disclaimer
These demos are very likely to be OS and machine dependent. For example,
the memory page size of 4096 bytes is hard-coded. I only tested it on a Linux
4.9.189 x86_64 machine. Using other operating systems and CPU architectures
may result in error in the program.

## `page2frame`
This demo gets a memory page of a process in user space by directly reading
memory frame from the kernel space.

To run this demo, **you need a Linux kernel which is compiled with
`CONFIG_STRICT_DEVMEM=n`**. Or the last step of reading `/dev/mem` will fail.
For some hints on compiling, see below.

To run the demo, use:
```
sudo python3 page2frame.py | hexdump -C
```

The Python program, `page2frame.py`, will:
1. Compile the program `page2frame.c`, run it, and record its pid.
2. Read `/proc/[pid]/maps` and find index of the page with permission column
   `-w-p` (only writing permission). 
3. Check and print corresponding data in `/proc/kpagecount` and
   `/proc/kpageflags`.
4. Read the page in `/dev/mem`, and print it in binary form (can be read
   using `hexdump` or `xxd`).

The C program, `page2frame.c`, will:
1. `mmap` a memory page with only writing permission.
2. Fill the page with some specific pattern. Namely, some integers at the
   beginning and "EOF" at the end.
3. Print something (so that the Python program knows it has done with step
   1 and 2, and then go to sleep.

## `page_table`
This demo displays the virtual page table of a program. This program uses the
[graphviz](https://pypi.org/project/graphviz/) module in Python 3, which can be
installed using `pip`. You also need to install `graphviz` so that the `dot`
command is available. 

To run the demo, which shows the page table for `page2frame.c`, use:
```
python3 page_table.py /output/image.pdf
```

You can use any other formats that graphviz supports (e.g. `png`, `jpg`)

To view page table for some existing process with pid `[pid]`, use:
```
python3 page_table.py /output/image.pdf [pid]
```

Note: this program is still evolving.

## Compiling Linux
I am using
"[Building a custom kernel from Debian kernel source](https://kernel-team.pages.debian.net/kernel-handbook/ch-common-tasks.html#s-common-building)"
to compile a Linux kernel with `CONFIG_STRICT_DEVMEM=n`. The Linux version I
compiled is 4.9.189.

Following the instructions, at the step of `make nconfig`, go to "Kernel
hacking" and uncheck "Filter access to /dev/mem" (at about line 50). Then
the `CONFIG_STRICT_DEVMEM` macro will be set correctly.

## Sample page tables
Sample page table of `page2frame`:
![Page table sample](/images/page2frame.png)

`page2frame` in another system:
[pdf](/images/page2frame.pdf)

Page table of `find`:
[pdf](/images/find.pdf)
