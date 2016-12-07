from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from search.models import Search
from search.serializers import SearchSerializer
from django.conf import settings
import urllib2
import urllib
import json

# Create your views here.
class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def search(request):
	"""
	Perform the actual movie search
	"""
	if request.method == 'GET':
		title = request.GET.get('title')
		name = request.GET.get('person')
		if title:
			return search_by_title(title)
		elif name:
			return search_by_person(name)
		else:
			return JSONResponse({})

def search_by_title(title):
	"""
	Perform the actual movie search via title
	"""
	url = tmdb_api("search/movie")+"&query="+urllib.quote_plus(title)
	response = json.load(urllib2.urlopen(url))
	return JSONResponse(response)

def search_by_person(name):
	"""
	Perform the actual movie search via actor name
	"""
	ids = get_id_by_name(name)
	if not ids:
		return JSONResponse({}) # No actors with the name found
	url = tmdb_api("discover/movie")+"&with_cast="+'|'.join(map(str, ids))
	response = json.load(urllib2.urlopen(url))
	return JSONResponse(response)

def tmdb_api(api_path):
	return settings.API_URL + api_path + "?api_key="+settings.API_KEY

def get_id_by_name(name):
	url = tmdb_api("search/person")+"&query="+urllib.quote_plus(name)
	r = json.loads(urllib2.urlopen(url).read())
	ids = []
	for person in r['results']:
		ids.append(person['id'])
	return ids
