import sys, getopt
from instance import *
from multiprocessing.pool import ThreadPool



if len(sys.argv) <= 3:
	print "credoaws.py [num of instance to launch] [dns record type] [dns name]"
	sys.exit(0)


if __name__ == "__main__": 

	number_of_instance=sys.argv[1]
	postint=int(number_of_instance)
	dns_type=sys.argv[2]
	dns_name=sys.argv[3]

	pool = ThreadPool(processes=4)

	a = Instance()
	a.name=dns_name
	a.dns_type=dns_type
	
	print pool.map(a.runInstance, range(postint))
