#!/usr/bin/python
import os
import sys
import getopt
import re

G_IP2nodes = {}
G_IPcount = 1
G_edges = []
G_choose = 0

_IP2int = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
_int2IP = lambda x: '.'.join([str(int(x)/(256**i)%256) for i in range(3,-1,-1)])

def Process_data_set(data_set):
	global G_IP2nodes
	global G_edges
	global G_choose
	global G_IPcount
	
	length = len(data_set)
	if length < 1:
		return

	for i in range(length):
		ip = data_set[i].split()[1]
		if ip == "*":
			continue
		elif ip not in G_IP2nodes:
			G_IP2nodes[ip] = [_IP2int(ip),G_IPcount]
			G_IPcount = G_IPcount+1

	for i in range(length-1):
		ip1 = data_set[i].split()[1]
		ip2 = data_set[i+1].split()[1]
		if ip1 == "*" or ip2 == "*":
			continue
		string = str(G_IP2nodes[ip1][G_choose])+" "+str(G_IP2nodes[ip2][G_choose])
		if string not in G_edges:
			G_edges.append(string)
	
def Usage():
	print '''
Usage:
\t-f inputfile
\t-o outputfile
\t-h show the Usage
\t--serial-nodes\t add when you want label nodes with serial numbers
\t--route\t add when you want ignore destination IPs as a node
'''

def main():
	global G_choose

	inputfile = ""
	outputfile = ""
	count = 0
	flag = 0

	try:
		opts,args = getopt.getopt(sys.argv[1:],"f:o:h",["serial-nodes","route"])
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
		elif option in ("--serial-nodes"):
			G_choose = 1
		elif option in ("--route"):
			flag = 1
		else:
			Usage()
			sys.exit()
	if inputfile == "" or outputfile == "":
		sys.exit()
	
	if flag == 0:
		f = open(inputfile)
		pattern = re.compile(r'traceroute')
		data_set = []
		for line in f:
			line = line.strip()
			match = pattern.match(line)
			if match:
				Process_data_set(data_set)
				count = count+1
				data_set = []
				continue
			else:
				data_set.append(line)
		Process_data_set(data_set)
		count = count+1
		f.close()

	elif flag == 1:
		f = open(inputfile)
		data_set = []
		dst_IP = ""
		pattern = re.compile(r'traceroute .* to (\d+\.\d+\.\d+\.\d+)')
		for line in f:
			line = line.strip()
			match = pattern.match(line)
			if match:
				count = count+1
				if data_set == []:
					dst_IP = match.group(1)
					continue
				elif data_set[-1].split()[1] == dst_IP:
					del data_set[-1]
					dst_IP == ""
				dst_IP = match.group(1)
				Process_data_set(data_set)
				data_set = []
				continue
			else:
				data_set.append(line)
		if data_set == []:
			pass
		elif data_set[-1].split()[1] == dst_IP:
			del data_set[-1]
		Process_data_set(data_set)
		f.close()
	
	f = open(outputfile,"w")
#output points as well as ip-ipcount
#	for i in G_IP2nodes:
#		f.write(i+" "+str(G_IP2nodes[i][1])+"\n")
#output edges
	for i in G_edges:
		f.write(i+"\n")	
	f.close()
	print "Processed: %d" % count
	print "Find edges: %d" % len(G_edges)
	print "Find points: %d" % len(G_IP2nodes)

if __name__ == '__main__':
	main()

