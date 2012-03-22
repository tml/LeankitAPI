import requests
from requests.auth import HTTPBasicAuth
import json
import pdb


OK_RESPONSE_CODES = [
	requests.codes.ok,
	requests.codes.created,
	requests.codes.accepted,
	requests.codes.non_authoritative_info
]

class Entry(dict):
	""" Sometimes attribut access to dict keys looks nicer """
	def __getattr__(self, k):
		try:
			return self[k]
		except KeyError as e:
			raise AttributeError(e)

	def __setattr__(self, k, v):
		self[k] = v

class Board(Entry):
	pass

class Lane(Entry):
	pass

class Card(Entry):
	pass

class Comment(Entry):
	pass

class Attachment(Entry):
	pass

class Account(object):
	""" Represents your Leankit Kanban account """
	def __init__(self, hostname, username=None, password=None):
		self.base = 'https://%s.leankitkanban.com/Kanban/Api' % hostname

		if (username is not None and password is not None):
			self._auth=HTTPBasicAuth(username, password)
		else:
			raise NotImplementedError("Account does not allow anonymous authentication")

	def boards(self):
		self._boards = []
		for board in self.fetch('Boards'):
			boardData = self.fetch('Boards/%d' % board.Id)[0]
			self._boards.append(Board(boardData))
		return self._boards

	def fetch(self, url):
		try:
			r = requests.get("%s/%s" % (self.base, url), headers={'Content-Type':'application/json'}, auth=self._auth)
		except Exception as e:
			raise IOError("Unable to complete HTTP Request: %s" % e.message)

		if (r.status_code not in OK_RESPONSE_CODES):
			pdb.set_trace()
			raise IOError("Error from Leankit [%d] %s" % (r.status_code, r.content))

		self._last_json = r.text
		replyData = json.loads(r.text)['ReplyData']
		response = []
		try:
			for record in replyData:
				response.append(Entry(record))
		except ValueError as e:
			for record in replyData[0]:
				response.append(Entry(record))
		return response