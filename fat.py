import sys
import struct

name=['','','','','','','','','']
idx=0

def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 512)
    return fd.read(count * 512)
	
def BtoD(data):

	return int(("0x"+data[::-1].hex()),16)

	
def check_boot_recode(data):
	if(data[510]==0x55 and data[511]==0xaa):
		return 1
	else:
		return -1
	
def Bps(data):
	if(check_boot_recode(data) == 1):
		return BtoD(data[11:13])
	else:
		return -1
def Root_dir_sector(data):
	return (BtoD(data[17:19])*32+(Bps(data)-1))/Bps(data)
	
def First_data_sector(data):
	return int(BtoD(data[14:16])+BtoD(data[36:40])*BtoD(data[16:17])+Root_dir_sector(data))

def Cluster_to_sector(cluster,data):
	return (cluster-2)*BtoD(data[13:14])+First_data_sector(data)

def parse(data):

	global idx
	global name
	#print(data.hex())
	
	if(len(data) <= 0):
		return 0
	
	if(BtoD(data[11:12]) == 0x08):
		
		if(BtoD(data[0:1]) == 0xe5):
		
			print("삭제된 ", end='')
		
		else:
			name1=data[0:11]
			print("Volumn name :",name1.decode('euc-kr'))
				
	if(BtoD(data[11:12]) == 0x0f):
		n=""
		name1=data[1:11].decode('utf-16').split(b'\x00\x00'.decode('utf-16'))[0]
		name2=data[14:26].decode('utf-16').split(b'\x00\x00'.decode('utf-16'))[0]
		name3=data[28:32].decode('utf-16').split(b'\x00\x00'.decode('utf-16'))[0]
		#print(idx)
		name[idx]=(name1+name2+name3).split(b'\xff\xff'.decode('utf-16'))[0]
		idx+=1
		#print(name)
		if(BtoD(data[43:44]) != 0x0f):
			if(BtoD(data[0:1]) == 0xe5):
				print("삭제된 ", end='')
			print("LFN: ",end='')
			while(idx >= 0):
				n+=name[idx]
				idx-=1
			print(n)
			name=['','','','','','','','','']
			idx=0
			
	if(BtoD(data[11:12]) == 0x16):
		
		if(BtoD(data[0:1]) == 0xe5):
			print("삭제된 ", end='')
		
		name1=data[0:11].decode('euc-kr')
		print("SFN: ",name1)
		
	if(BtoD(data[11:12]) == 0x10):
		
		if(BtoD(data[0:1]) == 0xe5):
			print("삭제된 ", end='')
		
		name1=data[0:8].decode('euc-kr')
		print("Directory Name: ",name1)
		
	if(BtoD(data[11:12]) == 0x20):
		
		if(BtoD(data[0:1]) == 0xe5):
			name1="!"+data[1:8].decode('euc-kr')
			print("삭제된 ", end='')
			
		else:
			name1=data[0:8].decode('euc-kr')
			
		if(data[8:9] != b'\x20'):
			name1+="."+data[8:11].decode('euc-kr')
		print("File Name: ",name1)
		
	
	parse(data[32:])
		

filename = sys.argv[1]
f = open(filename, "rb")
data=read_sectors(f,0)
data=read_sectors(f,Cluster_to_sector(2,data),1)	# Root_Dir 
parse(data)
