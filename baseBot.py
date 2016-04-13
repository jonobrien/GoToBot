import time
import datetime
import string
import random
import urllib.request
import os.path
import queue
from slackclient import SlackClient
import sys, traceback
import json
import re
# add more features
import poll


class GoTo:

    def __init__(self):
        self.start()


    def start(self):
        print("start")
        self.token = ""
        with open("token.txt", "r") as tRead:
                 self.token = tRead.read()

        self.sc             = SlackClient(self.token)
        self.id             = json.loads(self.sc.api_call("auth.test", token=self.token).decode("utf-8"))["user_id"]
        self.quoteChan      = "G0CCGHGKS"
        self.userDict       = {}   # {"ID":"@username","ID2":"@username2"}
        self.idDict         = {}   # {"@username":"ID","@user2":"ID2"}
        self.groupDict      = {}   # {"ID":"channel info...", ... } metadata about channels
        self.polls          = []   # list of polls
        self.messageCount   = 0    # for distractionChannel()
        self.whiteWrite     = open # fd for whitelist
        self.whitelist      = []   # list of channels bot can post in
        self.legalChars     = string.printable.replace("`", "") # characters that can be manipulated/printed
        with open("whitelist.txt", "r") as self.whiteRead:
            self.whitelist  = self.whiteRead.read().split(" ")

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


    def startBot(self):
        try:
            print("startBot")
            # need groups.list api call for the dict of private group info dict by id key
            # make it once at startup, save it for later
            users = json.loads(self.sc.api_call("users.list", token=self.token).decode("utf-8"))["members"]
            groups = json.loads(self.sc.api_call("groups.list", token=self.token).decode("utf-8"))["groups"]
            ims = json.loads(self.sc.api_call("im.list", token=self.token).decode("utf-8"))["ims"]
            for user in users:
                self.userDict[user["id"]] = user["name"]
                self.idDict[user["name"]] = user["id"]
            # setup the groupDict used for private group/im info and id reference
            # contains all meta data about those channels and can be used later
            # get it once, so every delete call doesn't repeat them
            for group in groups:
                self.groupDict[group['id']] = group
            for im in ims:
                self.groupDict[im['id']] = im

            print(datetime.datetime.now())




            if self.sc.rtm_connect():
                print("connected")
                while True:

                    msgs = self.sc.rtm_read()
                    for msg in msgs:

                        if("type" in msg and msg["type"] == "error"):
                            print("\n[!!] error: \n" + msg + "\n")
                            self.sendError()
                        elif("type" in msg and msg["type"] == "message"and "text" in msg and 
                            all(c in self.legalChars for c in msg["text"].replace("'",""))):

                            self.inWhitelist(msg)

                            if(msg["channel"] in self.whitelist):
                                m = msg["text"]
                                #  cuts text contained between <> ex: <test>
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


    def removeComments(s):
        while(s.contains("<") and s.contains(">")):
            left = s.indexOf("<")
            right = s.indexOf(">")
            s = s.substring(0, left)


def quote(bot, msg):
    try:
        print(msg)
        # pad with None values if nothing there on split
        # protects against empty strings as well
        cmd,person,text = ([x for x in msg["text"].split(",") if x != ""] + [None]*3)[:3]
        channel = msg["channel"]
        if(person is not None):
            # can handle all cases and forms of the '@uSerName' 'username' etc
            person = person.lower().replace("@","")
        if (channel != bot.quoteChan):
            print("quote check")
            return -1
        #  new quote
        if (cmd and person and text):
            if(person in bot.idDict):
                fileName = person + "Quotes.txt"  
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
            if(person in bot.idDict):
                fileName = person + "Quotes.txt"
                if(os.path.isfile(fileName)):
                    with open(fileName, "r") as read:
                        quotes = read.read().split(",")
                else:
                    bot.sendMessage(channel, "no quotes for " + person + " you should add some")
                if(quotes):
                    quote = random.choice(quotes)
                    bot.sendMessage(channel, quote)
        else:
            bot.sendMessage(channel, "not enough args for ~quote,person,text or ~quote,person (actual input is -> " +cmd+"," + str(person) + ", " + str(text) + ")")

            return -1
    except Exception:
        print("[!!] error in quote")
        bot.sendError()


# delete the last message posted by the bot in the channel requested
# tried doing it based off the message json but `key errors` happened
def delete(bot, msg):
    print("\ndeleting last message in specified channel: " + str(msg["channel"]))
    msgResponse = bot.sc.api_call("groups.history", token=bot.token, channel=msg["channel"])
    msgJson = json.loads(msgResponse.decode("utf-8"))
    if("messages" in msgJson):
        for message in msgJson["messages"]:
            # can only delete messages owned by sender
            if ("user" in message and message["user"] == bot.id and ("subtype" not in message)):
                bot.sc.api_call("chat.delete", token=bot.token, ts=message["ts"], channel=msg["channel"])
                print("deleted: " + message["ts"])
                break
    else:
        bot.sendMessage(msg['channel'], "no bot messages in channel")
    print("done deleting\n")


# delete every message sent, from last 100, in private groups and ims
# TODO -- needs to have "has_more" check for > 100
def deleteAll(bot, msg):
    print("\ndeleting all messages in private groups and ims")
    for chan in bot.groupDict:
        if(chan.startswith("D")):
            print("deleting ims for: " + chan + " -> " +  str(bot.userDict[bot.groupDict[chan]['user']]))
            msgResponse = bot.sc.api_call("im.history", token=bot.token, channel=bot.groupDict[chan]["id"])
            msgJson = json.loads(msgResponse.decode("utf-8"))
        elif (chan.startswith("G")):
            print("deleting group messages in: " + chan + " -> " +  str(bot.groupDict[chan]['name']))
            msgResponse = bot.sc.api_call("groups.history", token=bot.token, channel=bot.groupDict[chan]["id"])
            msgJson = json.loads(msgResponse.decode("utf-8"))
        for message in msgJson["messages"]:
            # can only delete messages owned by sender
            if ("user" in message and message["user"] == bot.id and ("subtype" not in message)):
                bot.sc.api_call("chat.delete", token=bot.token, ts=message["ts"], channel=bot.groupDict[chan]["id"])
                print("deleted: " + message["ts"])
    print("done deleting\n")


if __name__ == "__main__":
    # TODO -- move out of this file
    router = [{  "text": ["~help"],
      "callback":GoTo.help,
      "type": "text"
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
      "text": ["~deleteall"],
      "callback":deleteAll,
      "type": "text",
      "help": "`~deleteall`            - Deletes all private group/dm messages sent by the bot."
    },{
      "text": ["~delete"],
      "callback":delete,
      "type": "text",
      "help": "`~delete`               - Deletes the last message sent by bot in the specified channel."
    },{
      "text": ["~dm"],
      "callback":GoTo.sendDM,
      "type": "text",
      "help": ""
    },
    # {
    #   "text": ["Sorry, but you aren"t authorized to use this command.", "luna"],
    #   "callback": luna,
    #   "type": "text",
    #   "help": ""
    # }
    ]
    g = GoTo()
    g.start()
