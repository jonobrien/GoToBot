import time
import datetime
import string
import random
import urllib.request
import os.path
import datetime
import queue
from slackclient import SlackClient
from slacker import Slacker
import sys, traceback
import json
#import pony as p
import poll
import wave
import pyaudio
import images
import catFacts
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
        self.sc = SlackClient(self.token)
        self.id = 'U0CK96B71'
        self.interns = ["Jon","Yura", "Steven G", "Avik", "Tommy"]
        self.slackers = ["jono","steveng","yurak","alexb", "tommyf", "derek","avikd"]
        self.people = self.interns + ["Omar", "David", "Alan", "Alison", "Bulent", "Carlos", 
                "Jeff", "Steven", "Thurston", "Linda","Derek", "Sean"]
        self.bots = ["U0CK96B71","U0CK96B71","U0ARYU2CT"]
        self.timestamp = queue.Queue()
        self.last_channel = ""
        #{"ID":"@username","ID2":"@username2"}
        self.userDict = {}
        #{"@username":"ID","@user2":"ID2"}
        self.idDict = {}
        self.polls = []
        self.messageCount = 0
        self.whiteWrite = open
        self.whitelist = []
        self.words = []
        self.legalChars = string.printable.replace("`", "")
        with open("whitelist.txt", "r") as self.whiteRead:
            self.whitelist = self.whiteRead.read().split(" ")
        with open("EN_dict.txt", "r") as readLines:
            self.words = readLines.read().split("\n")
        print("starting bot loop")
        self.startBot()

    def connect(self):
        print("connect")
    def main(self):
        pass

    def getSC(self):
        return sc

    def startBot(self):
        try:
            print("startBot")
            slack = Slacker(self.token)
            #slack.chat.post_message('G0ARYMG3E', 'slacker test')
            response = slack.users.list()
            users = response.body['members']
            for user in users:
                self.userDict[user["id"]] = user["name"]
                self.idDict[user["name"]] = user["id"]
            print(datetime.datetime.now())
            #print(self.userDict)
            # g = git.cmd.Git("C:\\Users\\D\\pfpui")
            #whitelist.remove('')
            # g.pull()
            if self.sc.rtm_connect():
                print("connected")
                while True:
                    now = time.strftime("%H:%M:%S")
                    if (now == "16:20:00" or now == "16:20:30"):
                        images.blaze(self)

                    msg = self.sc.rtm_read()
                    if(len(msg) == 1):
                        msg = msg[0]
                        #print(msg)
                        images.distractionChan(self)
                        catFacts.subbedToCatFacts(self)

                        if("subtype" in msg and msg["subtype"] == 'group_join'):
                            print("remove")
                            print(self.sc.api_call("groups.kick",channel=msg["channel"], user="U0CNP6WRK"))
                        elif("type" in msg and msg["type"] == "presence_change" and 
                                                        msg["presence"] == "active" and msg["user"]):
                            if(msg["user"] not in self.bots):
                                #not b0t, Luna, gotoo
                                #post to interns-education as "user is active"
                                message = self.userDict[msg["user"]] + " is active"
                                #sendMessage("G09LLA9EW",message)
                                #print("[I] sent: "+message)
                        elif("type" in msg and msg["type"] == "error"):
                            print("\n[!!] error: \n" + msg)
                            error = "message error - probably no quotes found"
                            self.sendMessage(self.last_channel, error) # error messages don't have a channel
                            self.sendError()
                        elif("type" in msg and msg["type"] == "message"and "text" in msg and 
                                                        all(c in self.legalChars for c in msg["text"].replace("'",""))):
                            #print(msg)
                            if("user" in msg and msg["user"] == self.idDict["steveng"]):
                                print("corn")
                                channel = msg["channel"]
                                timestamp = msg["ts"]
                                self.addReaction(channel,timestamp,"corn")
                            self.inWhitelist(msg)
                            if(msg["channel"] in self.whitelist):
                                for r in router:
                                    for t in r["text"]:
                                        if(t.lower() in msg["text"].lower()):
                                            r["callback"](self, msg)
                        elif("ok" in msg and msg["ok"] == True):
                            self.timestamp.put({"ts":msg["ts"],"channel":self.last_channel})
                    elif(len(msg) > 1):
                        print(msg)
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
            self.sc = SlackClient(self.token)
            self.start()


    def inWhitelist(self,msg):
        if (msg['text'].lower() == '~addgrouptowhitelist' and msg['channel'] not in self.whitelist):
            self.whitelist.append(msg['channel'])
            print('whitelist added: ' + msg['channel'])
            with open('whitelist.txt', 'w') as self.whiteWrite:
                self.whiteWrite.write(' '.join(self.whitelist))
            return True #this definitely might be implied/0


    def sendMessage(self,channel, message):
        try:
            self.sc.rtm_send_message(channel, message)
            self.last_channel = channel
        except Exception:
            exception = traceback.print_exc(file=sys.stdout)
            self.sendError()


    def sendError(self):
        print("\n[!!] sending failed")
        traceback.print_exc(file=sys.stdout)
        print("\n[!!] restarting the bot\n")
        self.sc = SlackClient(self.token)
        self.start()


    #~DM,user,msg - user has to be the @'user' string
    def sendDM(self,msg):
        print("\n" + str(msg) + "\n\n")
        args = msg["text"].split(",")
        userName = args[1]
        message = args[2]
        print(args)
        try:
            recipient = self.idDict[userName]
            slack = Slacker(self.token)
            imOpen = slack.im.open(user=recipient) 
            #send = self.sc.api_call("im_open",token=self.token, user=sendUser)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            dmChannel = imOpen.body["channel"]["id"]
            chatPost = slack.chat.post_message(channel=dmChannel, text=message, as_user="true")
            #whitelist the channel
            msg = {}
            msg["text"] = "~addgrouptowhitelist"
            msg["channel"] = dmChannel
            self.inWhitelist(msg)
            #self.sc.api_call("chat.postMessage", as_user="true", channel=sendUser, text=message)
        except Exception:
            self.sendError()


    def addReaction(self, channel,timestamp,reaction):
        slack = Slacker(self.token)
        try:
            slack.reactions.add(channel=channel,timestamp=timestamp, name=reaction)
        except Exception:
            exception = traceback.print_exc(file=sys.stdout)
            self.sendError()



