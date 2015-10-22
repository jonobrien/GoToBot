import time
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

#import git

def connect():
    pass
def main():
    pass

token = ""
with open("token.txt", "r") as tRead:
         token = tRead.read()
#global sc
sc = SlackClient(token)
interns = ["Jon", "Yura", "Alex", "Avik", "Tommy","StevieG"]
people = interns + ["Omar", "David", "Alan", "Alison", "Bulent", "Carlos", "Jeff", "Steven", "Thurston", "Linda","Derek"]
bots = ["U0CK96B71","U0CK96B71","U0ARYU2CT"]
timestamp = queue.Queue()
last_channel = ""
#{"@username":"ID","@user2":"ID2"}
userDict = {}
polls = []

def startBot():
    try:
        slack = Slacker(token)
        #slack.chat.post_message('G0ARYMG3E', 'slacker test')
        response = slack.users.list()
        users = response.body['members']
        for user in users:
            userDict[user["id"]] = user["name"]
        print(datetime.datetime.now())
        print (userDict)
        # g = git.cmd.Git("C:\\Users\\D\\pfpui")
        whiteWrite = open
        whitelist = []
        global last_channel
        with open("whitelist.txt", "r") as whiteRead:
             whitelist = whiteRead.read().split(" ")
        #whitelist.remove('')
        # g.pull()
        if sc.rtm_connect():
            print("connected")
            while True:
                msg = sc.rtm_read()
                if(len(msg) == 1):
                    print(msg)
                    msg = msg[0]
                    #error checking
                    #[{'type': 'user_typing', 'user': 'U054XSGNL', 'channel': 'D0CK8L0S1'}]
                    #[{'text': 'message', 'ts': '1445352439.000002', 'user': 'U054XSGNL', 'team': 'T04QY6Z1G', 'type': 'message', 'channel': 'D0CK8L0S1'}]
                    #join message
                    #[{'type': 'group_joined', 'channel': {'topic': {'last_set': 0, 'value': '', 'creator': ''}, 'name': 'website', 'last_read': '1445356948.000853', 'creator': 'U051UQDN6', 'is_mpim': False, 'is_archived': False, 'created': 1436198627, 'is_group': True, 'members': ['U051UQDN6', 'U052GCW57', 'U054XSGNL', 'U0665DKSL', 'U09JUD8PN', 'U09JVCNTX', 'U0B20MP8C', 'U0CK96B71'], 'unread_count': 0, 'is_open': True, 'purpose': {'last_set': 1440532002, 'value': 'general p3scan issues, questions, discussions, rants about scala/play problems...', 'creator': 'U054XSGNL'}, 'unread_count_display': 0, 'id': 'G0786E43B', 'latest': {'reactions': [{'count': 1, 'name': '-1', 'users': ['U09JUD8PN']}], 'text': 'Mine still breaks', 'type': 'message', 'user': 'U09JVCNTX', 'ts': '1445356948.000853'}}}]
                    #[{'text': '<@U0CK96B71|b0t> has joined the group', 'ts': '1445357442.000855', 'subtype': 'group_join', 'inviter': 'U054XSGNL', 'type': 'message', 'channel': 'G0786E43B', 'user': 'U0CK96B71'}]
                    
                    if("type" in msg and msg["type"] == "presence_change" and msg["presence"] == "active" and msg["user"]):
                        if(msg["user"] not in bots):
                            #not b0t, Luna, gotoo
                            #post to interns-education as "user is active"
                            message = userDict[msg["user"]] + " is active"
                            #sendMessage("G09LLA9EW",message)
                            #print("[I] sent: "+message)
                    if("type" in msg and msg["type"] == "error"):
                        #need a proper reconnect function
                        #doesnt regain connection token
                        print ("[!!] error in message, restarting bot")
                        error = "message error - no quotes found"
                        sendMessage(last_channel, error)
                    #print("type" in msg and msg["type"] == "message"and "text" in msg)
                    if("type" in msg and msg["type"] == "message"and "text" in msg and all(c in string.printable for c in msg["text"].replace("'",""))):
                        #print(msg)
                        if(msg["text"].lower() == "~addgrouptowhitelist" and msg['channel'] not in whitelist):
                            whitelist.append(msg["channel"])
                            with open("whitelist.txt", "w") as whiteWrite:
                                whiteWrite.write(" ".join(whitelist))
                        elif(msg["channel"] in whitelist):
                            for r in router:
                                if(r["text"].lower() in msg["text"]):
                                    r["callback"](msg)
                    elif("ok" in msg and msg["ok"] == True):
                        timestamp.put({"ts":msg["ts"],"channel":last_channel})
                elif(len(msg) > 1):
                    print(msg)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                time.sleep(1)
        else:
            print("Connection Failed, invalid token?")
    except AttributeError:
        global sc
        print("[!!] error - probably in the send")
        traceback.print_exc(file=sys.stdout)
        print("[!!] restarting the bot")
        sc = SlackClient(token)
        startBot()
    except Exception:
        print("[!!] uncaught error")
        traceback.print_exc(file=sys.stdout)
        print("[!!] restarting the bot")
        sc = SlackClient(token)
        startBot()


