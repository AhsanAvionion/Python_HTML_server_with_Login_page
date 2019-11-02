#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import time
PORT_NUMBER = 80
auth = False
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		global auth
		print "get self.path",self.path
		if self.path=="/":
			self.path="/index.html"
		elif self.path=="/welcome_page.html" and auth == True:
			self.path="/welcome_page.html"
		else:
			self.wfile.write("Wrong Entry")
			return
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".png"):
				mimetype='image/png'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
				return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		global auth
		print "post self.path",self.path
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			print "name:%s" % form["uname"].value
			print "psw:%s" % form["psw"].value
			if form["uname"].value == "admin" and form["psw"].value == "admin":

				#Redirect the browser on the main page
				auth = True 
				self.send_response(302)
				self.send_header('Location','/welcome_page.html')
				self.end_headers()
			else:
				auth = False
				self.send_response(200)
				self.end_headers()
				self.wfile.write("Wrong Password")
			return	
		elif self.path=="/update":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			print "Your name is: %s" % form["your_name"].value
			self.send_response(302)
			self.send_header('Location','/welcome_page.html')
			self.end_headers()
			return	
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()