def colorCode(bot, msg):
    print("color")
    name = msg["text"][1 + msg["text"].find(" "):]
    if(name == msg['text']):
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
        args = msg["text"].split(",")
        channel = msg["channel"]
        if (channel != "G0CCGHGKS"):
            print("quote check")
            return -1
        if(len(args) >= 3):
            if(args[1] in bot.people):
                fileName = bot.people[bot.people.index(args[1])] + "Quotes.txt"
                #need to get full quote
                if(os.path.isfile(fileName)):
                    with open(fileName, "a+") as f:
                        f.write("," + args[2])
                else:
                    with open(fileName, "a+") as f:
                        f.write(args[2])
                bot.sendMessage(channel, "Quote added " + args[2])
        elif(len(args) == 2):
            quotes = []
            if(args[1] in bot.people):
                fileName = bot.people[bot.people.index(args[1])] + "Quotes.txt"
                if(os.path.isfile(fileName)):
                    with open(fileName, "r") as read:
                        quotes = read.read().split(",")
                else:
                    bot.sendMessage(channel, "no quotes for " + args[1] + " you should add some")
                if(len(quotes) > 0):
                    bot.sendMessage(channel, random.choice(quotes))
        else:
            print("[!!] not enough args")
            return -1
    except Exception:
        sendError()


# messages - needs to be updated
def delete(bot, msg):
    if(not bot.timestamp.empty()):
        ts = bot.timestamp.get()
        for w in bot.whitelist:
            bot.sc.api_call("chat.delete",channel=w, ts=str(ts["ts"]))


# delete every message sent, from last 100
# needs to have 'has_more' check for > 100
def deleteAll(bot, msg):
    slack = Slacker(bot.token)
    print("\ndeleting all messages in private groups")
    # delete private group messages
    for chan in slack.groups.list().body['groups']: # for every group the bot has access to
        print("deleting in: " + str(chan['name']))
        #print(chan)
        messages = slack.groups.history(channel=chan['id']).body['messages']
        #print(messages)
        for message in messages:
            if (message['user'] == bot.id and ('subtype' not in message)): #can only delete messages owned by sender
                    slack.chat.delete(ts=message['ts'], channel=chan['id'])
                    print('deleted: ' + message['ts'])

    # delete DMs
    # for chan in slack.im.list().body['ims']:
    #     for msg in slack.im.history(channel=chan['id']).body['messages']:
    #         pass
    print("done deleting")
    ### deprecated
    # while not bot.timestamp.empty():
    #     ts = bot.timestamp.get()
    #     print(ts)
    #     for w in bot.whitelist:
    #         bot.sc.api_call("chat.delete",channel=w, ts=str(ts["ts"]))


def test(bot, msg):
    testing = "blackbox whitebox "*random.randrange(5,20)
    bot.sendMessage(msg["channel"], testing)


def pony(bot, msg):
    #print(dir(p.pony))
    bot.sendMessage(msg["channel"], "```" + p.Pony.getPony() + "```")


def randominterns(bot,msg):
    bot.sendMessage(msg["channel"],"Alex")


def luna(bot,msg):
    bot.sendMessage(msg["channel"], "luna shutdown")


