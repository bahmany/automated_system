from datetime import datetime

import deepdiff
from django.contrib.auth.models import Group
from fcm_django.models import FCMDevice

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time, get_date_str
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Sales.models import ExtisFiles, ExitsSMS, HamkaranCustomerNotes, HamkaranKhoroojItems, HamkaranKhorooj, \
    HamkaranKhoroojSMS, HamkaranKhoroojFiles, HamkaranKhoroojSigns, HamkaranIssuePermitItem, HamkaranHavaleForoosh, \
    HamkaranHavaleForooshOrderApprove, HamkaranKhoroojSignsSnapshot
from amspApp.Sales.serializers.CustomerProfileSerializer import HamkaranCustomerNotesSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from rest_framework import serializers


class HamkaranKhroojItemsSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranKhoroojItems


class HamkaranKhoroojSignsSnapshotSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranKhoroojSignsSnapshot

    def to_representation(self, instance):
        result = super(HamkaranKhoroojSignsSnapshotSerializer, self).to_representation(instance)
        dtt = {
            'ID': result.get('snapshot', {}).get('khorooj', {}).get('ID', None),
            'PartUnit': result.get('snapshot', {}).get('khorooj', {}).get('PartUnit', None),
            't0_InventoryVoucherID': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get(
                't0_InventoryVoucherID', None),
            't0_Number': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t0_Number', None),
            't0_CounterpartEntityText': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get(
                't0_CounterpartEntityText', None),
            't0_CounterpartDLCode': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get(
                't0_CounterpartDLCode', None),
            't0_Description': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t0_Description', None),
            't2_Number1': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number1', None),
            't2_Number2': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number2', None),
            't2_Number3': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number3', None),
            't2_Number4': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number4', None),
            't2_Number5': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number5', None),
            't2_Number6': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number6', None),
            't2_Number7': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number7', None),
            't2_Number8': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number8', None),
            't2_Number9': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number9', None),
            't2_Number10': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Number10', None),
            't2_String1': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String1', None),
            't2_String2': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String2', None),
            't2_String3': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String3', None),
            't2_String4': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String4', None),
            't2_String5': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String5', None),
            't2_String6': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String6', None),
            't2_String7': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String7', None),
            't2_String8': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String8', None),
            't2_String9': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String9', None),
            't2_String10': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_String10', None),
            't2_Lookup2': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup2', None),
            't2_Lookup3': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup3', None),
            't2_Lookup4': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup4', None),
            't2_Lookup5': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup5', None),
            't2_Lookup6': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup6', None),
            't2_Lookup7': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup7', None),
            't2_Lookup8': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup8', None),
            't2_Lookup9': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup9', None),
            't2_Lookup10': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Lookup10', None),
            't2_Reference1': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Reference1', None),
            't3_noe_vasileh': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t3_noe_vasileh', None),
            't2_Reference2': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Reference2', None),
            't4_name_barbari': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t4_name_barbari',
                                                                                                None),
            't2_Reference3': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Reference3', None),
            't2_Reference4': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Reference4', None),
            't2_Reference5': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('t2_Reference5', None),
            'TotalQty': result.get('snapshot', {}).get('khorooj', {}).get('exp', {}).get('TotalQty', None),
        }
        ss = []
        for i in result.get('snapshot', {}).get('khorooj_items', []):
            pp = {
                'PartName': i.get('item', {}).get('PartName'),
                'Code': i.get('item', {}).get('Code'),
                'PartUnit': i.get('item', {}).get('PartUnit'),
                'Number': i.get('item', {}).get('Number'),
                'MajorUnitQuantity': i.get('item', {}).get('MajorUnitQuantity'),
                'Quantity': i.get('item', {}).get('Quantity'),
            }
            ss.append(pp)
        ss = {
            'items': ss
        }
        dtt.update(ss)
        return dtt


