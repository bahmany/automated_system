from djangular.forms import NgModelFormMixin, NgFormValidationMixin
from djangular.styling.bootstrap3.forms import Bootstrap3ModelForm
from django import forms
from amspApp.Administrator.Billings.models import Billing_Payments, Billing_Strategies
from amspApp.Administrator.Customers.models import Billing_Customer

__author__ = 'mohammad'

"""
    createdUserID = models.IntegerField(null=False, blank=False)
    dateOfPost = models.DateTimeField(default=datetime.now(), blank=True)
    billingStrategyLink = models.ForeignKey(Billing_Strategies, blank=False, null=False)
    customerLink = models.ForeignKey(Billing_Customer, blank=False, null=False)
    loadedPrice = models.BigIntegerField(null=False, blank=False)
    bankID = models.CharField()
    paymentType = (
                            (1, 'پرداخت آنلاین'), # آنلاین
                            (2, 'فیش بانکی'),#
                            (3, 'پرداخت نقدی'),#
                            (4, 'پرداخت اولیه قرارداد'),# هنگامی که قرارداد بسته می شود و پیش پرداخت می دهند
                            (5, 'پرداخت مرحله ای قرارداد'),#
                            (6, 'پرداخت نهایی قرارداد'),#
                            (7, 'هدیه'),#
                        )
    totalPrice = models.BigIntegerField(null=False, blank=False)
    exp = models.TextField()
    """


class PaymentForm(Bootstrap3ModelForm):
    Title = forms.CharField(
        min_length=5,
        max_length=600,
        required=True,
        label="عنوان پرداخت",
        help_text="اگه حال کردید وارد کنید یه چیزی"
    )
    paymentType = forms.ChoiceField(
        required=True,
        label="نوع پرداخت",
        choices=Billing_Payments().paymentType,
        help_text="نوع پرداخت را انتخاب نمایید",
        widget=forms.Select

    )
    # billingStrategyLink = forms.ChoiceField(
    #     required=True,
    #     label="انتخاب استراتژی فروش",
    #     help_text="انتخاب کنید",
    #     choices=[(x["id"], x['Title']) for x in Billing_Strategies.objects.all().values("id", "Title")],
    #     widget=forms.Select
    #
    # )
    billingStrategyLink = forms.ModelChoiceField(
        required=True,
        label="انتخاب استراتژی فروش",
        help_text="انتخاب کنید",
        initial=0,
        queryset=Billing_Strategies.objects.all(),
        widget=forms.Select

    )
    customerLink = forms.ModelChoiceField(
        required=True,
        label="انتخاب خریدار",
        help_text="انتخاب مشتری وارد شده در سیستم",
        queryset=Billing_Customer.objects.all(),
        widget=forms.Select
    )
    # customerLink = forms.ChoiceField(
    #     required=True,
    #     label="انتخاب خریدار",
    #     help_text="انتخاب مشتری وارد شده در سیستم",
    #     choices=[(x["id"], x['customerName']) for x in Billing_Customer.objects.all().values("id", "customerName")],
    #
    # )
    loadedPrice = forms.IntegerField(
        required=True,
        label="مبلغ پرداخت شده",
        help_text="مبلغ را وارد نمایید"
    )
    totalPrice = forms.IntegerField(
        required=False,
        label="مانده حساب",
        widget=forms.NumberInput(attrs={"readonly":"readonly"})
    )
    bankID = forms.CharField(
        min_length=3,
        max_length=30,
        required=True,
        label="کد بانک",
        help_text="کد بانک یا شماره فیش یا شماره قرارداد و یا شماره چک"
    )
    exp = forms.CharField(
        min_length=5,
        max_length=600,
        required=True,
        label="توضیحات ضروری",
        help_text="اگه حال کردید وارد کنید یه چیزی"
    )


    def __init__(self, *args, **kw):
        super(PaymentForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'Title',
            'paymentType',
            'billingStrategyLink',
            'customerLink',
            'loadedPrice',
            'bankID',
            'exp'
        ]

    class Meta:
        model = Billing_Payments
        fields = '__all__'
        exclude = [ 'dateOfPost']




