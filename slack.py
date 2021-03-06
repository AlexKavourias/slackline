from slackclient import SlackClient
from slack_screen import SlackTerminal
import os
import json
import threading
import time

class SlackLine(object):
    _name_to_ids = None
    _ids_to_names = None
    _user_id = None
    
    _commands = ("lc", "sc", "exit", "quit", "is_online")

    def __init__(self, slack_name, token=None, channel_id=None, channel_name=None):
        """ Will look for a json file called "slack.json", if it's found, will load token and other
           information from there.  Otherwise, defaults to init params

           slack.json format:
           {"token": ...}
        """
        assert token or 'slack.json' in os.listdir(os.getcwd())
        self.token = token if token else json.loads(open('slack.json').read().replace('\n', ''))['token']
        self.client = self.get_client(self.token)
        self.server = self.client.server
        self.name = slack_name
        self.terminal = None #Setup in start
        self._logs = []
        self.channels = self.server.channels
        self.attach_all_channels()
        if channel_id:
            self.current_channel = [chnl for chnl in self.channels if chnl.id == channel_id][0]
        elif channel_name:
            self.current_channel = [chnl for chnl in self.channels if chnl.name == channel_name][0]  
        else:
            self.current_channel = self.channels[0]
        self.current_users = self.current_channel
        self._get_user_id()

    def where_am_i(self):
        self.terminal.add_message("Log", "Currently talking in channel " +
                self.current_channel.name)

    def _get_user_id(self):
        '''Gets current user id and stores name/ids for all team users'''
        self._name_to_ids = {}
        for user in json.loads(self.server.api_call('users.list'))['members']:
            if user['name'] == self.name:
                self.user = user['id']
            self._name_to_ids[user['name']] = user['id']
        self._ids_to_names = {v:k for k,v in self._name_to_ids.items()}

    def list_users_in_channel(self):
        self.terminal.add_message('Log', 'Current Users in %s' % self.current_channel.name)
        resp = self.server.api_call('channels.info', channel=self.current_channel.id)['memmbers']
        for user_id in resp:
            self.terminal.add_message(self._ids_to_names[user_id])

    def list_channels(self):
        self.terminal.add_message("Log", "Channel List (type 'switch <channel name>'")
        for number, channel in enumerate(self.channels):
            self.terminal.add_message("\t", "\t%s) %s" % (number, channel.name))

    def switch_channels(self, channel_name=None, channel_id=None):
        if not (channel_id or channel_name):
            self.terminal.add_message("Error", "specify channel name/id. Use lc to view list")
            return
        for channel in self.channels:
            if channel.id == channel_id or channel.name == channel_name:
                self.current_channel = channel
                self.terminal.add_message("Log", "Switched to channel %s" % channel.name)
                return

    def list_commands(self):
        for command in self._commands:
            self.terminal.add_message("\t", command)

    def attach_all_channels(self):
        for channel in json.loads(self.client.api_call('channels.list'))['channels']:
            self.server.attach_channel(channel['name'], channel['id'])

    def test_is_authenticated(self):
        return json.loads(self.client.api_call('channels.list'))['ok']

    def get_client(self, token):
        a = SlackClient(token)
        print a.server
        return a

    @staticmethod
    def start():
        try:
            slack = SlackLine('alex', channel_name="coding")
            stream = MessageReceiver(slack, slack._user_id)
            slack.terminal = SlackTerminal(slack)
            stream_thread = threading.Thread(target=stream.read_messages,
                                            args=(slack.terminal, stream.basic_filter))
            stream_thread.daemon = True
            stream_thread.start()
            slack.terminal.simulate_raw_input()
        except KeyboardInterrupt:
            slack.terminal.teardown()
            exit(0)

class MessageReceiver(object):
    """ Receive messages over real-time messaging api
        Filters out messages that belong to current user
    """

    def __init__(self, slackline, user_id):
        self.client = slackline.client
        self._slackline = slackline
        self.server = self.client.server
        #Filters all user messages received that match this id
        self.filter_id = user_id

    def read_messages(self, terminal, filter_func):
        while True:
            data = self.client.rtm_read()
            messages = []
            if data:
                for msg in data:
                    if filter_func(msg):
                        terminal.add_message(self._slackline._ids_to_names[msg['user']], msg['text'])
            time.sleep(.250)

    def basic_filter(self, msg):
        """
           Returns True if
             'text' is in the message dictionary
             the 'from user' is not the user currently using slackline
             the channel the message originated in eqauls the current channel
        """
        return 'text' in msg and 'user' in msg and msg['user'] != self.filter_id\
            and self._slackline.current_channel.id == msg['channel']

if __name__ == '__main__':
    SlackLine.start()
