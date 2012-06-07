remoteStorage.py
================

A Python library for adding [remoteStorage](http://unhosted.org/#remoteStorage) to your application. Based on [remoteStorage.js](https://github.com/unhosted/remoteStorage.js).

At the moment it only supports the WebDAV protocol.


## Code example
```python
# Create an instance of remoteStorage
rs = remoteStorage()
# Get the storage info
rs.get_storage_info('lukashed@owncube.com')

# Gets you an oauth address like https://owncube.com/apps/remoteStorage/auth.php/lukashed?redirect_uri=http%3A%2F%2Flukasklein.com%2F&scope=remoteStorage.py&response_type=token&client_id=lukasklein.com
# The scope specifies the categories that you want to access, the redirect uri can basically be any URL, that's the bad part about
# remoteStorage.py. You have to manually copy that address to your browser and then copy the generated bearer token from the redirect
# URI. Do you have any suggestions on how to make this better?
print rs.create_oauth_address(['remoteStorage.py'], 'http://lukasklein.com/')

# Creates a client instance for the given category. Token is optional, but if you need write access it's obviously compulsory.
cl = rs.create_client('remoteStorage.py', 'thebearertoken')
# Puts some data
cl.put('test', 'This is just a Test.')
# And gets it again
print cl.get('test')
```