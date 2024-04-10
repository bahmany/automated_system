from fcm_django.models import FCMDevice
from rest_framework_mongoengine import viewsets

from amspApp.Notifications.models import GoogleToken
from amspApp.Notifications.serializers.NotificationSerializer import GoogleTokenSerializer
from amspApp._Share.ListPagination import ListPagination


class GoogleTokenViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = GoogleTokenSerializer
    queryset = GoogleToken.objects.all().order_by('-id').limit(100)

    def create(self, request, *args, **kwargs):
        request.data["userID"] = request.user.id
        typeOf = "android"
        if request.data.get("dest"):
            typeOf = request.data.get("dest")
        FCMDevice.objects.filter(registration_id = request.data.get("token")).delete()
        dt = dict(
            registration_id=request.data["token"],
            user=request.user,
            type=typeOf,
            # device_id=request.user.id,
            name=typeOf+"_"+str(request.user.id)

        )

        newDevice = FCMDevice(**dt)
        newDevice.save()

        return super(GoogleTokenViewSet, self).create(request, *args, **kwargs)
