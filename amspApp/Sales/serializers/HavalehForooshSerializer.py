from asq.initiators import query
from django.contrib.auth.models import Group
from mongoengine import IntField
from rest_framework import serializers
from rest_framework_mongoengine.fields import ObjectIdField

from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time, mil_to_sh
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Sales.models import HavalehForooshConv, HavalehForooshSigns, HavalehForooshApprove, \
    HamkaranHavaleForoosh, HamkaranHavaleForooshOrderApprove, HavalehForooshs, HamkaranIssuePermitItem, \
    HamkaranIssuePermit\
    # , HavalehForooshSignsSnapshot
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class OldHavalehForooshSerializer(DynamicFieldsDocumentSerializer):
    # lastSignDate = serializers.DateTimeField(allow_null=True, required=False)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HavalehForooshs
        # model = HavalehForooshs


class OldHavalehForooshApproveSerializer(DynamicFieldsDocumentSerializer):
    parent = ObjectIdField(required=False, allow_null=True, )
    positionID = IntField(required=False, )  # position ID of havaleh foroosh Creator

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HavalehForooshApprove
        # model = HavalehForooshApprove


class OldHavalehForooshConvSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HavalehForooshConv

    def save(self, **kwargs):
        result = super(OldHavalehForooshConvSerializer, self).save(**kwargs)
        approve = HamkaranHavaleForooshOrderApprove.objects.get(id=result.HavalehForooshApproveLink.id)

        notification_reciever_group_name = "group_havalehforoosh"
        groups = Group.objects.filter(name__contains=notification_reciever_group_name)
        c = []
        [c.extend(x.user_set.all()) for x in groups]
        users = query(c).distinct(lambda x: x.id).to_list()
        dt = {}

        for u in users:
            profileInstance = Profile.objects.filter(userID=u.id).first()
            profileSerial = ProfileSerializer(instance=profileInstance).data

            dt = {
                'type': 6,
                'typeOfAlarm': 3,
                'informType': 6,
                'userID': u.id,
                'extra': {
                    'prevSignerName': profileSerial['extra']['Name'],
                    'prevSignerAvatar': profileSerial['extra']['profileAvatar']['url'],
                    'approveForooshID': result.HavalehForooshApproveLink.id,
                    'dbid': str(approve.havalehForooshLink),
                    'customer': approve.item['items'][0]['OrderItemRecipient'],
                    'qty': query(approve.item['items']).sum(lambda x: x['OrderItemQuantity']),
                    'dateOf': mil_to_sh_with_time(result.HavalehForooshApproveLink.havalehForooshLink.tarikheSodoor),
                }
            }

            ntSerial = NotificationsSerializer(data=dt)
            ntSerial.is_valid(raise_exception=True)
            ntSerial.save()
        return result


