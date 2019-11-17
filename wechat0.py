# wechat-
copy了最近狗屁不通文章生成器，移植到了wechat上
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 21:23:25 2019

@author: Mario
"""
#微信自动回复消息
import itchat
import random,readjosn_myself
from itchat.content import *

data = readjosn_myself.readjosn_myself(r"e:/Python/work/BullshitGenerator-master/data.json")
ana = data["famous"] # a 代表前面垫话，b代表后面垫话
before_word = data["before"] # 在名人名言前面弄点废话
after_word = data['after']  # 在名人名言后面弄点废话
rubbish = data['bosh'] # 代表文章主要废话来源
time0 = 2

def traverse(lis):
    global time0
    pool = list(lis) * time0
    while True:
        random.shuffle(pool)
        for i in pool:
            yield i

next_rub = traverse(rubbish)
next_ana = traverse(ana)

def get_ana():
    global next_ana
    xx = next(next_ana)
    xx = xx.replace(  "a",random.choice(before_word) )
    xx = xx.replace(  "b",random.choice(after_word) )
    return xx

def next_para():
    xx = ". "
    xx += "\r\n"
    xx += "    "
    return xx
tmp = str()
def send_msg(get_msg):
    xx = str(get_msg)
    for x in xx:
        tmp = str()
        while ( len(tmp) < 300 ) :
            branch = random.randint(0,100)
            if branch < 10:
                tmp += next_para()
            elif branch < 40 :
                tmp += get_ana()
            else:
                tmp += next(next_rub)
        tmp = tmp.replace("x",xx)
        return tmp


@itchat.msg_register(TEXT)  #这里的TEXT表示如果有人发送文本消息，那么就会调用下面的方法
def simple_reply(msg):
  #这个是向发送者发送消息
  itchat.send_msg('已经收到了文本消息，消息内容为%s'%msg['Text'],toUserName=msg['FromUserName'])
  get_msg = msg['Content']
  tosend_word = send_msg(get_msg)
  return tosend_word   #返回的给对方的消息，msg["Text"]表示消息的内容

itchat.auto_login(hotReload=True)
itchat.run()
