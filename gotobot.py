import time
import datetime
import string
import random
import urllib.request
import os.path
import datetime
import queue
from slackclient import SlackClient
import sys, traceback
import json
#import pony as p
import poll
import wave
import pyaudio
import images
import catFacts
import re
#import git
class GoTo:

    def __init__(self):
        self.start()


    def start(self):
        print("start")
        self.token = ""
        with open("token.txt", "r") as tRead:
                 self.token = tRead.read()
        #global sc
        self.sc             = SlackClient(self.token)
        self.id             = json.loads(self.sc.api_call("auth.test", token=self.token).decode("utf-8"))["user_id"]
        self.distrChan      = "G0EFAE1EE"
        self.quoteChan      = "G0CCGHGKS"
        self.interns        = ["Alex","Yura", "Steven G", "Avik", "Tommy","Jon"] # all the interns separately
        self.people         = self.interns + ["Omar", "David", "Alan", "Alison", 
                                "Bulent", "Carlos", "Jeff", "Steven", "Thurston", "Linda","Derek", "Sean"] # everyone in the company
        self.bots           = ["U0CK96B71","U0CK96B71","U0ARYU2CT"] # list of bots in use
        self.timestamp      = queue.Queue() # queue for deleting messages
        self.last_channel   = ""   # last channel message received from
        self.userDict       = {}   # {"ID":"@username","ID2":"@username2"}
        self.idDict         = {}   # {"@username":"ID","@user2":"ID2"}
        self.polls          = []   # list of polls
        self.messageCount   = 0    # for distractionChannel()
        self.whiteWrite     = open # fd for whitelist
        self.whitelist      = []   # list of channels bot can post in
        self.words          = []   # list of words in eng. dictionary
        self.legalChars     = string.printable.replace("`", "") # characters that can be manipulated/printed
        with open("whitelist.txt", "r") as self.whiteRead:
            self.whitelist  = self.whiteRead.read().split(" ")
        with open("EN_dict.txt", "r") as readLines:
            self.words      = readLines.read().split("\n")
        print("starting bot loop")
        self.startBot()


    def help(self, msg):
        info = "```\n"
        info += "A Python Slack API bot:\n\n"
        info += "hosted on Github:\n"
        info += "https://github.com/Omodi/GoToBot\n"
        info += "https://github.com/jonobrien/GoToBot\n"
        info += "https://github.com/ThomasFoertmeyer/GoToBot\n\n"
        info += "Available Commands:\n"
        for command in router:
            if "help" in command and len(command["help"]) > 0:
                info += command["help"] if command["help"][-1] == "\n" else command["help"] + "\n"
        info +="```"
        self.sendMessage(msg["channel"], info)


    def connect(self):
        print("connect")

    def main(self):
        pass

    def getSC(self):
        return sc

    def startBot(self):
        try:
            print("startBot")
            users = json.loads(self.sc.api_call("users.list", token=self.token).decode("utf-8"))["members"]
            for user in users:
                self.userDict[user["id"]] = user["name"]
                self.idDict[user["name"]] = user["id"]
            print(datetime.datetime.now())
            #print(self.userDict)
            if self.sc.rtm_connect(): # connected to slack real-time messaging api
                print("connected")
                while True:
                    now = time.strftime("%H:%M:%S")
                    if (now == "16:20:00" or now == "16:20:30"):
                        print("420 time")
                        images.blaze(self)

                    msgs = self.sc.rtm_read()
                    for msg in msgs:
                        #print(msg)
                        images.distractionChan(self)
                        catFacts.subbedToCatFacts(self)

                        #### kick a user when they join a channel #####################################
                        #
                        # if("subtype" in msg and msg["subtype"] == "group_join"):
                        #     print("remove")
                        #     print(self.sc.api_call("groups.kick",channel=msg["channel"], user="U0CNP6WRK"))##bots can't kick, use your user api key not bot key to have bot kick users
                        #
                        ##### send message everytime a user becomes active ############################
                        #
                        #elif("type" in msg and msg["type"] == "presence_change" and 
                        #                                msg["presence"] == "active" and msg["user"]):
                        #    # if(msg["user"] not in self.bots):
                        #        # not b0t, Luna, gotoo
                        #        # post to interns-education as "user is active"
                        #        # message = self.userDict[msg["user"]] + " is active"
                        #        # sendMessage("G09LLA9EW",message)
                        #        # print("[I] sent: "+message)
                        ###############################################################################

                        if("type" in msg and msg["type"] == "error"):
                            print("\n[!!] error: \n" + msg)
                            # user_is_bot errors because bot cannot use that api function
                            error = "message error - probably no quotes found"
                            self.sendMessage(self.last_channel, error) # error messages don"t have a channel
                            self.sendError()
                        elif("type" in msg and msg["type"] == "message"and "text" in msg and 
                                            all(c in self.legalChars for c in msg["text"].replace("'",""))):
                            #print(msg)
                            self.inWhitelist(msg)
                            ### the reactions are unwanted double spacing #############################
                            #
                            # if("user" in msg and msg["user"] == self.idDict["steveng"]):
                            #     print("corn")
                            #     channel = msg["channel"]
                            #     timestamp = msg["ts"]
                            #     self.addReaction(channel,timestamp,"corn")
                            # elif("user" in msg and msg["user"] == self.idDict["jono"]):
                            #     print("hancock")
                            #     channel = msg["channel"]
                            #     timestamp = msg["ts"]
                            #     self.addReaction(channel,timestamp,"hancock")
                            # elif("user" in msg and msg["user"] == self.idDict["osardar"]):
                            #      print("hancock")
                            #      channel = msg["channel"]
                            #      timestamp = msg["ts"]
                            #      self.addReaction(channel,timestamp,"partyparrot")
                            # elif("user" in msg and msg["user"] == self.idDict["derek"]):
                            #     print("derek")
                            #     channel = msg["channel"]
                            #     timestamp = msg["ts"]
                            #     self.addReaction(channel,timestamp,"derek")
                            ###########################################################################

                            if(msg["channel"] in self.whitelist):
                                m = msg["text"]
                                m = re.sub(r'&lt;(.*?)&gt;', '', m)
                                msg["santized"] = m
                                for r in router:
                                    for t in r["text"]:
                                        if(t.lower() in m.lower()):
                                            r["callback"](self, msg)
                        elif("ok" in msg and msg["ok"] == True):
                            self.timestamp.put({"ts":msg["ts"],"channel":self.last_channel})
                    time.sleep(1)
            else:
                print("[!!] Connection Failed, invalid token?")
        except AttributeError:
            print("[!!] error - probably in the send")
            traceback.print_exc(file=sys.stdout)
            print("[!!] restarting the bot")
            self.sc = SlackClient(self.token)
            self.start()
        except Exception:
            print("[!!] uncaught error")
            traceback.print_exc(file=sys.stdout)
            print("[!!] restarting the bot")
            time.sleep(5)
            self.sc = SlackClient(self.token)
            self.start()


    def inWhitelist(self,msg):
        if (msg["text"].lower() == "~addgrouptowhitelist" and msg["channel"] not in self.whitelist):
            self.whitelist.append(msg["channel"])
            print("whitelist added: " + msg["channel"])
            with open("whitelist.txt", "w") as self.whiteWrite:
                self.whiteWrite.write(" ".join(self.whitelist))
            return True


    def sendMessage(self,channel, message):
        try:
            #self.sc.rtm_send_message(channel, message)
            self.sc.api_call("chat.postMessage", channel=channel, 
                        text=message, as_user=True, unfurl_media=True)
            self.last_channel = channel
        except Exception:
            exception = traceback.print_exc(file=sys.stdout)
            self.sendError()


    # need to figure out how to clean the stack
    # for a fresh restart on errors
    # traces seem to just get huge due to all except handling
    # should just try and fix some looping of excepts
    def sendError(self):
        print("\n[!!] sending failed")
        traceback.print_exc(file=sys.stdout)
        print("\n[!!] restarting the bot\n")
        self.sc = SlackClient(self.token)
        self.start()


    # ~dm,user,msg - user has to be the @"user" string
    # ex: @jono would be `~dm,jono,message text here`
    def sendDM(self,msg):
        print("\n" + str(msg) + "\n\n")
        cmd,userName,message = ([x for x in msg["text"].split(",") if x != ""] + [None]*3)[:3]
        if (userName and message):
            try:
                recipient = self.idDict[userName]
                imOpen = self.sc.api_call("im.open", token=self.token, user=recipient)
                imJson = json.loads(imOpen.decode("utf-8"))
                dmChannel = imJson["channel"]["id"]
                chatPost = self.sc.api_call("chat.postMessage",token=self.token, 
                                channel=dmChannel, text=message, as_user="true")
                #whitelist the channel
                self.inWhitelist(msg)
            except Exception:
                self.sendError()


    def addReaction(self, channel,timestamp,reaction):
        try:
            self.sc.api_call("reactions.add", token=self.token, name=reaction, 
                            channel=channel, timestamp=timestamp)
        except Exception:
            self.sendError()


    def removeComments(s):
        while(s.contains("<") and s.contains(">")):
            left = s.indexOf("<")
            right = s.indexOf(">")
            s = s.substring(0, left)


