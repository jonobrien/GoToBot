import time
import string
import random
import urllib.request
import os.path
import queue
from slackclient import SlackClient
import sys, traceback
import json
import pony as p
import poll
# import wave
# import pyaudio
import images
import catFacts
import re
import partyparrot.partyparrot as pp
import partyparrot.alphabet as al
#import git
class GoTo:

    def __init__(self):
        self.start()


    def start(self):
        print("initializing bot...")
        self.token = ""
        with open("token.txt", "r") as tRead:
                 self.token = tRead.read()
        #global sc
        self.sc             = SlackClient(self.token)
        authTestResult = self.sc.api_call("auth.test", token=self.token)
        if "error" in authTestResult:
            raise ValueError("Invalid Token")
        self.id             = authTestResult["user_id"]
        #self.distrChan      = "G0EFAE1EE"
        self.quoteChan      = "G0CCGHGKS"
        self.interns        = ["Steven G", "Micheal", "Tommy", "Yura"]
        self.people         = self.interns + ["Zach", "David", "Alan", "Alison",
                                "Bulent", "Carlos", "Jeff", "Steven", "Thurston", "Linda","Derek"]
        self.bots           = ["U0CK96B71","U0CK96B71","U0ARYU2CT"] # list of bots in use
        self.last_channel   = ""   # last channel message received from
        self.userDict       = {}   # {"ID":"@username","ID2":"@username2"}
        self.idDict         = {}   # {"@username":"ID","@user2":"ID2"}
        self.chanDict       = {}   # {"ID":"channel info...", ... }
        self.polls          = []   # list of polls
        self.messageCount   = 0    # for distractionChannel()
        self.whiteWrite     = open # fd for whitelist
        self.whitelist      = []   # list of channels bot can post in
        self.words          = ["pizza", "cat"]   # list of words in eng. dictionary
        self.legalChars     = string.printable.replace("`", "") # characters that can be manipulated/printed
        # need to make these files initially, otherwise FNF Error
        with open("whitelist.txt", "r") as self.whiteRead:
            self.whitelist  = self.whiteRead.read().split(" ")
        with open("EN_dict.txt", "r") as readLines:
            self.words      = readLines.read().split("\n")


        print("bot initialized, starting...")
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



    def startBot(self):
        try:
            print("startBot() id: " + self.id)
            # need groups.list api call for the dict of private group info dict by id key
            # make it once at startup, save it for later
            users = (self.sc.api_call("users.list", token=self.token))["members"]
            groups = (self.sc.api_call("groups.list", token=self.token))["groups"]
            ims = (self.sc.api_call("im.list", token=self.token))["ims"]
            channels = (self.sc.api_call("channels.list", token=self.token))["channels"]
            for user in users:
                self.userDict[user["id"]] = user["name"]
                self.idDict[user["name"]] = user["id"]

            # setup the chanDict used for private group/im and public channel info and id reference
            # contains all meta data about those channels and can be used later
            # get it once, so every delete call doesn't repeat them
            # TODO -- seems like joining a channel after starting the bots
            #   allows for deletion even though bot joined after the dictionary was created
            for group in groups:
                self.chanDict[group['id']] = group
            for im in ims:
                self.chanDict[im['id']] = im
            for chan in channels:
                self.chanDict[chan['id']] = chan
            if self.sc.rtm_connect(): # connected to slack real-time messaging api
                print("connected")

                while True:
                    msgs = self.sc.rtm_read()
                    for msg in msgs:
                        # debug messages
                        ##if ("subtype" not in msg):
                        ######print(msg)

                        #images.distractionChan(self)

                        catFacts.subbedToCatFacts(self)

                        #### kick a user when they join a channel #####################################
                        #      (need user api key, not bot key)
                        #
                        #
                        # if("subtype" in msg and msg["subtype"] == "group_join"):
                        #     print("remove")
                        #     print(self.sc.api_call("groups.kick",channel=msg["channel"], user="U0CNP6WRK"))##bots can't kick, use your user api key not bot key to have bot kick users
                        #
                        #
                        ##### send message every time a user becomes active ###########################
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

                            if(msg["channel"] in self.whitelist):
                                m = msg["text"]
                                #  cuts text contained between <> ex: <test>
                                # TODO -- more detailed usage info for specific commands
                                # to allow for future ~help,<~function> to only display the help message
                                m = re.sub(r'&lt;(.*?)&gt;', '', m)
                                msg["santized"] = m
                                for r in router:
                                    for t in r["text"]:
                                        if(t.lower() in m.lower()):
                                            r["callback"](self, msg)
                    time.sleep(1)
            else:
                print("[!!] Connection Failed, invalid token?")
        except AttributeError:
            print("[!!] error - probably in the send")
            traceback.print_exc(file=sys.stdout)
            print("[!!] restarting the bot")
            self.sc = SlackClient(self.token)
            time.sleep(5)
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
            self.sendMessage(msg["channel"], "channel whitelisted")
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
            recipient = ''
            # slack converts the @name to the uid number when you mention someone via text
            if (userName.startswith("@")):
                recipient = self.userDict[userName] # @U1234 passed in
            try:
                recipient = self.idDict[userName] # jono passed in

                if (recipient == self.id):
                    self.sendMessage(msg["channel"], "bot cannot dm self\n")
                imOpenJson = self.sc.api_call("im.open", token=self.token, user=recipient)
                dmChannel = imOpenJson["channel"]["id"]
                # don't whitelist everytime, also this doesn't work as text deosn't pass check, user case 1
                self.inWhitelist(msg) # check returned json for already open channel, inform user case 2
                chatPost = self.sc.api_call("chat.postMessage",token=self.token,
                                channel=dmChannel, text=message, as_user="true")
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


    # delete the last message posted by the bot in the channel requested
    # tried doing it based off the message json but `key errors` happened
    def delete(self, msg):
        print("\ndeleting last message in specified channel: " + str(msg["channel"]))
        msgResponse = self.sc.api_call("groups.history", token=self.token, channel=msg["channel"])
        msgJson =msgResponse
        if("messages" in msgJson):
            for message in msgJson["messages"]:
                # can only delete messages owned by sender
                if ("user" in message and message["user"] == self.id and ("subtype" not in message)):
                    self.sc.api_call("chat.delete", token=self.token, ts=message["ts"], channel=msg["channel"])
                    print("deleted: " + message["ts"])
                    break
        else:
            self.sendMessage(msg['channel'], "no bot messages in channel")
        print("done deleting\n")


    # delete every message sent, from last 100, in private groups and ims
    # TODO -- needs to have "has_more" check for > 100
    def deleteAll(self, msg):
        print("\ndeleting all messages in private groups, ims, public channels")
        queryStr = ''
        im = "im.history"
        group = "groups.history"
        chanStr = "channels.history"

        for chan in self.chanDict:
            hasMore = {}
            if(chan.startswith("D")):
                queryStr = im
                print("            deleting ims for: " + chan + " -> " +  str(self.userDict[self.chanDict[chan]['user']]))
            elif (chan.startswith("G")):
                queryStr = group
                print("  deleting group messages in: " + chan + " -> " +  str(self.chanDict[chan]['name']))
            elif (chan.startswith("C")):
                queryStr = chanStr
                print("deleting messages in channel: " + chan + " -> " +  str(self.chanDict[chan]['name']))
            msgJson = self.sc.api_call(queryStr, token=self.token, channel=self.chanDict[chan]["id"])
            #print(msgJson)
            if ("has_more" in msgJson and msgJson["has_more"] == True):
                for message in msgJson["messages"]: # collect initial 100
                    message["chann"] = chan
                    hasMore[message["ts"]] = message  #'ts' is unique enough for each message in indiv. chan
                more = msgJson
                while(msgJson["has_more"] == True):
                    msgJson = self.sc.api_call(queryStr, token=self.token,
                                channel=chan, latest=more["messages"][-1]["ts"], inclusive=1) # need to page through history
                    for message in msgJson["messages"]: # collect remaining history
                        message["chann"] = chan
                        hasMore[message["ts"]] = message  #'ts' is unique enough for each message in indiv. chan
            if (hasMore): # if has more, this is all messages in that channel
                time.sleep(1) # rate limit prevention
                lim = 0
                for message in hasMore.values():
                    lim+=1
                    if (lim % 20 == 0):
                        time.sleep(3)
                    # seems slack added a bot_id field, different from what they say userid is...
                    if ("user" in message and message["user"] == self.id and ("subtype" not in message)):
                        self.sc.api_call("chat.delete", token=self.token, ts=message["ts"], channel=chan)
                        print("deleted: " + message["ts"])
            elif (msgJson["messages"]): # <= 100 to delete, has messages
                for message in msgJson["messages"]:
                    if ("user" in message and message["user"] == self.id and ("subtype" not in message)):
                        self.sc.api_call("chat.delete", token=self.token, ts=message["ts"], channel=chan)
                        print("deleted: " + message["ts"])
            else:
                if(chan.startswith("D")):
                    print("no messages to delete in: " + chan + " -> " +  str(self.userDict[self.chanDict[chan]['user']]))
                else:
                    print("no messages to delete in: " + chan + " -> " +  str(self.chanDict[chan]['name']))
        print("done deleting\n")


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
    if ranIntern == "Steven G":
        ranIntern = ":tubieg: :steveng: :partyg: :zoomieg:"
    bot.sendMessage(msg["channel"], ranIntern)


