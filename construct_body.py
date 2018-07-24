#!/usr/bin/env python

# these globals should come from a config in /etc i think
message_file_path = '/tmp/slack_warnings'

# you need to `pip install PyYAML, sorry not sorry
import yaml

def get_host():
    import os.path as path
    to_return = {'username': 'Special Circumstances [identity unknown]'}
    if path.exists('/etc/fullname'):
        to_return['username'] = open('/etc/fullname').read().rstrip()
    return to_return

def get_alarms(force=False):
    # each entry in the alarms log file should be fo the form:
    # - [<some date entry>, <some source>, <some message>]
    # where each item must have a minus in column zero and a space in column 1, and then something that parses as a three element array, each of which is a string
    # where each item in <> is seen as a string by the yaml parser (may or may not require quotes, safer to use them)
    to_return = {}
    import os.path as path
    try:
        messages = yaml.load(open(message_file_path, 'r').read())['to_send']
        sorted_messages = {}
        if messages:
            for m in messages or []:
                sorted_messages[m[1]] = '\n'.join([sorted_messages.get(m[1], ''), '{}: {}'.format(m[0],m[2])]).lstrip()
            attachments = [{'fallback': 'message decoding failed', 'color': 'danger'}]
            fields = [{'short':False, 'title': key, 'value': value} for key,value in sorted_messages.items()]
            attachments[0]['fields'] = fields
            to_return.update({'attachments':attachments})
        elif force:
            to_return.update({'text':'Regular interval checkin; nothing to report'})
    except Exception as e:
        to_return.update({'text':'warnings file exists but unable to parse; I require assistance'})
        raise
    return to_return

def say_hi():
    to_return = {}
    to_return.update({'text': 'Returning to the conversation'})
    return to_return

def say_bye():
    to_return = {}
    to_return.update({'text': 'Going radio silent'})
    return to_return

if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', help="force a message, even if no alerts in /tmp/slack_warnings", action='store_true')
    parser.add_argument('-q', '--quit', help="generate a goodbye message", action='store_true')
    parser.add_argument('-w', '--welcome', help="generate message indicating starting to monitor", action='store_true')
    options = parser.parse_args()
    a_post = {}
    if options.welcome:
        a_post.update(say_hi())
    elif options.quit:
        a_post.update(say_bye())
    else:
        a_post.update(get_alarms(force=options.force))
    if a_post:
        a_post.update(get_host())
        print(json.dumps(a_post))
