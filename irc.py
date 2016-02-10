# -*- coding: utf-8 -*-

import re
import redis
from ircmessage import IRCMessage
from queue import Queue
from setting import botnick
from steam import search_id, game_choice

class Bot():
    irc = None
    msgQueue = Queue()
    channel_list = []


    def __init__(self):
        from ircconnector import IRCConnector
        self.irc = IRCConnector(self.msgQueue)
        self.irc.setDaemon(True)
        self.irc.start()
        self.irc.joinchan('#nemo')
        self.irc.joinchan('#botworld2')

    def run(self):
        idmap = redis.StrictRedis()
        adduser = re.compile("#Steambot add ([A-za-z0-9]+)")
        randomgame = re.compile("#Steambot search ([A-za-z0-9]+)")
        while True:
            packet = self.msgQueue.get()
            if packet['type'] == 'msg':
                msg = packet['content']
                for channel in self.channel_list:
                    self.irc.sendmsg(channel, msg)

            elif packet['type'] == 'irc':
                message = packet['content']
                msgstr = message.msg
                print(message)
                print(type(message.channel))
                print(message.channel)
                if message.msgType == 'INVITE':
                    self.irc.joinchan(message.channel)

                elif message.msgType == 'MODE':
                    if msgstr == '+o ' + botnick:
                        self.irc.sendmsg(message.channel, '감사합니다 :)')

                elif message.msgType == 'KICK':
                    if message.channel in self.channel_list:
                        self.channel_list.remove(message.channel)

                elif message.msgType == 'PRIVMSG':
                    validuser = adduser.match(msgstr)
                    validsearch = randomgame.match(msgstr)
                    if validuser:
                        new_id = validuser.group(1)
                        search = search_id(new_id)
                        if search:
                            idmap.set(new_id,search)
                            self.irc.sendmsg(message.channel, "유저 %s가 등록되었습니다" % new_id)
                        else:
                            self.irc.sendmsg(message.channel, "존재하지 않거나 접근할 수 없는 아이디 입니다." )
                    elif validsearch:
                        get_id = idmap.get(validsearch.group(1))
                        if get_id:
                            self.irc.sendmsg(message.channel, game_choice(get_id.decode('utf8')))
                        else:
                            self.irc.sendmsg(message.channel, "등록되지 않은 아이디 입니다." )
                    


if __name__ == '__main__':
    bot = Bot()
    bot.run()