from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Edari.Morekhasi.models import MorekhasiSaati
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class MorekhasiSaatieSerializers(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MorekhasiSaati

    def to_representation(self, instance):
        result = super(MorekhasiSaatieSerializers, self).to_representation(instance)

        return result

    def save(self, **kwargs):
        result = super(MorekhasiSaatieSerializers, self).save(**kwargs)
        """
        برای نوتیفیکیشن ها
        لازم است یکی برای مدیر متقاضی برود وقتی که لازم است امضا کند
        راستی لازم است برای صاحبین مجاز امضای مرخصی نیز باید ارسال شود
        دیگری وقتی مدیر تایید کرد
        و بعدی وقتی مدیر رد کرد
        و دوباره برای متقاضی باید زمانی برود که مدیر یا مسیول اداری تایید کرد
        برای انتظامات لزومی ندارد نوتیف برود
        """
        moteghazi_signed = result.exp['pos_vahede_darkhat'].get('is_signed') == True
        modir_signed = result.exp['pos_modire_vahede_darkhat'].get('is_signed') == True
        modir_disagree = result.exp['pos_modire_vahede_darkhat'].get('is_disagree') == True
        modirmali_signed = result.exp['pos_modire_mali'].get('is_signed') == True
        masoole_edari_signed = result.exp['pos_masoole_edari'].get('is_signed') == True

        notif = {}
        notif['typeOfAlarm'] = 1
        notif['periority'] = 1
        notif['informType'] = 1
        extra = {}
        extra['moteghaziName'] = result.exp.get('pos_vahede_darkhat', {}).get('profileName','')
        extra['moteghaziChart'] = result.exp.get('pos_vahede_darkhat', {}).get('chartName','')
        extra['moteghaziAvatar'] = result.exp.get('pos_vahede_darkhat', {}).get('avatar','')
        extra['az'] = result.exp['az']
        extra['id'] = str(result['id'])
        extra['taa'] = result.exp['taa']
        extra['dateofmorekhasi'] = result.exp['dateofmorekhasi']
        extra['mizan'] = result.exp.get('mizan','')
        notif["extra"] = extra

        """
        ارسال پیام برای مدیر واحد متقاضی
        """
        if (moteghazi_signed and not modir_signed):
            notif['type'] = 546345


            notif['userID'] = result.exp['pos_modire_vahede_darkhat']['userID']
            vs = NotificationsSerializer(data=notif)
            vs.is_valid(raise_exception=True)
            vs.save()
            if result.exp['pos_emaza_konandeha'] == None: result.exp['pos_emaza_konandeha'] = []
            for hh in result.exp.get('pos_emaza_konandeha',[]):
                notif['type'] = 546345
                notif['userID'] = hh['userID']
                vs = NotificationsSerializer(data=notif)
                vs.is_valid(raise_exception=True)
                vs.save()
        """
        ارسال پیام برای مدیرمالی
        و
        مسئول اداری
        و متقاضی 
        در خصوص اینکه مدیر واحد امضا کرده و همکنون نوبت به امضای مسئول یا مدیر اداری هست
        
        """
        if moteghazi_signed and modir_signed and (not modirmali_signed and not masoole_edari_signed):
            notif['type'] = 798448
            notif['userID'] = result.exp['pos_vahede_darkhat']['userID']
            vs = NotificationsSerializer(data=notif)
            vs.is_valid(raise_exception=True)
            vs.save()
            notif['type'] = 8675446
            notif['userID'] = result.exp['pos_modire_mali']['userID']
            vs = NotificationsSerializer(data=notif)
            vs.is_valid(raise_exception=True)
            vs.save()
            notif['type'] = 3462661
            notif['userID'] = result.exp.get('pos_masoole_edari', {}).get('userID', False)
            if (notif['userID']):
                vs = NotificationsSerializer(data=notif)
                vs.is_valid(raise_exception=True)
                vs.save()
        """
        برای متقاضی پیام رد درخواست ارسال می شود
        """
        if moteghazi_signed and modir_disagree and (not modirmali_signed and not masoole_edari_signed):
            notif['type'] = 849811
            notif['userID'] = result.exp['pos_modire_vahede_darkhat']['userID']
            vs = NotificationsSerializer(data=notif)
            vs.is_valid(raise_exception=True)
            vs.save()

        return result


