# slackline
A Simple command line version of Slack


Sadly, this does not work on Windows, only unix systems.  There's no Windows port for the curses module, which is what is used to create a split screen in the terminal.


Supports sending messages, switching channels, listing channels, and viewing channel members.


<b><h3> Getting Start </h3></b>

Make sure you have python 2.7.* installed.

Get yourself a slack api token. (https://api.slack.com/web)  These tokens are team and user specific, so each user has an api for every team they belong to!  Stick this in a text file called "slack.json" with the form " {'token' : blahblah}

Setting up your dependencies
```
  pip install requirements.txt
```

```
  python slack.py
```

If for some reason SlackLine  crashes (sorry!), your terminal will look like it's had a really bad day.  Don't fret, just type "reset" and hit enter, or close out the terminal tab.
