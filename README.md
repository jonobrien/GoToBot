# GoToBot
A Slack bot written in Python 3.
Requires Python 3.X

# Key Features
Using a mapping dictionary with callbacks to function calls:
- add quotes of your co-workers
- generate memes/gifs from various APIs
- create/vote/edit polls for your team to decide on tasks/delegation
- choose among the interns on your team who has to do a task
- bot message deletion available
- bot can private message team members
- auto-restart

# Setup for gotobot.py
1. clone the repo
2. make a file called token.txt and put your slack api key inside
3. make a newline delimited text file called 'EN_dict.txt' and put it into the root dir, such as one from: [here](https://github.com/dwyl/english-words)
4. run with `python3 gotobot.py`

# Setup for baseBot.py
1. clone the repo
2. make a file in the same directory as the bot file called `token.txt` and put your slack api key inside
3. run with `python3 baseBot.py`



# Docs and API Wrappers
- [python-slackclient](https://github.com/slackhq/python-slackclient)
- [Slack API](https://api.slack.com/)
