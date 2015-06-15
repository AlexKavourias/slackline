from slackclient import SlackClient
from slack_screen import SlackTerminal
import os
import json
import threading
import time
import readline, sys, struct, fcntl, termios
import pprint

class SlackLine(object):
    _name_to_ids = None
    _ids_to_names = None
    _user_id = None

    def __init__(self, slack_name, token=None, channel_id=None, channel_name=None):
        assert token or 'token.txt' in os.listdir(os.getcwd())
	self.token = token if token else open('token.txt').read().replace('\n', '')
        self.client = self.get_client(self.token)
	self.server = self.client.server
	self.name = slack_name
        self._logs = []
        self.attach_all_channels()
        if channel_id:
            self.current_channel = [chnl for chnl in self.server.channels if chnl.id == channel_id]
        else:
            self.current_channel = self.server.channels[0]
        self.current_users = self.current_channel
        self._get_user_id()

    def _get_user_id(self):
        '''Gets current user id and stores name/ids for all team users'''
        self._name_to_ids = {}
        for user in json.loads(self.server.api_call('users.list'))['members']:
            if user['name'] == self.name:
                self.user = user['id']
            self._name_to_ids[user['name']] = user['id']
        self._ids_to_names = {v:k for k,v in self._name_to_ids.items()}

    def attach_all_channels(self):
        for channel in json.loads(self.client.api_call('channels.list'))['channels']:
            self.server.attach_channel(channel['name'], channel['id'])

    def test_is_authenticated(self):
	return json.loads(self.client.api_call('channels.list'))['ok']

    def switch_channel(self): #TODO
        pass

    def get_client(self, token):
        return SlackClient(token)

    @staticmethod
    def start():
        try:
            slack = SlackLine('alex')
            stream = MessageReceiver(slack, slack._user_id)
            terminal = SlackTerminal(slack)
            stream_thread = threading.Thread(target=stream.read_messages,
                                            args=(terminal, stream.basic_filter))
            stream_thread.daemon = True
            stream_thread.start()
            terminal.simulate_raw_input()
        except KeyboardInterrupt:
            terminal.teardown()
            exit()

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
                #terminal.add_message('DEBUG', data)
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
    client = SlackLine('alex')
    client.start()
