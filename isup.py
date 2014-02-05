from specifics import *
import urllib
import urllib2
import json
import praw
import time
urltocheck = "b-15.net http://google.com http://151.236.29.11 https://151.236.29.11"

def runcheck(url):
    serverstried = 0
    httpup = 0
    dnsresolve = 0
    serverconnected = 0
    serverids = ""
    servercities = ""
    resolvedto = ""

    for server in servers:
        serverstried += 1
        try:
            data = {"url": url,"api":apikey}
            data = urllib.urlencode(data)
            request = urllib2.Request(server + '?' + data)
            response = urllib2.urlopen(request)
            page = response.read()
            j = json.loads(page)
            print j
            if j:
                servercities += " "+j['city']+", "+j['country']+"."
                serverids += "^"+str(j['serverid'])+" "
                serverconnected += 1
                if j['http'] == 200:
                    httpup += 1
                if j['resolved'] == True:
                    if str(j['dns']) not in resolvedto:
                        resolvedto += str(j['dns'])+" "
                    dnsresolve += 1
        except:
             pass

    serverstried = str(serverstried)
    serverconnected = str(serverconnected)
    dnsresolve = str(dnsresolve)
    httpup = str(httpup)
    response = ""
    response += "Hello! I\'m the IsItUpBot!\n\nResults:"
    response +="\n\nOf the "+serverstried+" servers tried, I connected to "+serverconnected+". They were located in: "+servercities
    response += "\n\n"+dnsresolve+"/"+serverconnected+" servers indicated "+url+" resolved with DNS: "+resolvedto
    response += "\n\n"+httpup+"/"+serverconnected+" servers indicated "+url+" is up."
    response += "\n\n"+footerGen(mention.permalink)+" ^| ^I ^contacted ^servers: "+serverids
    return response

def footerGen(permalink):
    return '[^report ^a ^mistake](http://www.reddit.com/message/compose/?to=chpwssn&subject=IsItUpBot%20Error%20Report&message='+permalink+') ^| [^more ^info](http://www.reddit.com/r/IsItUpBot/wiki/index)'


r = praw.Reddit('ChemBot v2.0 by u/chpwssn. Responds to username mentions with information on chemical compounds listed in the comment.')
r.login(botuser,botpass)
#Open the file used to keep track of the mentions we've already scanned for words
with open("isitupbotscanned.txt") as scannedfile:
    scanned = scannedfile.read().splitlines()
print scanned
done_this_time = set()
loop = True
loops = 0
while loop:
    loops += 1
    if loops%100 == 0:
        print "Done "+str(loops)+" loops, completed: "+str(done_this_time)
    #Get the username mentions we have in our inbox
    mentions = r.get_mentions()
    for mention in mentions:
        #If we haven't scanned the mention yet previously or in this time running the script
        if mention.id not in scanned and mention.id not in done_this_time:
            #Record the mention as scanned in the file and the set
            with open("isitupbotscanned.txt", "a") as scannedfile:
                scannedfile.write(mention.id+'\n')
                done_this_time.add(mention.id)
            print mention
            print mention.id
            words = mention.body.split()
            for word in words:
                if word.lower() != "/u/isitupbot":
                    mention.reply(runcheck(word))
    time.sleep(2)