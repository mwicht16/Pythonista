'''
Copyright 2015 Paul Sidnell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
Takes an Apple Maps pin exported via a WorkFlow action extension and opens it in
OmniFocus as a new containing the address and links to that location in various
mapping apps, TomTom, Apple Maps, Google Maps, Waze and Open Streetmap.

The Workflow Action Extension app (accepts:URLs) is:
	
URL Encode:
	Mode: Encode
Set Variable:
	URL
Text:
	pythonista://Location2OF?action=run&args=(URL)
Open URLs
'''

import sys
import urllib
import urlparse
import location
import webbrowser
from string import Template

def locationToNote( address, lat, long):
	
	tpl = Template (
		"$street\n" +
		"$city\n" +
		"$zip\n" + 
		"$country\n" +
		"\n" + 
		"Apple: http://maps.apple.com/?z=12&q=$lat,$long\n" +
		"\n" + 
		"Google: https://google.com/maps/place/$lat,$long/@$lat,$long,12z\n" + 
		"\n" + 
		"Open Street Map: http://www.openstreetmap.org/?mlat=$lat&mlon=$long#map=12/$lat/$long/m\n" + 
		"\n" +
		"TomTom: tomtomhome://geo:action=show&lat=$lat&long=$long&name=Pin\n" + 
		"\n" +
		"Waze: waze://?ll=$lat,$long&navigate=yes");
	
	params = {
		"street" : address.get("Street"),
		"city" : address.get("City"), \
		"zip" : address.get("ZIP"), \
		"country" : address.get("Country"),
		"lat" : lat, 
		"long" : long};
	
	return tpl.substitute(params);
	
url = sys.argv[1];
#url="http://maps.apple.com/maps?address=31%20Stanton%20Road%20Bristol%20England%20BS10%205SJ%20United%20Kingdom&ll=51.504456,-2.590899&q=51.504456,-2.590899&t=m";
ll = urlparse.parse_qsl(url, True)[2][1].split(",");
lat = float(ll[0]);
long = float(ll[1]);
address = location.reverse_geocode({"latitude" : lat, "longitude" : long})[0];
note = locationToNote (address, lat, long);
ofnote = {"name" : address.get("Street"), "note" : note};
webbrowser.open("omnifocus:///add?" + urllib.urlencode(ofnote).replace('+','%20'));