def playGong(bot, msg):
    CHUNK = 1024
    wf = wave.open('gong.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    router = [{
      "text": ["~colorname", "~color name"],
      "callback":colorCode,
      "type": "text"
    },{
      "text": ["~randomintern"],
      "callback":randomIntern,
      "type": "text"
    },{
      "text": ["~catfacts", "~cat facts"],
      "callback":catFacts.catFacts,
      "type": "text"
    },{
      "text": ["~quote"],
      "callback":quote,
      "type": "text"
    },{
      "text": ["~startpoll","~poll","~createpoll","~start poll","~poll","~create poll"],
      "callback":poll.startPoll,
      "type": "text"
    },{
      "text": ["~stoppoll",'~removepoll',"~stop poll",'~remove poll'],
      "callback":poll.stopPoll,
      "type": "text"
    },{
      "text": ["~vote","~votepoll","~vote poll"],
      "callback":poll.vote,
      "type": "text"
    },{
      "text": ["~addoption"],
      "callback":poll.addOption,
      "type": "text"
    },{
      "text": ["~deleteall"],
      "callback":deleteAll,
      "type": "text"
    },{
      "text": ["~delete"],
      "callback":delete,
      "type": "text"
    },{
      "text": ["~nye"],
      "callback":images.nye,
      "type": "text"
    },{
      "text": ["test"],
      "callback":test,
      "type": "text"
    },{
      "text": ["~meme"],
      "callback":images.getMeme,
      "type": "text"
    },{
      "text": ["ship it",":shipit:", "shipit"],
      "callback":images.shipIt,
      "type": "text"
    },{
      "text": ["~gif"],
      "callback":images.getGiphy,
      "type": "text"
    },{
      "text": ["~insanity"],
      "callback":images.getMemeInsanity,
      "type": "text"
    },
    # {
    #   "text": ["~dm"],
    #   "callback":GoTo.sendDM,
    #   "type": "text"
    # },
    # {
    #   "text": ["pony", "Good morning! Here are the results from last night's nightly test:"],
    #   "callback": pony,
    #   "type": "text"
    # },
    {
      "text": ["~random intern", "~ randomintern"],
      "callback": randominterns,
      "type": "text"
    },
    # {
    #   "text": ["Sorry, but you aren't authorized to use this command.", "luna"],
    #   "callback": luna,
    #   "type": "text"
    # }
    {
      "text": ["zach", "zachisan", "<3", ":heart:",":heart_decoration:", "zack", 
            ":heart_eyes:",":heartbeat:",":heartpulse:",":hearts:"],
      "callback": playGong,
      "type": "text"
    }]
    g = GoTo()
    g.start()

#slack json for experimenting
# [{'type': 'user_typing', 'user': 'U054XSGNL', 'channel': 'D0CK8L0S1'}]
# [{'text': 'message', 'ts': '1445352439.000002', 'user': 'U054XSGNL', 'team': 'T04QY6Z1G', 'type': 'message', 'channel': 'D0CK8L0S1'}]
#join message
# [{'type': 'group_joined', 'channel': {'topic': {'last_set': 0, 'value': '', 'creator': ''}, 'name': 'website', 'last_read': '1445356948.000853', 'creator': 'U051UQDN6', 'is_mpim': False, 'is_archived': False, 'created': 1436198627, 'is_group': True, 'members': ['U051UQDN6', 'U052GCW57', 'U054XSGNL', 'U0665DKSL', 'U09JUD8PN', 'U09JVCNTX', 'U0B20MP8C', 'U0CK96B71'], 'unread_count': 0, 'is_open': True, 'purpose': {'last_set': 1440532002, 'value': 'general p3scan issues, questions, discussions, rants about scala/play problems...', 'creator': 'U054XSGNL'}, 'unread_count_display': 0, 'id': 'G0786E43B', 'latest': {'reactions': [{'count': 1, 'name': '-1', 'users': ['U09JUD8PN']}], 'text': 'Mine still breaks', 'type': 'message', 'user': 'U09JVCNTX', 'ts': '1445356948.000853'}}}]
# [{'text': '<@U0CK96B71|b0t> has joined the group', 'ts': '1445357442.000855', 'subtype': 'group_join', 'inviter': 'U054XSGNL', 'type': 'message', 'channel': 'G0786E43B', 'user': 'U0CK96B71'}]
#slacker responses
# imOpen.body = {'no_op': True, 'already_open': True, 'ok': True, 'channel': {'id': 'D0CK8L0S1'}}
# chatPost.body = {'message': {'text': 'test message', 'type': 'message', 'user': 'U0CK96B71', 'ts': '1447953215.000002'}, 'ok': True, 'ts': '1447953215.000002', 'channel': 'D0CK8L0S1'}