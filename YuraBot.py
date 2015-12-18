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
        with open("tokenYura.txt", "r") as tRead:
                 self.token = tRead.read()
        #global sc
        self.sc             = SlackClient(self.token)
        self.id             = json.loads(self.sc.api_call("auth.test", token=self.token).decode("utf-8"))["user_id"]
        self.distrChan      = "G0EFAE1EE"
        self.interns        = ["Alex","Yura", "Steven G", "Avik", "Tommy","Jon"] # all the interns separately
        self.people         = self.interns + ["Omar", "David", "Alan", "Alison", 
                                "Bulent", "Carlos", "Jeff", "Steven", "Thurston", "Linda","Derek", "Sean"] # everyone in the company
        self.bots           = ["U0CK96B71","U0CK96B71","U0ARYU2CT"] # list of bots in use
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
                    msgs = self.sc.rtm_read()
                    for msg in msgs:
                        #print(msg)
                        if("type" in msg and msg["type"] == "error"):
                            print("\n[!!] error: \n" + msg)
                            # user_is_bot errors because bot cannot use that api function
                            error = "message error - probably no quotes found"
                            self.sendMessage(self.last_channel, error) # error messages don"t have a channel
                            self.sendError()
                        elif("type" in msg and msg["type"] == "presence_change" and 
                                                       msg["presence"] == "active" and msg["user"]):
                            print(msg)
                            if(msg["user"] =="U0665DKSL"):
                               #post to interns-education as "user is active"
                               #message = self.userDict[msg["user"]] + " is active"
                               message = "Yura is the fake one"
                               self.sendMessage("G09LLA9EW",message)
                               print("[I] sent: "+message)
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


    #~DM,user,msg - user has to be the @"user" string
    def sendDM(self,msg):
        print("\n" + str(msg) + "\n\n")
        args = msg["text"].split(",")
        userName = args[1]
        message = args[2]
        print(args)
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

g = GoTo()
g.start()