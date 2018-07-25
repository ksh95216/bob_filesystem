import sys
import struct

SLBA=[0,0,0,0,0,0,0,0,0,0]
FLBA=[0,0,0,0,0,0,0,0,0,0]
EBR=[0,0,0,0,0,0,0,0,0,0]

LINDEX=0
EINDEX=0
CHECK=0
err=0
def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 512)
    return fd.read(count * 512)

def check_boot(data):
	if(data[510] != 85 or data[511] != 170):
		print(data[510],data[511])
		print("########"*3+"No Boot Recode!"+"########"*3+"\n")
		return 0
	else:
		print("########"*3+"Start Parsing!"+"########"*3+"\n")
		return 1
		
def make_num(data):
	num=int(("0x"+data[::-1].hex()),16)*512
	return num

def parse_1(data):
	return data[512-65:]

def parsee(parse, idx=0):
	global LINDEX
	global EINDEX
	global CHECK
	global err
	
	idx=EINDEX
	data=parse[3:15]
	#print(data)
	#print("check : ",CHECK, EINDEX)
	if(err == 1):
		return 0
	
	if(parse.hex() == 'aa'):
		CHECK+=1
		data = read_sectors(f,round((EBR[EINDEX-1]/512)))
		parse=parse_1(data)
		#print(CHECK, EINDEX)
		#print("chcocococococcocccccccccccccccccccccccccccc")
		if(CHECK != EINDEX):
			err=1
		parsee(parse,EINDEX)
	

	
	if(data[0] == 7 and idx == 0):
		#print("LBA")
		SLBA[LINDEX]=make_num(data[4:8])
		FLBA[LINDEX]=make_num(data[8:12])
		#print(SLBA)
		#print(FLBA)
		LINDEX=LINDEX+1
	
	if(data[0] == 7 and idx != 0):
		#print("LBA")
		SLBA[LINDEX]=make_num(data[4:8])+EBR[EINDEX-1]
		FLBA[LINDEX]=make_num(data[8:12])
		#print(SLBA)
		#print(FLBA)
		LINDEX=LINDEX+1

		
	if(data[0] == 5 and idx == 0):
		#print("EBR")
		EBR[EINDEX]=make_num(data[4:8])
		EINDEX=EINDEX+1
		#print(EINDEX)
	
	if(data[0] == 5 and idx != 0):
		#print("EBR")
		EBR[EINDEX]=make_num(data[4:8])+EBR[0]
		#print(make_num(data[4:8]),EBR)
		EINDEX=EINDEX+1
		#print(EINDEX)
		
		
	return parsee(parse[16:])
	
filename = sys.argv[1]
f = open(filename, "rb")

data = read_sectors(f, 0)
check=check_boot(data)
parse=parse_1(data)
parsee(parse)

i=0
while(EBR[i] != 0):
	print("EBR Start {}: {}".format(i+1,hex(EBR[i])))
	i+=1
i=0
print("")
print("#"*60)
print("")
while(SLBA[i] != 0):
	print("Partition {} start: {}, End: {} Size: {}\n".format(i+1,hex(SLBA[i]),hex(SLBA[i]+FLBA[i]),hex(FLBA[i])))
	i+=1
print("#"*60)



	