class HavalehForooshSignSerializer(DynamicFieldsDocumentSerializer):
    comment = serializers.CharField(allow_blank=True, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HavalehForooshSigns

    def save(self, **kwargs):
        result = super(HavalehForooshSignSerializer, self).save(**kwargs)

        if result.whichStep < 7:
            notification_reciever_group_name = "group_havalehforoosh_permited_to_view_" + str(result.whichStep + 1)
            joint_users = Group.objects.filter(name=notification_reciever_group_name)
            for j in joint_users:
                users = j.user_set.all()
                for u in users:
                    profileInstance = Profile.objects.filter(userID=u.id).first()
                    profileSerial = ProfileSerializer(instance=profileInstance).data
                    hfs = HamkaranHavaleForooshOrderApprove.objects.filter(id=result.HavalehForooshApproveLink)
                    if hfs.count != 0:
                        hfs = hfs.first()
                    else :
                        hfs = HamkaranHavaleForooshOrderApprove.objects.get(id=result.HavalehForooshApproveLink)

                    fsi = \
                    HamkaranHavaleForooshOrderApprove.objects.get(id=result.HavalehForooshApproveLink).item['items'][0]
                    dt = {
                        'type': 5,
                        'typeOfAlarm': 3,
                        'informType': 5,
                        'userID': u.id,
                        'extra': {
                            'prevSignerName': profileSerial['extra']['Name'],
                            'prevSignerAvatar': profileSerial['extra']['profileAvatar']['url'],
                            'havalehForooshID': str(fsi['OrderItemID']),
                            'dbid': str(hfs.havalehForooshLink.id),
                            'customer': fsi['OrderItemRecipient'],
                            'qty': int(
                                query(HamkaranHavaleForooshOrderApprove.objects.get(
                                    id=result.HavalehForooshApproveLink).item[
                                          'items']).sum(lambda x: x['OrderItemQuantity'])),
                            'dateOf': mil_to_sh(hfs.havalehForooshLink.tarikheSodoor, splitter="/"),
                        }
                    }

                    ntSerial = NotificationsSerializer(data=dt)
                    ntSerial.is_valid(raise_exception=True)
                    ntSerial.save()

        if self.data['whichStep'] == 5:
            hff = HamkaranHavaleForooshOrderApprove.objects.get(id=result.HavalehForooshApproveLink)
            item = hff.item
            item['thisApproveFinished'] = True
            hffs = HavalehForooshApproveSerializer(instance=hff, data={'item': item}, partial=True)
            hffs.is_valid(raise_exception=True)
            hffs.save()

        if self.data['whichStep'] == 7:
            hff = HamkaranHavaleForooshOrderApprove.objects.get(id=result.HavalehForooshApproveLink)
            item = hff.item
            item['thisApproveReadyToExit'] = True
            item['closed'] = True
            hffs = HavalehForooshApproveSerializer(instance=hff, data={'item': item}, partial=True)
            hffs.is_valid(raise_exception=True)
            hffs.save()

        return result


class HavalehForooshSerializer(DynamicFieldsDocumentSerializer):
    # lastSignDate = serializers.DateTimeField(allow_null=True, required=False)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranHavaleForoosh
        # model = HavalehForooshs


class HavalehForooshApproveSerializer(DynamicFieldsDocumentSerializer):
    parent = ObjectIdField(required=False, allow_null=True, )

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranHavaleForooshOrderApprove
        # model = HavalehForooshApprove

class HamkaranIssuePermitItemSerializer(DynamicFieldsDocumentSerializer):
    parent = ObjectIdField(required=False, allow_null=True, )

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranIssuePermitItem
        # model = HavalehForooshApprove

class HamkaranIssuePermitSerializer(DynamicFieldsDocumentSerializer):
    parent = ObjectIdField(required=False, allow_null=True, )

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranIssuePermit
        # model = HavalehForooshApprove


class HavalehForooshConvSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HavalehForooshConv

    def save(self, **kwargs):
        result = super(HavalehForooshConvSerializer, self).save(**kwargs)
        approve = HamkaranHavaleForooshOrderApprove.objects.get(id=result.HavalehForooshApproveLink.id)

        notification_reciever_group_name = "group_havalehforoosh"
        groups = Group.objects.filter(name__contains=notification_reciever_group_name)
        c = []
        [c.extend(x.user_set.all()) for x in groups]
        users = query(c).distinct(lambda x: x.id).to_list()
        dt = {}

        for u in users:
            profileInstance = Profile.objects.filter(userID=u.id).first()
            profileSerial = ProfileSerializer(instance=profileInstance).data

            dt = {
                'type': 6,
                'typeOfAlarm': 3,
                'informType': 6,
                'userID': u.id,
                'extra': {
                    'prevSignerName': profileSerial['extra']['Name'],
                    'prevSignerAvatar': profileSerial['extra']['profileAvatar']['url'],
                    'approveForooshID': result.HavalehForooshApproveLink.id,
                    'dbid': str(approve.havalehForooshLink.id),
                    'customer': approve.item['items'][0]['OrderItemRecipient'],
                    'qty': query(approve.item['items']).sum(lambda x: x['OrderItemQuantity']),
                    'dateOf': mil_to_sh_with_time(result.HavalehForooshApproveLink.havalehForooshLink.tarikheSodoor),
                }
            }

            ntSerial = NotificationsSerializer(data=dt)
            ntSerial.is_valid(raise_exception=True)
            ntSerial.save()
        return result



class HavalehForooshSignsSnapshotSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    # class Meta:
        # model = HavalehForooshSignsSnapshot