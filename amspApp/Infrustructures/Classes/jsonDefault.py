import base64
import calendar
import re

import decimal
from bson import ObjectId, DBRef, RE_TYPE, Regex, SON, MinKey, MaxKey, Timestamp, Code, Binary,  PY3
import bson
from bson.json_util import _json_convert
import datetime

from pymongo.command_cursor import CommandCursor
from six import binary_type


def defaultMorabaa(obj):

    # We preserve key order when rendering SON, DBRef, etc. as JSON by
    # returning a SON for those types instead of a dict. This works with
    # the "json" standard library in Python 2.6+ and with simplejson
    # 2.1.0+ in Python 2.5+, because those libraries iterate the SON
    # using PyIter_Next. Python 2.4 must use simplejson 2.0.9 or older,
    # and those versions of simplejson use the lower-level PyDict_Next,
    # which bypasses SON's order-preserving iteration, so we lose key
    # order in Python 2.4.
    if isinstance(obj, ObjectId):
        return  str(obj)
    if isinstance(obj, decimal.Decimal):
        return  float(obj)
    if isinstance(obj, DBRef):
        return _json_convert(obj.as_doc())
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y/%m/%d %H:%M:%S")
        # TODO share this code w/ bson.py?

        # if obj.utcoffset() is not None:
        #     obj = obj - obj.utcoffset()
        # millis = int(calendar.timegm(obj.timetuple()) * 1000 +
        #              obj.microsecond / 1000)
        # return {"$date": millis}
    if isinstance(obj, (RE_TYPE, Regex)):
        flags = ""
        if obj.flags & re.IGNORECASE:
            flags += "i"
        if obj.flags & re.LOCALE:
            flags += "l"
        if obj.flags & re.MULTILINE:
            flags += "m"
        if obj.flags & re.DOTALL:
            flags += "s"
        if obj.flags & re.UNICODE:
            flags += "u"
        if obj.flags & re.VERBOSE:
            flags += "x"
        if isinstance(obj.pattern, str):
            pattern = obj.pattern
        else:
            pattern = obj.pattern.decode('utf-8')
        return SON([("$regex", pattern), ("$options", flags)])
    if isinstance(obj, MinKey):
        return {"$minKey": 1}
    if isinstance(obj, MaxKey):
        return {"$maxKey": 1}
    if isinstance(obj, Timestamp):
        return {"$timestamp": SON([("t", obj.time), ("i", obj.inc)])}
    if isinstance(obj, Code):
        return SON([('$code', str(obj)), ('$scope', obj.scope)])
    if isinstance(obj, CommandCursor):
        return list(obj)

    if isinstance(obj, Binary):
        return SON([
            ('$binary', base64.b64encode(obj).decode()),
            ('$type', "%02x" % obj.subtype)])
    if PY3 and isinstance(obj, binary_type):
        return SON([
            ('$binary', base64.b64encode(obj).decode()),
            ('$type', "00")])
    if bson.has_uuid() and isinstance(obj, bson.uuid.UUID):
        return {"$uuid": obj.hex}

    raise TypeError("%r is not JSON serializable" % obj)