def sendMessage(channel, message):
    global last_channel
    try:
        sc.rtm_send_message(channel, message)
        last_channel = channel
    except Exception:
        exception = traceback.print_exc(file=sys.stdout)
        sendError()


def sendError():
    global sc
    print("\n[!!] sending failed")
    traceback.print_exc(file=sys.stdout)
    print("\n[!!] restarting the bot\n")
    sc = SlackClient(token)
    startBot()

#~DM,user,msg
def sendDM(msg):
    global last_channel
    last_channel = msg["channel"]
    args = msg["text"].split(",")
    user = args[1]
    message = args[2]
    try:
        sendUser = userDict[user]
        print(token)
        print(sendUser)
        send = sc.api_call("im_open",token=token, user=sendUser)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(send)
        sc.api_call("chat.postMessage", as_user="true", channel=sendUser, text=message)
    except Exception:
        sendError()


def getGiphy(msg):
    url = "http://api.giphy.com/v1/gifs/search?q="
    keywords = ",".join(msg["text"].split(",")[1:])
    print(keywords)
    data = urllib.request.urlopen(url + keywords +"&api_key=dc6zaTOxFJmzC&limit=1").read().decode("utf-8")#.read())
    jsonData = json.loads(data)
    try:
        gif = jsonData["data"][0]["images"]["original"]["url"]
    except IndexError:
        gif = "gif not found"
    sendMessage(msg["channel"], gif)
    #print (jsonData)#(json.dumps(data, sort_keys=True, indent=4))
    #print()
    #print(jsonData["data"])
    ###for i in jsonData["data"][0].keys():
    ###    print (jsonData["data"][0][i])
    ###print(jsonData["data"][0]["images"]["original"]["url"])

def colorCode(msg):
    print("color")
    name = msg["text"][1 + msg["text"].find(" "):]
    if(name == msg['text']):
        message = "invalid arguments"
        sendMessage(msg["channel"], message)
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
    sendMessage(msg["channel"], h)

def randomIntern(msg):
    sendMessage(msg["channel"], random.choice(interns))

def quote(msg):
    args = msg["text"].split(",")
    channel = msg["channel"]
    if (channel != "G0CCGHGKS"):
        print("quote check")
        return -1
    if(len(args) >= 3):
        if(args[1] in people):
            fileName = people[people.index(args[1])] + "Quotes.txt"
            #need to get full quote
            if(os.path.isfile(fileName)):
                with open(fileName, "a+") as f:
                    f.write("," + args[2])
            else:
                with open(fileName, "a+") as f:
                    f.write(args[2])
            sendMessage(msg["channel"], "Quote added " + args[2])
    elif(len(args) == 2):
        quotes = []
        if(args[1] in people):
            fileName = people[people.index(args[1])] + "Quotes.txt"
            if(os.path.isfile(fileName)):
                with open(fileName, "r") as read:
                    quotes = read.read().split(",")
            else:
                sendMessage(msg["channel"], "no quotes for " + args[1] + " you should add some")
            if(len(quotes) > 0):
                sendMessage(msg["channel"], random.choice(quotes))
    else:
        print("[!!] not enough args")
        return -1


