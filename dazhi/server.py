#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #print ("Got a request of: %s\n" % self.data.decode("utf-8"))

        split_data = self.data.decode("utf-8").split('\r\n')
        first_line_request = split_data[0].split(' ')

        
        if (first_line_request[0] == "GET") :
        #only view files
            if_correct = 0
            root = "www"
            baseAddress = first_line_request[1]
            url = root + baseAddress
            baseURL = "http://127.0.0.1:8080" + baseAddress

            if ( baseAddress[len(baseAddress)-1] == '/' ):
                url = url + "index.html"

            split_url = url.split(".")

            if ( len(split_url) == 1 ):
            #judge if an index.html file is contained under the directory
                url = url + "/index.html"
                BaseURL = baseURL + "/"
                if_correct = 1

            elif ( len(split_url) == 2 ):
                #support css and html
                if ( not ( (split_url[1] == "css") or (split_url[1] == "html") ) ):
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                    return 0
            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                return 0

            try:
            #open return file
                files = open(url, "r")
            except:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                return 0

            content_type = "Content-Type: text/html\r\n"
            if ( (url.split("."))[1] == "css" ):
                content_type = "Content-Type: text/css\r\n"

            
            if (if_correct == 0):
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
            elif (if_correct == 1):
            #if there is an inde.html under the directory add '/' to the end if it does not exists
                #https://zh.wikipedia.org/wiki/HTTP_301 Viewed this page for how to format 301 status code
                self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n",'utf-8'))
                self.request.sendall(bytearray("Location: " + BaseURL + "\r\n",'utf-8'))
            self.request.sendall(bytearray(content_type,'utf-8'))
            
            data = files.read(1024)
            #view the file
            while (data):
                self.request.send( bytearray(data,'utf-8') )
                data = files.read(1024)

            files.close()
            return 0
        #405 when handle POST, PUT or DELETE requests
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed",'utf-8'))
            return 0

        #self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()