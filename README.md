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
4. make an entry in your environment variables for `slack_token` and set the generated token
5. make a newline delimited text file called 'EN_dict.txt' and put it into the root dir, such as one from: [here](https://github.com/dwyl/english-words) to allow for distraction functionality
6. run with `python gotobot.py`

# Setup for baseBot.py
1. clone the repo
2. login to slack and go to `https://<TEAMNAME>.slack.com/apps/build/custom-integration`
3. click `bots` and choose a username, click `add bot integration`
4. make a file called `token.txt` in the same directory as the bot file and put the bot slack api key inside
5. run with `python baseBot.py`

# for Heroku
1. create heroku account
2. download heroku toolbelt and login locally
3. configure python buildpack for heroku stack
4. scale the dyno to tell remote what to run when deployed `heroku ps:scale web=1 --app=<APPNAME>`
5. if there is an issue building remotely: `heroku run python gotobot.py --app=<APPNAME>`

# Docs and API Wrappers
- [python-slackclient](https://github.com/slackhq/python-slackclient)
- [Slack API](https://api.slack.com/)
