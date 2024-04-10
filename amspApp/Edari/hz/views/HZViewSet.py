import base64
import hashlib
import http.client
from time import sleep
from urllib.parse import urlencode

import bs4
from asq.initiators import query
from django.http import HttpResponse
from httplib2 import Http
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi, getCurrentMonthShamsi


class HZViewSet(viewsets.ModelViewSet):
    # lookup_field = 'id'
    # queryset = MaterialConvSale.objects.all().order_by('-id')
    # serializer_class = MaterialConvSaleSerializer
    #
    # pagination_class = DetailsPagination
    hz_host = "172.16.5.20"
    hz_port = 8091
    hz_login = "/Account/Login"

    def makeheader(self):
        conn = http.client.HTTPConnection(host=self.hz_host, port=self.hz_port)
        conn.request(method="GET", url="/Account/Login", headers={})
        res = conn.getresponse()
        headers = res.getheaders()
        setCookies = query(headers).where(lambda x: x[0] == 'Set-Cookie').to_list()
        requestHeader = query(setCookies).select(lambda x: {x[1].split("=")[0]: x[1].split("=")[1]}).to_list()

        newHeader = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'ASP.NET_SessionId=' + requestHeader[0]['ASP.NET_SessionId'] + '; __RequestVerificationToken=' +
                      requestHeader[2]['__RequestVerificationToken'],
            'Host': self.hz_host + ':' + str(self.hz_port),
            'Origin': 'http://' + self.hz_host + ':' + str(self.hz_port),
            'Referer': 'http://' + self.hz_host + ':' + str(self.hz_port) + self.hz_login,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        }
        htmlcontent = res.read()
        content = bs4.BeautifulSoup(htmlcontent, 'html.parser')
        hash = hashlib.sha512(str('****').encode("utf-8")).hexdigest()
        newForm = {
            '__RequestVerificationToken': content.find("input", attrs={'name': '__RequestVerificationToken'}).attrs[
                'value'],
            'Username': 'AutomationLink',
            'PasswordHash': hash,
            'Password': '****',
            # 'Username': 'Admin',
            # 'Password': '****',
        }

        h = Http()
        resp, content = h.request("http://" + self.hz_host + ":" + str(self.hz_port) + self.hz_login, "POST",
                                  urlencode(newForm),
                                  headers=newHeader)

        WKF = query(resp['set-cookie'].split(';')).where(lambda x: x.find('WKF') != -1).first()
        ASPXAUTH = query(resp['set-cookie'].split(';')).where(lambda x: x.find('ASPXAUTH') != -1).first()
        ASPXAUTH = query(ASPXAUTH.split(' ')).where(lambda x: x.find('ASPXAUTH') != -1).first()

        newHeader = {
            '__RequestVerificationToken': newForm['__RequestVerificationToken'],
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': self.hz_host + ":" + str(self.hz_port),
            'Origin': 'http://' + self.hz_host + ':8091',
            # 'Referer': 'http://172.16.1.33:8091/Tradod/Index/' + request.user.personnel_code + '?y=' + year + '&m=' + month + '&st=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        newHeader['Cookie'] = \
            'ASP.NET_SessionId=' + requestHeader[0][
                'ASP.NET_SessionId'] + '; ' + WKF + '; ' + ASPXAUTH + ';__RequestVerificationToken=' + requestHeader[2][
                '__RequestVerificationToken']
        newHeader['Content-Type'] = 'application/json; charset=UTF-8'

        return newHeader

    @list_route(methods=['post'])
    def getTaradod(self, request, *args, **kwargs):
        if request.user.personnel_code == '0':
            return Response()

        year = request.data['year']
        month = request.data['month']
        if year == 0:
            year = getCurrentYearShamsi()
        if month == 0:
            month = getCurrentMonthShamsi()
        year = str(year)
        month = str(month)

        # req = {
        #     'id': request.user.personnel_code,
        #     'm': 6,
        #     'st': 0,
        #     'y': 1399,
        # }

        if request.user.personnel_code is None:
            raise APIException('کد پرسنلی هنوز وارد نشده')

        if request.user.personnel_code == "0" or request.user.personnel_code == "":
            raise APIException('کد پرسنلی هنوز وارد نشده')

        import os
        newHeader = self.makeheader()

        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=chrome-data")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        if os.name == 'nt':
            browser = webdriver.Chrome(executable_path='C:/chromedriver_win32/chromedriver.exe',
                                       chrome_options=chrome_options)
            # browser = webdriver.Firefox(executable_path='C:/geckodriver-v0.27.0-win64/geckodriver.exe')
        else:
            browser = webdriver.Chrome(executable_path='/home/mohammad/chromedriver', chrome_options=chrome_options)

        browser.set_window_size(1400, 1900)

        def getCookieStr(headerStr, cookieName):
            q = query(headerStr.split(";")).where(lambda x: x.find(cookieName) != -1).first()
            return {

                'name': cookieName,
                'value': q.split("=")[1],
                "domain": "",  # google chrome
                "expires": "",
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }

        browser.get("http://" + self.hz_host + ":8091/")
        browser.add_cookie(getCookieStr(newHeader['Cookie'], 'ASP.NET_SessionId'))
        browser.add_cookie(getCookieStr(newHeader['Cookie'], 'WKF'))
        browser.add_cookie(getCookieStr(newHeader['Cookie'], '.ASPXAUTH'))
        browser.add_cookie(getCookieStr(newHeader['Cookie'], '__RequestVerificationToken'))

        browser.get(
            "http://" + self.hz_host + ":8091/Tradod/Index/" + request.user.personnel_code + '?y=' + year + '&m=' + month + '&st=0')
        browser.find_elements_by_css_selector('[ng-click="ShowKarkardReportButtonOnClick()"]')[0].click()
        sleep(4)

        bbb = b'data:image/png;base64,' + base64.b64encode(browser.get_screenshot_as_png())
        browser.close()
        return HttpResponse(bbb)

        # nav = browser.find_element_by_id("mainnav")
        #
        # print(nav.text)
        #
        # r = requests.post(
        #     url="http://172.16.1.33:8091/Tradod/GetTradodData",
        #     data=json.dumps(req),
        #     headers=newHeader)
        # return Response(json.loads(r.content))