def colorCode(bot, msg):
    print("color")
    name = msg["text"][1 + msg["text"].find(" "):]
    if(name == msg["text"]):
        message = "invalid arguments"
        bot.sendMessage(msg["channel"], message)
        return
    # tmp="#"
    # for ch in name[:3]:
    #     tmp += hex(ord(ch))[2:]
    if(name.lower() == "jon"):
        h = "#39FF14"
    elif(name.lower() == "verbose"):
        h = "#b00bee"
    else:
        h = "#" + hex(abs(hash(name)))[2:8]
    #print (h)
    bot.sendMessage(msg["channel"], h)


def randomIntern(bot, msg):
    ranIntern = random.choice(bot.interns)
    if (ranIntern != "Alex"):
        bot.sendMessage(msg["channel"], ranIntern)
    else:
        bot.sendMessage(msg["channel"], "nope")


def quote(bot, msg):
    try:
        print(msg)
        # pad with None values if nothing there on split
        # protects against empty strings as well
        cmd,person,text = ([x for x in msg["text"].split(",") if x != ""] + [None]*3)[:3]
        channel = msg["channel"]
        if (channel != bot.quoteChan):
            print("quote check")
            return -1
        #  new quote
        if (cmd and person and text):
            if(person in bot.idDict):             # bot.people):
                fileName = person + "Quotes.txt"  # bot.people[bot.people.index(person)] + "Quotes.txt"
                if(os.path.isfile(fileName)):
                    with open(fileName, "a+") as f:
                        f.write("," + text)
                else:
                    with open(fileName, "a+") as f:
                        f.write(text)
                bot.sendMessage(channel, "Quote added " + text)
        # user requested quote from saved files
        elif(cmd and person):
            quotes = []
            if(person in bot.idDict):              # bot.people):
                fileName = person + "Quotes.txt"   # bot.people[bot.people.index(person)] + "Quotes.txt"
                if(os.path.isfile(fileName)):
                    with open(fileName, "r") as read:
                        quotes = read.read().split(",")
                else:
                    bot.sendMessage(channel, "no quotes for " + person + " you should add some")
                if(quotes):
                    quote = random.choice(quotes)
                    ### Alex pleonasm feature #############################
                    # if (person == "Alex"):
                    #     pleo1 = " Pleonasms"*random.randrange(1,3)
                    #     pleo2 = " Pleonasms"*random.randrange(2,5)
                    #     quote =  pleo1 + "\n" + quote + "\n" + pleo2
                    bot.sendMessage(channel, quote)
        else:
            print("[!!] not enough args (cmd, person, text): ")
            print(cmd)
            print(person)
            print(text)
            print()
            return -1
    except Exception:
        print("[!!!] error in quote")
        bot.sendError()


