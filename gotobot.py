import time
import string
import random
import urllib.request
import os.path
import datetime
import queue
from slackclient import SlackClient
import sys, traceback

#import git

def connect():
    pass
def main():
    pass


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
token = ""
with open("token.txt", "r") as tRead:
         token = tRead.read()
#global sc
sc = SlackClient(token)
interns = ["Jon", "Yura", "Alex", "Avik", "StevieG", "Tommy"]*3+["Alex"]
people = interns + ["Omar", "David", "Alan", "Alison", "Bulent", "Carlos", "Jeff", "Steven", "Thurston", "Linda","Derek"]
timestamp = queue.Queue()
last_channel = ""
polls = []
def startBot():
    try:
        print(datetime.datetime.now())
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
                    #print(msg)
                    msg = msg[0]
                    #error checking
                    if("type" in msg and msg["type"] == "error"):
                        #need a proper reconnect function
                        #doesnt regain connection token
                        print ("[!!] error in message, restarting bot")
                        error = "error - no quotes found"
                        try:
                            sc.rtm_send_message(last_channel, error)
                        except Exception:
                            print("[!!] sending failed")
                            traceback.print_exc(file=sys.stdout)
                        sc = SlackClient(token)
                        startBot()
                    #print("type" in msg and msg["type"] == "message"and "text" in msg)
                    if("type" in msg and msg["type"] == "message"and "text" in msg and all(c in string.printable for c in msg["text"].replace("'",""))):
                        #print(msg)
                        if(msg["text"].lower() == "~addgrouptowhitelist" and msg['channel'] not in whitelist):
                            whitelist.append(msg["channel"])
                            with open("whitelist.txt", "w") as whiteWrite:
                                whiteWrite.write(" ".join(whitelist))
                        elif(msg["channel"] in whitelist):
                            #print("whitelisted")
                            if("~colorname" in msg["text"].lower()):
                                colorCode(msg)
                            elif("~randomintern" in msg["text"].lower()):
                                last_channel = msg["channel"]
                                try:
                                    sc.rtm_send_message(last_channel, random.choice(interns))
                                except Exception:
                                    print("[!!] sending failed")
                                    traceback.print_exc(file=sys.stdout)
                            elif("~catfacts" in msg["text"].lower()):
                                print("cat")
                                request = str(urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read())
                                last_channel = msg["channel"]
                                try:
                                    sc.rtm_send_message(last_channel, request[request.find('[') + 2:request.find(']') - 1])
                                except Exception:
                                    print("[!!] sending failed")
                                    traceback.print_exc(file=sys.stdout)
                            elif("~quote" in msg["text"].lower()):
                                print("quote")
                                quote(msg)
                            elif("~startpoll" in msg["text"].lower()):
                                print("poll")
                                startPoll(msg)
                            elif("~stoppoll" in msg["text"].lower()):
                                stopPoll(msg)
                            elif("~vote" in msg["text"].lower()):
                                vote(msg)
                            elif("~deleteall" in msg["text"].lower()):
                                while not timestamp.empty():
                                    ts = timestamp.get()
                                    print(ts)
                                    for w in whitelist:
                                        sc.api_call("chat.delete",channel=w, ts=str(ts["ts"]))
                            elif("~delete" in msg["text"].lower()):
                                if(not timestamp.empty()):
                                    ts = timestamp.get()
                                    for w in whitelist:
                                        sc.api_call("chat.delete",channel=w, ts=str(ts["ts"]))
                            #sc.rtm_send_message(msg["channel"], msg["text"])
                            elif ("~nye" in msg["text"].lower()):
                                nyeMlg = "http://i.giphy.com/m6ILp14NR2RDq.gif"
                                try:
                                    sc.rtm_send_message(msg["channel"], nyeMlg)
                                except Exception:
                                    print("[!!] sending failed")
                                    traceback.print_exc(file=sys.stdout)
                            elif ("testing" in msg["text"].lower()):
                                testing = "blackbox whitebox "*random.randrange(1,4)
                                try:
                                    sc.rtm_send_message(msg["channel"], testing)
                                except Exception:
                                    print("[!!] sending failed")
                                    traceback.print_exc(file=sys.stdout)
                            elif("ship it" in msg["text"]):
                                last_channel = msg["channel"]
                                sc.rtm_send_message(last_channel, random.choice(squirrels))
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
        print("uncaught error")
        print("!!!")
        traceback.print_exc(file=sys.stdout)
        print("[!!] restarting the bot")
        sc = SlackClient(token)
        startBot()

