from django.http import HttpResponseForbidden


class ForbiddenMiddleware(object):
    def process_response(self, request, response):
        # if response.status_code == 403:
        #     return HttpResponseForbidden(
        #         "عدم دسترسی - شما به صفحه درخواستی دسترسی ندارید - لطفا به مدیر سیستم اطلاع دهید")
        return response
