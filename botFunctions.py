

class Router:
    def __init__(self):
        self.router = [{
          "text": ["~colorname", "~color name"],
          "callback":colorCode,
          "type": "text",
          "help": "`~colorname (string)`   - the space is necessary.  Returns an associated hex color code derived from input"
        },{
          "text": ["~randomintern"],
          "callback":randomIntern,
          "type": "text",
          "help": "`~randomintern`         - select a random intern to give a task to"
        },{
          "text": ["~help"],
          "callback":GoTo.help,
          "type": "text"
        },{
          "text": ["~catfacts", "~cat facts"],
          "callback":catFacts.catFacts,
          "type": "text",
          "help": "`~catfacts`             - Returns a random catfact"
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
          "text": ["ship it",":shipit:", "shipit"],
          "callback":images.shipIt,
          "type": "text",
          "help": "`ship it`               - Returns ship it squirrel image"
        },{
          "text": ["~deleteall"],
          "callback":GoTo.deleteAll,
          "type": "text",
          "help": "`~deleteall`            - Deletes all private group/dm messages sent by the bot."
        }
        # ,{
        #   "text": ["~delete"],
        #   "callback":GoTo.delete,
        #   "type": "text",
        #   "help": "`~delete`               - Deletes the last message sent by bot in the specified channel."
        # }
        ,{
          "text": ["~nye"],
          "callback":images.nye,
          "type": "text",
          "help": "`~nye`                  - Returns a bill nye gif"
        }
        # ,{
        #   "text": ["test"],
        #   "callback":test,
        #   "type": "text",
        #   "help": "`test` `testing`        - any appearance of the string `test` there will be a response posted"
        # }
        ,{
          "text": ["~meme"],
          "callback":images.getMeme,
          "type": "text",
          "help": "`~meme,(keyword)`       - Gets a meme with given keyword.  Returns nope.jpg if no meme found"
        },{
          "text": ["~gif"],
          "callback":images.getGiphy,
          "type": "text",
          "help": "`~gif,(keyword)`        - Returns a gif with the given keyword"
        },{
          "text": ["~insanity"],
          "callback":images.getMeme,
          "type": "text",
          "help": "`~insanity`             - Returns an insanity wolf meme"
        },
        # {
        #   "text": ["~dm"],
        #   "callback":GoTo.sendDM,
        #   "type": "text",
        #   "help": ""
        # },
        # {
        #   "text": ["~pony"],
        #   "callback": pony,
        #   "type": "text",
        #   "help": "sends ascii art"
        # },
        {
          "text": ["~random intern", "~ randomintern"],
          "callback": randominterns,
          "type": "text",
          "help": ""
        },
        {
          "text":["~partyparrot"],
          "callback": partyParrotMsg,
          "type": "text",
          "help": "`~partyparrot (string)` - Converts text to party parrot"
        },
        {
          "text":["~send87"],
          "callback": send87,
          "type": "text",
          "help": "`~send87` - Test function that sends 87"
        }
        # {
        #   "text": ["zach", "zachisan", "<3", ":heart:",":heart_decoration:", "zack",
        #         ":heart_eyes:",":heartbeat:",":heartpulse:",":hearts:"],
        #   "callback": playGong,
        #   "type": "text",
        #   "help": ""
        # }
    ]