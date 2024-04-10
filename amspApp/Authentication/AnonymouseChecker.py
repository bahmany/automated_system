from re import compile as _compile
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
from amsp import settings
from amspApp.amspUser.models import positionIDLastActivities
from amspApp.amspUser.serializers.UserSerializer import positionIDLastActivitiesSerializer
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset

__author__ = 'mohammad'

EXEMPT_URLS = [_compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [_compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(SessionMiddleware):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def process_response(self, request, response):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        if not request.user.is_authenticated():

            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                response.delete_cookie("authenticatedUser")
                # request.COOKIES.pop("authenticatedUser",None)
                return response
        # else:
        #     return redirect("/login")
        if request.user.is_authenticated():
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            positionIDLastActivities.objects.filter(positionID=posiIns.positionID).delete()
            posi = dict(positionID=posiIns.positionID, companyID=posiIns.companyID, dateOfPost=timezone.now())
            posiSer = positionIDLastActivitiesSerializer(data=posi)
            posiSer.is_valid(raise_exception=True)
            posiSer.save()

        return response