class HamkaranKhoroojSignsSerializer(DynamicFieldsDocumentSerializer):
    comment = serializers.CharField(allow_blank=True, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranKhoroojSigns

    def to_representation(self, instance):
        result = super(HamkaranKhoroojSignsSerializer, self).to_representation(instance)
        signer_name = {
            'positionName': '',
            'positionchartName': ''
        }
        positionInstance = PositionsDocument.objects.filter(positionID=instance.positionID).first()
        if positionInstance:
            signer_name['positionName'] = positionInstance.profileName
            signer_name['positionchartName'] = positionInstance.chartName

        result.update(signer_name)

        snapshot_ins = HamkaranKhoroojSignsSnapshot.objects.filter(khoroojSignLink=result['id']).first()
        if snapshot_ins:
            snapshots = HamkaranKhoroojSignsSnapshotSerializer(
                instance=HamkaranKhoroojSignsSnapshot.objects.filter(khoroojSignLink=result['id']).first()).data
            result['snapshots'] = snapshots

        return result

    def save(self, **kwargs):
        result = super(HamkaranKhoroojSignsSerializer, self).save(**kwargs)
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
                            'exitID': str(result.khoroojLink.id),
                            'customer': result.khoroojLink.exp.get('t0_CounterpartEntityText', "-"),
                            'qty': int(HamkaranKhoroojItems.objects.filter(khoroojLink=result.khoroojLink.id).sum(
                                'item.Quantity')),
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
            exitInstance = result.khoroojLink

            total_qty = int(HamkaranKhoroojItems.objects.filter(khoroojLink=exitInstance.id).sum('item.Quantity'))

            for ju in joint_users:
                users = ju.user_set.all()
                for u in users:
                    lll = FCMDevice.objects.filter(user_id=u.id)
                    for l in lll:
                        title = "خروج کامل محصول"
                        dt = datetime.now()
                        dt = mil_to_sh_with_time(dt)
                        msg = "فرآیند خروج %s جهت %s توسط %s مورخه %s پایان یافت" % (
                            str(total_qty) + " کیلو",
                            exitInstance.exp.get('t0_CounterpartEntityText', "-")
                            , "حراست",
                            dt)
                        l.send_message(
                            title=title,
                            body=msg,
                            delay_while_idle=True,
                            sound="default",
                            time_to_live=20)

        return result


class HamkaranKhoroojSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranKhorooj

    def to_representation(self, instance):
        result = super(HamkaranKhoroojSerializer, self).to_representation(instance)
        dt = dict(
            dateOfPost=instance.exp.get('t0_CreationDate'),
            hahScan=HamkaranKhoroojFiles.objects.filter(khoroojLink=instance.id).count() > 0,
            hasSms=HamkaranKhoroojSMS.objects.filter(khoroojLink=instance.id).count() > 0,
            readSms=HamkaranKhoroojSMS.objects.filter(khoroojLink=instance.id, seenDate__ne=None).count() > 0,
            signCount=HamkaranKhoroojSigns.objects.filter(khoroojLink=instance.id).count(),
            signTitle="",
            TotalQty=0)
        result.update(dt)
        # HamkaranKhoroojItems.objects.filter(khoroojLink=instance.id)
        result['exp']['TotalQty'] = HamkaranKhoroojItems.objects.filter(item__InventoryVoucherRef=instance.ID).sum(
            'item.Quantity')

        result['phones'] = HamkaranCustomerNotesSerializer().get_phones(instance.exp.get('t0_CounterpartEntityRef'))
        result['phones'] = [x[:4] + '****' + x[8:] for x in result['phones']]
        issue_item = HamkaranIssuePermitItem.objects.filter()
        result['signs'] = HamkaranKhoroojSignsSerializer(
            HamkaranKhoroojSigns.objects.filter(khoroojLink=instance.id), many=True, ).data
        for s in result['signs']:
            del s['khoroojLink']
        result['items'] = HamkaranKhroojItemsSerializer(
            instance=HamkaranKhoroojItems.objects.filter(item__InventoryVoucherRef=instance.ID), many=True).data
        result['dateOfPostPretty'] = get_date_str(result['dateOfPost'])
        result['PartUnit'] = "کیلوگرم"
        """
        اینجا لازم هست هر چی که نول هستند مقدار دهی شوند
        برای اینکه موبایل قاطی نکند
        """
        for k in result['exp'].keys():
            if result['exp'][k] is None:
                if k.find("Number") != -1:
                    result['exp'][k] = 0
                if k.find("String") != -1:
                    result['exp'][k] = 0

        for ss in result['items']:
            result['PartUnit'] = ss['item']['PartUnit']
            issue_instance = HamkaranIssuePermitItem.objects.filter(ID=ss['item']['ReferenceRef']).first()
            if issue_instance:
                hiss = HamkaranHavaleForooshOrderApprove.objects.filter(
                    item__items__OrderItemID=issue_instance['exp']['ProductSourceItemRef']).first()
                if hiss:
                    if len(hiss.item['items']) > 0:
                        ss['pishfactor'] = hiss.item['items'][0]['OrderItemSourceNumber']
                        havaleh = HamkaranHavaleForoosh.objects.filter(
                            ID=hiss.item['items'][0]['OrderItemOrderID']).first()
                        if havaleh:
                            ss['havaleh_foroosh_code'] = havaleh.Number
                            ss['havaleh_foroosh_id'] = str(havaleh.id)
                            ss['havaleh_foroosh_tarikh'] = havaleh.tarikheSodoor
                        else:
                            ss['havaleh_foroosh_code'] = 'قدیمی'
                            ss['havaleh_foroosh_tarikh'] = 'قدیمی'
                else:
                    ss['pishfactor'] = "از واحد مالی استعلام شود"
                    ss['havaleh_foroosh_code'] = "از واحد مالی استعلام شود"

        # detecting changes
        all_snaps = []
        for sign_snap in result.get('signs', []):
            if sign_snap.get('snapshots', False):
                snaps = sign_snap.get('snapshots', None)
                # snaps['sign_id'] = sign_snap['id']
                all_snaps.append(snaps)
        # ------------------
        diffs = []
        if len(all_snaps) > 1:
            for a in all_snaps:
                diff = deepdiff.DeepDiff(all_snaps[0], a).get('values_changed', False)
                if diff:
                    diffs.append(diff)
        result['change_found'] = False
        if len(diffs) > 0:
            result['change_found'] = True
            result['what_to_changed'] = diffs
        return result

    # depth = 1


class KhoroojFilesSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = ExtisFiles

    depth = 1


class KhoroojSMSSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranKhoroojSMS


class HamkaranKhoroojFilesSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranKhoroojFiles
