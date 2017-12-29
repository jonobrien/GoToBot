import partyparrot.partyparrot as pp
import partyparrot.alphabet as al
import pony as p
import poll
import quote
import images
import catFacts
from gotobot import GoTo
# import wave
# import pyaudio




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
    # print (h)
    bot.sendMessage(msg["channel"], h)


def randominterns(bot, msg):
    bot.sendMessage(msg["channel"], "Alex")


def randomIntern(bot, msg):
    ranIntern = random.choice(bot.interns)
    if ranIntern == "Steven G":
        ranIntern = ":tubieg: :steveng: :partyg: :zoomieg:"
    bot.sendMessage(msg["channel"], ranIntern)


def luna(bot, msg):
    bot.sendMessage(msg["channel"], "luna shutdown")


def partyParrotMsg(bot, msg):
    txt = msg['text'].lower()
    txt = txt[12: len(txt)].strip()
    txt = ''.join(ch for ch in txt if ch in al.ALPHABET)
    print(txt)
    print(pp.convert_str_to_emoji(txt))
    bot.sendMessage(msg["channel"], pp.convert_str_to_emoji(txt, space="           "))


def send87(bot, msg):
    bot.sendMessage(msg["channel"], "87")


def test(bot, msg):
    testing = "blackboxwhitebox" * random.randrange(5, 20)
    bot.sendMessage(msg["channel"], testing)


def pony(bot, msg):
    bot.sendMessage(msg["channel"], "```" + p.Pony.getPony() + "```")


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

def formatHelpMsg(cmd, msg):
    justifyLength = 24
    cmdLen = len(cmd)
    msgLen = len(msg)
    if cmdLen < justifyLength:  # within formatting bounds
        return cmd.ljust(justifyLength, ' ') + msg
    if justifyLength < cmdLen:  # overflow to next line for message
        return cmd + '\n'.ljust(justifyLength + 1, ' ') + msg


"""
dictionary for routing function calls read from incoming messages over the slack rtm api

text     - regex string matching for individual commands
callback - function called when text string is matched
help     - string printed when help command is called,
               show users which functions are enabled for use (blank they do not know it exists)
"""
router = [
    {
        "text": ["~colorname", "~color name"],
        "callback":colorCode,
        "type": "text",
        "help": formatHelpMsg("`~colorname (string)`",
                              "- Returns hex color code derived from input")
    }, {
        "text": ["~randomintern"],
        "callback":randomIntern,
        "type": "text",
        "help": formatHelpMsg("`~randomintern`",
                              "- select a random intern to give a task to")
    }, {
        "text": ["~help"],
        "callback":GoTo.help,
        "type": "text",
        "help": formatHelpMsg("`~help`", "- display this message")
    }, {
        "text": ["~catfacts", "~cat facts"],
        "callback":catFacts.catFacts,
        "type": "text",
        "help": formatHelpMsg("`~catfacts`", "- Returns a random catfact")
    }, {
        "text": ["~quote"],
        "callback":quote,
        "type": "text",
        "help": ""
    }, {
        "text": ["~startpoll", "~poll", "~createpoll", "~start poll", "~poll", "~create poll"],
        "callback":poll.startPoll,
        "type": "text",
        "help": formatHelpMsg("`~startpoll,(nameOfPoll),(option1),(option2),...(optionX)`",
                              "- Creates a poll that can be voted on, closed or have an option added to the poll")
    }, {
        "text": ["~stoppoll", "~removepoll", "~stop poll", "~remove poll"],
        "callback":poll.stopPoll,
        "type": "text",
        "help": formatHelpMsg("`~stoppoll,(pollName)`", "- Ends the poll and displays results")
    }, {
        "text": ["~vote", "~votepoll", "~vote poll"],
        "callback":poll.vote,
        "type": "text",
        "help": formatHelpMsg("`~vote,(pollName),(option)`",
                              "- Votes for (option). If you have aready voted it removes your old vote")
    }, {
        "text": ["~addoption"],
        "callback":poll.addOption,
        "type": "text",
        "help": formatHelpMsg("`~addoption,(pollName),(newOption)`",
                              "- Creates a new option for a poll")
    }, {
        "text": ["ship it", ":shipit:", "shipit"],
        "callback":images.shipIt,
        "type": "text",
        "help": formatHelpMsg("`ship it`", "- Returns ship it squirrel image")
    }, {
        "text": ["~deleteall"],
        "callback":GoTo.deleteAll,
        "type": "text",
        "help": formatHelpMsg("`~deleteall`",
                              "- Deletes all private group/dm messages sent by the bot.")
    }, {
        "text": ["~nye"],
        "callback":images.nye,
        "type": "text",
        "help": formatHelpMsg("`~nye`", "- Returns a bill nye gif")
    }, {
        "text": ["~meme"],
        "callback":images.getMeme,
        "type": "text",
        "help": formatHelpMsg("`~meme,(keyword)`",
                              "- Gets a meme for given keyword.  Returns 'nope.jpg' if no meme found")
    }, {
        "text": ["~gif"],
        "callback":images.getGiphy,
        "type": "text",
        "help": formatHelpMsg("`~gif,(keyword)`", "- Returns a gif with the given keyword")
    }, {
        "text": ["~insanity"],
        "callback":images.getMeme,
        "type": "text",
        "help": formatHelpMsg("`~insanity`", "- Returns an insanity wolf meme")
    }, {
        "text": ["~dm"],
        "callback":GoTo.sendDM,
        "type": "text",
        "help": ""
    }, {
        "text": ["~random intern", "~ randomintern"],
        "callback": randominterns,
        "type": "text",
        "help": ""
    }, {
        "text": ["~partyparrot"],
        "callback": partyParrotMsg,
        "type": "text",
        "help": formatHelpMsg("`~partyparrot (string)`", "- Converts text to party parrots")
    }, {
        "text": ["~send87"],
        "callback": send87,
        "type": "text",
        "help": formatHelpMsg("`~send87`", "- Test function that sends 87")
    }

    # , {
    #     "text": ["zach", "zachisan", "<3", ":heart:",":heart_decoration:", "zack",
    #              ":heart_eyes:",":heartbeat:",":heartpulse:",":hearts:"],
    #     "callback": playGong,
    #     "type": "text",
    #     "help": ""
    # }, {
    #   "text": ["~delete"],
    #   "callback":GoTo.delete,
    #   "type": "text",
    #   "help": "`~delete`               - Deletes the last message sent by bot in the specified channel."
    # }, {
    #   "text": ["test"],
    #   "callback":test,
    #   "type": "text",
    #   "help": "`test` `testing`        - any appearance of the string `test` there will be a response posted"
    # }, {
    #       "text": ["~pony"],
    #       "callback": pony,
    #       "type": "text",
    #       "help": "sends ascii art"
    # }

]
