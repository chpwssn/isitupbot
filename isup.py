from specifics import *
import urllib,urllib2,json
urltocheck = "b-15.net http://google.com"

def runcheck(url):
    serverstried = 0
    httpup = 0
    dnsresolve = 0
    serverconnected = 0
    servercities = ""

    for server in servers:
        serverstried += 1
        try:
            data = {"url": url,"api":apikey}
            data = urllib.urlencode(data)
            request = urllib2.Request(server + '?' + data)
            response = urllib2.urlopen(request)
            page = response.read()
            j = json.loads(page)
            if j:
                servercities += " "+j['city']+", "+j['country']
                serverconnected += 1
                if j['http'] == 200:
                    httpup += 1
                if j['dns'] == True:
                    dnsresolve += 1
        except:
             pass

    serverstried = str(serverstried)
    serverconnected = str(serverconnected)
    dnsresolve = str(dnsresolve)
    httpup = str(httpup)
    print "\nResults:"
    print "Of the "+serverstried+" servers tried, I connected to "+serverconnected+" they were located in: "+servercities
    print dnsresolve+"/"+serverconnected+" servers indicated "+url+" resolved with DNS"
    print httpup+"/"+serverconnected+" servers indicated "+url+" responded with a 200 message."

for word in urltocheck.split():
    runcheck(word)