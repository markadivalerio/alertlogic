from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from favorites.models import Favorites
from favorites.serializers import FavoritesSerializer
from django.conf import settings
import urllib2
import urllib
import httplib
import json

session_id = 0
account_id = 0

# Create your views here.
class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

"""
Gets the session id and account id, then calls the api to retrieve the favorite movies
"""
@csrf_exempt
def list_favorites(request):
	if request.method == 'GET':
		sid = get_session_id()
		aid = get_account_id()
		url = tmdb_api("account/"+str(aid)+"/favorite/movies")+"&session_id="+str(sid)
		response = json.load(urllib2.urlopen(url))
		return JSONResponse(response)

"""
Adds the movie id to the list of favorites to the user
"""
@csrf_exempt
def add_to_favorites(request):
	if request.method == 'POST':
		for key in request.POST:
		    print(key)
		    value = request.POST[key]
		    print(value)
		media_id = request.POST.get('media_id')
		sid = get_session_id()
		aid = get_account_id()
		headers = {"Content-type":"application/json;charset=utf-8"}
		data = urllib.urlencode({'media_type':'movies','favorite':True,'media_id':752})
		print(data)
		url = tmdb_api("account/"+str(aid)+"/favorite")+"&session_id="+str(sid)+"&"+data
		print(url)
		req = urllib2.Request(url, data, headers)
		response = urllib2.urlopen(req).read()
		return JSONResponse(response)

def tmdb_api(api_path):
	return settings.API_URL + api_path + "?api_key="+settings.API_KEY

"""
Gets the session id
"""
def get_session_id():
	return settings.SESSION_ID
	# global session_id
	# if not session_id:
	# 	url = tmdb_api("authentication/session/new")+"&request_token="+settings.API_REQUEST_TOKEN
	# 	print(url)
	# 	response = json.load(urllib2.urlopen(url))
	# 	session_id = response['session_id']
	# return session_id

"""
Get the user's account id
"""
def get_account_id():
	global account_id
	if not account_id:
		sid = get_session_id()
		url = tmdb_api("account")+"&session_id="+sid
		response = json.load(urllib2.urlopen(url))
		account_id = response['id']
	return account_id