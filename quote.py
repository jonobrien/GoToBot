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
                bot.sendMessage(channel, "incorrect args for ~quote,person,text " +
                        "(actual input is -> " + cmd + "," + str(person) + ", " + str(text) + ")")
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
                bot.sendMessage(channel, "incorrect args for ~quote,person (actual input is -> " +
                                                                    cmd + "," + str(person) + ")")
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
            bot.sendMessage(channel, "not enough args for ~quote,person,text or " +
                                                "~quote,person (actual input is -> " +cmd+"," +
                                                str(person.lower()) + ", " + str(text) + ")")
            return -1
    except Exception:
        print("[!!!] error in quote")
        bot.sendError()
