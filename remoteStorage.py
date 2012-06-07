from webfinger import WebFinger
import urllib

class remoteStorage:
	def __init__(self):
		self.storage_info = None

	def get_storage_info(self, user_address):
		self.storage_info = WebFinger(user_address).finger()
		return self.storage_info

	def createOAuthAddress(self, scopes, redirect_uri):
		if self.storage_info.type == 'https://www.w3.org/community/rww/wiki/read-write-web-00#simple':
			scopes_str = ' '.join(scopes)
		else:
			scopes_str = ','.join([scope.split(':')[0].split('/')[0] for scope in scopes])

		host_and_rest = redirect_uri[redirect_uri.find('://')+3:]
		host = host_and_rest.split(':')[0].split('/')[0]

		attrs = [
			'redirect_uri='+urllib.quote_plus(redirect_uri),
			'scope='+urllib.quote_plus(scopes_str),
			'response_type=token',
			'client_id='+urllib.quote_plus(host)
		]
		authHref = self.storage_info.properties['http://oauth.net/core/1.0/endpoint/request']

		return authHref+("?" if authHref.find('?') == -1 else "&")+'&'.join(attrs)

if __name__ == "__main__":
	rs = remoteStorage()
	rs.get_storage_info('lukashed@owncube.com')
	print rs.createOAuthAddress('', 'http://lukasklein.com')