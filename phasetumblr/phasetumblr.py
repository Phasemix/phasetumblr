# -*- coding: utf-8 -*-
from datetime import datetime
import pytumblr
import phasetumblr_errors 

class TumblrBlog():

	def __init__(self, credentials, blog, web_starter_kit = True):
		try:
			self.client = pytumblr.TumblrRestClient(credentials)
		except:
			raise phasetumblr_errors.TumblrBlogException(
				phasetumblr_errors.WRONG_CREDENTIALS)
		if blog:
			self.blog = blog
		else:
			raise phasetumblr_errors.TumblrBlogException(
				phasetumblr_errors.WRONG_BLOG_NAME)

		# Are you going to generate HTMLs using Starter kit ?, if that's the 
		# case, special HTML will be inserted when parsing.
		self.web_starter_kit = web_starter_kit

	def get_allposts(self):
		''' Return all posts in blog sorted by date
		'''
		result = self.client.posts(self.blog, offset = 0, limit = 1)
		try: 
			total_posts = result['total_posts']
		except:
			raise phasetumblr_errors.TumblrBlogException(result['meta']['msg'])

		delta = (total_posts / 10) + 1

		all_posts = []
		posts_ids = []
		for j in range(delta):
			start = j * 10
			end = (j + 1) * 10
			posts = self.client.posts(self.blog, offset = start, limit = end)['posts']
			if not len(posts):
				break
			for i in posts:
				if i['id'] in posts_ids:
					continue
				description = split_body(i['body'])
				body = split_body(i['body'], 1)
				post = {}
				post['title'] = i['title']
				post['link'] = i['post_url']
				post['date'] = datetime.strptime(i['date'], '%Y-%m-%d %H:%M:%S %Z')
				post['tags'] = i['tags']
				post['id'] = i['id']
				post['body'] = body
				post['description'] = description
				all_posts.append(post)
				posts_ids.append(i['id'])

		newlist = sorted(all_posts, key=lambda k: k['date']) 
		return newlist

	def _split_body(body, elem=0):
		try:
			body = body.split('<!-- more -->')[elem]
		except:
			print 'Error parsing post.'

		if not elem:
			body = body.replace('<p></p>','')
			body = body.replace('<p>','')
			body = body.replace('</p>','')
		else:
			if self.web_starter_kit:
				body = body.replace('<p>','<p class="g-wide--pull-1" id="article-body">')
		return body
