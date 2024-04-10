from django import forms
from djangular.forms import NgFormValidationMixin
from djangular.forms import NgModelFormMixin
from djangular.styling.bootstrap3.forms import Bootstrap3ModelForm, Bootstrap3Form


def createDefaultCharField(PersianName, HelpText, Max, Min, Required):
    return forms.CharField(
        min_length=Min,
        max_length=Max,
        required=Required,
        label=PersianName,
        help_text=HelpText
    )


class SaleCustomerFormDetailsForm(Bootstrap3Form):
    # CEO
    nameKamel = createDefaultCharField("نام کامل", "", 60, 3, True)
    codeMelli = createDefaultCharField("کد یا شناسه ملی", "", 60, 3, True)
    codeSabti = createDefaultCharField("کد ثبت", "", 60, 3, True)
    codeEghtesadi = createDefaultCharField("کد اقتصادی", "", 60, 3, True)
    dateSabt = createDefaultCharField("تاریخ ثبت", "", 60, 3, True)
    dateEtmameArzesheAfzoodeh = createDefaultCharField("تاریخ اتمام ارزش افزوده", "", 60, 3, True)
    addressOffice = createDefaultCharField("آدرس دفتر", "", 60, 3, True)
    addressKarkhaneh = createDefaultCharField("آدرس کارخانه", "", 60, 3, True)
    addressOffice2 = createDefaultCharField("آدرس دفتر 2", "", 60, 3, True)
    addressKarkhaneh2 = createDefaultCharField("آدرس کارخانه 2", "", 60, 3, True)
    OfficeTel1 = createDefaultCharField("تلفن 1", "", 60, 3, True)
    OfficeTel2 = createDefaultCharField("تلفن 2", "", 60, 3, True)
    OfficeTel3 = createDefaultCharField("تلفن 3", "", 60, 3, True)
    OfficeTel4 = createDefaultCharField("تلفن 4", "", 60, 3, True)
    OfficeFax = createDefaultCharField("فکس", "", 60, 3, True)
    FactoryTel1 = createDefaultCharField("تلفن کارخانه 1", "", 60, 3, True)
    FactoryTel2 = createDefaultCharField("تلفن کارخانه 2", "", 60, 3, True)
    FactoryTel3 = createDefaultCharField("تلفن کارخانه 3", "", 60, 3, True)
    FactoryTel4 = createDefaultCharField("تلفن کارخانه 4", "", 60, 3, True)
    FactoryFax = createDefaultCharField("فکس کارخانه", "", 60, 3, True)


class SaleCustomerFormDetailsFormV(NgModelFormMixin, NgFormValidationMixin, SaleCustomerFormDetailsForm):
    # Apart from an additional mixin class, the Form declaration from the
    # 'Classic Subscription' view, has been reused here.
    pass
