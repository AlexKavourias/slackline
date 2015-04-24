from slackclient import SlackClient

def get_client(token):
    return SlackClient(token)

token = open('token.txt').read()
print get_client(token)
