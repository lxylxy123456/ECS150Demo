#  
#  ECS150Demo - Some demo programs related to the operating systems class
#  Copyright (C) 2019  lxylxy123456
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#  

'''
	Access system memory frame from process page information
'''

import os, sys, re, time, struct
from subprocess import Popen

EXEC_NAME = 'page2frame'
PAGE_SIZE = 4096		# Use `getconf PAGE_SIZE`
PAGEMAP_ENTRY = 8		# 64 bits
KPAGECOUNT_ENTRY = 8	# 64 bits
KPAGEFLAGS_ENTRY = 8	# 64 bits
KPF_MMAP = 11
KPF_ANON = 12

def print_w_mem(pid) :
	'Print the only memory region in the program with permission -w-p'
	# Read /proc/[pid]/maps, get virtual page location. See proc(5)
	write_only = []
	for i in open('/proc/%d/maps' % pid).readlines() :
		if ' -w-p ' in i :
			write_only.append(i)
	assert len(write_only) == 1
	print('Virtual memory mapping found:\n', write_only[0].split(),
			file=sys.stderr)
	vir_address, perms, offset, dev, inode = write_only[0].split()
	# Read /proc/[pid]/pagemap, get physical page address
	low_hex, high_hex = vir_address.split('-')
	low = int(low_hex, 16)
	high = int(high_hex, 16)
	assert low + 0x1000 == high
	assert low % PAGE_SIZE == 0
	f_pagemap = open('/proc/%d/pagemap' % pid, 'rb')
	f_pagemap.seek(low // PAGE_SIZE * PAGEMAP_ENTRY)
	pagemap, = struct.Struct('Q').unpack(f_pagemap.read(PAGEMAP_ENTRY))
	assert (pagemap >> 63) & 1 == 1			# the page is present in RAM
	assert (pagemap >> 62) & 1 == 0			# the page is NOT in swap space
	assert (pagemap >> 61) & 1 == 0			# private anonymous page
	assert (pagemap >> 57) & 0b11111 == 0	# 60-57
	assert (pagemap >> 56) & 1 == 1			# exclusively mapped
	assert (pagemap >> 55) & 1 == 1			# PTE  is  soft-dirty
	pfn = pagemap & ((1 << 54) - 1)			# requires root
	if not pfn :
		raise PermissionError('Need root privilege')
	print('PFN:', hex(pfn), file=sys.stderr)
	# Read /proc/kpagecount, should only have 1 reference count
	f_kpagecount = open('/proc/kpagecount', 'rb')
	f_kpagecount.seek(KPAGECOUNT_ENTRY * pfn)
	kpagecount, = struct.Struct('Q').unpack(f_kpagecount.read(KPAGECOUNT_ENTRY))
	assert kpagecount == 1
	# Read /proc/kpageflags
	f_kpageflags = open('/proc/kpageflags', 'rb')
	f_kpageflags.seek(KPAGEFLAGS_ENTRY * pfn)
	kpageflags, = struct.Struct('Q').unpack(f_kpageflags.read(KPAGEFLAGS_ENTRY))
	print('Flags:', bin((1<<64) + kpageflags)[3:], file=sys.stderr)
	assert kpageflags & (1 << KPF_MMAP)
	assert kpageflags & (1 << KPF_ANON)
	# Access /dev/mem
	f_mem = open('/dev/mem', 'rb')
	f_mem.seek(pfn * PAGE_SIZE)
	try :
		mem = f_mem.read(PAGE_SIZE)
	except PermissionError as e :
		print(file=sys.stderr)
		print('This error happens because /dev/mem cannot be read.',
				file=sys.stderr)
		print('If you are running this program with root, you probably need to '
				're-compile your Linux kernel with `CONFIG_STRICT_DEVMEM=n`.',
				file=sys.stderr)
		print('See mem(4).', file=sys.stderr)
		print(file=sys.stderr)
		raise PermissionError('Cannot read /dev/mem')
	sys.stdout.buffer.write(mem)

if __name__ == '__main__' :
	# Set up program
	assert os.system('make %s 1>&2' % EXEC_NAME) == 0
	cmd = [os.path.join('.', EXEC_NAME)]
	p = Popen(cmd, stdin=-1, stdout=-1, stderr=-1)
	p.stdout.read(1)
	pid = p.pid
	# Analyze
	print_w_mem(pid)
	# Terminate program
	p.kill()
	p.wait()

