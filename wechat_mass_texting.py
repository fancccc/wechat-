# wechat-
#这是一个简单微信群发功能
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 18:25:14 2019

@author: Mario
"""

import itchat
from itchat.content import *

def mass_texting(word):
    friends = itchat.get_friends(update=True)[0:]
    for i in range(len(friends)):
        to_id = friends[i]['UserName']
        itchat.send_msg(word,toUserName=to_id)
        
sta=''

@itchat.msg_register(TEXT)  #这里的TEXT表示如果有人发送文本消息，那么就会调用下面的方法
def simple_reply(msg):
  #这个是向发送者发送消息
  itchat.send_msg('已经收到了文本消息，消息内容为 %s'%msg['Text'],toUserName=msg['FromUserName'])
  if msg['Content']=='群发1010110':
      global sta
      sta='群发'
      return 'please input mass texting '
  elif msg['Content']=='取消群发1010110':
      sta=''
      return '已取消 '
  elif sta=='群发':
      mass_texting(msg['Content'])
      sta=''
      return '群发成功'

itchat.auto_login(hotReload=True)
itchat.run()
