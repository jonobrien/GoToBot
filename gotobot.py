import time
import string
import random
import urllib.request
import os.path
import queue
from slackclient import SlackClient
import sys, traceback
import json
import botFunctions
import catFacts
import re




class GoTo:

    def __init__(self):
        self.start()


    def start(self):
        print("initializing bot...")
        self.token = ""
        #with open("token.txt", "r") as tRead:
        #         self.token = tRead.read()
        # read me from the environment...heroku
        self.router = botFunctions.router
        self.token = os.environ.get("slack_token")
        self.sc             = SlackClient(self.token)
        authTestResult = self.apiCall("auth.test")
        if "error" in authTestResult:
            raise ValueError("Invalid Token")
        self.id             = authTestResult["user_id"]
        #self.distrChan      = "G0EFAE1EE" # used with distractionChan() in images.py
        #self.quoteChans     = ["G0CCGHGKS"] # uncomment check in quote() to restrict channels
        self.interns        = ["Micheal"]
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
        self.legalChars     = string.printable.replace("`", "") # characters that can be printed
        with open("whitelist.txt", "a+") as self.whiteRead:
            self.whiteRead.seek(0)
            self.whitelist  = self.whiteRead.read().split(" ")
        with open("EN_dict.txt", "a+") as readLines:
            readLines.seek(0)
            self.words      = readLines.read().split("\n")
        print("bot initialized, starting...")
        self.startBot()


    def help(self, msg):
        info = "```\n"
        info += "A Python Slack API bot:\n\n"
        info += "hosted on Github:\n"
        info += "https://github.com/Omodi/GoToBot\n"
        info += "https://github.com/jonobrien/GoToBot\n"
        info += "https://github.com/immaterialism/GoToBot\n\n"
        info += "Available Commands:\n"
        for command in self.router:
            if "help" in command and len(command["help"]) > 0:
                info += command["help"] if command["help"][-1] == "\n" else command["help"] + "\n"
        info +="```"
        self.sendMessage(msg["channel"], info)


    def connect(self):
        print("connect")


    def main(self):
        pass

    def apiCall(self, endpoint):
        return self.sc.api_call(endpoint, token=self.token)


    def startBot(self):
        try:
            print("startBot() id: " + self.id)
            # need groups.list api call for the dict of private group info dict by id key
            # make it once at startup, save it for later
            users    = (self.apiCall('users.list'))['members']
            groups   = (self.apiCall('groups.list'))['groups']
            ims      = (self.apiCall('im.list'))['ims']
            channels = (self.apiCall('channels.list'))["channels"]
            self.teamInfo = (self.apiCall('team.info')) # preserve enterprise info

            for user in users:
                self.userDict[user['id']] = user['name']
                self.idDict[user['name']] = user['id']

            # setup the chanDict used for private group/im and public channel info and id reference
            # contains all meta data about those channels and can be used later
            # get it once, so every delete call doesn't repeat them
            # TODO -- seems like joining a channel after starting the bots
            #   allows for deletion even though bot joined after the dictionary was created
            # ^* this is due to the bot deleting based on whitelist, it has knowledge of
            # ^* existing names already, so that is expected
            for group in groups:
                self.chanDict[group['id']] = group
            for im in ims:
                self.chanDict[im['id']] = im
            for chan in channels:
                self.chanDict[chan['id']] = chan
            if self.sc.rtm_connect(): # connected to slack real-time messaging api
                print('connected to team: {0}'.format(self.teamInfo['team']['name']))

                while True:
                    msgs = self.sc.rtm_read()
                    for msg in msgs:
                        # debug messages
                        ##if ("subtype" not in msg):
                        ######print(msg)

                        # this uses the 'EN_dict.txt' file
                        #images.distractionChan(self)

                        catFacts.subbedToCatFacts(self)

                        #### kick a user when they join a channel #################################
                        #      (need user api key, not bot key)
                        #
                        #
                        # if("subtype" in msg and msg["subtype"] == "group_join"):
                        #     print("remove")
                        #     ## bots can't kick, use your user api key
                        #     ## not bot key to have bot kick users
                        #     print(self.sc.api_call("groups.kick",channel=msg["channel"], 
                        #           user="U0CNP6WRK"))
                        #
                        #
                        ##### send message every time a user becomes active #######################
                        #
                        #elif("type" in msg and msg["type"] == "presence_change" and
                        #                           msg["presence"] == "active" and msg["user"]):
                        #    # if(msg["user"] not in self.bots):
                        #        # not b0t, Luna, gotoo
                        #        # post to interns-education as "user is active"
                        #        # message = self.userDict[msg["user"]] + " is active"
                        #        # sendMessage("G09LLA9EW",message)
                        #        # print("[I] sent: "+message)
                        ###########################################################################

                        if("type" in msg and msg["type"] == "error"):
                            print("\n\n[!!] error: \n" + msg + "\n\n")
                            # user_is_bot errors because bot cannot use that api function
                            error = "message error - probably no quotes found"
                            self.sendMessage(self.last_channel, error) # err msgs don't have a chan
                            self.restartBot()
                        elif("type" in msg and msg["type"] == "message"and "text" in msg and
                                    all(c in self.legalChars for c in msg["text"].replace("'",""))):

                            if(self.inWhitelist(msg)):
                                m = msg["text"]
                                #  cuts text contained between <> ex: <test>
                                # TODO -- more detailed usage info for specific commands
                                # to allow for future ~help,<~function> to only display the help msg
                                m = re.sub(r'&lt;(.*?)&gt;', '', m)
                                msg["santized"] = m
                                for r in self.router:
                                    for t in r["text"]:
                                        if(t.lower() in m.lower()):
                                            r["callback"](self, msg)

                    time.sleep(1) # artificial rate-limit
            else:
                print("[!!] Connection Failed, invalid token?")

        except AttributeError:
            self.restartBot()
        except Exception:
            self.restartBot()


    def inWhitelist(self,msg):
        if (msg["text"].lower() == "~addgrouptowhitelist" and msg["channel"] not in self.whitelist):
            self.whitelist.append(msg["channel"])
            self.sendMessage(msg["channel"], "channel whitelisted")
            with open("whitelist.txt", "w") as self.whiteWrite:
                self.whiteWrite.write(" ".join(self.whitelist))
            return True
        if (msg["channel"] in self.whitelist):
            return True
        return False


    def sendMessage(self,channel, message):
        try:
            #self.sc.rtm_send_message(channel, message)
            self.sc.api_call("chat.postMessage", channel=channel,
                        text=message, as_user=True, unfurl_media=True)
            self.last_channel = channel
        except Exception:
            exception = traceback.print_exc(file=sys.stdout)
            self.restartbot("\n[!!] sending failed")


    # need to figure out how to clean the stack
    # for a fresh restart on errors
    # traces seem to just get huge due to all except handling
    # should just try and fix some looping of excepts
    def restartBot(self, msg='\n[!!] exception, restarting in 5s'):
        print(msg)
        traceback.print_exc(file=sys.stdout)
        time.sleep(5)
        print("\n[!!] restarting the bot\n")
        self.sc = SlackClient(self.token)
        self.start()


    # ~dm,user,msg - user has to be the @"user" string
    # ex: @jono would be `~dm,jono,msg`
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
                self.restartbot()


    def addReaction(self, channel,timestamp,reaction):
        try:
            self.sc.api_call("reactions.add", token=self.token, name=reaction,
                            channel=channel, timestamp=timestamp)
        except Exception:
            self.restartbot()



    """ TODO implement this:
    it would be interesting to provide individual help messages
    for certain functions to show examples and other usage information
    """
    def removeComments(s):
        while(s.contains("<") and s.contains(">")):
            left = s.indexOf("<")
            right = s.indexOf(">")
            s = s.substring(0, left)


    """
    only delete messages that the bot sent and skip messages
    that have already been deleted
    """
    def deleteBotMessage(self, msg, chan):
        if "user" in msg and (msg["user"] == self.id) and ("subtype" not in msg):
            self.sc.api_call("chat.delete", token=self.token, ts=msg["ts"], channel=chan)
            tofix = 'deleted: {0}'.format(msg["ts"])
            padded = tofix.rjust(len(tofix) + 8, ' ') # r/l is side string is on, padded from opposite
            print(padded)


    """
    delete the last message posted by the bot in the channel requested
      * tried doing it based solely off the message json
      * but `key errors` occur, need to check owner id
    """
    def delete(self, msg):
        print("\ndeleting last message in specified channel: {0}"
                                            .format(msg["channel"]))
        msgResponse = self.sc.api_call("groups.history", token=self.token, channel=msg["channel"])
        msgJson = msgResponse
        if("messages" in msgJson):
            for message in msgJson["messages"]:
                # can only delete messages owned by sender
                if ("user" in message and message["user"] == self.id and ("subtype" not in message)):
                    self.sc.api_call("chat.delete", token=self.token,
                                                       ts=message["ts"],
                                                  channel=msg["channel"]
                                    )
                    print("deleted: {0}".format(message["ts"]))
                    break
        else:
            self.sendMessage(msg['channel'], "no bot messages in channel")
        print("done deleting\n")


    """
    delete every message sent by bot
    that are in private groups and ims
    * don't check the whitelist as the bot could be woken from sleep for this
    """
    def deleteAll(self, msg):
        print("\n[I] deleting all messages in private groups, ims, public channels")
        queryStr = '' # default is empty so we can be explicit
        im = "im.history"
        group = "groups.history"
        chanStr = "channels.history"

        for chan in self.chanDict:
            hasMore = {}
            currChanName = None
            if 'name' in self.chanDict[chan]:
                currChanName = self.chanDict[chan]['name']
            else:
                currChanName = "dm'd -> need to invite/~addgrouptowhitelist"
            if chan not in self.whitelist:
                print('[I] channel not in whitelist: {0} -> {1}'
                                        .format(chan, currChanName))
                continue
            elif(chan.startswith("D")):
                queryStr = im
                userName = self.userDict[self.chanDict[chan]['user']]
                print('    [I] deleting ims for: {0} -> {1}'
                                        .format(chan, userName))
            elif (chan.startswith("G")):
                queryStr = group
                print('    [I] deleting group messages in: {0} -> {1}'
                                        .format(chan, currChanName))
            elif (chan.startswith("C")):
                queryStr = chanStr
                print('    [I] deleting messages in channel: {0} -> {1}'
                                        .format(chan, currChanName))
            msgJson = self.sc.api_call(queryStr, token=self.token,
                                               channel=self.chanDict[chan]['id'])

            if ('has_more' in msgJson and msgJson['has_more'] == True):
                print('        has_more, pagination')
                for message in msgJson['messages']: # collect initial 100
                    message["chann"] = chan # add channel to each message
                    hasMore[message['ts']] = message  #'ts' is "unique" for message in indiv. chan
                more = msgJson
                pageCount = 0
                # 100*100 message history per free team, restrict large single channel histories
                while("has_more" in msgJson and msgJson['has_more'] == True and pageCount < 100):
                    pageCount += 1
                    # need to page through history
                    msgJson = self.sc.api_call(queryStr, token=self.token,
                                channel=chan, latest=more['messages'][-1]['ts'], inclusive=1)
                    try:
                        for message in msgJson['messages']: # collect remaining history
                            message["chann"] = chan # add channel to each message
                            hasMore[message["ts"]] = message #'ts' is "unique" for message in indiv. chan
                    except KeyError: # when there are no more messages it sometimes errors??? skip it
                        continue
                print('        no more')
            if (hasMore): # all messages in that channel
                time.sleep(.2) # rate limit prevention
                lim = 0
                for message in hasMore.values():
                    lim += 1
                    if (lim % 20 == 0):
                        time.sleep(.1)
                    # seems slack added a NEW bot_id field, different from what they say userid is
                    self.deleteBotMessage(message, chan)
            elif ('messages' in msgJson and msgJson['messages']): # <= 100 to delete, has messages
                for message in msgJson['messages']:
                    self.deleteBotMessage(message, chan)
            else:
                noneFound = 'no messages to delete in: '
                if(chan.startswith("D")):
                    print('{0} {1} -> {2}'.format(noneFound, chan,
                                                    self.userDict[self.chanDict[chan]['user']]))
                else:
                    print('{0} {1} -> {2}'.format(noneFound, chan, currChanName))
        print("done deleting\n")


if __name__ == "__main__":
    g = GoTo()
    g.start()
