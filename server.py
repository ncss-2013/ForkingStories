#!/usr/bin/env/python3
import os
from tornado import Server

# Handlers:
import handler_login
import handler_main
import handler_story
import handler_story_tree
import handler_comment
import handler_user
# import handler_chat
import handler_register
import handler_search
import handler_spellcheck
import handler_misc
import handler_admin

server = Server(port=int(os.environ.get('PORT', 8080)))

server.register('/', handler_main.index)

server.register('/authenticate', handler_login.authenticate)
server.register('/logout', handler_login.logout)
server.register('/changepassword', handler_login.changepassword)

server.register('/user/(\w[\w\d]+)', handler_user.user)
server.register('/profiles', handler_user.profiles)
server.register('/check_username/(\w[\w\d]+)', handler_user.check_username)

server.register('/view_story/([0-9]+)', handler_story_tree.display_story_tree)
server.register('/add_to_story/(\d+)', handler_story_tree.add_to_story_tree)

server.register('/add_comment/([0-9]+)', handler_comment.add_comment)

server.register('/new_story', handler_story.new_story)
server.register('/process_new_story', handler_story.process_new_story)

server.register('/register', handler_register.register)
server.register('/process_register', handler_register.process_register)

server.register('/search', handler_search.SearchStories)

server.register('/spellcheck', handler_spellcheck.spellcheck)

# we need an admin/moderator interface
server.register('/admin', handler_admin.AdminIndex)
server.register(r'/admin/user/delete/(?P<user_id>\d+)', handler_admin.DeleteUser)

# this is something we forgot. add yourself if i forgot someone
server.register('/credits', handler_misc.credits)

server.run()
