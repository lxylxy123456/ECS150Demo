//  
//  ECS150Demo - Some demo programs related to the operating systems class
//  Copyright (C) 2019  lxylxy123456
//  
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Affero General Public License as
//  published by the Free Software Foundation, either version 3 of the
//  License, or (at your option) any later version.
//  
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Affero General Public License for more details.
//  
//  You should have received a copy of the GNU Affero General Public License
//  along with this program.  If not, see <https://www.gnu.org/licenses/>.
//  

#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>

int main(void)
{
	char *a = (char *)mmap(NULL, 0x1000, PROT_WRITE,
			       MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	for (int i = 0x0; i < 0x200; i++)
		((int16_t *) a)[i] = i;
	a[0xffd] = 'E';
	a[0xffe] = 'O';
	a[0xfff] = 'F';
	printf("Hello, world!\n");
	fflush(stdout);
	pause();
	return 0;
}
