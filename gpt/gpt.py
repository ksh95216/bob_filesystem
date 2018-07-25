import sys
import struct

def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 1024)
    return fd.read(count * 1024)

def parsing(f):
	for i in range(50):
		data = read_sectors(f, i,i+1)
		#print(data)
		if(data[510] == 85 and data[511] == 170):
			parse="0x"+data[512+72:512+80][::-1].hex()
			parse=int(parse,16)/2
			parse=round(parse)

			data = read_sectors(f, parse, parse+1)
			idx=0
			while(data[32] != 0):
				p=int((data[32:40][::-1].hex()),16)*512
				p1=int((data[40:48][::-1].hex()),16)*512
			
				print("Partition {} start: {} Size: {}".format(idx+1,hex(p),hex(p1-p+(1*512
				))))
				data=data[128:]
				idx+=1
			break
	
	


filename = sys.argv[1]
f = open(filename, "rb")
parsing(f)

