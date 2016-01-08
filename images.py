import urllib.request
import json
import random
import sys, traceback


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


# get a meme of keyword passed in
# used memeGenerator API to query for memes
# ~insanity
# ~meme,keyword
def getMeme(bot, msg):
    try:
        if ("~insanity" in msg["text"]):
            url = "http://version1.api.memegenerator.net/Instances_Select_ByNew?languageCode=en&pageIndex=0&pageSize=12&urlName=Insanity-Wolf"
            data = urllib.request.urlopen(url).read().decode("utf-8")#.read())
        else:
            keyword = msg["text"].split(",")[1]
            url = "http://version1.api.memegenerator.net/Instances_Select_ByNew?languageCode=en&pageIndex=0&pageSize=12&urlName="
            data = urllib.request.urlopen(url+keyword).read().decode("utf-8")
        jsonData = json.loads(data)
        meme = jsonData["result"][random.randrange(0,len(jsonData["result"]))]["instanceImageUrl"]
    except IndexError:
        meme = "wolf not found"
    except Exception as e:
        meme = "nope.jpg"
        print("exception getMeme " + str(e))
        print()
        traceback.print_exc(file=sys.stdout)
    bot.sendMessage(msg["channel"],meme)


def distractionChan(bot):
    bot.messageCount += 1
    # send a message every 50 messages
    if (bot.messageCount % 50 == 0):
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
        bot.sendMessage(bot.distrChan, wordGif)
        bot.sendMessage(bot.distrChan, randomWord)


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