#requirement : pip3 install vt, hashlib, OTXv2
import vt
from OTXv2 import OTXv2
import hashlib
import get_malicious
import readline
import configparser


config = configparser.ConfigParser()
config.read('config.cfg')

#ConfigVT
VT_API = config.get('CONFIG', 'VT_API') #Enter your VirusTotal API key in the config file
client = vt.Client(VT_API)
#Config OTX
OTX_API = config.get('CONFIG', 'OTX_API') #Enter your Alienvault API key in the config file
OTX_SERVER = config.get('CONFIG', 'OTX_SERVER')
otx = OTXv2(OTX_API, server=OTX_SERVER)

print("------------------------------------------------\n")
print("                   VT Scan                      \n")
print("Author                                      Date\n"+
      "SkallZou                                    2021\n"+
      "------------------------------------------------\n")

print("What do you want to do ?\n")
print("1. Check file")
print("2. Check URL")
choice = input()

if choice == "1":
    print("---------------------------------------\n" +
          "               CHECK FILE              \n" +
          "---------------------------------------")
    #to make tabulation complete
    readline.set_completer_delims(' \t\n=')
    readline.parse_and_bind("tab: complete")
    file_path = input("Please indicate the file path: ")
    file_md5 = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    file_to_analyze = client.get_object("/files/{}", format(file_md5))
    file_analyzed = file_to_analyze.last_analysis_stats
    print("Suspicious: " + str(file_analyzed.get("suspicious")) +
          "\nMalicious: " + str(file_analyzed.get("malicious")) +
          "\nFail: " + str(file_analyzed.get("failure")) +   
          "\nUndetected : " + str(file_analyzed.get("undetected")))


elif choice == "2":
    print("---------------------------------------\n" +
          "                CHECK URL              \n" +
          "---------------------------------------")

    url_user = input("Please enter the URL to check: ")
    url_id = vt.url_id(url_user)
    url = client.get_object("/urls/{}", format(url_id))
    print("Suspicious: " + str(url.get("suspicious")) +
          "\nMalicious: " + str(url.get("malicious")) +
          "\nFail: " + str(url.get("failure")) +          
          "\nUndetected : " + str(url.get("undetected")))

elif choice == "3":
    print("---------------------------------------\n" +
          "                CHECK IP               \n" +
          "---------------------------------------")
    user_ip = input("Please enter the IP address to check: ")
    print("VirusTotal Analysis: ")
    ip_to_analyze = client.get_object("/ip_addresses/{}", format(user_ip))
    print(ip_to_analyze.last_analysis_stats)

    print("Alienvault Analysis: ")
    alerts = get_malicious.ip(otx, user_ip)


client.close()
                                