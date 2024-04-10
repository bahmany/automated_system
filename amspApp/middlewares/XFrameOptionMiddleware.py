from django.middleware.clickjacking import XFrameOptionsMiddleware
from amsp import settings


class TFXFrameOptionsMiddleware(XFrameOptionsMiddleware):
    def get_xframe_options_value(self, request, response):
        if request.META['REMOTE_ADDR'] in settings.XFRAME_EXEMPT_IPS:
            return 'ALLOWALL' # non standard, equivalent to omitting
        return getattr(settings, 'X_FRAME_OPTIONS', 'SAMEORIGIN').upper()