def quote(bot, msg):
    try:
        print(msg)
        # pad with None values if nothing there on split
        # protects against empty strings as well
        cmd,person,text = ([x for x in msg["text"].split(",") if x != ""] + [None]*3)[:3]
        channel = msg["channel"]
        if("~quote,person" in msg["text"]):
            print('inf loop check')
            return -1
        if(person is not None):
            # can handle all cases and forms of the '@uSerName' 'username' etc
            person = person.upper().replace("@","").replace("<","").replace(">","").replace(" ","")
        #if (channel != bot.quoteChan):
        #    print("quote check")
        #    return -1
        #  new quote
        if (cmd and person and text):
            name = person
            if (name.startswith("U")): # user typed ~quote,@name
                name = bot.userDict[name]
            if (name.lower() in bot.idDict): # user typed ~quote,name as orig, expected
                name = name.lower()
            else:
                #print('[!!] cmd person text else\n')
                bot.sendMessage(channel, "incorrect args for ~quote,person,text (actual input is -> "
                                            + cmd + "," + str(person) + ", " + str(text) + ")")
                return -1
            fileName = name.lower() + "Quotes.txt"
            if (os.path.isfile(fileName)):
                with open(fileName, "a+") as f:
                    f.write("," + text)
            else:
                with open(fileName, "a+") as f:
                    f.write(text)
            bot.sendMessage(channel, "Quote added for: " + name + " " + text)

        # user requested quote from saved files
        elif (cmd and person):
            name = person.lower()
            print(name)
            quotes = []
            if (name.upper().startswith("U")): # user typed ~quote,@name
                name = bot.userDict[person]
            if (name.lower() in bot.idDict): # user typed ~quote,name as orig, expected
                name = name.lower()
            else:
                #print('[!!] cmd person else\n')
                bot.sendMessage(channel, "incorrect args for ~quote,person (actual input is -> " + cmd + "," + str(person) + ")")
                return -1
            fileName = name.lower() + "Quotes.txt"
            if (os.path.isfile(fileName)):
                with open(fileName, "r") as read:
                       quotes = read.read().split(",")
            else:
                bot.sendMessage(channel, "no quotes for " + name.lower() + " you should add some")
            if (quotes):
                quote = random.choice(quotes)
                bot.sendMessage(channel, quote)

        else:
            #print('[!!] outer else\n')
            bot.sendMessage(channel, "not enough args for ~quote,person,text or ~quote,person (actual input is -> " +cmd+"," + str(person.lower()) + ", " + str(text) + ")")
            return -1
    except Exception:
        print("[!!!] error in quote")
        bot.sendError()


