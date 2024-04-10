from datetime import datetime
from mongoengine import *


#
# class ProfileDetailsField(EmbeddedDocument):
#     AboutMe=StringField(max_length=200)
#     Name
#     Phones
#     Title
#     profileAvatar
#     profileHeaderBackground
#     friends


class Notifications(Document):
    """
    type:
        1 = when someone send letter and it is unread after two min
        2 = it means you have new job in your bpms inbox
        3 = it means you have new job in your bpms message





        4 = it وقتی از باسکول به انبار رفته و از ابنرا پیاده می شود
        5 = it وقتی از باسکول به انبار می رسد و مشکل دارد ولی در محل مورد نظر قرار میگیرد
        6 = it وقای ار باسکول به محل می رود و مشل دارد و کنترل کیفیت آنرا به محل دیگری منتقل می کند
        7 = it یباسکول بادکد جدیدی ایجاد کرده است


        87976544 = it وقتی از باسکول به انبار رفته و از ابنرا پیاده می شود
        8845344 = it وقتی از باسکول به انبار می رسد و مشکل دارد ولی در محل مورد نظر قرار میگیرد
        7463333 = it وقای ار باسکول به محل می رود و مشل دارد و کنترل کیفیت آنرا به محل دیگری منتقل می کند
        6431684864 = it یباسکول بادکد جدیدی ایجاد کرده است

546345=درخواست مرخصی برای مدیر واحد پیام ارسال می شود
798448=درخواست مرخضی ساعتی مورد تایید مدیر قرار گرفت و پیام برای متقاضی و مدیر و مسئول ادرای ارسال می شود
849811 = برای متقاضی رد درخواست ارسال می شود


    """
    type = IntField()
    """
     typeOfAlarm:
        1 = notification buttons at top
        2= 1 and email
        3= 1 and sms
        4= exit sign

    """
    typeOfAlarm = IntField()

    """
    priority:
    1= normal
    2= high
    3= very high
    """
    priority = IntField(default=1)
    """
    informType:
    1= information
    2= alarm
    3= error
    4= police alarm
    5= warning

    """
    informType = IntField(default=1)
    userID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
    extra = DictField()


class HasNotifications(Document):
    userID = IntField()
    sessionID = StringField()
    has = BooleanField(default=False)
    dateOfPost = DateTimeField(default=datetime.now())
    desc = DictField()


class GoogleToken(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    userID = IntField()
    token = StringField()


class SimpleNotificatoin(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    chartID = IntField()
    read = BooleanField()
    exp = DictField()




# class GotifyUsers(Document):
#     dateOfPost = DateTimeField(default=datetime.now())
#     userID = IntField(unique=True)
#     applicationToken = StringField(unique=True)
#     clientToken = StringField(unique=True)