# messages - needs to be updated
def delete(bot, msg):
    if(not bot.timestamp.empty()):
        ts = bot.timestamp.get()
        for w in bot.whitelist:
            bot.sc.api_call("chat.delete",channel=w, ts=str(ts["ts"]))


# delete every message sent, from last 100
# needs to have "has_more" check for > 100
# TODO -- delete DMs as well using 'python-slackclient'
def deleteAll(bot, msg):
    print("\ndeleting all messages in private groups")
    grpResponse = bot.sc.api_call("groups.list", token=bot.token)
    grpJson = json.loads(grpResponse.decode("utf-8"))
    for chan in grpJson["groups"]:
        print("deleting in: " + str(chan["name"]) + " + " + str(chan["id"]))
        msgResponse = bot.sc.api_call("groups.history", token=bot.token, channel=chan["id"])
        msgJson = json.loads(msgResponse.decode("utf-8"))
        for message in msgJson["messages"]:
            # can only delete messages owned by sender
            if ("user" in message and message["user"] == bot.id and ("subtype" not in message)):
                bot.sc.api_call("chat.delete",token=bot.token,ts=message["ts"], channel=chan["id"])
                print("deleted: " + message["ts"])
    print("done deleting")


def test(bot, msg):
    testing = "blackbox whitebox "*random.randrange(5,20)
    bot.sendMessage(msg["channel"], testing)


