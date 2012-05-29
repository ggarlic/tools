#!/usr/bin/env python
# -*- coding:utf8 -*-
import random
import time
import smtplib
from email.mime.text import MIMEText
import count

"""
Usage:
    1, modify items in "default config" section to fit your need 
    2, in my situation, our smtp server doesn't need user/password 
       to send out mails. maybe you should add ss.login() to fit your
       need
    3, add it to cron, e.g. we use it like this:

        30 11 * * * /usr/bin/python /home/ggarlic/food.py >/dev/null 2>&1

Enjoy yourself

"""
##########deafault config##########

#places to eat
MENU=["面道", "沙县小吃", "驴肉火烧", "陕西面馆", "南城香"]

#people to notify
mailto_list = ['zhangsan@xxx.com', 'lisi@xxx.com']

#smtp host
mail_host = "xxx.xxx.com"

#sender
me = "lunch@xxx.com"

#mail messages
message = """
吃货们：

        经组织研究决定，目标%s , 收拾一下，准备出发。
            
                          --sent by xxx美食研究组

        下面是来自世界末日组的统计信息：
"""
##########deafault config##########

def send_mail(to_list, sub, context):
    msg = MIMEText(context)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        ss = smtplib.SMTP()
        ss.connect(mail_host)
        #our smtp server doesn't need user passwd 
        #so we doesn't use ss.login()
        #ss.login(user, password)
        ss.sendmail(me, to_list, msg.as_string())
        ss.close()
        return True
    except (Exception, e):
        print(str(e))

if __name__ == '__main__':
    ff =  open('./.food.log', 'a')
    with open('./.food.log', 'r') as rf:
        lines = rf.readlines()
        if lines:
            lastfood = lines[-1].split(' ')[1].rstrip()
        else:
            lastfood = "blah"
        print lastfood

    choice = MENU[random.randrange(0, len(MENU))]
    while choice == lastfood:
        choice = MENU[random.randrange(0, len(MENU))]
    
    mail_body = message % choice + count.countfood()



    send_mail(mailto_list, "go for lunch", mail_body)
    
    nowtime = time.strftime('%Y-%m-%d', time.gmtime(time.time()))
    ff.write(nowtime + " " + choice + '\n')
    ff.close()
