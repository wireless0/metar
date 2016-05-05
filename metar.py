from bottle import route, run
import urllib2
import xmltodict
import socket

def get_metar(airfield):
    if not airfield.isalpha():
        return "Invalid station string\n"
    file = urllib2.urlopen('https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString={}&hoursBeforeNow=1'.format(airfield))
    data = file.read()
    file.close()
    data = xmltodict.parse(data)

    if data['response']['data']['@num_results'] == '1':
        return data['response']['data']['METAR']['raw_text']
    elif data['response']['data']['@num_results'] == '0':
        return 'No data for {}'.format(airfield)
    else:
        return data['response']['data']['METAR'][0]['raw_text']

@route('/')
@route('/<name>')
def metar(name = 'OEDF'):
    return get_metar(name)

run(host=socket.gethostname(), port=80, debug=True)