def colorCode(msg):
    global last_channel
    print("color")
    name = msg["text"][1 + msg["text"].find(" "):]
    if(name == msg['text']):
        last_channel = msg["channel"]
        try:
            sc.rtm_send_message(msg["channel"], "Invalid arguments")
            return
        except Exception:
            print("[!!] sending failed")
            traceback.print_exc(file=sys.stdout)
            return -1
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
    last_channel = msg["channel"]
    try:
        sc.rtm_send_message(msg["channel"], h)
    except Exception:
        print("[!!] sending failed")
        traceback.print_exc(file=sys.stdout)
        return -1


def quote(msg):
    global last_channel
    print(msg)
    last_channel = msg["channel"]
    args = msg["text"].split(",")
    channel = msg["channel"]
    if (channel != "G0CCGHGKS"):
        print("quote check")
        return -1
    print(len(args))
    print(args)
    if(len(args) >= 3):
        print(3)
        if(args[1] in people):
            fileName = people[people.index(args[1])] + "Quotes.txt"
            #need to get full quote
            if(os.path.isfile(fileName)):
                with open(fileName, "a+") as f:
                    f.write("," + args[2])
            else:
                with open(fileName, "a+") as f:
                    f.write(args[2])
            last_channel = msg["channel"]
            sc.rtm_send_message(msg["channel"], "Quote added " + args[2])
    elif(len(args) == 2):
        print(2)
        quotes = []
        if(args[1] in people):
            fileName = people[people.index(args[1])] + "Quotes.txt"
            if(os.path.isfile(fileName)):
                with open(fileName, "r") as read:
                    quotes = read.read().split(",")
            else:
                try:
                    sc.rtm_send_message(msg["channel"], "no quotes for " + args[1] + " you should add some")
                except Exception:
                    print("[!!] sending failed")
                    traceback.print_exc(file=sys.stdout)
                    return -1
            if(len(quotes) > 0):
                last_channel = msg["channel"]
                try:
                    sc.rtm_send_message(last_channel, random.choice(quotes))
                except Exception:
                    print("[!!] sending failed")
                    traceback.print_exc(file=sys.stdout)
                    return -1
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
    global last_channel
    args = msg["text"].split(",")
    last_channel = msg["channel"]
    if(len(args) > 4):
        poll = {"name":args[1].lower()}
        i = 2
        while(i < len(args)):
            poll[args[i]] = 0
            i += 1
        polls.append(poll)
        sc.rtm_send_message(msg["channel"], "Poll created")
    else:
        sc.rtm_send_message(msg["channel"], "Not enough arguments")

def vote(msg):
    global polls
    global last_channel
    args = msg["text"].split(",")
    last_channel = msg["channel"]
    if(len(args) == 3):
        d = findName(polls, args[1])
        if(d != None):
            if(args[2] in d):
                d[args[2]] += 1
                printPoll(d,msg)
            else:
                sc.rtm_send_message(msg["channel"], "Invalid vote option")
        else:
            sc.rtm_send_message(msg["channel"], "Could not find poll")
    else:
        sc.rtm_send_message(msg["channel"], "Incorrect number of arugments")

def stopPoll(msg):
    print("endpoll")
    global polls
    global last_channel
    args = msg["text"].split(",")
    last_channel = msg["channel"]
    if(len(args) == 2):
        d = findName(polls, args[1].lower())
        if(d != None):
            polls.remove(d)
            printPoll(d, msg)
        else:
            sc.rtm_send_message(msg["channel"], "Could not find poll")
    else:
        sc.rtm_send_message(msg["channel"], "Incorrect number of arugments")

def printPoll(poll, msg):
    global polls
    global last_channel
    #p = findName(polls,name).copy()
    p = poll.copy()
    name = p["name"]
    del(p["name"])
    s = "```" + name
    for w in sorted(p, key=p.get, reverse=True):
        s += "\n  " + str(w) + (" " * (10 - len(w))) + " " + str(p[w])
    s += "```"
    #print(s)
    last_channel = msg["channel"]
    sc.rtm_send_message(msg["channel"], s)


    



#def send(msg):



startBot()