# -*- coding: utf-8 -*-
import copy
import http
import logging
import re
import wsgiref
from http.cookiejar import CookieJar, Cookie
from json import JSONEncoder
from urllib.request import build_opener, HTTPCookieProcessor

import requests
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import QueryDict
from django.utils.http import urlencode
from django.utils.six.moves import urllib
from httpproxy.views import HttpProxy

from amsp import settings
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset

logger = logging.getLogger(__name__)

REWRITE_REGEX = re.compile(r'((?:src|action|href)=["\'])/(?!\/)')


class myProxyView(HttpProxy):
    """
    # here we must check if there is no registered user , activiti
    # must register the user and add enough data to header and cookies

    security reasons
    1 :
    activiti has remember me cookie
    each time i want to create user i must get
    administrator remember key cookies to create new user

    2 :
    headers can not be completely

    """


    def checkUsername(self, username , password):
        s = requests.session()
        cj = CookieJar()
        ck = requests.cookies.RequestsCookieJar()
        for kv in list(self.request.COOKIES.keys()):
            ck.set(kv, self.request.COOKIES[kv])
        ck.set("authenticatedUser", None)
        s.cookies = ck
        s.get(settings.ACTIVITI_HTTP_REFERER)

        result = s.post(settings.ACTIVITI_AUTH_URL,
                        data={"j_username": username,
                              "j_password": password,
                              "_spring_security_remember_me": True,
                              "submit": "Login"}
                        )

        return result

    """
    this method creates user if does not exists
    user formula :
    username : domainID_companyID_chartID_positionID@rahsoon.com
    password : chartID__pa^yh@@ss__positionID

    """
    def create_user(self ):
        # generating username to login activiti
        currentPositionID = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        currentCompanyID = self.request.user.current_company_id
        currentSubDomainID = self.request.subdomain.id
        currentChartID = currentPositionID.chartID
        currentPosition = currentPositionID.positionID
        activiti_username = "rahsoon_"+str(currentSubDomainID)+"_"+str(currentCompanyID)+"_"+str(currentChartID)+"_"+str(currentPosition)+"@rahsoon.com"
        activiti_password = str(currentChartID)+"__pa^yh@@ss__"+str(currentPosition)
        # -------------------------------------------
        # check activiti login and getting remember me keys
        result = self.checkUsername(activiti_username, activiti_password)
        # checking for creating user
        if result.status_code == 401 :
            pass
        # -------------------------------------------



        self = self



    """
    this method creates user with admin login remember key
    95/12/23
    """
    def getAdminRemeberMeKey(self):
        s = requests.session()
        cj = CookieJar()
        ck = requests.cookies.RequestsCookieJar()
        for kv in list(self.request.COOKIES.keys()):
            ck.set(kv, self.request.COOKIES[kv])
        ck.set("authenticatedUser", None)
        s.cookies = ck
        s.get(settings.ODOO_Platform)

        # result = s.post(settings.ACTIVITI_AUTH_URL,
        #                 data={"j_username": "admin@app.activiti.com",
        #                       "j_password": "admin",
        #                       "_spring_security_remember_me": True,
        #                       "submit": "Login"}
        #                 )

        return ""

    def get_myRequest(self, headers):
        s = requests.session()
        cj = CookieJar()
        ck = requests.cookies.RequestsCookieJar()
        for kv in list(self.request.COOKIES.keys()):
            ck.set(kv, self.request.COOKIES[kv])
        ck.set("authenticatedUser", None)
        s.cookies = ck
        s.get(settings.ACTIVITI_HTTP_REFERER)

        result = s.post(settings.ACTIVITI_AUTH_URL,
                        data={"j_username": "admin@app.activiti.com",
                              "j_password": "admin",
                              "_spring_security_remember_me": True,
                              "submit": "Login"}
                        )
        self.create_user()

        return result

    def dispatch(self, request, url, *args, **kwargs):
        # print("---------------------- replied ------------------------")
        request.META["HTTP_HOST"] = settings.ODOO_HTTP_HOST
        request.META["HTTP_REFERER"] = settings.ODOO_HTTP_REFERER
        # request.META["SERVER_PORT"] = settings.ACTIVITI_SERVER_PORT
        # request.META["SERVER_ORIGIN"] = settings.ACTIVITI_SERVER_ORIGIN
        self.url = url
        self.original_request_path = request.path
        request = self.normalize_request(request)
        if self.mode == 'play':
            response = self.play(request)
            # TODO: avoid repetition, flow of logic could be improved
            if self.rewrite:
                response = self.rewrite_response(request, response)
            return response
        # clearing rahsoon cookies :
        # if "rahsoon-CSRF-TOKEN" in request.COOKIES: del request.COOKIES["rahsoon-CSRF-TOKEN"]
        # if "sessionid" in request.COOKIES: del request.COOKIES["rahsoon-CSRF-TOKEN"]

        # dropping unused cookies !
        if "rahsoon-CSRF-TOKEN" in request.COOKIES: del request.COOKIES["rahsoon-CSRF-TOKEN"]
        if "sessionid" in request.COOKIES: del request.COOKIES["sessionid"]
        if "timezone" in request.COOKIES: del request.COOKIES["timezone"]

        cooStr = []
        for rc in request.COOKIES.keys():
            cooStr.append(rc + "=" + request.COOKIES[rc])
        cooStr = ';'.join(cooStr)
        request.META['HTTP_COOKIE'] = cooStr
        self.request.META['HTTP_COOKIE'] = cooStr

        if "timezone" in request.COOKIES: del request.COOKIES["timezone"]

        response = super(myProxyView.__base__, self).dispatch(request, *args, **kwargs)
        if self.mode == 'record':
            self.record(response)
        if self.rewrite:
            response = self.rewrite_response(request, response)

        # print("-----------------------repnseddd-------------------")
        return response

    def get(self, *args, **kwargs):
        regex = re.compile('^HTTP_')
        _header = dict((regex.sub('', header), value) for (header, value)
                       in self.request.META.items() if header.startswith('HTTP_'))
        # _header["HOST"] = settings.ACTIVITI_HTTP_HOST
        # self.get_myRequest(headers=_header)
        result = self.get_response(headers=_header)
        return result

    def post(self, request, *args, **kwargs):
        headers = {}
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                       in request.META.items() if header.startswith('HTTP_'))
        if request.META.get('CONTENT_TYPE'):
            headers['Content-type'] = request.META.get('CONTENT_TYPE')

        headers["HOST"] = settings.ACTIVITI_HTTP_HOST
        headers["ORIGIN"] = settings.ACTIVITI_SERVER_ORIGIN

        resultOfAuth = self.get_myRequest(headers=headers)
        result = self.get_response(body=request.body, headers=headers)
        # print(resultOfAuth)
        result._headers["set-cookie"] = ('Set-Cookie', resultOfAuth.raw.headers['set-cookie'],)
        return result

    def put(self, request, *args, **kwargs):
        headers = {}
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                       in request.META.items() if header.startswith('HTTP_'))
        if request.META.get('CONTENT_TYPE'):
            headers['Content-type'] = request.META.get('CONTENT_TYPE')
        headers["HOST"] = settings.ACTIVITI_HTTP_HOST
        headers["ORIGIN"] = settings.ACTIVITI_SERVER_ORIGIN
        self.get_myRequest(headers=headers)
        return self.get_response(body=request.body, headers=headers)

    def patch(self, request, *args, **kwargs):
        headers = {}
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                       in request.META.items() if header.startswith('HTTP_'))
        if request.META.get('CONTENT_TYPE'):
            headers['Content-type'] = request.META.get('CONTENT_TYPE')
        headers["HOST"] = settings.ACTIVITI_HTTP_HOST
        headers["ORIGIN"] = settings.ACTIVITI_SERVER_ORIGIN
        self.get_myRequest(headers=headers)
        return self.get_response(body=request.body, headers=headers)

    def delete(self, request, *args, **kwargs):
        headers = {}
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                       in request.META.items() if header.startswith('HTTP_'))
        if request.META.get('CONTENT_TYPE'):
            headers['Content-type'] = request.META.get('CONTENT_TYPE')
        headers["HOST"] = settings.ACTIVITI_HTTP_HOST
        headers["ORIGIN"] = settings.ACTIVITI_SERVER_ORIGIN
        self.get_myRequest(headers=headers)
        return self.get_response(body=request.body, headers=headers)

    def push(self, request, *args, **kwargs):
        headers = {}
        regex = re.compile('^HTTP_')
        headers = dict((regex.sub('', header), value) for (header, value)
                       in request.META.items() if header.startswith('HTTP_'))
        if request.META.get('CONTENT_TYPE'):
            headers['Content-type'] = request.META.get('CONTENT_TYPE')
        headers["HOST"] = settings.ACTIVITI_HTTP_HOST
        headers["ORIGIN"] = settings.ACTIVITI_SERVER_ORIGIN
        self.get_myRequest(headers=headers)
        return self.get_response(body=request.body, headers=headers)

    def create_request(self, url, body=None, headers={}):
        request = urllib.request.Request(url, body, headers, method=self.request.method)
        logger.info('%s %s' % (request.get_method(), request.get_full_url()))
        return request

    def credentials(self, url, username, password):
        p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        p.add_password(None, url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(p)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

    def get_response(self, body=None, headers={}):
        request_url = self.get_full_url(self.url)
        # self.credentials(request_url, "admin@app.activiti.com","admin")
        request = self.create_request(request_url, body=body, headers=headers)
        request.headers["Host"] = settings.ODOO_HTTP_HOST
        request.headers["Referer"] = settings.ODOO_HTTP_REFERER
        request.headers["Cookie"] = ""
        try:
            response = urllib.request.urlopen(request)
            response_body = response.read()
            status = response.getcode()
            header = {}
            for xx in response.headers._headers:
                header[xx[0].lower()] = xx[1]
            logger.debug(self._msg % response_body)
        except urllib.error.HTTPError as e:
            header = {}
            for xx in e.headers._headers:
                header[xx[0].lower()] = xx[1]
            response_body = e.read()
            logger.error(self._msg % response_body)
            status = e.code
            return HttpResponse(response_body, status=status, content_type=header["content-type"])

        # this is require because i handed headers
        def rr(cc):
            return False

        # this hoppish does not allow to send django standard response headers
        wsgiref.util._hoppish = rr
        if "content-type" in header:
            result = HttpResponse(response_body, status=status, content_type=header["content-type"])
        else:
            result = HttpResponse(response_body, status=status)

        # for head in header.keys():
        #     result._headers[head] = (head.title(),header[head],)
        # result._headers["x-xss-protection"] = ("X-XSS-Protection", result._headers["x-xss-protection"][1],)

        return result
