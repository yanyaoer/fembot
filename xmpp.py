#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import logging
import subprocess
from sleekxmpp import ClientXMPP
import config


def cmd(string):
    process = subprocess.Popen(string,
                               shell=True,
                               stdout=subprocess.PIPE,
    )
    return  process.communicate()[0]

class SimpleBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        logging.debug("body: " + msg['body'])
        logging.debug("from: " + msg['from'].user)
        if msg['type'] in ('chat', 'normal'):
            if config.command_filter(msg):
                content = cmd(msg['body'][2:])
            else:
                content = "Thanks for sending\n%(body)s" % msg
            msg.reply(content).send()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = SimpleBot(config.bot['username'], config.bot['password'])
    xmpp.connect()
    xmpp.process(block=True)
