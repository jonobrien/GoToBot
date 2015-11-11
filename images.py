

def getGiphy(bot, msg):
    url = "http://api.giphy.com/v1/gifs/search?q="
    keywords = ",".join(msg["text"].split(",")[1:])
    if("jon" in keywords.lower()):
        keywords = "sloth"
    print(keywords)
    data = urllib.request.urlopen(url + keywords +"&api_key=dc6zaTOxFJmzC&limit=1").read().decode("utf-8")#.read())
    jsonData = json.loads(data)
    try:
        gif = jsonData["data"][0]["images"]["original"]["url"]
    except IndexError:
        gif = "gif not found"
    bot.sendMessage(msg["channel"], gif)
    #print (jsonData)#(json.dumps(data, sort_keys=True, indent=4))
    #print()
    #print(jsonData["data"])
    ###for i in jsonData["data"][0].keys():
    ###    print (jsonData["data"][0][i])
    ###print(jsonData["data"][0]["images"]["original"]["url"]





# sends a 420 giphy at 16:20:00 and 16:20:30
def blaze(bot):
    url = "http://api.giphy.com/v1/gifs/search?q="
    keywords = "420"
    print(keywords)
    data = urllib.request.urlopen(url + keywords +"&api_key=dc6zaTOxFJmzC&limit=1").read().decode("utf-8")#.read())
    jsonData = json.loads(data)
    try:
        gif = jsonData["data"][0]["images"]["original"]["url"]
    except IndexError:
        gif = "can't blaze it"
    bot.sendMessage("G09LLA9EW", gif)



# get a meme of keyword passed in
# used memeGenerator API to query for memes
def getMeme(bot, msg):
    keyword = msg["text"].split(",")[1]
    url = "http://version1.api.memegenerator.net/Instances_Select_ByNew?languageCode=en&pageIndex=0&pageSize=12&urlName="
    data = urllib.request.urlopen(url+keyword).read().decode("utf-8")
    jsonData = json.loads(data)
    try:
        meme = jsonData["result"][random.randrange(0,len(jsonData["result"]))]["instanceImageUrl"]
    except:
        meme = "nope.jpg"
    bot.sendMessage(msg["channel"],meme)




def getMemeInsanity(bot, msg):
    url = "http://version1.api.memegenerator.net/Instances_Select_ByNew?languageCode=en&pageIndex=0&pageSize=12&urlName=Insanity-Wolf"
    data = urllib.request.urlopen(url).read().decode("utf-8")#.read())
    jsonData = json.loads(data)
    try:
        randomWolf = jsonData["result"][random.randrange(0,len(jsonData["result"]))]["instanceImageUrl"]
    except IndexError:
        randomWolf = "wolf not found"
    bot.sendMessage(msg["channel"], randomWolf)


