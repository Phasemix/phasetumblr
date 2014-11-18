# -*- coding: utf-8 -*-
from datetime import datetime
import pytumblr
from phasepersist import phasepersist
import settings

client = pytumblr.TumblrRestClient(
    settings.CREDENTIALS['consumer_key'], 
    settings.CREDENTIALS['consumer_secret'], 
    settings.CREDENTIALS['token'], 
    settings.CREDENTIALS['token_secret']
)

def get_allposts():
	''' Return all posts in blog sorted by date
	'''
	result = client.posts(settings.BLOG, offset = 0, limit = 1)
	total_posts = result['total_posts']
	delta = (total_posts / 10) + 1

	all_posts = []
	posts_ids = []
	for j in range(delta):
		start = j * 10
		end = (j + 1) * 10
		posts = client.posts(settings.BLOG, offset = start, limit = end)['posts']
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

def split_body(body, elem=0):
	try:
		body = body.split('<!-- more -->')[elem]
	except:
		print 'Error parsing post.'

	if not elem:
		body = body.replace('<p></p>','')
		body = body.replace('<p>','')
		body = body.replace('</p>','')
	else:
		if settings.WEB_STARTER_KIT:
			body = body.replace('<p>','<p class="g-wide--pull-1" id="article-body">')
	return body

if __name__ == "__main__":
	posts = get_allposts()
	phasepersist.save(posts, 'tumblrposts.pkl')
