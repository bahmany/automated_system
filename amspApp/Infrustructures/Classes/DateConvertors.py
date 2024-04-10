# coding=utf-8
import re
from datetime import datetime, timedelta

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.core.cache import cache
import pytz
from amspApp.Infrustructures.Classes.date_utils import calendar_util
from amspApp._Share import num2words
from amspApp.amspUser.models import MyUser
from amspApp._Share.num2words import fa

months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']





def convertToZone(userInstance, datetime, resultWithTime=False):
    currentUserTimeZone = userInstance.timezone
    pass


def parseZoneAwareDateStr(milDateStr):
    return parse(milDateStr)


def CheckShamsiDateValidationInRequestAndConvert(request, datename, fieldStrName, errorMessage):
    if datename in request.data:
        if request.data[datename] != "":
            if request.data[datename] != None:
                if not is_valid_shamsi_date(request.data[datename], False, True):
                    return {"result": False, "fieldStrName": fieldStrName, "errorMessage": errorMessage}

                RESUTL = convertZoneToMilday(request.user.id, request.data[datename])
                return {"result": True, "fieldStrName": fieldStrName, "errorMessage": None, "converted": str(RESUTL)}
            else:
                return {"result": True, "fieldStrName": fieldStrName, "errorMessage": None, "converted": None}
        else:
            return {"result": True, "fieldStrName": fieldStrName, "errorMessage": None, "converted": None}
    else:
        return {"result": True, "fieldStrName": fieldStrName, "errorMessage": None, "converted": None}


def changeDateNameToShamsiDate(d):
    if d == "Saturday":
        return "شنبه"
    if d == "Sunday":
        return "یکشنبه"
    if d == "Monday":
        return "دوشنبه"
    if d == "Tuesday":
        return "سه شنبه"
    if d == "Wednesday":
        return "چهارشنبه"
    if d == "Thursday":
        return "پنجشنبه"
    if d == "Friday":
        return "جمعه"
    return None


def convertZoneToMilday(userID, convDate, spliter="/"):
    cacheName = "user_" + str(userID)
    userInstance = cache.get(cacheName)

    if userInstance == None:
        userInstance = MyUser.objects.get(id=userID)
        cache.set(cacheName, userInstance, 120)
    userInstance = cache.get(cacheName)

    if convDate == "":
        return datetime.now()
    if convDate == None:
        return None

    timeZone = userInstance.timezone
    if timeZone == "Asia/Tehran":
        return convertTimeZoneToUTC(timeZone, convDate)
    else:
        return convDate


def mil_to_sh_with_time(mildate, splitter="-", returnSecond=True):
    # dd = datetime.strptime(mildate)

    if type(mildate) is datetime:
        mildate = mildate.strftime("%Y/%m/%d %H:%M:%S")

    if mildate == None:
        return ""
    if len(mildate.split("-")) <= 1:
        splitter = "/"
    if len(mildate.split("/")) <= 1:
        splitter = "-"

    # mildate = mildate.__str__()
    splittter = " "
    if len(mildate.split("T")) > 1:
        splittter = "T"

    m = calendar_util.jd_to_persian(
        calendar_util.gregorian_to_jd(
            int(mildate.split(" ")[0].split(splitter)[0]),
            int(mildate.split(" ")[0].split(splitter)[1]),
            int(mildate.split(" ")[0].split(splitter)[2].split(splittter)[0])
        ))
    splittter = " "

    if len(mildate.split("T")) > 1:
        splittter = "T"

    m_0 = str(m[0])
    m_1 = str(m[1])
    m_2 = str(m[2])
    if len(m_1) == 1:
        m_1 = "0" + m_1
    if len(m_2) == 1:
        m_2 = "0" + m_2

    dt = m_0 + "/" + m_1 + "/" + m_2 + " " + mildate.split(splittter)[1]
    dt = dt.split(".")[0]
    return dt


