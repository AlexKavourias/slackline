from slackclient import SlackClient

def get_client(token='4577027817.4577075131'):
    return SlackClient(token)

print get_client().api_call('api.test')

