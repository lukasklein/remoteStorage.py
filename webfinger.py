import urllib, urllib2
from xml.etree import ElementTree

class WebFingerResult:
	def __init__(self, ssl, api, auth, template):
		self.ssl = ssl
		self.api = api
		self.auth = auth
		self.template = template
		if self.api == 'simple':
			self.type = 'https://www.w3.org/community/unhosted/wiki/remotestorage-2011.10#simple'
		elif self.api == 'WebDAV':
			self.type = 'https://www.w3.org/community/unhosted/wiki/remotestorage-2011.10#webdav'
		elif self.api == 'CouchDB':
			self.type = 'https://www.w3.org/community/unhosted/wiki/remotestorage-2011.10#couchdb'
		else:
			raise WebFingerException('api not recognized')
		self.properties = {
			'access-methods': ['http://oauth.net/core/1.0/parameters/auth-header'],
			'auth-methods': ['http://oauth.net/discovery/1.0/consumer-identity/static'],
			'http://oauth.net/core/1.0/endpoint/request': self.auth
		}

class WebFingerException(Exception):
	pass

class WebFinger:
	def __init__(self, identifier):
		if identifier[:5]=='acct:':
			identifier = identifier[5:]

		self.user = identifier[:identifier.find('@')]
		self.host = identifier[identifier.find('@')+1:]
		
		self.opener = urllib2.build_opener(urllib2.HTTPRedirectHandler())
		self.opener.addheaders = [('User-agent', 'python-webfinger')]

	def host_meta(self, protocol):
		hostmeta_url = "%s://%s/.well-known/host-meta"%(protocol,self.host)
		connection = self.opener.open(hostmeta_url)
		response = connection.read()
		connection.close()
		return response

	def get_template(self, host_meta):
		tree = ElementTree.fromstring(host_meta)
		for link in tree.findall('{http://docs.oasis-open.org/ns/xri/xrd-1.0}Link'):
			template = link.attrib.get('template')
			if template:
				return template

	def get_data(self, template):
		data_url = template.replace('{uri}', '%s')%("acct:%s@%s"%(self.user, self.host))
		connection = self.opener.open(data_url)
		response = connection.read()
		connection.close()

		tree = ElementTree.fromstring(response)
		for link in tree.findall('{http://docs.oasis-open.org/ns/xri/xrd-1.0}Link'):
			rel = link.attrib.get('rel')
			if rel=='remoteStorage':
				return {'template': link.attrib.get('template'), 'api': link.attrib.get('api'), 'auth': link.attrib.get('auth')}


	def finger(self):
		try:
			host_meta = self.host_meta('https')
			self.ssl = True
		except (urllib2.HTTPError, urllib2.URLError):
			host_meta = self.host_meta('http')
			self.ssl = False

		template = self.get_template(host_meta)
		data = self.get_data(template)

		return WebFingerResult(ssl=self.ssl, api=data['api'], auth=data['auth'], template=data['template'])