def mil_to_sh(mildate, splitter="-"):
    if type(mildate) is datetime:
        mildate = mildate.strftime("%Y/%m/%d")

    if mildate == None:
        return ""
    if len(mildate.split("-")) <= 1:
        splitter = "/"
    if len(mildate.split("/")) <= 1:
        splitter = "-"

    # dd = datetime.strptime(mildate)
    # print mildate.split(" ")[0]
    # mildate = mildate.__str__()

    if mildate == None:
        return ""

    m = calendar_util.jd_to_persian(
        calendar_util.gregorian_to_jd(
            int(mildate.split(" ")[0].split(splitter)[0]),
            int(mildate.split(" ")[0].split(splitter)[1]),
            int(mildate.split(" ")[0].split(splitter)[2].split("T")[0])
        ))
    year = m[0].__str__()
    month = m[1].__str__()
    day = m[2].__str__()

    if len(month) == 1: month = "0" + month
    if len(day) == 1: day = "0" + day
    dt = year + "/" + month + "/" + day
    return dt


def is_valid_shamsi_date(ShamsiDate, isNullReturnTrue=False, isItContainTime=False):
    if isNullReturnTrue == True:
        if ShamsiDate == "":
            return True
    try:
        _time = ""
        if isItContainTime:
            _time = ShamsiDate.split(" ")[1]
            ShamsiDate = ShamsiDate.split(" ")[0]

        # dd = datetime.strptime(mildate)
        y = int(ShamsiDate.split("/")[0])
        m = int(ShamsiDate.split("/")[1])
        d = int(ShamsiDate.split("/")[2])
        if y > 1500: return False
        if m > 12: return False
        if d > 31: return False
        if isItContainTime:
            hh = int(_time.split(":")[0])
            mm = int(_time.split(":")[1])
            if hh > 24: return False
            if mm > 59: return False

        m = calendar_util.jd_to_gregorian(
            calendar_util.persian_to_jd(y, m, d))
        dt = m[0].__str__() + "/" + m[1].__str__() + "/" + m[2].__str__()
        return True
    except Exception as inst:
        return False





def sh_to_mil(mildate, has_time=False, ResultSplitter="/", returnSecond=True):
    # dd = datetime.strptime(mildate)
    if len(mildate) == 6:
        mildate = "13" + mildate[0:2] + "/" + mildate[2:4] + "/" + mildate[4:6]

    if mildate == "":
        return ""
    if not mildate:
        return ""
    _time = ""
    __dt = ""
    if has_time:
        m = mildate.split(" ")
        mildate = m[0]
        if len(m) == 1:
            _time = " " + datetime.now().strftime("%H:%m")
        else:
            _time = " " + m[1]
    m = calendar_util.jd_to_gregorian(
        calendar_util.persian_to_jd(
            int(mildate.split(ResultSplitter)[0]),
            int(mildate.split(ResultSplitter)[1]),
            int(mildate.split(ResultSplitter)[2])
        ))

    __dt = m[0].__str__() + ResultSplitter + m[1].__str__() + ResultSplitter + m[2].__str__()

    if returnSecond == False:
        if len(_time.split(":")) == 3:
            _time = _time.split(":")
            _time = _time[0] + ":" + _time[1]

    __dt += _time if has_time else ""

    return __dt


days_of_month = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 30],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 30],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 30],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 30],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 30],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 30],
]


def getCurrentYearShamsi():
    current = datetime.now()
    return mil_to_sh(current).split("/")[0]


def getMonthDays(month):
    if int(month) >= 6:
        return '31'
    else:
        return '30'


def getCurrentMonthShamsi():
    current = datetime.now()
    return mil_to_sh(current).split("/")[1]


def getCurrentDayShamsi():
    current = datetime.now()
    return mil_to_sh(current).split("/")[2]


def getCurrentYearShamsi2digit():
    current = datetime.now()
    return mil_to_sh(current).split("/")[0][2:4]


def PrettyDayShow(dateStr):

    if type(datetime.now()) != type(dateStr):
        date = datetime.strptime(dateStr, "%Y/%m/%d %H:%M")
    date = dateStr
    now = datetime.now()
    dif = now - date
    if dif.days == 0:
        return "امروز"
    if dif.days <= 4:
        return str(dif.days) + " روز پیش"
    return mil_to_sh(dateStr, "/")


