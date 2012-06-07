import urllib2, urllib

class WebDAV:
	def get(self, url, token):
		return self.do_call('GET', url, None, token)

	def put(self, url, value, token):
		return self.do_call('PUT', url, value, token)

	def delete(self, url, token):
		return self.do_call('DELETE', url, None, token)

	def do_call(self, method, url, value, token):
		if not token:
			token = ''
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(url, data=value)
		request.add_header('Authorization', 'Bearer '+urllib.unquote(token))
		request.add_header('Content-Type', 'text/plain;charset=UTF-8')
		request.get_method = lambda: method
		url = opener.open(request)
		return url.read()