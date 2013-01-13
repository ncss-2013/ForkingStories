#!/usr/bin/env python3.3

class ConnectionHandler(object):
  @classmethod 
  def register(cls, connection):
    pass
  
  @classmethod
  def sendMsg(cls, connection, msg):
    pass
    # foreach user talking in connection.channel
    #    call onMessageRecv
  
  @classmethod
  def unregister(cls, connection):
    pass
    #....

  foo = set()

class Connection(object):
  def __init__(self, name, channel):
    #....
    self.name = name
    self.channel = channel
    ConnectionHandler.register(self)

  def onMessageRecv(self, msg):
    pass
    # websocket stuff

  def onMessageSend(self, msg):
    ConnectionHandler.sendMsg(self, msg)


