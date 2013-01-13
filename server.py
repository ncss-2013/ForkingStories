#!/usr/local/bin/python3
from tornado import Server

# Handlers:
import handler_login
import handler_main
import handler_story
import handler_user
import handler_chat
import handler_register

server = Server()
server.register('/', handler_main.index)

server.register('/login', handler_login.login)
server.register('/authenticate', handler_login.authenticate)
server.register('/logout', handler_login.logout)
server.register('/changepassword', handler_login.changepassword)

server.register('/user/(\w[\w\d]+)', handler_user.user)
server.register('/profiles', handler_user.profiles)

server.register('/view_story', handler_story.view_story)
server.register('/add_to_stories', handler_story.add_to_stories)
server.register('/new_story', handler_story.new_story)
server.register('/view_story_list', handler_story.view_story_list)

server.register('/register', handler_register.register)
server.register('/process_register', handler_register.process_register)

server.run()