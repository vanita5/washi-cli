#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
#
#	Python client for http://waschi.org
#
#
# author:	vanita5
# contact:	mail@vanita5.tk
# twitter:	@_vanita5
#
#
# Have fun!

import sys, getopt
import requests
import HTMLParser

from random import choice

from colorama import init
from termcolor import colored

#initialize Colorama to make Termcolor work on Windows, too
init()

#washi keys
key1 = 'Waschschhscihahaischihwaschiw45'
key2 = '1087409385898FAFASDTEGAJAN'

class Washi():
	def getServerList(self):
		payload = {'key1': key1, 'key2': key2}
		r = requests.post('http://waschi.meikodis.org/servers.php', data = payload)
		
		if r.text.find('ERROR!') == 0:
			q = raw_input('Could not get server list. Try again? (yes/no)')
			if q.lower() == 'yes':
				serverList = getServerList()
			else:
				exit()
		
		list = r.text.split()
		
		serverList = []
		for server in list:
			serverList.append(server.replace('receive.php', ''))
			
		return serverList
		
	def printServerList(self):
		list = Washi().getServerList()
		for server in list:
			print server
			
	def randomPointlessWord(self):
		r = requests.get('http://dev.revengeday.de/pointlesswords/api/')
		return HTMLParser.HTMLParser().unescape(r.text)
			
	def find(self, object):
		objectstr = ''
		if object == []:
			print 'You need a object to wasch! Use -f object or --find object'
			exit()
			
		for i in range(1, len(object)):
			objectstr = objectstr + object[i] + ' '
		
		if objectstr == '--object':
			objectstr = Washi().randomPointlessWord()
			print objectstr + '\n'
			
		serverList = Washi().getServerList()
		
		for server in serverList:
			r = requests.get(server + 'found')
			
			if objectstr in r.text:
				print colored('[OK]		', 'green') + server
			else:
				print colored('[Not Found]	', 'red') + server
				
	def wash(self, object):
		objectstr = ''
		if object == []:
			print 'You need a object to wasch! Use -f object or --find object'
			exit()
			
		for i in range(1, len(object)):
			objectstr = objectstr + object[i] + ' '
			
		if objectstr == '--object':
			objectstr = Washi().randomPointlessWord()
		
		try:
			serverList = Washi().getServerList()
			
			serverUrl = choice(serverList)
			
			url = serverUrl + 'echowash.php'
			
			payload = {'key1': key1, 'key2': key2, 'Kleidung': objectstr}
			r = requests.post(url, data = payload)
			
		except:
			print 'Something went wrong...'
		
		response = HTMLParser.HTMLParser().unescape(r.text) + '\n your ' + objectstr + ' from Server: ' + serverUrl
		
		return response
	

	def usage():
		print 'Python client for http://waschi.org \n' \
		'Usage:\n' \
		'   -w object or --wash object      Wash some object\n' \
		'   -f object or --find object      Find some object\n' \
		'   --serverlist                    Print a list with the Servers\n\n' \
		'If you have no idea for an object you can generate one with\n' \
		'--object\n' \
		'Example:\n' \
		'-f --object'

def main(argv):
	w = Washi()
	try:
		opts, args = getopt.getopt(argv, 'hw:f', ['help', 'wash', 'find',  'serverlist', 'object'])
	except getopt.GetOptError:
		usage()
		sys.exit(2)
		
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()
			sys.exit()
			
		elif opt in ('-w', '--wash'):
			print w.wash(argv[1:])
		
		elif opt in ('-f', '--find'):
			w.find(argv[1:])
		
		elif opt == '--serverlist':
			w.printServerList()
		
if __name__ == "__main__":
	main(sys.argv[1:])