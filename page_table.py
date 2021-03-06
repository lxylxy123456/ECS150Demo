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
	Print process page table using graphviz
'''

import os, sys, re, time, struct, math
import graphviz
from subprocess import Popen

EXEC_NAME = 'page2frame'
PAGE_SIZE = 4096	# Use `getconf PAGE_SIZE`
PAGEMAP_ENTRY = 8	# 64 bits

def hex64(num) :
	assert num < (1<<64)
	return '0x' + hex(num + (1<<64))[3:]

def print_page_table(pid, ofile, oformat) :
	# Read /proc/[pid]/maps, get virtual page location. See proc(5)
	table = []
	for i in open('/proc/%d/maps' % pid).readlines() :
		vir_address, perms, offset, dev, inode, *pathname = i.split()
		if pathname == ['[vsyscall]',] :
			continue
		low_hex, high_hex = vir_address.split('-')
		low = int(low_hex, 16)
		high = int(high_hex, 16)
		assert low % PAGE_SIZE == 0
		table.append((low, high, perms, inode, pathname))
	table.sort()
	table.append((1<<64, 1<<64, None, None, None))
	memory_range = [(range(0, 0), (None, None, None))]
	for low, high, perms, inode, pathname in table :
		if memory_range[-1][0].stop != low :
			memory_range.append((range(memory_range[-1][0].stop, low), None))
		memory_range.append((range(low, high), (perms, inode, pathname)))
	memory_range.pop(-1)
	memory_range.pop(0)
	# Begin drawing
	page_table = graphviz.Digraph(comment='Page Table')
	page_table.graph_attr['fontname'] = 'Courier 10 Pitch'
	page_table.node_attr['fontname'] = 'Courier 10 Pitch'
	page_table.edge_attr['fontname'] = 'Courier 10 Pitch'
	page_table.graph_attr['rankdir'] = 'LR'
	# Generate the HTML table
	html = ('<table border="0" cellborder="1" cellspacing="0" '
			'cellpadding="4">')
	for r, k in reversed(memory_range) :
		low = hex64(r.start)
		high = hex64(r.stop - 1)
		label_str = '<x%s>' % low
		html += '<tr>'
		nspace = max(int(math.log10(r.stop - r.start) / 3), 1)
		space = '<br/>' * nspace
		html += '<td>%s%s%s</td>' % (high, space, low)
		bg_str = 'bgcolor="green"'
		if k :
			port_str = 'port="%s"' % ('x%s' % low)
			html += '<td %s>r</td>' % (bg_str if 'r' in k[0] else '')
			html += '<td %s>w</td>' % (bg_str if 'w' in k[0] else '')
			html += '<td %s>x</td>' % (bg_str if 'x' in k[0] else '')
			html += '<td %s %s>p</td>' % (port_str, 
											bg_str if 'p' in k[0] else '')
		else :
			html += '<td colspan="4"></td>'
		html += '</tr>'
	html += '</table>'
	page_table.node('master', label='<%s>' % html, shape='none', margin='0')
	for r, k in memory_range :
		label = hex64(r.start)
		if k is not None :
			if k[2] :
				filename = k[2][0]
				if filename.endswith('/' + EXEC_NAME) :
					filename = EXEC_NAME
				page_table.edge('master:x%s' % label, filename)
			else :
				page_table.edge('master:x%s' % label, 'y%s' % label)
				page_table.node('y%s' % label, label='mmap?')
	page_table.render(ofile, format=oformat, view=True)

if __name__ == '__main__' :
	if len(sys.argv) < 2 :
		print('Usage: python3 page_table.py output_file.{png|pdf|...} [pid]')
		exit(1)
	ofile, oext = os.path.splitext(sys.argv[1])
	oformat = oext.lstrip('.')
	if len(sys.argv) > 2 :
		pid = int(sys.argv[2])
		print_page_table(pid, ofile, oformat)
	else :
		# Set up program
		assert(os.system('make %s 1>&2' % EXEC_NAME) == 0)
		cmd = [os.path.join('.', EXEC_NAME)]
		p = Popen(cmd, stdin=-1, stdout=-1, stderr=-1)
		p.stdout.read(1)
		pid = p.pid
		# Analyze
		print_page_table(pid, ofile, oformat)
		# Terminate program
		p.kill()
		p.wait()

