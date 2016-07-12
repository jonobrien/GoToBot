# GoToBot
A Slack bot written in Python 3.
Requires Python 3.4


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
2. login to slack and go to `https://<TEAMNAME>.slack.com/apps/build/custom-integration`
3. click `bots` and choose a username, click `add bot integration`
4. make a file called `token.txt` in the same directory as the bot file and put the bot slack api key inside
5. make a newline delimited text file called 'EN_dict.txt' and put it into the root dir, such as one from: [here](https://github.com/dwyl/english-words) to allow for distraction functionality
6. run with `python3 gotobot.py`

# Setup for baseBot.py
1. clone the repo
2. login to slack and go to `https://<TEAMNAME>.slack.com/apps/build/custom-integration`
3. click `bots` and choose a username, click `add bot integration`
4. make a file called `token.txt` in the same directory as the bot file and put the bot slack api key inside
5. run with `python3 baseBot.py`

# Docs and API Wrappers
- [python-slackclient](https://github.com/slackhq/python-slackclient)
- [Slack API](https://api.slack.com/)
