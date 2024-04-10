import string


def isEnglishSimpleText(s):
    for i in s:
        res = string.ascii_letters.find(i)
        if res == -1:
            return False
        res = string.digits.find(i)
        if res == -1:
            return False
    return True


def isEnglishUsername(s):
    if string.digits.find(s[0]) != -1:
        return False
    if string.punctuation.find(s[0]) != -1:
        return False
    for i in s:
        res = (string.ascii_letters+string.digits).find(i)
        if res == -1:
            return False
    return True

def isEnglishPassword(s):
    for i in s:
        res = string.printable.find(i)
        if res == -1:
            return False
    return True

