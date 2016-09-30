# *.* coding: utf-8 *.*
'''
Format	C Type	Python type	Standard size	Notes
x	pad byte	no value
c	char	string of length 1	1
b	signed char	integer	1	(3)
B	unsigned char	integer	1	(3)
?	_Bool	bool	1	(1)
h	short	integer	2	(3)
H	unsigned short	integer	2	(3)
i	int	integer	4	(3)
I	unsigned int	integer	4	(3)
l	long	integer	4	(3)
L	unsigned long	integer	4	(3)
q	long long	integer	8	(2), (3)
Q	unsigned long long	integer	8	(2), (3)
f	float	float	4	(4)
d	double	float	8	(4)
s	char[]	string
p	char[]	string
P	void *	integer	 	(5), (3)
'''
from struct import *

pack('hhl', 1, 2, 3)
#'\x00\x01\x00\x02\x00\x00\x00\x03'
unpack('hhl', '\x00\x01\x00\x02\x00\x00\x00\x03')
#(1,2,3)

calcsize('hhl')
#8
