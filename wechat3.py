# wechat-
#copy了最近狗屁不通文章生成器，移植到了wechat上
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 16:48:10 2019

@author: Mario
"""
import itchat
from itchat.content import *
import requests
import random,readjosn_myself
import jieba
from wordcloud import WordCloud,ImageColorGenerator
import codecs
import jieba.finalseg
import imageio
import matplotlib.pyplot as plt
import numpy as nu
import os
import json


data = readjosn_myself.readjosn_myself("data.json")
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
        while ( len(tmp) < 1600 ) :
            branch = random.randint(0,100)
            if branch < 5:
                tmp += next_para()
            elif branch < 20 :
                tmp += get_ana()
            else:
                tmp += next(next_rub)
        tmp = tmp.replace("x",xx)
        return tmp

def mass_texting(word):
    friends = itchat.get_friends(update=True)[0:]
    for i in range(len(friends)):
        to_id = friends[i]['UserName']
        itchat.send_msg(word,toUserName=to_id)
        
def get_tuling_reponse(msg0):
    api_url = 'http://openapi.tuling123.com/openapi/api/v2'  ##指定的api地址
    data = {
    	"reqType":0,
        "perception": {
            "inputText": {
                "text": msg0
            },
            "inputImage": {
                "url": "imageUrl"
            }
        },
        "userInfo": {
            "apiKey": "***********************",
            "userId": "fanc"
        }
    }

    data = json.dumps(data)
    res = requests.post(api_url,data).json()
    return res['results'][0]['values']['text']
'''    
    res = requests.post(api_url,data).json()  ##发送数据到指定的网址，获取网址返回的数据
    return(res['text'])        
'''
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """
    :param word:
    :param font_size:
    :param position:
    :param orientation:
    :param random_state:
    :param kwargs:
    :return:
    Description:
        调配词云中文字的颜色
    """
    return "hsl(210, 100%%, %d%%)" % nu.random.randint(10, 80)  # 这里以蓝色为基本色调

# 绘制词云
def draw_wordcloud(file):
    #读入一个txt文件
    try:
        comment_text = open(file,'r',encoding='utf-8',errors="ignore").read()
    except:
        comment_text = open(file,'r',encoding='gbk').read()
    #结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    #d = path.dirname(__file__) # 当前文件文件夹所在目录
    color_mask = imageio.imread("/python/1.png") # 读取背景图片
    cloud = WordCloud(
        #设置字体，不指定就会出现乱码
        #font_path="hwxk.ttf",
        font_path = 'msyhl.ttc',
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=40
    )
    #print(cut_text)
    word_cloud = cloud.generate(cut_text) # 产生词云
    word_cloud.to_file("MyWordCloud.jpg") #保存图片
    #  显示词云图片
    #plt.imshow(word_cloud)
    #使词云颜色跟背景图片颜色一致
'''    
    img_color = ImageColorGenerator(color_mask)
    word_cloud_color = cloud.recolor(color_func=img_color) #图片色调
    word_cloud_color = cloud.recolor(color_func=color_func) #自定义色调
    #plt.imshow(word_cloud_color)
    word_cloud_color.to_file("/python/MyWordCloud_color.jpg")
    #plt.axis('off')
    #plt.show()
''' 

msg_text_bd = '你好啊'
def baidu_ai_robot(msg_text_bd):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【百度云应用的AK】&client_secret=【百度云应用的SK】'
    response = requests.get(host)
    
    if response:
        rejson = response.json()    
    access_token = rejson['access_token']
    url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + access_token
    post_data = {"log_id":"UNITTEST_10000","version":"2.0","service_id":"S24514","session_id":"","request":{"query":msg_text_bd,"user_id":"88888"},"dialog_state":{"contexts":{"SYS_REMEMBERED_SKILLS":["1057"]}}}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    post_data = json.dumps(post_data)
    print(post_data)
    response = requests.post(url, data=post_data, headers=headers)
    robot_replys = []
    if response:
        robot_reply = response.json()    
        for i in range(len(robot_reply['result']['response_list'][1]['action_list'])):
            robot_replys.append(robot_reply['result']['response_list'][1]['action_list'][i]['say'])
    my_reply = random.choice(robot_replys)
    return my_reply
      
sta1=''
sta2=''
sta3=''
newname=''

@itchat.msg_register(TEXT)  #这里的TEXT表示如果有人发送文本消息，那么就会调用下面的方法
def simple_reply(msg):
  #itchat.send_msg('已经收到了文本消息，消息内容为%s'%msg['Text'],toUserName=msg['FromUserName'])
  friends = itchat.get_friends(update=True)[0:]
  if msg['Content']=='群发1010110':
      global sta1,sta2,sta3
      sta1='群发'
      return 'please input mass texting '
  elif msg['Content']=='取消群发1010110':
      sta1=''
      return '已取消 '
  elif sta1=='群发':
      mass_texting(msg['Content'])
      sta1=''
      return '群发成功'
  elif msg['Content']=='废话机器1010110':
      sta2='启动'
      return '启动成功'
  elif msg['Content']=='关闭1010110':
      sta2=''
      return '关闭成功'
  elif sta2=='启动':
      get_msg = msg['Content']
      tosend_word = send_msg(get_msg)
      return tosend_word
  elif msg['Content']=='myrobot':
      sta3='robot'
      return '百度ai机器人启动成功'
  elif msg['Content']=='closerobot':
      sta3=''
      return '百度ai机器人关闭成功 '
  elif sta3=='robot':
      content = msg['Content']  ##返回文本信息内容
#      returnContent = get_tuling_reponse(content)  ## 将好友的消息发送给机器人去处理，处理的结果就是返回给好友的信息
      returnContent = baidu_ai_robot(content)
#      itchat.send_msg('[wechat_robot]',toUserName=msg['FromUserName'])
      returnContent = '[AI]'+returnContent
      return returnContent

@itchat.msg_register(ATTACHMENT)
def dis_files(msg):
    msg['Text'](msg['FileName'])
    filename = msg['FileName']
    portion = os.path.splitext(filename)
    itchat.send_msg('已收到文件',toUserName=msg['FromUserName'])
    global newname
    if portion[1] != ".txt":#根据后缀来修改,如无后缀则空
        newname = portion[0]+".txt"#要改的新后缀
        os.rename(filename,newname)
    else:
        newname = msg['FileName']
    try:
        draw_wordcloud(str(newname))
    except IOError:
        return "Error: 没有找到文件或读取文件失败"
    else:
        itchat.send_image('/python/MyWordCloud.jpg',toUserName=msg['FromUserName'])
        return "sussess"        
        

itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.run()
