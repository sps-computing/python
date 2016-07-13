
# the requests module is for making http calls and grabbing webpages. 
import requests 
import datetime 
import config # storing the TfL API key in a file that won't be saved to GitHub 
# some very useful stuff from https://dateutil.readthedocs.io/en/stable/index.html, via http://stackoverflow.com/a/4771733/2902 
import dateutil.tz
import dateutil.parser 
from dateutil.relativedelta import relativedelta

# API documnentation: https://api-portal.tfl.gov.uk/docs 

def route(x):
	r = requests.get('https://api.tfl.gov.uk/line/{0}/stoppoints'.format(x))
	json_result = r.json()
	keys = ["commonName", "stopLetter", "indicator", "stationNaptan", "naptanId"]
	print(keys)
	for stop in json_result:
		output = "" 
		for key in keys: 
			value = stop.get(key, "<empty>")
			output += value + ", "
		print(output)


#	print(json_result)
route(200)

# https://api.tfl.gov.uk/line/200/route - returns route details 
# https://api.tfl.gov.uk/line/24/route/sequence/outbound - returns route sequence (outbound and inbound is based on the route details)
# https://api.tfl.gov.uk/StopPoint/490005183E - gives intersection information 


# please note that these are app specific keys and should not be saved into Github! 
def arrivals(naptan, app_id=None, app_key=None):

	if app_id == None or app_key == None:
		app_id, app_key = config.get_key()

	payload = {'app_id': app_id, 'app_key': app_key}
	r = requests.get('https://api.tfl.gov.uk/StopPoint/{0}/Arrivals'.format(naptan), params=payload)

	json_result = r.json()
	timestamp = ""

	to_zone = dateutil.tz.tzlocal()

	now = datetime.datetime.now(to_zone)
	for arrival in json_result:
		eta = dateutil.parser.parse(arrival['expectedArrival'])
		local = eta.astimezone(to_zone)
		rd = relativedelta(local, now)
		#expectedArrival=datetime.datetime.strptime( arrival['expectedArrival'], "%Y-%m-%dT%H:%M:%SZ" )
		#eta = expectedArrival.strftime('%H:%M:%S %Z')
		#utc = eta.replace(tzinfo=from_zone)
		#local = utc.astimezone(to_zone)

		print("Stop {1}: {2} towards {0}: {3}, {4} minutes".format(arrival['destinationName'], arrival['platformName'], arrival['lineName'], local.strftime('%H:%M'), rd.minutes))
		timestamp = arrival['timestamp']
	print("ts/now: {0}/{1}".format(timestamp, datetime.datetime.now().time()))

#arrivals('490001143B')


# OLD METHODS: 

# with due credit to http://www.danielforsyth.me/catching-the-bus-to-class-with-python/
# this method has been a little bit deprecated, so it is probably better to use the other API methods. 
def getTime(stops):
	my_stops = []
	for stop in stops:
		r = requests.get('http://countdown.tfl.gov.uk/stopBoard/{0}'.format(stop[0]))
		json_result = r.json()
		all_stops = json_result['arrivals']

		for st in all_stops:
			if st['isRealTime']== True:
				wait = int(st['estimatedWait'].split(' ')[0])
				x = (wait, stop[1])
				my_stops.append(x)

	waitsorted = sorted(my_stops, key=lambda tup: tup[0])
	print (waitsorted)

# getTime()

raynes_park = (50470, (0, 255, 0))
mitcham = (47864, (255, 0, 0))

#getTime([raynes_park, mitcham])
