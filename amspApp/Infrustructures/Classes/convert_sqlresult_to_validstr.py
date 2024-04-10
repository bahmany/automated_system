import codecs, sys
from decimal import Decimal

newmap = {}
newmap[129] = "پ"
newmap[141] = "چ"
newmap[142] = "ژ"
newmap[144] = "گ"
newmap[152] = "ک"
newmap[194] = "آ"
newmap[198] = "ئ"
newmap[199] = "ا"
newmap[200] = "ب"
newmap[201] = "پ"
newmap[202] = "ت"
newmap[203] = "ث"
newmap[204] = "ج"
newmap[205] = "ح"
newmap[206] = "خ"
newmap[207] = "د"
newmap[208] = "ذ"
newmap[209] = "ر"
newmap[210] = "ز"
newmap[211] = "س"
newmap[212] = "ش"
newmap[213] = "ص"
newmap[214] = "ض"
newmap[216] = "ط"
newmap[217] = "ظ"
newmap[218] = "ع"
newmap[219] = "غ"
newmap[221] = "ف"
newmap[222] = "ق"
newmap[225] = "ل"
newmap[227] = "م"
newmap[228] = "ن"
newmap[229] = "ه"
newmap[230] = "و"
newmap[237] = "ی"


def convert_sqlresultstr_to_valid_str(resultdict):
    for r in resultdict:
        for k in r.keys():
            if type(r[k]) == str:
                newc = ""
                for c in r[k]:
                    newc = newc + newmap.get(ord(c), c)

                r[k] = newc
    return resultdict


def convert_sqlresultstr_to_valid_numbers(resultdict):
    for r in resultdict:
        for k in r.keys():
            if type(r[k]) == Decimal:
                r[k] = int(r[k])
    return resultdict

