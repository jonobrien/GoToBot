import urllib.request
subbedUsers = []

def subbedToCatFacts(bot):
    global subbedUsers
    for u in subbedUsers:
        catF = str(urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read())
        dm = "~DM," + u +"," + catF
        bot.sendDM({"text":dm})

def catFacts(bot, msg):
    request = str(urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read())
    bot.sendMessage(msg["channel"], request[request.find('[') + 2:request.find(']') - 1])

def subToCatFacts(bot, msg):
    global subbedUsers
    pass