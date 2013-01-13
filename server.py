#!/usr/local/bin/python3
from tornado import Server

# Handlers:
import handler_login
import handler_main
import handler_story
import handler_comment
import handler_user
# import handler_chat
import handler_register
import handler_search
import handler_spellcheck

server = Server()
server.register('/', handler_main.index)

server.register('/login', handler_login.login)
server.register('/authenticate', handler_login.authenticate)
server.register('/logout', handler_login.logout)
server.register('/changepassword', handler_login.changepassword)

server.register('/user/(\w[\w\d]+)', handler_user.user)
server.register('/profiles', handler_user.profiles)
server.register('/check_username/(\w[\w\d]+)', handler_user.check_username)

server.register('/view_story/([0-9]+)', handler_story.view_story)

server.register('/new_story', handler_story.new_story)
server.register('/process_new_story', handler_story.process_new_story)
server.register('/add_to_story/([0-9]+)', handler_story.add_to_story)
server.register('/add_comment/([0-9]+)', handler_comment.add_comment)

server.register('/register', handler_register.register)
server.register('/process_register', handler_register.process_register)

server.register('/search', handler_search.search_results)
server.register('/spellcheck', handler_spellcheck.spellcheck)

server.run()
