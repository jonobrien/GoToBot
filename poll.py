def findName(bot, ds, nam):
    for d in ds:
        if("name" in d):
            if(d["name"] == nam):
                return d
    return None


def startPoll(bot, msg):
    args = msg["text"].split(",")
    if(len(args) > 2):
        poll = {"name":args[1].lower(), "voted":{}}
        i = 2
        while(i < len(args)):
            poll[args[i].lower().strip()] = 0
            i += 1
        bot.polls.append(poll)
        bot.sendMessage(msg["channel"], "Poll created")
    else:
        bot.sendMessage(msg["channel"], "Not enough arguments")

def vote(bot, msg):
    args = msg["text"].split(",")
    if(len(args) == 3):
        d = findName(bot, bot.polls, args[1])
        if(d != None):
            if(args[2].lower().strip() in d):
                if(msg["user"] not in d["voted"]):
                    print("New")
                    d[args[2].lower().strip()] += 1
                    d["voted"][msg["user"]] = args[2].lower().strip()
                else:
                    print("Old")
                    d[args[2].lower().strip()] += 1
                    d[d["voted"][msg["user"]] ] -= 1
                    d["voted"][msg["user"]] = args[2].lower().strip()
                printPoll(bot, d,msg)
            else:
                bot.sendMessage(msg["channel"], "Invalid vote option")
        else:
            bot.sendMessage(msg["channel"], "Could not find poll")
    else:
        bot.sendMessage(msg["channel"], "Incorrect number of arugments")

def stopPoll(bot, msg):
    print("endpoll")
    args = msg["text"].split(",")
    if(len(args) == 2):
        d = findName(bot, bot.polls, args[1].lower())
        if(d != None):
            bot.polls.remove(d)
            printPoll(bot, d, msg)
        else:
            bot.sendMessage(msg["channel"], "Could not find poll")
    else:
        bot.sendMessage(msg["channel"], "Incorrect number of arugments")

def addOption(bot, msg):
    args = msg["text"].split(",")
    if(len(args) == 3):
        d = findName(bot, bot.polls, args[1].lower())
        if(d != None):
            d[args[2].lower().strip()] = 0
            printPoll(bot, d, msg)
        else:
            bot.sendMessage(msg["channel"], "Could not find poll")
    else:
        bot.sendMessage(msg["channel"], "Incorrect number of arugments")

def printPoll(bot, poll, msg):
    #p = findName(polls,name).copy()
    p = poll.copy()
    name = p["name"]
    del(p["name"])
    del(p["voted"])
    s = "```" + name
    for w in sorted(p, key=p.get, reverse=True):
        s += "\n  " + str(w) + (" " * (20 - len(w))) + " " + str(p[w])
    s += "```"
    #print(s)
    bot.sendMessage(msg["channel"], s)