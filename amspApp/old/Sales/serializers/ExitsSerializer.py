from datetime import datetime

from django.contrib.auth.models import Group
from fcm_django.models import FCMDevice
from rest_framework import serializers

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, mil_to_sh_with_time
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Sales.models import Exits, ExtisFiles, ExitsSMS, ExitsSigns
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class ExitsSerializer(DynamicFieldsDocumentSerializer):
    scan = serializers.CharField(required=False, allow_null=True)
    cellNoToSMS = serializers.CharField(required=False, allow_null=True)
    smsResult = serializers.CharField(required=False, allow_null=True)
    visitorDate = serializers.DateTimeField(required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = Exits

    depth = 1

    def create(self, validated_data):
        result = super(ExitsSerializer, self).create(validated_data)
        # sending beginning notifications to google not to notification model
        start_exit_notify = "group_extis_start_notification"
        joint_users = Group.objects.filter(name=start_exit_notify)
        return result

        # for j in joint_users:
        #     users = j.user_set.all()
        #     for u in users:
        #         lll = FCMDevice.objects.filter(user_id=u.id)
        #         for l in lll:
        #             title = "شروع فرآیند حواله خروج"
        #             dt = datetime.now()
        #             dt = mil_to_sh_with_time(dt)
        #             msg = "فرآیند خروج %s جهت %s توسط %s مورخه %s شروع شد" % (
        #                 str(result.item.get("TotalQty", "0")) + " کیلو",
        #                 result.item.get("CntrprtTitle", "-")
        #                 , "انباردار",
        #                 dt)
        #
        #             l.send_message(
        #                 title=title,
        #                 body=msg,
        #                 delay_while_idle=True,
        #                 sound="default",
        #                 time_to_live=20)
        #
        # return result


class ExtisFilesSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ExtisFiles

    depth = 1


class ExitsSMSSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ExitsSMS

    depth = 1


class ExitsSignSerializer(DynamicFieldsDocumentSerializer):
    comment = serializers.CharField(allow_blank=True, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ExitsSigns

    def save(self, **kwargs):
        result = super(ExitsSignSerializer, self).save(**kwargs)
        if result.whichStep < 5:
            notification_reciever_group_name = "group_extis_permited_to_view_" + str(result.whichStep + 1)
            joint_users = Group.objects.filter(name=notification_reciever_group_name)
            for j in joint_users:
                users = j.user_set.all()
                for u in users:
                    profileInstance = Profile.objects.filter(userID=u.id).first()
                    profileSerial = ProfileSerializer(instance=profileInstance).data

                    dt = {
                        'type': 4,
                        'typeOfAlarm': 3,
                        'informType': 5,
                        'userID': u.id,
                        'extra': {
                            'prevSignerName': profileSerial['extra']['Name'],
                            'prevSignerAvatar': profileSerial['extra']['profileAvatar']['url'],
                            'exitID': str(result.exitsLink.id),
                            'customer': result.exitsLink.item.get('CntrprtTitle', "-"),
                            'qty': int(result.exitsLink.item.get('TotalQty', "0")),
                            # 'dateOf': mil_to_sh_with_time(result.exitsLink.item.get('TransDate', "2010/01/01")),
                            'dateOf': mil_to_sh_with_time(datetime.now()),
                        }
                    }

                    ntSerial = NotificationsSerializer(data=dt)
                    ntSerial.is_valid(raise_exception=True)
                    ntSerial.save()
        if result.whichStep == 5:
            start_exit_notify = "group_extis_end_notification"
            joint_users = Group.objects.filter(name=start_exit_notify)
            exitInstance = result.exitsLink
            for ju in joint_users:
                users = ju.user_set.all()
                for u in users:
                    lll = FCMDevice.objects.filter(user_id=u.id)
                    for l in lll:
                        title = "خروج کامل محصول"
                        dt = datetime.now()
                        dt = mil_to_sh_with_time(dt)
                        msg = "فرآیند خروج %s جهت %s توسط %s مورخه %s پایان یافت" % (
                            str(exitInstance.item.get("TotalQty", "0")) + " کیلو",
                            exitInstance.item.get("CntrprtTitle", "-")
                            , "حراست",
                            dt)
                        l.send_message(
                            title=title,
                            body=msg,
                            delay_while_idle=True,
                            sound="default",
                            time_to_live=20)

            pass

        return result

    depth = 0
