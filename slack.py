from slackclient import SlackClient
import time
import os


class SlackLine(object):

    def __init__(self, token=None, channel_id=None, channel_name=None):
        assert token or 'token.txt' in os.listdir(os.getcwd())
        self.client = self.get_client(token if token else open('token.txt').read())
        self.server = self.client.server
        self._logs = []
        #Attach All Channels in the User's view
        #TODO

    def switch_channel(self): #TODO
        pass

    def get_client(self, token):
        return SlackClient(token)

    def chat_forever(self):
        print 'Welcome to SlackLine!'
        print '\t Talking in Chat : %s' % self.current_channel
        while True:
            cmd = raw_input('>>> ')
            if cmd.startswith('send'):
                #send message
                pass
            if cmd.startswith('quit'):
                self.flush_logs()
                break
        cmd = raw_input('Exit SlackLine? [Y/n]')

client = SlackLine().client
