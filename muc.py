#!/usr/bin/env python
# -*- coding: utf-8 -*-

# [ref](https://github.com/fritzy/SleekXMPP/blob/develop/examples/muc.py)

import sleekxmpp


class MUCBot(sleekxmpp.ClientXMPP):
  def __init__(self, jid, password, room, nick, msg):
    sleekxmpp.ClientXMPP.__init__(self, jid, password)

    self.room = room
    self.nick = nick
    self.msg = msg

    self.add_event_handler("session_start", self.start)


  def start(self, event):
    self.get_roster()
    self.send_presence()
    self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)
    self.send_message(mto=self.room,
                      mbody=self.msg,
                      mtype='groupchat')
    self.disconnect(wait=True)
