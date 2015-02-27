bot = {
    'username': '',
    'password': ''
}

def command_filter(msg):
    """run command when body start with '$ '

    eg. '$ ls /tmp'
    """
    return msg['body'].startswith('$ ')