def findName(ds, nam):
    for d in ds:
        if("name" in d):
            if(d["name"] == nam):
                return d
    return None


def startPoll(msg):
    global polls
    args = msg["text"].split(",")
    if(len(args) > 4):
        poll = {"name":args[1].lower()}
        i = 2
        while(i < len(args)):
            poll[args[i]] = 0
            i += 1
        polls.append(poll)
        sendMessage(msg["channel"], "Poll created")
    else:
        sendMessage(msg["channel"], "Not enough arguments")

def vote(msg):
    global polls
    args = msg["text"].split(",")
    if(len(args) == 3):
        d = findName(polls, args[1])
        if(d != None):
            if(args[2] in d):
                d[args[2]] += 1
                printPoll(d,msg)
            else:
                sendMessage(msg["channel"], "Invalid vote option")
        else:
            sendMessage(msg["channel"], "Could not find poll")
    else:
        sendMessage(msg["channel"], "Incorrect number of arugments")

def stopPoll(msg):
    print("endpoll")
    global polls
    args = msg["text"].split(",")
    if(len(args) == 2):
        d = findName(polls, args[1].lower())
        if(d != None):
            polls.remove(d)
            printPoll(d, msg)
        else:
            sendMessage(msg["channel"], "Could not find poll")
    else:
        sendMessage(msg["channel"], "Incorrect number of arugments")

def printPoll(poll, msg):
    global polls
    #p = findName(polls,name).copy()
    p = poll.copy()
    name = p["name"]
    del(p["name"])
    s = "```" + name
    for w in sorted(p, key=p.get, reverse=True):
        s += "\n  " + str(w) + (" " * (10 - len(w))) + " " + str(p[w])
    s += "```"
    #print(s)
    sendMessage(msg["channel"], s)

def catFacts(msg):
    request = str(urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read())
    sendMessage(msg["channel"], request[request.find('[') + 2:request.find(']') - 1])

def delete(msg):
    if(not timestamp.empty()):
        ts = timestamp.get()
        for w in whitelist:
            sc.api_call("chat.delete",channel=w, ts=str(ts["ts"]))
def deleteAll(msg):
    while not timestamp.empty():
        ts = timestamp.get()
        print(ts)
        for w in whitelist:
            sc.api_call("chat.delete",channel=w, ts=str(ts["ts"]))
def nye(msg):
    nyeMlg = "http://i.giphy.com/m6ILp14NR2RDq.gif"
    sendMessage(msg["channel"], nyeMlg)
def test(msg):
    testing = "blackbox whitebox "*random.randrange(1,4)
    sendMessage(msg["channel"], testing)
def shipIt(msg):
    squirrels = [
      "http://shipitsquirrel.github.io/images/ship%20it%20squirrel.png",
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
    sc.rtm_send_message(msg["channel"], random.choice(squirrels))
#def send(msg):

router = [{
  "text": "~colorname",
  "callback":colorCode
},{
  "text": "~randomintern",
  "callback":randomIntern
},{
  "text": "~catfacts",
  "callback":catFacts
},{
  "text": "~quote",
  "callback":quote
},{
  "text": "~startpoll",
  "callback":startPoll
},{
  "text": "~stoppoll",
  "callback":stopPoll
},{
  "text": "~vote",
  "callback":vote
},{
  "text": "~deleteall",
  "callback":deleteAll
},{
  "text": "~delete",
  "callback":delete
},{
  "text": "~nye",
  "callback":nye
},{
  "text": "test",
  "callback":test
},{
  "text": "ship it",
  "callback":shipIt
},{
  "text": "~gif",
  "callback":getGiphy
},]
startBot()