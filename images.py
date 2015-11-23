import urllib.request
import json
import random

def nye(bot, msg):
    nyeMlg = "http://i.giphy.com/m6ILp14NR2RDq.gif"
    bot.sendMessage(msg["channel"], nyeMlg)

def getGiphy(bot, msg):
    urlStart = "http://api.giphy.com/v1/gifs/search?q="
    urlEnd = "&api_key=dc6zaTOxFJmzC&limit="
    imageLimit = "1"
    keywords = ",".join(msg["text"].split(",")[1:])
    if("jon" in keywords.lower()):
        keywords = "sloth"
    print(keywords)
    data = urllib.request.urlopen(urlStart + keywords +urlEnd + imageLimit).read().decode("utf-8")#.read())
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
    data = urllib.request.urlopen(url + keywords +"&api_key=dc6zaTOxFJmzC&limit=4").read().decode("utf-8")#.read())
    jsonData = json.loads(data)
    try:
        jsonData = random.choice(jsonData["data"]) # take a random gif from the array of returned images
        gif = jsonData["images"]["original"]["url"]#jsonData["data"][0]["images"]["original"]["url"]
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
        # url string
        randomWolf = jsonData["result"][random.randrange(0,len(jsonData["result"]))]["instanceImageUrl"]
        # data = {}
        # data['text'] = randomWolf
        # data['unfurl_url'] = True
        # randomWolf = json.dumps(data)
    except IndexError:
        randomWolf = "wolf not found"
    bot.sendMessage(msg["channel"], randomWolf)


def distractionChan(bot):
    bot.messageCount += 1
    if (bot.messageCount % 20 == 0):
        print("messageCount: " + str(int(bot.messageCount)))
        randomWord = random.choice(bot.words)
        print("random word: " + randomWord)
        url = "http://api.giphy.com/v1/gifs/search?q="
        data = urllib.request.urlopen(url + randomWord +"&api_key=dc6zaTOxFJmzC&limit=1").read().decode("utf-8")#.read())
        jsonData = json.loads(data)
        try:
            wordGif = jsonData["data"][0]["images"]["original"]["url"]
        except IndexError:
            wordGif = "random gif not found for " + randomWord
        bot.sendMessage("G0EFAE1EE", wordGif)


def shipIt(bot, msg):
    squirrels = [
      "http://shipitsquirrel.github.io/images/ship%20it%20squirrel.png",
      "http://shipitsquirrel.github.io/images/squirrel.png",
      "http://images.cheezburger.com/completestore/2011/11/2/aa83c0c4-2123-4bd3-8097-966c9461b30c.jpg",
      "http://images.cheezburger.com/completestore/2011/11/2/46e81db3-bead-4e2e-a157-8edd0339192f.jpg",
      "http://28.media.tumblr.com/tumblr_lybw63nzPp1r5bvcto1_500.jpg",
      "http://i.imgur.com/DPVM1.png",
      "http://d2f8dzk2mhcqts.cloudfront.net/0772_PEW_Roundup/09_Squirrel.jpg",
      "http://www.cybersalt.org/images/funnypictures/s/supersquirrel.jpg",
      "http://www.zmescience.com/wp-content/uploads/2010/09/squirrel.jpg",
      "http://img70.imageshack.us/img70/4853/cutesquirrels27rn9.jpg",
      "http://img70.imageshack.us/img70/9615/cutesquirrels15ac7.jpg",
      "https://dl.dropboxusercontent.com/u/602885/github/sniper-squirrel.jpg",
      "http://1.bp.blogspot.com/_v0neUj-VDa4/TFBEbqFQcII/AAAAAAAAFBU/E8kPNmF1h1E/s640/squirrelbacca-thumb.jpg",
      "https://dl.dropboxusercontent.com/u/602885/github/soldier-squirrel.jpg",
      "https://dl.dropboxusercontent.com/u/602885/github/squirrelmobster.jpeg",
    ]
    bot.sendMessage(msg["channel"], random.choice(squirrels))