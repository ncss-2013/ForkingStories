#!/usr/bin/env python3.3

from collections import defaultdict
from tornado import websocket
import template
from html import escape

class ConnectionHandler(object):
	
	channels = defaultdict(set)

	@classmethod 
	def register(cls, connection):
		cls.channels[connection.channel].add(connection)
	
	@classmethod
	def sendMsg(cls, connection, msg):
		msg = escape(msg)
		for conn in cls.channels[connection.channel]:
			conn.onMessageRecv(msg)
	
	@classmethod
	def unregister(cls, connection):
		cls.channels[connection.channel].remove(connection)


class ChannelConnection(object):
	def __init__(self, socket, name, channel):
		self.name = name
		self.channel = channel
		self.socket = socket
		self._hashed = None
		ConnectionHandler.register(self)

	def onMessageRecv(self, msg):
		self.socket.write_message(self.channel + ':' + msg)

	def onMessageSend(self, msg):
		ConnectionHandler.sendMsg(self, msg)

	def close(self):
		ConnectionHandler.unregister(self)

	def __hash__(self):
		if self._hashed is None:
			chan = self.channel
			self._hashed = hash(id(self))
		return self._hashed


class ChatWebSocket(websocket.WebSocketHandler):
	def open(self):
		self.channels = dict()

	def on_message(self, message):
		
		msg_type, msg_params = message[:4], message[4:]
		
		print(msg_type, msg_params)

		if msg_type == 'USER':
			self.name = msg_params

		elif msg_type == 'JOIN':
			self.channels[msg_params] = ChannelConnection(self, self.name, msg_params)

		elif msg_type == 'QUIT':
			self.channels[msg_params].close()
			del self.channels[msg_params]

		elif msg_type == 'CHAT':
			channel, msg = msg_params.split(':', 1)
			self.channels[channel].onMessageSend(msg)

	def on_close(self):
		for conn in self.channels.values():
			conn.close()

def serve_chat(resp):
	resp.write(template.render_file('chat_test.html', {'channels': [('Global', 'global'), ('Story', 'story')], 'name': 'James'} ))