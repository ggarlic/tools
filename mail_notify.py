#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pyinotify
import mailbox
import pynotify
import os
import gtk
import re
from email.header import decode_header
from os.path import expanduser


MAILBOX = ["~/.mail/gmail/inbox", "~/.mail/work/inbox"] #mailboxes
MASK = pyinotify.IN_MOVED_TO #event to trigger
SOUND = "~/.mybashscripts/mail.wav" #notification sound


def parse_encoding(value):
    _r = []
    #"=?utf-8?B?eWFuZ2JvLCDmnajljZo=?=" <yangbo#xxx.com>
    #WTF, From section in qq enterprise mailbox has a pair quotes around name
    value = re.sub('"(.*?)"', r'\1', value)

    for msg, enc in decode_header(value):        
        if enc == 'gb2312' or not enc:
            _r.append((msg, 'gb18030'))
        else:
            _r.append((msg, enc))
        
    return ' '.join(item[0].decode(item[1]) for item in _r)

def get_mbox_name(path):
    #path's pattern: /home/ggarlic/.mail/gmail/inbox/new
    mailbox_name = path.split("/")[-3]
    return '[' + mailbox_name + ']'

def parse_mail(event):
    with open(event.pathname, "r") as f:
        msg = mailbox.MaildirMessage(f)
        msg_from = parse_encoding(msg["From"])
        msg_subject = parse_encoding(msg["subject"])

        #todo: markup and multiline
        notifier = pynotify.Notification(get_mbox_name(event.path)+msg_from,
                                         msg_subject)
        notifier.set_icon_from_pixbuf(gtk.Label()
                                         .render_icon(gtk.STOCK_DIALOG_INFO,
                                                      gtk.ICON_SIZE_DIALOG))
        os.system("aplay -q " + SOUND)
    notifier.show()

wm = pyinotify.WatchManager()
pynotify.init("mail notifier")
notifier = pyinotify.Notifier(wm, parse_mail)

for mbox in MAILBOX:
    wm.add_watch(expanduser(mbox)+"/new", MASK)

notifier.loop()
