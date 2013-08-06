import json
import tornado.ioloop
import tornado.web
from muc import MUCBot

jid = ''
password = ''
room = ''
nick = ''



class main(tornado.web.RequestHandler):
  def get(self):
    self.write("Hello, world")

  def post(self):
    obj = json.loads(self.request.body)
    msg = """{user} push {commit_count} commits to {ref}\n{commits}\n---\n""".format(
      user=obj['user_name'],
      commit_count=obj['total_commits_count'], 
      ref=obj['ref'], 
      commits='\n'.join([x.get('message','') for x in obj['commits']]), 
    )
    xmpp = MUCBot(jid, password, room, nick, unicode(msg))
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping
    if xmpp.connect():
      xmpp.process(block=True)


application = tornado.web.Application([
  (r"/", main),
], debug=True)

if __name__ == "__main__":
  application.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
