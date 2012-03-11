import requests
from requests.auth import HTTPBasicAuth
import json


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

class Account(object):
	""" Represents your Leankit Kanban account """
	def __init__(self, hostname, username=None, password=None):
		self.url = 'https://%s.leankitkanban.com' % hostname

		if (username is not None and password is not None):
			self._auth=HTTPBasicAuth(username, password)
		else:
			raise NotImplementedError("Account does not allow anonymous authentication")

	def _fetchAccountInfo(self):
		try:
			r = requests.get(self.url)
		except Exception as e:
			raise IOError("Unable to complete HTTP Request: %s" % e.message)

		response = Entry(json.loads(r.text))
		if (r.status_code not in OK_RESPONSE_CODES):
			raise IOError("Error from Leankit [%d] %s" % (r.status_code, r.content))
		return response