def pony(bot, msg):
    bot.sendMessage(msg["channel"], "```" + p.Pony.getPony() + "```")


def randominterns(bot,msg):
    bot.sendMessage(msg["channel"],"Alex")


def luna(bot,msg):
    bot.sendMessage(msg["channel"], "luna shutdown")


def playGong(bot, msg):
    CHUNK = 1024
    wf = wave.open("gong.wav", "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data != "":
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    # TODO -- move out of this file
    router = [{
      "text": ["~colorname", "~color name"],
      "callback":colorCode,
      "type": "text",
      "help": "`~colorname (string)`   - the space is necessary.  Returns a hex color code derived from input"
    },{
      "text": ["~randomintern"],
      "callback":randomIntern,
      "type": "text",
      "help": "`~randomintern`         - select a random intern to give a task to"
    },{  "text": ["~help"],
      "callback":GoTo.help,
      "type": "text"
    },{
      "text": ["~catfacts", "~cat facts"],
      "callback":catFacts.catFacts,
      "type": "text",
      "help": "`~catfacts`             - Returns a random catfact"
    },{
      "text": ["~quote"],
      "callback":quote,
      "type": "text",
      "help": ""
    },{
      "text": ["~startpoll","~poll","~createpoll","~start poll","~poll","~create poll"],
      "callback":poll.startPoll,
      "type": "text",
      "help": "`~startpoll,(nameOfPoll),(option1),(option2),...(optionX)`\n                        - Creates a poll that can be voted on, closed or have an option added to the poll"
    },{
      "text": ["~stoppoll","~removepoll","~stop poll","~remove poll"],
      "callback":poll.stopPoll,
      "type": "text",
      "help": "`~stoppoll,(pollName)`  - Ends the poll and displays results"
    },{
      "text": ["~vote","~votepoll","~vote poll"],
      "callback":poll.vote,
      "type": "text",
      "help": "`~vote,(pollName),(option)`\n                        - Votes for (option). If you have aready voted it removes your old vote"
    },{
      "text": ["~addoption"],
      "callback":poll.addOption,
      "type": "text",
      "help": "`~addoption,(pollName),(newOption)`\n                        - Creates a new option for a poll"
    },{
      "text": ["ship it",":shipit:", "shipit"],
      "callback":images.shipIt,
      "type": "text",
      "help": "`ship it`               - Returns ship it squirrel image"
    },{
      "text": ["~deleteall"],
      "callback":deleteAll,
      "type": "text",
      "help": "`~deleteall`            - Deletes all private group messages sent by the bot. (under development for DMs)"
    },{
      "text": ["~delete"],
      "callback":delete,
      "type": "text",
      "help": "`~delete`               - Deletes the last message sent by bot. Group agnostic"
    },{
      "text": ["~nye"],
      "callback":images.nye,
      "type": "text",
      "help": "`~nye`                  - Returns a bill nye gif"
    },{
      "text": ["test"],
      "callback":test,
      "type": "text",
      "help": "`test` `testing`        - any appearance of the string `test` there will be a response posted"
    },{
      "text": ["~meme"],
      "callback":images.getMeme,
      "type": "text",
      "help": "`~meme,(keyword)`       - Gets a meme with given keyword.  Returns nope.jpg if no meme found"
    },{
      "text": ["~gif"],
      "callback":images.getGiphy,
      "type": "text",
      "help": "`~gif,(keyword)`        - Returns a gif with the given keyword"
    },{
      "text": ["~insanity"],
      "callback":images.getMeme,
      "type": "text",
      "help": "`~insanity`             - Returns an insanity wolf meme"
    },
    # {
    #   "text": ["~dm"],
    #   "callback":GoTo.sendDM,
    #   "type": "text",
    #   "help": ""
    # },
    # {
    #   "text": ["pony", "Good morning! Here are the results from last night"s nightly test:"],
    #   "callback": pony,
    #   "type": "text",
    #   "help": ""
    # },
    {
      "text": ["~random intern", "~ randomintern"],
      "callback": randominterns,
      "type": "text",
      "help": ""
    },
    # {
    #   "text": ["Sorry, but you aren"t authorized to use this command.", "luna"],
    #   "callback": luna,
    #   "type": "text",
    #   "help": ""
    # }
    {
      "text": ["zach", "zachisan", "<3", ":heart:",":heart_decoration:", "zack", 
            ":heart_eyes:",":heartbeat:",":heartpulse:",":hearts:"],
      "callback": playGong,
      "type": "text",
      "help": ""
    }]
    g = GoTo()
    g.start()