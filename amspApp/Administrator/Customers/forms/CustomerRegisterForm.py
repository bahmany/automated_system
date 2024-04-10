from djangular.forms import NgModelFormMixin, NgFormValidationMixin
from djangular.styling.bootstrap3.forms import Bootstrap3ModelForm
from django import forms
from amspApp.Administrator.Customers.models import Billing_Customer

__author__ = 'mohammad'




# userID = models.IntegerField(null=False, blank=False)
# dateOfPost = models.DateTimeField(default=datetime.now(), required=False)
# subdomainName = models.CharField(max_length=30, unique=True, blank=False)
# customerName = models.CharField(max_length=50, blank=False)
# customerMobile = models.CharField(max_length=13, blank=False)
# address = models.TextField(blank=True, null=True)
# exp = models.TextField(blank=True, null=True)

class CustomerRegistrationForm(Bootstrap3ModelForm):
    subdomainName = forms.CharField(
        min_length=3,
        max_length=30,
        required=True,
        label="دومین اختصاصی",
        help_text="لطفا ساب دومین را وارد نمایید"
    )
    username = forms.CharField(
        min_length=3,
        max_length=30,
        required=False,
        label="نام کاربری",
        help_text="اولین نام کاربری که کاربر با آن می تواند لوگین کند"
    )
    password = forms.CharField(
        min_length=3,
        max_length=30,
        required=False,
        label="رمز عبور",
        help_text="اولین رمز عبوری که کاربر می تواند بوسیله ی آن لوگین نماید"
    )
    customerName = forms.CharField(
        min_length=4,
        max_length=50,
        required=True,
        label="نام خریدار",
        help_text="این فیلد ضروریست - لطفا نام خریدار را بصورت کامل وارد نمایید"
    )
    customerMobile = forms.CharField(
        min_length=13,
        max_length=13,
        required=True,
        label="شماره همراه",
        help_text="این فیلد ضروریست - لطفا شماره همراه خریدار را بصورت کامل وارد نمایید"
    )
    customerEmail = forms.EmailField(
        min_length=5,
        max_length=60,
        required=True,
        label="پست الکترونیکی",
        help_text="این فیلد ضروریست - لطفا ایمیل خریدار را بصورت کامل وارد نمایید"
    )
    address = forms.CharField(
        min_length=5,
        max_length=600,
        required=True,
        label="آدرس",
        help_text="آدرس محل اسقرار سفارش دهنده را وارد نمایید"
    )
    exp = forms.CharField(
        min_length=2,
        max_length=600,
        required=False,
        label="سایر توضیحات",
        help_text="اطلاعات مورد نیاز را در این قسمت وارد نمایید"
    )

    defaultLoginPage = forms.CharField(
        min_length=2,
        max_length=600,
        required=False,
        label="صفحه ورودی پیش فرض"+" login.html",
        help_text="اطلاعات مورد نیاز را در این قسمت وارد نمایید",
        widget=forms.TextInput(attrs={'value':'login.html'}),
        initial = "login.html"
    )

    defaultTemplate = forms.CharField(
        min_length=2,
        max_length=600,
        required=False,
        label="سایر توضیحات"+" base.html",
        help_text="اطلاعات مورد نیاز را در این قسمت وارد نمایید",
        widget=forms.TextInput(attrs={'value':'base.html'}),
        initial="base.html"

    )

    def __init__(self, *args, **kw):
        super(CustomerRegistrationForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'customerName',
            'subdomainName',
            'username',
            'password',
            'customerMobile',
            'customerEmail',
            'address',
            'exp'
        ]

    class Meta:
        model = Billing_Customer
        fields = '__all__'
        exclude = ['userID', 'dateOfPost', 'isDeleted', 'isSuspended']




