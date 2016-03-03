#!/usr/bin/python
import os
import sys
import getopt

MAX_COUNT = 19
IP_NUMBER = 100
_IPtoint = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
_inttoIP = lambda x: '.'.join([str(int(x)/(256**i)%256) for i in range(3,-1,-1)])
def Usage():
	print '''
Usage:
\t-f inputfile
\t-o outputfile
\t-h show the Usage
\t-m number\tinput the subnet you wanted, default is 19
\t-n number\tinput the ip number you wanted, which is in range(0,255), default is 100
'''

def main():
	global MAX_COUNT
	global IP_NUMBER

	inputfile = ""
	outputfile = ""
	iplist = []

	try:
		opts,args = getopt.getopt(sys.argv[1:],"f:o:m:n:h")
	except getopt.GetoptError,info:
		print info.msg
		sys.exit()
	for option,value in opts:
		if option in ('-f'):
			inputfile = value
		elif option in ('-o'):
			outputfile = value
		elif option in ('-h'):
			Usage()
		elif option in ('-m'):
			MAX_COUNT = int(value)
		elif option in ('-n'):
			IP_NUMBER = int(value)
		else:
			Usage()
			sys.exit()

	if inputfile == "" or outputfile == "":
		sys.exit()
	MAX_COUNT = 2**(32-MAX_COUNT)
	f = open(inputfile)
	data = f.readlines()
	f.close()
	for i in data:
		line = i.strip()
		iprange,count = line.split("|")
		if int(count) > MAX_COUNT-1:
			number = int(count)/MAX_COUNT
			for j in range(number):
				iplist.append(_inttoIP(_IPtoint(iprange)+j*MAX_COUNT+IP_NUMBER)+"\n")
	f = open(outputfile,"w")
	for i in iplist:
		f.write(i)
	f.close()	
if __name__ == '__main__':
	main()