def convertJerkStrDateTime(jerkDate):
    return "13" + jerkDate[:2] + "/" + jerkDate[2:4] + "/" + jerkDate[4:6] + " " + jerkDate[6:8] + ":" + jerkDate[8:10]


def convertTimeZoneToUTC(timezoneTitle, strShmasiDate):
    enrtyDate = sh_to_mil(strShmasiDate, has_time=True).replace(' ', 'T').replace('/', '-')
    settingstime_zone = pytz.timezone(timezoneTitle)
    enrtyDate = settingstime_zone.localize(datetime.strptime(enrtyDate, "%Y-%m-%dT%H:%M")).astimezone(
        pytz.utc).strftime('%Y-%m-%dT%H:%M')
    return enrtyDate


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    monday = datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w")
    return monday, monday + timedelta(days=6.9)


def get_date_str(__date):
    dayname = __date.strftime("%A")
    currenttime_sh = mil_to_sh(__date)
    monthnum = currenttime_sh.split("/")[1]
    monthnum = months[int(monthnum) - 1]
    dayname = changeDateNameToShamsiDate(dayname)
    return {
        'dayname': dayname,
        'daynumber': int(currenttime_sh.split("/")[2]),
        'monthname': monthnum,
        'yearname': fa.convert(int(currenttime_sh.split("/")[0])),
        'dayword': fa.convert(int(currenttime_sh.split("/")[2]))
    }
def get_today_str():
    currenttime = datetime.now()
    dayname = datetime.now().strftime("%A")
    currenttime_sh = mil_to_sh(currenttime)
    monthnum = currenttime_sh.split("/")[1]
    monthnum = months[int(monthnum) - 1]
    dayname = changeDateNameToShamsiDate(dayname)
    return {
        'dayname': dayname,
        'daynumber': int(currenttime_sh.split("/")[2]),
        'monthname': monthnum,
        'yearname': fa.convert(int(currenttime_sh.split("/")[0])),
        'dayword': fa.convert(int(currenttime_sh.split("/")[2]))
    }


