from slackclient import SlackClient
import os
import json
import threading
import time
import readline, sys, struct, fcntl, termios


class SlackLine(object):
    _name_to_ids = None
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
        print json.loads(self.server.api_call('users.list'))
        for user in json.loads(self.server.api_call('users.list')):
            user = user['profile']
            if user['name'] == self.name:
                self.user['id']
            self._name_to_ids[user['name']] = user['id']

    def attach_all_channels(self):
        for channel in json.loads(self.client.api_call('channels.list'))['channels']:
            self.server.attach_channel(channel['name'], channel['id'])

    def test_is_authenticated(self):
	return json.loads(self.client.api_call('channels.list'))['ok']

    def switch_channel(self): #TODO
        pass

    def get_client(self, token):
        return SlackClient(token)

    def chat_forever(self):
        print 'Welcome to SlackLine!'
        print 'Talking in Chat : %s' % self.current_channel.name
        while True:
            self.server.ping()
            cmd = raw_input('>>> ')
            if cmd.startswith('quit'):
                self.flush_logs()
                break
            else:
                self.current_channel.send_message(cmd)

    def start(self):
        stream = MessageReceiver(self.client)
        stream_thread = threading.Thread(target=stream.read_messages, args=())
        stream_thread.start()

class MessageReceiver(object):
    """ Receive messages over real-time messaing api
        Filters out messages that belong to current user
    """

    def __init__(self, client):
        self.client = client
        self.server = self.client.server

    def read_messages(self):
        def blank_current_readline():
            (rows, cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))
            text_len = len(readline.get_line_buffer())+2
            sys.stdout.write('\x1b[2k')
            sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))
            sys.stdout.write('\x1b[0G')

        while True:
            data = self.client.rtm_read()
            if data:
                print data
                for msg in data:
                    if 'text' in msg and 'user' in msg and msg['user'] != self.client._user_id:
                        #print msg['user'], msg['text']
                        blank_current_readline()
                        sys.stdout.write('>>> ' + readline.get_line_buffer())
                        sys.stdout.flush()
                time.sleep(.250)

if __name__ == '__main__':
    client = SlackLine('alex')
    #client.start()
    #client.chat_forever()
