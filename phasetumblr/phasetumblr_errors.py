# -*- coding: utf-8 -*-

# Errors 
WRONG_CREDENTIALS = u"Wrong or malformed credentials. Credentials must be a python tuple \
with the values Tumblr gives you at https://api.tumblr.com/console/calls/user/info"
WRONG_BLOG_NAME = u"Wrong blog name" 

class TumblrBlogException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
