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
	Python 3 implementation of synchronization barrier using semaphores
	Ref: https://stackoverflow.com/questions/6331301/implementing-an-n-process
'''

import os, sys, threading, time, itertools

class Barrier :
	def __init__(self, n, incorrect) :
		self.n = n
		self.c = 0
		self.incorrect = incorrect
		self.mutex = threading.Semaphore(1)
		self.queue1 = threading.Semaphore(0)
		self.queue2 = threading.Semaphore(0)
	def wait(self) :
		self.mutex.acquire()
		self.c += 1
		c = self.c
		self.mutex.release()
		if self.c == self.n :
			self.c = 0
			for i in range(self.n - 1) :
				self.queue1.release()
		else :
			self.queue1.acquire()
		if self.incorrect :
			return
		# Reuse self.c and self.mutex
		self.mutex.acquire()
		self.c += 1
		c = self.c
		self.mutex.release()
		if self.c == self.n :
			self.c = 0
			for i in range(self.n - 1) :
				self.queue2.release()
		else :
			self.queue2.acquire()

def thread(b) :
	for i in itertools.count() :
		print(i)
		b.wait()

def main(argv) :
	n = int(argv[1]) if len(argv) > 1 else 10
	incorrect = int(argv[2]) if len(argv) > 2 else 0
	b = Barrier(n, incorrect)
	for i in range(n) :
		t = threading.Thread(target=thread, args=(b,), daemon=True)
		t.start()
	while True :
		time.sleep(3600)

if __name__ == '__main__' :
	main(sys.argv)