def get_filter_times():
    currenttime = datetime.now()
    last_1_hour_time = currenttime - timedelta(hours=1)
    last_2_hour_time = currenttime - timedelta(hours=3)
    last_3_hour_time = currenttime - timedelta(hours=5)
    start_of_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=1)
    end_of_today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=9)
    start_of_yesterday = (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=1)
    end_of_yesterday = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=9)
    current_week_number = datetime.now().strftime("%V")
    if datetime.now().strftime("%A") == 'Saturday':
        current_week_number = str(int(current_week_number) + 1)
    current_year = datetime.now().year
    current_week_start, current_week_end = get_start_and_end_date_from_calendar_week(current_year, current_week_number)
    current_week_start = current_week_start.replace(hour=0, minute=0, second=0, microsecond=1)
    current_week_start = current_week_start - timedelta(days=2)
    current_week_end = current_week_end.replace(hour=23, minute=59, second=59, microsecond=999)
    current_week_end = current_week_end - timedelta(days=2)

    current_week_number = str(int(datetime.now().strftime("%V")) - 1)
    if datetime.now().strftime("%A") == 'Saturday':
        current_week_number = str(int(current_week_number) + 1)
    current_year = datetime.now().year
    _from, _to = get_start_and_end_date_from_calendar_week(current_year, current_week_number)
    _from = _from.replace(hour=0, minute=0, second=0, microsecond=1)
    _from = _from - timedelta(days=2)
    _to = _to.replace(hour=23, minute=59, second=59, microsecond=999)
    _to = _to - timedelta(days=2)
    previous_week_start = _from
    previous_week_end = _to

    _from = datetime.strptime(
        sh_to_mil("{}/{}/{}".format(getCurrentYearShamsi(), getCurrentMonthShamsi(), "01")) + " 00:00:00",
        "%Y/%m/%d %H:%M:%S")
    _to = datetime.strptime(
        sh_to_mil("{}/{}/{}".format(
            getCurrentYearShamsi(),
            getCurrentMonthShamsi(),
            str(getMonthDays(getCurrentMonthShamsi()))
        )) + " 23:59:59",
        "%Y/%m/%d %H:%M:%S")
    start_date_of_current_month = _from
    end_date_of_current_month = _to - timedelta(days=1)

    cc = int(getCurrentMonthShamsi()) - 1
    from_month = str(cc) if cc != 1 else "12"
    from_year = getCurrentYearShamsi() if cc != 1 else str(int(getCurrentYearShamsi()) - 1)

    _from = datetime.strptime(
        sh_to_mil("{}/{}/{}".format(from_year, from_month, "01")) + " 00:00:00",
        "%Y/%m/%d %H:%M:%S")

    _to = datetime.strptime(
        sh_to_mil(
            "{}/{}/{}".format(from_year, from_month, str(getMonthDays(getCurrentMonthShamsi())))) + " 23:59:59",
        "%Y/%m/%d %H:%M:%S")
    start_date_of_previous_month = _from
    end_date_of_previous = _to

    startdate = getCurrentYearShamsi()
    enddate = getCurrentYearShamsi()
    start_date_of_current_year = datetime.strptime(sh_to_mil(startdate + '/1/1') + ' 00:00:01', "%Y/%m/%d %H:%M:%S")
    end_date_of_current_year = datetime.strptime(sh_to_mil(enddate + "/12/29") + " 23:59:59", "%Y/%m/%d %H:%M:%S")

    startdate = str(int(getCurrentYearShamsi()) - 1)
    enddate = str(int(getCurrentYearShamsi()) - 1)
    end_date_of_previous_year = datetime.strptime(sh_to_mil(enddate + "/12/29") + " 23:59:59", "%Y/%m/%d %H:%M:%S")
    start_date_of_previous_year = datetime.strptime(sh_to_mil(startdate + '/1/1') + ' 00:00:01', "%Y/%m/%d %H:%M:%S")

    dt = dict(
        currenttime=currenttime,
        last_1_hour_time=last_1_hour_time,
        last_2_hour_time=last_2_hour_time,
        last_3_hour_time=last_3_hour_time,
        start_of_today=start_of_today,
        end_of_today=end_of_today,
        start_of_yesterday=start_of_yesterday,
        end_of_yesterday=end_of_yesterday,
        current_week_number=int(current_week_number),
        current_year=current_year,
        current_week_start=current_week_start,
        current_week_end=current_week_end,
        previous_week_start=previous_week_start,
        previous_week_end=previous_week_end,
        start_date_of_current_month=start_date_of_current_month,
        end_date_of_current_month=end_date_of_current_month,
        start_previous_month=start_date_of_previous_month,
        end_previous_month=end_date_of_previous,
        start_date_of_current_year=start_date_of_current_year,
        end_date_of_current_year=end_date_of_current_year,
        start_date_of_previous_year=start_date_of_previous_year,
        end_date_of_previous_year=end_date_of_previous_year,
    )

    dt['loop'] = [
        ['یک ساعت پیش', dt['last_1_hour_time'], dt['currenttime']],
        ['دو ساعت پیش', dt['last_2_hour_time'], dt['currenttime']],
        ['سه ساعت پیش', dt['last_3_hour_time'], dt['currenttime']],
        ['امروز', dt['start_of_today'], dt['end_of_today']],
        ['دیروز', dt['start_of_yesterday'], dt['end_of_yesterday']],
        ['این هفته', dt['current_week_start'], dt['current_week_end']],
        ['هفته پیش', dt['previous_week_start'], dt['previous_week_end']],
        ['این ماه', dt['start_date_of_current_month'], dt['end_date_of_current_month']],
        ['ماه پیش', dt['start_previous_month'], dt['end_previous_month']],
        ['امسال', dt['start_date_of_current_year'], dt['end_date_of_current_year']],
        ['سال پیش', dt['start_date_of_previous_year'], dt['end_date_of_previous_year']],
    ]
    return dt
