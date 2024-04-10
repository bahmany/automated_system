from datetime import datetime

from django.utils import timezone
from mongoengine import *

# Moeen Store
from rest_framework.fields import CharField


class MaterialLocations(Document):
    name = StringField(unique=True)
    x = IntField(default=0)
    y = IntField(default=0)
    z = IntField(default=0)
    desc = DictField(default={})


class Barcodes(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    locationLink = ReferenceField(MaterialLocations)
    barcode = StringField(max_length=40, unique=True, null=False, required=True)
    barcodePositionID = IntField(null=True, required=False)
    x = IntField(default=0)
    y = IntField(default=0)
    z = IntField(default=0)
    """
    
    87976544 = با موفقیت در انبار نشست
    6656336 = m مصرف شد
    6322344 = deleted
    8845344 = has_qc_claim کیفیت نظر دارد ولی در محل مورد نظر هم نشسته است
    7463333 = has_qc_claim_and_another_place کیفیت نظر دارد و به محل دیگری منتقل کرده است
    6879789 = converted to scrap
    4854746 = it مقداری تولید شده و مقداری نیز مانده است
    
    """
    position = IntField()
    mizaneMasraf = IntField()
    confirmLocation = BooleanField(default=False)
    confirmTime = DateTimeField(null=True, required=False)
    confirmPositionID = IntField(null=True, required=False)
    desc = DictField(default={})
    hamkaranSanad = IntField(null=True, required=False)


class MaterialHamkaranTafzil(Document):
    Char3PartCode = StringField(max_length=1, unique=False, null=False, required=True)
    HamkaranSystemTitle = StringField(max_length=100, unique=False, null=False, required=True)
    SherkateVaset = StringField(max_length=100, unique=False, null=False, required=True)
    CodeSherkateVaset = StringField(max_length=6, unique=False, null=False, required=True)


class MaterialConvSale(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField(required=True)
    desc = DictField(default={})


class MaterialTolidOrder(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    forDate = DateTimeField(default=datetime.now())  # تعیین زمان تولید
    positionID = IntField(required=True)
    desc = DictField(default={})


class MaterialTolidOrderItems(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField(required=True)
    linkMaterialTolid = ReferenceField(MaterialTolidOrder)
    linkBarcode = ReferenceField(Barcodes)
    mizaneMasraf = IntField()
    desc = DictField(default={})
