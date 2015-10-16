import time
import string
import random
import urllib.request
import os.path
import datetime
import queue
from slackclient import SlackClient
#import git
token = ""
with open("token.txt", "r") as tRead:
         token = tRead.read()
sc = SlackClient(token)
interns = ["Jon", "Yura", "Alex", "Avik", "Derek", "Tommy"]
people = interns + ["Omar", "David", "Alan", "Alison", "Bulent", "Carlos", "Jeff", "Steven", "Thurston", "Linda"]
timestamp = queue.Queue()
last_channel = ""
def startBot():
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
        while True:
            msg = sc.rtm_read()
            if(len(msg) == 1):
                #print(msg)
                msg = msg[0]
                if("type" in msg and msg["type"] == "error"):
                    print ("[!!] error in message, restarting bot")
                    error = "error - no quotes found"
                    sc.rtm_send_message(last_channel, error)
                    startBot()
                #print("type" in msg and msg["type"] == "message"and "text" in msg)
                if("type" in msg and msg["type"] == "message"and "text" in msg and all(c in string.printable for c in msg["text"].replace("'",""))):
                    #print(1)
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
                            sc.rtm_send_message(msg["channel"], random.choice(interns))
                        elif("~catfacts" in msg["text"].lower()):
                            print("cat")
                            request = str(urllib.request.urlopen("http://catfacts-api.appspot.com/api/facts?number=1").read())
                            last_channel = msg["channel"]
                            sc.rtm_send_message(msg["channel"], request[request.find('[') + 2:request.find(']') - 1])
                        elif("~quote" in msg["text"].lower()):
                            print("quote")
                            quote(msg)
                        elif("~startpoll" in msg["text"].lower()):
                            print("poll")
                            startPoll(msg)
                        elif("~stoppoll" in msg["text"].lower()):
                            pass
                            stopPoll(msg)
                        elif("~vote" in msg["text"].lower()):
                            pass
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
                            sc.rtm_send_message(msg["channel"], nyeMlg)
                elif("ok" in msg and msg["ok"] == True):
                    timestamp.put({"ts":msg["ts"],"channel":last_channel})
            elif(len(msg) > 1):
                print(msg)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            time.sleep(.5)
    else:
        print("Connection Failed, invalid token?")


def colorCode(msg):
    global last_channel
    print("color")
    name = msg["text"][1 + msg["text"].find(" "):]
    if(name == msg['text']):
        last_channel = msg["channel"]
        sc.rtm_send_message(msg["channel"], "Invalid arguments")
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
    last_channel = msg["channel"]
    sc.rtm_send_message(msg["channel"], h)

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
            
                
            sc.rtm_send_message(msg["channel"], "Quote added " + args[2])
    elif(len(args) == 2):
        print(2)
        quotes = []
        if(args[1] in people):
            fileName = people[people.index(args[1])] + "Quotes.txt"
            if(os.path.isfile(fileName)):
                with open(fileName, "r") as read:
                    quotes = read.read().split(",")
            if(len(quotes) > 0):
                last_channel = msg["channel"]
                sc.rtm_send_message(msg["channel"], random.choice(quotes))

def startPoll(msg):
    pass

#def send(msg):



startBot()