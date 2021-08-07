# randomized_http_exfil

This project was started to improve my python writing skills and test some assumptions about HTTP requests. 

This tool is made of two parts, one is the exfil client which runs on the victim machine while the exfil_server is ran on a publicly available host controlled by the attacker. 
The client agent breaks a specificed target into base64 encoded chunks and sends them within a header inside of a HTTP request out to the attack controlled webserver. Each request has a randomly selected host and user-agent header field to avoid any spikes or detectiosn of those data points. 

Once the all of the pieces of the file have been sent a final packet is sent to the server to initialize the closure of the web server and the aggregation of the data pieces. The resulting file lives on the attackers server and is a intact replication of the original file from the victim client. 