def test(bot, msg):
    testing = "blackboxwhitebox"*random.randrange(5,20)
    bot.sendMessage(msg["channel"], testing)


def pony(bot, msg):
    bot.sendMessage(msg["channel"], "```" + p.Pony.getPony() + "```")


def randominterns(bot,msg):
    bot.sendMessage(msg["channel"],"Alex")


def luna(bot,msg):
    bot.sendMessage(msg["channel"], "luna shutdown")

def partyParrotMsg(bot,msg):
    txt = msg['text'].lower()
    txt = txt[12: len(txt)].strip()
    txt = ''.join(ch for ch in txt if ch in al.ALPHABET)
    print(txt)
    print(pp.convert_str_to_emoji(txt))
    bot.sendMessage(msg["channel"], pp.convert_str_to_emoji(txt, space="           "))


# def playGong(bot, msg):
#     CHUNK = 1024
#     wf = wave.open("gong.wav", "rb")
#     p = pyaudio.PyAudio()
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)
#     data = wf.readframes(CHUNK)
#     while data != "":
#         stream.write(data)
#         data = wf.readframes(CHUNK)
#     stream.stop_stream()
#     stream.close()
#     p.terminate()


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
    },{
      "text": ["~help"],
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
      "callback":GoTo.deleteAll,
      "type": "text",
      "help": "`~deleteall`            - Deletes all private group/dm messages sent by the bot."
    }
    # ,{
    #   "text": ["~delete"],
    #   "callback":GoTo.delete,
    #   "type": "text",
    #   "help": "`~delete`               - Deletes the last message sent by bot in the specified channel."
    # }
    ,{
      "text": ["~nye"],
      "callback":images.nye,
      "type": "text",
      "help": "`~nye`                  - Returns a bill nye gif"
    }
    # ,{
    #   "text": ["test"],
    #   "callback":test,
    #   "type": "text",
    #   "help": "`test` `testing`        - any appearance of the string `test` there will be a response posted"
    # }
    ,{
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
    #   "text": ["~pony"],
    #   "callback": pony,
    #   "type": "text",
    #   "help": "sends ascii art"
    # },
    {
      "text": ["~random intern", "~ randomintern"],
      "callback": randominterns,
      "type": "text",
      "help": ""
    },
    {
      "text":["~partyparrot"],
      "callback": partyParrotMsg,
      "type": "text",
      "help": "`~partyparrot (string)` - Converts text to party parrot"
    }
    # {
    #   "text": ["zach", "zachisan", "<3", ":heart:",":heart_decoration:", "zack",
    #         ":heart_eyes:",":heartbeat:",":heartpulse:",":hearts:"],
    #   "callback": playGong,
    #   "type": "text",
    #   "help": ""
    # }
    ]
    g = GoTo()
    g.start()
