import requests
import re
import os
import sys
from colorama import Fore, init, Style
import time
from datetime import date

init(autoreset=True)
os.system('cls' if os.name=='nt' else 'clear')

def Dump(domain):
	headers = {
		'Host': 'crt.sh',
		'User-Agent': 'Mozilla/5.0 (Linux; Android 11; MRX-AL09) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5795.197 Mobile Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
		'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
		'Upgrade-Insecure-Requests': '1',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-User': '?1',
		'Sec-Ch-Ua-Platform': '"iOS"',
		'Sec-Ch-Ua': '"Google Chrome";v="87", "Chromium";v="87", "Not=A?Brand";v="24"',
		'Sec-Ch-Ua-Mobile': '?1'
	}

	params = {
		'q': domain,
	}

	try:
		response = requests.get('https://crt.sh/', params=params, headers=headers)
	except:
		print(Fore.RED+"[-] Can't Access crt.sh, try again or change your IP")
		exit()
	if 'Issuer Name</A>' not in response.text:
		return False,"Can't Get Records!"
	else:
		return True,response.text

def Extractor(result):
	storage = []
	result = result.split('Issuer Name</A>')
	datas = result[1].split('<TR>')
	#print(datas[1])
	for index in datas:
		if '<A href="?id=' in index:
			temp = index.split("<TD>")
			domains = temp[2].replace('</TD>','').rstrip()
			if "<BR>" in domains:
				multiple_result = domains.split("<BR>")
				for line in multiple_result:
					if '*' in line:
						continue
					storage.append(line.replace('www.',''))
			else:
				if '*' in domains:
					continue
				storage.append(domains.replace('www.',''))
	
	storage = list(set(storage))
	return storage
			
def CheckUp(url):
	try:
		r = requests.head('https://'+url, timeout=2)
		return str(r.status_code)
	except:
		return False

try:
	target = sys.argv[1].lower()
except:
	print("Usage : python3 CertSubber.py domain.com")
	exit()


print("[+] Extracting "+target+" Certificate . . .")
result,content = Dump(target)
if result:
	folder = str(date.today()).replace('-','.')+' - '+target
	os.mkdir(folder)
	domains = Extractor(content)
	total = str(len(domains))
	print("[+] "+total+" Subdomain Found!, start checking!\n\n")
	time.sleep(2)
	counter = 0
	for line in domains:
		counter+=1
		status_code = CheckUp(line)
		if status_code:
			if '50' in status_code:
				print(Fore.BLUE+'['+str(counter)+"/"+total+"] "+status_code+" -> "+line)
				f = open(folder+"/500.txt",'a+')
				f.write(line+"\n")
				f.close()

			elif '20' in status_code:
				print(Style.BRIGHT+Fore.GREEN+'['+str(counter)+"/"+total+"] "+status_code+" -> "+line)
				f = open(folder+"/200.txt",'a+')
				f.write(line+"\n")
				f.close()

			elif '30' in status_code:
				print(Fore.CYAN+'['+str(counter)+"/"+total+"] "+status_code+" -> "+line)
				f = open(folder+"/300.txt",'a+')
				f.write(line+"\n")
				f.close()

			elif '40' in status_code:
				print(Fore.MAGENTA+'['+str(counter)+"/"+total+"] "+status_code+" -> "+line)
				f = open(folder+"/400.txt",'a+')
				f.write(line+"\n")
				f.close()

			elif '10' in status_code:
				print(Fore.MAGENTA+'['+str(counter)+"/"+total+"] "+status_code+" -> "+line)
				f = open(folder+"/100.txt",'a+')
				f.write(line+"\n")
				f.close()

		else:
			print(Fore.RED+'['+str(counter)+"/"+total+"] Down -> "+line)
			f = open(folder+"/down.txt",'w')
			f.write(line+"\n")
			f.close()

	print("\n[+] Operation Done, result saved to",folder)
